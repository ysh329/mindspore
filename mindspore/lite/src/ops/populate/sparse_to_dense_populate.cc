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
#include "nnacl/sparse_to_dense_parameter.h"

namespace mindspore {
namespace lite {
namespace {
OpParameter *PopulateSparseToDenseParameter(const void *prim) {
  auto *sparse_to_dense_param = reinterpret_cast<SparseToDenseParameter *>(malloc(sizeof(SparseToDenseParameter)));
  if (sparse_to_dense_param == nullptr) {
    MS_LOG(ERROR) << "malloc SparseToDenseParameter failed.";
    return nullptr;
  }
  memset(sparse_to_dense_param, 0, sizeof(SparseToDenseParameter));
  auto primitive = static_cast<const schema::Primitive *>(prim);
  sparse_to_dense_param->op_parameter_.type_ = primitive->value_type();
  return reinterpret_cast<OpParameter *>(sparse_to_dense_param);
}
}  // namespace

Registry g_sparseToDenseParameterRegistry(schema::PrimitiveType_SparseToDense, PopulateSparseToDenseParameter,
                                          SCHEMA_CUR);
}  // namespace lite
}  // namespace mindspore
