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
#include "ops/permute.h"
#include <string>
#include <algorithm>
#include <memory>
#include <set>
#include <vector>
#include "ops/op_utils.h"
#include "utils/check_convert_utils.h"
#include "abstract/primitive_infer_map.h"

namespace mindspore {
namespace ops {

void Permute::set_order(const std::vector<int64_t> &order) { this->AddAttr(kOrder, MakeValue(order)); }

std::vector<int64_t> Permute::get_order() const {
  auto value_ptr = GetAttr(kOrder);
  return GetValue<std::vector<int64_t>>(value_ptr);
}

void Permute::Init(const std::vector<int64_t> &order) { this->set_order(order); }
REGISTER_PRIMITIVE_C(kNamePermute, Permute);
}  // namespace ops
}  // namespace mindspore
