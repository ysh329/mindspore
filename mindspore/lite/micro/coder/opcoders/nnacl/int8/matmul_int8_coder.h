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

#ifndef MINDSPORE_LITE_MICRO_CODER_OPCODERS_NNACL_INT8_MATMUL_INT8_CODER_H_
#define MINDSPORE_LITE_MICRO_CODER_OPCODERS_NNACL_INT8_MATMUL_INT8_CODER_H_
#include <vector>
#include "coder/opcoders/op_coder.h"
#include "nnacl/matmul_parameter.h"
namespace mindspore::lite::micro::nnacl {
class MatMulInt8Coder final : public OperatorCoder {
 public:
  MatMulInt8Coder(const std::vector<Tensor *> &in_tensors, const std::vector<Tensor *> &out_tensors,
                  const Model::Node *node, size_t node_index, Target target)
      : OperatorCoder(in_tensors, out_tensors, node, node_index, target) {}
  ~MatMulInt8Coder() override;

  int Prepare(CoderContext *const context) override;

  int DoCode(CoderContext *const context) override;

 private:
  int Init();
  int ReSize(CoderContext *const context);

 private:
  Tensor *filter_tensor_{nullptr};
  Tensor *bias_tensor_{nullptr};
  MatMulParameter *params_{nullptr};
  MatmulQuantParameter quant_params_{0};
  size_t a_pack_ptr_size_{0};
  int8_t *a_pack_ptr_{nullptr};
  size_t b_pack_batch_ptr_size_{0};
  int8_t *b_pack_batch_ptr_{nullptr};
  size_t bias_prt_size_{0};
  int *bias_ptr_{nullptr};
  size_t input_sums_size_{0};
  int *input_sums_{nullptr};
  size_t weight_bias_sums_batch_size_{0};
  int *weight_bias_sums_batch_{nullptr};
  int thread_stride_{0};
  int thread_count_{0};
};
}  // namespace mindspore::lite::micro::nnacl
#endif  // MINDSPORE_LITE_MICRO_CODER_OPCODERS_NNACL_INT8_MATMUL_INT8_CODER_H_
