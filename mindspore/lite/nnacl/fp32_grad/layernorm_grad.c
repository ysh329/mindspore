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
#include "nnacl/fp32_grad/layernorm_grad.h"
#include <stddef.h>
#include <math.h>

void LayerNormGrad(const float *x, const float *dy, const float *var, const float *mean, const float *gamma,
                   int param_num, int param_size, int block_num, int block_size, float *dx, float *dg, float *db) {
  // var is actually 1/sqrf(var)-> var^0.5
  const float *var_sqrt_rev = var;
  for (size_t i = 0; i < param_num; ++i) {
    float dgamma = 0.0f;
    float dbeta = 0.0f;
    for (size_t j = i; j < param_size * param_num; j += param_num) {
      int norm_shift = (int)(j / block_size);
      dgamma += dy[j] * var_sqrt_rev[norm_shift] * (x[j] - mean[norm_shift]);
      dbeta += dy[j];
    }
    dg[i] = dgamma;
    db[i] = dbeta;
  }
  for (size_t i = 0; i < block_num; ++i) {
    float sum1 = 0.0f;
    float sum2 = 0.0f;
    float sum3 = 0.0f;
    for (size_t j = i * block_size; j < (i + 1) * block_size; ++j) {
      int param_shift = j % param_num;
      int norm_shift = (int)(j / block_size);
      float dxm = x[j] - mean[norm_shift];
      float dyg = dy[j] * gamma[param_shift];
      sum1 += -0.5f * dyg * dxm * var_sqrt_rev[norm_shift] * var_sqrt_rev[norm_shift] * var_sqrt_rev[norm_shift];
      sum3 += -2.0f * dxm;
    }
    for (size_t j = i * block_size; j < (i + 1) * block_size; ++j) {
      int param_shift = j % param_num;
      int norm_shift = (int)(j / block_size);
      float var_sqrt = var_sqrt_rev[norm_shift];
      float dx1 = dy[j] * gamma[param_shift] * var_sqrt;
      float dx2 = sum1 * 2.0f / block_size * (x[j] - mean[norm_shift]);
      float dx3 = (-1.0f * var_sqrt * sum2 + (1.0f / block_size) * sum1 * sum3) * (1.0f / block_size);
      dx[j] = dx1 + dx2 + dx3;
    }
  }
}
