/**
 * Copyright 2020 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "runtime/device/executor/dynamic_kernel.h"
#include <vector>
#include <stack>
#include <algorithm>
#include "backend/session/anf_runtime_algorithm.h"
#include "backend/optimizer/common/helper.h"
#include "common/trans.h"
#include "pipeline/jit/static_analysis/static_analysis.h"
#include "abstract/dshape.h"
#include "utils/utils.h"
#include "abstract/param_validator.h"

namespace mindspore {
namespace device {
void DynamicKernel::Initialize() {
  MS_LOG(INFO) << "Init Start";
  is_dynamic_shape_ = AnfAlgo::IsDynamicShape(cnode_ptr_);
  if (!is_dynamic_shape_) {
    MS_LOG(DEBUG) << "cnode is not dynamic shape:" << cnode_ptr_->fullname_with_scope();
    return;
  }

  is_input_dynamic_shape_ = AnfAlgo::GetBooleanAttr(cnode_ptr_, kAttrInputIsDynamicShape);
  is_output_dynamic_shape_ = AnfAlgo::GetBooleanAttr(cnode_ptr_, kAttrOutputIsDynamicShape);

  auto ret = abstract::GetDependsFormMap(cnode_ptr_);
  if (ret.empty()) {
    MS_LOG(DEBUG) << "No dynamic_shape_depends found";
    return;
  }
  MS_LOG(INFO) << "Have depends";
  (void)std::transform(ret.begin(), ret.end(), std::back_inserter(depend_list_),
                       [](const int64_t &value) { return static_cast<int>(value); });
  MS_LOG(INFO) << "Init End";
}

int DynamicKernel::GetKernelType() { return AnfAlgo::GetKernelType(cnode_ptr_); }

void DynamicKernel::RebuildDependTensor() {
  depend_tensor_map_.clear();
  for (auto depend : depend_list_) {
    auto pre_node_with_index = AnfAlgo::GetPrevNodeOutput(cnode_ptr_, depend);
    auto output_addr = AnfAlgo::GetPrevNodeMutableOutputAddr(cnode_ptr_, depend);
    std::vector<int64_t> shapes = trans::GetRuntimePaddingShape(pre_node_with_index.first, pre_node_with_index.second);
    auto host_type = AnfAlgo::GetOutputInferDataType(pre_node_with_index.first, pre_node_with_index.second);
    auto out_tensor = std::make_shared<tensor::Tensor>(host_type, shapes);
    out_tensor->set_device_address(output_addr);
    auto ret = depend_tensor_map_.try_emplace(depend, out_tensor);
    if (!ret.second) {
      MS_LOG(EXCEPTION) << "Insert map failed";
    }
  }
}

void DynamicKernel::InferShape() {
  if (!is_input_dynamic_shape_ && is_output_dynamic_shape_ && !have_depends()) {
    return;
  }
  MS_EXCEPTION_IF_NULL(cnode_ptr_);
  MS_LOG(INFO) << "InferShape start, node:" << cnode_ptr_->fullname_with_scope();
  InferShapeRecursive();

  auto inputs = cnode_ptr_->inputs();
  if (inputs.empty()) {
    MS_LOG(EXCEPTION) << "Invalid inputs";
  }
  AbstractBasePtrList args_spec_list;
  auto primitive = GetValueNode<PrimitivePtr>(inputs[0]);

  // rebuild depend tensor map for gpu dynamic memory allocation.
  RebuildDependTensor();

  auto input_size = AnfAlgo::GetInputTensorNum(cnode_ptr_);
  for (size_t i = 0; i < input_size; ++i) {
    auto input_with_index = AnfAlgo::GetPrevNodeOutput(cnode_ptr_, i);
    auto real_input = input_with_index.first;
    MS_EXCEPTION_IF_NULL(real_input);

    auto ret = depend_tensor_map_.find(i);
    if (ret != depend_tensor_map_.end()) {
      auto tensor_ptr = ret->second;
      MS_EXCEPTION_IF_NULL(tensor_ptr);
      // sync data from device to host
      tensor_ptr->data_sync();
      real_input->abstract()->set_value(tensor_ptr);
    }

    auto cnode_input = cnode_ptr_->input(i + 1);
    MS_EXCEPTION_IF_NULL(cnode_input);
    if (AnfAlgo::CheckPrimitiveType(cnode_input, prim::kPrimTupleGetItem)) {
      auto base_shape = real_input->Shape();
      if (!base_shape->isa<abstract::TupleShape>()) {
        MS_LOG(EXCEPTION) << "Node:" << cnode_ptr_->fullname_with_scope()
                          << " input is a tuple_get_item but real input node shape is not a TupleShape";
      }
      auto tuple_ptr = base_shape->cast<abstract::TupleShapePtr>();
      MS_EXCEPTION_IF_NULL(tuple_ptr);
      auto tuple_get_item_index = AnfAlgo::GetTupleGetItemOutIndex(cnode_input->cast<CNodePtr>());
      auto real_shape = tuple_ptr->shape().at(tuple_get_item_index);
      auto abstract_tensor = cnode_input->abstract()->cast<abstract::AbstractTensorPtr>();
      MS_EXCEPTION_IF_NULL(abstract_tensor);
      args_spec_list.emplace_back(std::make_shared<abstract::AbstractTensor>(abstract_tensor->element(), real_shape));
    } else if (cnode_input->isa<CNode>() && AnfAlgo::GetCNodeName(cnode_input) == prim::kPrimReshape->name()) {
      args_spec_list.emplace_back(cnode_input->abstract());
    } else {
      args_spec_list.emplace_back(real_input->abstract());
    }
  }

  auto eval_result = opt::CppInferShape(primitive, args_spec_list);
  cnode_ptr_->set_abstract(eval_result);
}

void DynamicKernel::InferShapeRecursive() {
  auto input_size = AnfAlgo::GetInputTensorNum(cnode_ptr_);
  for (size_t i = 0; i < input_size; i++) {
    auto input_node_with_index = AnfAlgo::GetPrevNodeOutput(cnode_ptr_, i);
    auto input_node = input_node_with_index.first;
    MS_EXCEPTION_IF_NULL(input_node);
    InferShapeForNopNode(&input_node);
  }
}

void DynamicKernel::InferShapeForNopNode(AnfNodePtr *input_node) {
  MS_EXCEPTION_IF_NULL(*input_node);
  if (!opt::IsNopNode(*input_node) || !AnfAlgo::IsDynamicShape(*input_node)) {
    MS_LOG(INFO) << "Input node is not a nop node, no need infer.";
    return;
  }
  MS_LOG(INFO) << "Infer shape for nop node.";
  std::stack<AnfNodePtr> nop_road;
  nop_road.push(*input_node);

  while (true) {
    auto input_node_with_idx = AnfAlgo::GetPrevNodeOutput(*input_node, 0);
    auto in_node = input_node_with_idx.first;
    MS_EXCEPTION_IF_NULL(in_node);
    if (opt::IsNopNode(in_node)) {
      nop_road.push(in_node);
      *input_node = in_node;
    } else {
      break;
    }
  }
  while (!nop_road.empty()) {
    auto nop_node = nop_road.top();
    AnfAlgo::InferShape(nop_node->cast<CNodePtr>());
    nop_road.pop();
  }
}
}  // namespace device
}  // namespace mindspore
