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
#ifndef MINDSPORE_LITE_NNACL_INFER_MAXIMUM_GRAD_INFER_H_
#define MINDSPORE_LITE_NNACL_INFER_MAXIMUM_GRAD_INFER_H_

#include "nnacl/infer/common_infer.h"

#ifdef __cplusplus
extern "C" {
#endif

int MaximumGradInferShape(const TensorC *const *inputs, size_t inputs_size, TensorC **outputs, size_t outputs_size,
                          OpParameter *parameter);

#ifdef __cplusplus
}
#endif
#endif  // MINDSPORE_LITE_NNACL_INFER_MAXIMUM_GRAD_INFER_H_
