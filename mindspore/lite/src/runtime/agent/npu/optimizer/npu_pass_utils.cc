/**
 * Copyright 2020-2021 Huawei Technologies Co., Ltd
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

#include "src/runtime/agent/npu/optimizer/npu_pass_utils.h"
#include "src/runtime/agent/npu/npu_manager.h"
#include "nnacl/transpose.h"
#include "src/ops/populate/populate_register.h"
#include "src/runtime/kernel/arm/fp32/transpose_fp32.h"

namespace mindspore::lite {
using kernel::KERNEL_ARCH::kCPU;
using kernel::KERNEL_ARCH::kNPU;

kernel::LiteKernel *NPUPassUtils::CreateNchw2NhwcKernel(const std::vector<Tensor *> &in_tensors,
                                                        const std::vector<Tensor *> &out_tensors,
                                                        const InnerContext *ctx, const std::string &name) {
  kernel::KernelKey key{kCPU, kNumberTypeFloat32, schema::PrimitiveType_Transpose};
  auto *transpose_param = reinterpret_cast<TransposeParameter *>(malloc(sizeof(TransposeParameter)));
  if (transpose_param == nullptr) {
    MS_LOG(ERROR) << "malloc TransposeParameter failed.";
    return nullptr;
  }
  memset(transpose_param, 0, sizeof(TransposeParameter));
  transpose_param->op_parameter_.type_ = schema::PrimitiveType_Transpose;
  transpose_param->perm_[0] = 0;
  transpose_param->perm_[1] = 2;
  transpose_param->perm_[2] = 3;
  transpose_param->perm_[3] = 1;
  transpose_param->num_axes_ = 4;

  auto kernel = new (std::nothrow)
    kernel::TransposeCPUKernel(reinterpret_cast<OpParameter *>(transpose_param), in_tensors, out_tensors, ctx);
  if (kernel != nullptr) {
    kernel->set_desc(key);
  } else {
    MS_LOG(ERROR) << "New Nchw2Nhwc Kernel failed.";
    return nullptr;
  }

  kernel->set_name(name);
  return kernel;
}

kernel::LiteKernel *NPUPassUtils::CreateNhwc2NchwKernel(const std::vector<Tensor *> &in_tensors,
                                                        const std::vector<Tensor *> &out_tensors,
                                                        const InnerContext *ctx, const std::string &name) {
  kernel::KernelKey key{kCPU, kNumberTypeFloat32, schema::PrimitiveType_Transpose};
  auto *transpose_param = reinterpret_cast<TransposeParameter *>(malloc(sizeof(TransposeParameter)));
  if (transpose_param == nullptr) {
    MS_LOG(ERROR) << "malloc TransposeParameter failed.";
    return nullptr;
  }
  memset(transpose_param, 0, sizeof(TransposeParameter));
  transpose_param->op_parameter_.type_ = schema::PrimitiveType_Transpose;
  transpose_param->perm_[0] = 0;
  transpose_param->perm_[1] = 3;
  transpose_param->perm_[2] = 1;
  transpose_param->perm_[3] = 2;
  transpose_param->num_axes_ = 4;

  auto kernel = new (std::nothrow)
    kernel::TransposeCPUKernel(reinterpret_cast<OpParameter *>(transpose_param), in_tensors, out_tensors, ctx);
  if (kernel != nullptr) {
    kernel->set_desc(key);
  } else {
    MS_LOG(ERROR) << "New Nhwc2Nchw Kernel failed.";
    return nullptr;
  }

  kernel->set_name(name);
  return kernel;
}

void NPUPassUtils::UpdateKernel(kernel::LiteKernel *kernel, const std::vector<kernel::LiteKernel *> &in_kernels,
                                const std::vector<kernel::LiteKernel *> &out_kernels,
                                const std::vector<Tensor *> &in_tensors, const std::vector<Tensor *> &out_tensors) {
  kernel->set_in_tensors(in_tensors);
  kernel->set_out_tensors(out_tensors);
  kernel->set_in_kernels(in_kernels);
  kernel->set_out_kernels(out_kernels);
}

void NPUPassUtils::UpdateNH2NCTransNodePreKernel(kernel::LiteKernel *pre_kernel, kernel::LiteKernel *trans_kernel,
                                                 kernel::LiteKernel *kernel) {
  // For kernel before trans, update the out_kernels; the output tensor of kernel is the input tensor of trans.
  std::vector<kernel::LiteKernel *> out_kernels = pre_kernel->out_kernels();
  for (size_t i = 0; i < out_kernels.size(); i++) {
    if (out_kernels[i] == kernel) {
      out_kernels[i] = trans_kernel;
      break;
    }
  }
  pre_kernel->set_out_kernels(out_kernels);
}

void NPUPassUtils::UpdateNC2NHTransNodePreKernel(kernel::LiteKernel *pre_kernel, kernel::LiteKernel *trans_kernel,
                                                 std::vector<kernel::LiteKernel *> kernels) {
  // For kernel before trans, there may be multiple outputs.
  auto cur_out_kernels = pre_kernel->out_kernels();
  for (size_t i = 0; i < kernels.size(); i++) {
    auto itr = find(cur_out_kernels.begin(), cur_out_kernels.end(), kernels[i]);
    if (itr != cur_out_kernels.end()) {
      cur_out_kernels.erase(itr);
    }
  }
  cur_out_kernels.push_back(trans_kernel);
  pre_kernel->set_out_kernels(cur_out_kernels);
  // For kernel before trans, the output tensor is used for output tensor of trans, so replace the output tensor with
  // the input tensor of trans.
  pre_kernel->set_out_tensors(trans_kernel->in_tensors());
}

void NPUPassUtils::UpdateNH2NCTransNodePostKernel(kernel::LiteKernel *trans_kernel, kernel::LiteKernel *post_kernel) {
  auto cur_in_tensors = post_kernel->in_tensors();
  cur_in_tensors[0] = trans_kernel->out_tensors()[0];
  post_kernel->set_in_tensors(cur_in_tensors);
  post_kernel->set_in_kernels({trans_kernel});
}

void NPUPassUtils::UpdateNC2NHPostKernelInTensors(kernel::LiteKernel *kernel, kernel::LiteKernel *trans_kernel,
                                                  kernel::LiteKernel *post_kernel) {
  // For post_kernel that doesn't require insert trans kernel, because the output tensor of kernel(input tensor of
  // trans_kernel) is updated, replace the input tensor of post_kernel.
  auto post_in_tensors = post_kernel->in_tensors();
  for (size_t i = 0; i < post_in_tensors.size(); i++) {
    if (post_in_tensors[i] == kernel->out_tensors()[0]) {
      post_in_tensors[i] = trans_kernel->in_tensors()[0];
      break;
    }
  }
  post_kernel->set_in_tensors(post_in_tensors);
}

void NPUPassUtils::UpdateNC2NHTransNodePostKernel(kernel::LiteKernel *kernel, kernel::LiteKernel *trans_kernel,
                                                  kernel::LiteKernel *post_kernel) {
  // The input tensor should be replaced with the output tensor of trans_kernel.
  auto post_in_tensors = post_kernel->in_tensors();
  Tensor *old_in_tensor = nullptr;
  // find out which input tensor of post_kernel should be updated
  for (size_t i = 0; i < post_in_tensors.size(); ++i) {
    if (KernelInputFromKernel(post_kernel, i) == kernel) {
      old_in_tensor = post_in_tensors.at(i);
      break;
    }
  }
  if (old_in_tensor == nullptr) {
    MS_LOG(WARNING) << "Could not find in tensor index";
    return;
  }
  std::replace(post_in_tensors.begin(), post_in_tensors.end(), old_in_tensor, trans_kernel->out_tensors().at(0));
  post_kernel->set_in_tensors(post_in_tensors);

  // For post_kernel after trans, kernel in in_kernels should be replaced with trans_kernel.
  auto post_in_kernels = post_kernel->in_kernels();
  if (kernel == nullptr) {
    post_in_kernels.push_back(trans_kernel);
  } else {
    std::replace(post_in_kernels.begin(), post_in_kernels.end(), kernel, trans_kernel);
  }
  post_kernel->set_in_kernels(post_in_kernels);
}

bool NPUPassUtils::IsNhwc2Nchw(const kernel::LiteKernel *kernel) {
  if (kernel == nullptr) {
    return false;
  }
  if (kernel->Type() != schema::PrimitiveType_Transpose) {
    return false;
  }
  auto parameter = reinterpret_cast<TransposeParameter *>(kernel->op_parameter());
  if (parameter->num_axes_ != 4) {
    return false;
  }

  std::vector<int> perm = {parameter->perm_[0], parameter->perm_[1], parameter->perm_[2], parameter->perm_[3]};
  std::vector<int> nh2nc_perm = {0, 3, 1, 2};
  if (nh2nc_perm == perm) {
    return true;
  }
  return false;
}

bool NPUPassUtils::IsNchw2Nhwc(const kernel::LiteKernel *kernel) {
  if (kernel == nullptr) {
    return false;
  }
  if (kernel->Type() != schema::PrimitiveType_Transpose) {
    return false;
  }
  auto parameter = reinterpret_cast<TransposeParameter *>(kernel->op_parameter());
  if (parameter->num_axes_ != 4) {
    return false;
  }

  std::vector<int> perm = {parameter->perm_[0], parameter->perm_[1], parameter->perm_[2], parameter->perm_[3]};
  std::vector<int> nh2nc_perm = {0, 2, 3, 1};
  if (nh2nc_perm == perm) {
    return true;
  }
  return false;
}
kernel::LiteKernel *NPUPassUtils::KernelInputFromKernel(const kernel::LiteKernel *kernel, size_t in_tensor_index) {
  // given kernel and input tensor index, get which kernel output this tensor.
  // If input tensor is graph input, return nullptr.
  if (kernel == nullptr) {
    return nullptr;
  }
  auto tensor = kernel->in_tensors().at(in_tensor_index);
  auto in_kernels = kernel->in_kernels();
  auto output_contain = [tensor](const kernel::LiteKernel *kernel) {
    auto out_tensors = kernel->out_tensors();
    return std::find(out_tensors.begin(), out_tensors.end(), tensor) != out_tensors.end();
  };
  auto it = std::find_if(in_kernels.begin(), in_kernels.end(), output_contain);
  if (it == in_kernels.end()) {
    return nullptr;
  }
  return *it;
}
}  // namespace mindspore::lite
