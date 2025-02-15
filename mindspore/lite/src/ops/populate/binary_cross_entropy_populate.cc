/**
 * Copyright 2019-2021 Huawei Technologies Co., Ltd
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
#include "src/ops/populate/populate_register.h"
#include "nnacl/fp32_grad/binary_cross_entropy.h"

namespace mindspore {
namespace lite {
OpParameter *PopulateBinaryCrossEntropyParameter(const void *prim) {
  BinaryCrossEntropyParameter *bce_param =
    reinterpret_cast<BinaryCrossEntropyParameter *>(malloc(sizeof(BinaryCrossEntropyParameter)));
  if (bce_param == nullptr) {
    MS_LOG(ERROR) << "malloc BinaryCrossEntropy Parameter failed.";
    return nullptr;
  }
  memset(bce_param, 0, sizeof(BinaryCrossEntropyParameter));
  auto primitive = static_cast<const schema::Primitive *>(prim);
  auto value = primitive->value_as_BinaryCrossEntropy();
  bce_param->op_parameter_.type_ = primitive->value_type();
  bce_param->reduction = value->reduction();
  return reinterpret_cast<OpParameter *>(bce_param);
}

Registry BinaryCrossEntropyParameterRegistry(schema::PrimitiveType_BinaryCrossEntropy,
                                             PopulateBinaryCrossEntropyParameter, SCHEMA_CUR);
}  // namespace lite
}  // namespace mindspore
