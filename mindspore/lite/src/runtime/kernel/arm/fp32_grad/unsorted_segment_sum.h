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

#ifndef MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_FP32_GRAD_UNSORTED_SEGMENT_SUM_H_
#define MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_FP32_GRAD_UNSORTED_SEGMENT_SUM_H_

#include <vector>
#include "src/lite_kernel.h"

namespace mindspore::kernel {
class UnsortedSegmentSumCPUKernel : public LiteKernel {
 public:
  UnsortedSegmentSumCPUKernel(OpParameter *parameter, const std::vector<lite::Tensor *> &inputs,
                              const std::vector<lite::Tensor *> &outputs, const lite::InnerContext *ctx)
      : LiteKernel(parameter, inputs, outputs, ctx) {}
  ~UnsortedSegmentSumCPUKernel() override = default;

  int Init() override;
  int ReSize() override;
  int Run() override;
  int Execute(int task_id);
  size_t unit_num_;
  size_t input_dim1_;
  size_t output_dim0_;
  size_t output_dim1_;

 private:
};
}  // namespace mindspore::kernel

#endif  // MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_FP32_GRAD_UNSORTED_SEGMENT_SUM_H_
