/**
 * Copyright 2021 Huawei Technologies Co., Ltd
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

#include "frontend/optimizer/irpass/load_eliminate.h"

#include <algorithm>
#include <memory>
#include <set>
#include <vector>

#include "frontend/operator/ops.h"

namespace mindspore::opt::irpass {
namespace {
// Return true if the node has Ref abstract.
bool HasAbstractRef(const AnfNodePtr &node) {
  if (node == nullptr) {
    return false;
  }
  auto &abs = node->abstract();
  return (abs != nullptr) && abs->isa<abstract::AbstractRef>();
}
}  // namespace

AnfNodePtr LoadEliminater::operator()(const OptimizerPtr &, const AnfNodePtr &node) {
  auto load_node = dyn_cast<CNode>(node);
  if (load_node == nullptr || load_node->inputs().empty()) {
    MS_LOG(WARNING) << "LoadEliminater encounter invalid node: " << node->DebugString();
    return nullptr;
  }
  constexpr size_t kFirstInputIndex = 1;
  auto &param = load_node->inputs().at(kFirstInputIndex);
  if (!HasAbstractRef(param)) {
    return param;
  }
  return nullptr;
}
}  // namespace mindspore::opt::irpass
