/**
 * Copyright 2019 Huawei Technologies Co., Ltd
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

#ifndef MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_FP32_GRAD_CONVOLUTION_H_
#define MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_FP32_GRAD_CONVOLUTION_H_

#include <vector>
#include "src/lite_kernel.h"

namespace mindspore::kernel {
class ConvolutionTrainCPUKernel : public LiteKernel {
 public:
  explicit ConvolutionTrainCPUKernel(OpParameter *parameter, const std::vector<lite::Tensor *> &inputs,
                                     const std::vector<lite::Tensor *> &outputs, const lite::InnerContext *ctx)
      : LiteKernel(parameter, inputs, outputs, ctx) {}
  ~ConvolutionTrainCPUKernel() override {}

  int Init() override;
  int ReSize() override;
  int Run() override;
  int Execute(int task_id);

 private:
  int ws_size_ = 0;
  bool do_img2col_ = true;
  bool do_dw_ = false;
#ifdef ENABLE_ARM32
  const int chunk_ = C4NUM * 2;
#else
  const int chunk_ = C12NUM * 2;
#endif
};

kernel::LiteKernel *CpuConvTrainFp32KernelCreator(const std::vector<lite::Tensor *> &inputs,
                                                  const std::vector<lite::Tensor *> &outputs, OpParameter *opParameter,
                                                  const lite::InnerContext *ctx, const kernel::KernelKey &desc);
}  // namespace mindspore::kernel

#endif  // MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_FP32_GRAD_CONVOLUTION_H_
