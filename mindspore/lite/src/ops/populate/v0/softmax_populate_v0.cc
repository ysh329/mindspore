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

#include "schema/model_v0_generated.h"
#include "src/ops/populate/populate_register.h"
#include "nnacl/softmax_parameter.h"

namespace mindspore {
namespace lite {
namespace {
OpParameter *PopulateSoftmaxParameter(const void *prim) {
  auto *primitive = static_cast<const schema::v0::Primitive *>(prim);
  auto softmax_prim = primitive->value_as_SoftMax();

  SoftmaxParameter *softmax_param = reinterpret_cast<SoftmaxParameter *>(malloc(sizeof(SoftmaxParameter)));
  if (softmax_param == nullptr) {
    MS_LOG(ERROR) << "malloc SoftmaxParameter failed.";
    return nullptr;
  }
  memset(softmax_param, 0, sizeof(SoftmaxParameter));
  softmax_param->op_parameter_.type_ = schema::PrimitiveType_Softmax;
  softmax_param->axis_ = softmax_prim->axis();
  return reinterpret_cast<OpParameter *>(softmax_param);
}
}  // namespace

Registry g_softMaxV0ParameterRegistry(schema::v0::PrimitiveType_SoftMax, PopulateSoftmaxParameter, SCHEMA_V0);
}  // namespace lite
}  // namespace mindspore
