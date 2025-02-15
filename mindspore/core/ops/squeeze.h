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

#ifndef MINDSPORE_CORE_OPS_SQUEEZE_H_
#define MINDSPORE_CORE_OPS_SQUEEZE_H_

#include <map>
#include <vector>
#include <string>
#include <memory>
#include <algorithm>
#include "ops/op_utils.h"
#include "ops/primitive_c.h"
#include "abstract/primitive_infer_map.h"
#include "abstract/abstract_value.h"
#include "utils/check_convert_utils.h"

namespace mindspore {
namespace ops {
constexpr auto kNameSqueeze = "Squeeze";
class Squeeze : public PrimitiveC {
 public:
  Squeeze() : PrimitiveC(kNameSqueeze) { InitIOName({"x"}, {"output"}); }
  ~Squeeze() = default;
  MS_DECLARE_PARENT(Squeeze, PrimitiveC);
  void Init(const std::vector<int64_t> &axis = {});
  void set_axis(const std::vector<int64_t> &axis);
  std::vector<int64_t> get_axis() const;
};

AbstractBasePtr SqueezeInfer(const abstract::AnalysisEnginePtr &, const PrimitivePtr &primitive,
                             const std::vector<AbstractBasePtr> &input_args);
using PrimSqueezePtr = std::shared_ptr<Squeeze>;

}  // namespace ops
}  // namespace mindspore

#endif  // MINDSPORE_CORE_OPS_SQUEEZE_H_
