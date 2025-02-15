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

#ifndef MINDQUANTUM_ENGINE_PARAMETER_GATE_H_
#define MINDQUANTUM_ENGINE_PARAMETER_GATE_H_
#include <string>
#include "mindquantum/gates/basic_gates.h"
#include "mindquantum/utils.h"

namespace mindspore {
namespace mindquantum {
class ParameterGate : public BasicGate {
 public:
  ParameterGate();
  ParameterGate(const std::string &, const Indexes &, const Indexes &, const ParameterResolver &);
};
}  // namespace mindquantum
}  // namespace mindspore
#endif  // MINDQUANTUM_ENGINE_PARAMETER_GATE_H_
