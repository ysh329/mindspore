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

#include "coder/generator/train/train_generator.h"
#include <vector>
#include <string>
#include "coder/generator/component/common_component.h"
#include "coder/generator/component/benchmark_component.h"
#include "coder/generator/component/train_component.h"
#include "coder/generator/component/const_blocks/license.h"

namespace mindspore::lite::micro {
void TrainGenerator::CodeGradientFunc(std::ofstream &ofs) const {
  ofs << "float " << config_->module_name() << "_ComputeLossAndGradient() {\n";
  ofs << "  float loss = 0;\n";
  for (const auto &block : ctx_->train_blocks()) {
    ofs << "\t{\n" << block << "\t}\n";
  }
  ofs << "  return loss;\n";
  ofs << "}\n";
}

int TrainGenerator::CodeNetHFile() {
  std::string net_include_file = net_inc_file_path_ + net_inc_hfile_;
  std::ofstream ofs(net_include_file);
  MS_CHECK_TRUE(!ofs.bad(), "filed to open file");
  MS_LOG(INFO) << "write " << net_include_file;
  ofs << g_hwLicense;
  if (config_->code_mode() == CodeMode::Inference) {
    ofs << "#include \"src/runtime/thread_pool.h\"\n";
  }
  ofs << "#include \"microtensor.h\"\n\n";
  CodeTrainParams(ofs);
  CodeInputAndOutputState(ofs, config_->module_name());
  if (config_->target() != kARM32M) {
    CodeInitWeightState(ofs, config_->module_name());
  }
  CodeManageResourceState(ofs, config_->module_name());
  CodeInferenceState(ofs, config_->module_name());
  CodeFeaturesState(ofs, config_->module_name());
  CodeTrainState(ofs, config_->module_name());
  return RET_OK;
}

int TrainGenerator::CodeNetCFile() {
  std::string net_impl_file = net_src_file_path_ + net_src_cfile_;
  std::ofstream ofs(net_impl_file);
  MS_CHECK_TRUE(!ofs.bad(), "filed to open file");
  MS_LOG(INFO) << "write " << net_impl_file;
  CodeSourceFileInclude(ofs, net_weight_hfile_, net_inc_hfile_);
  CodeInputAndOutputImplement(ofs, config_->module_name(), ctx_);
  CodeInitResourceImplement(ofs, config_->module_name(), ctx_);
  CodeFreeResourceImplement(ofs, config_->module_name(), ctx_);
  CodeFeaturesImplement(ofs, config_->module_name(), ctx_);
  CodeNetRunFunc(ofs);
  CodeGradientFunc(ofs);
  CodeTrainImplement(ofs, config_->module_name(), ctx_);
  ofs.close();
  return RET_OK;
}

int TrainGenerator::CodeBenchmarkFile() {
  std::string net_main_impl_file = net_main_file_path_ + net_main_cfile_;
  std::ofstream ofs(net_main_impl_file);
  MS_LOG(INFO) << "write " << net_main_impl_file;
  MS_CHECK_TRUE(!ofs.bad(), "filed to open file");
  std::vector<Tensor *> inputs = ctx_->graph_inputs();
  size_t inputs_num = inputs.size();
  CodeBenchmarkHeader(ofs, net_inc_hfile_);
  CodeBenchmarkUsage(ofs);
  CodeBenchmarkWarmup(ofs, config_->module_name());
  CodeBenchmarkSetInputs(ofs, config_->module_name(), ctx_);
  CodeBenchmarkSetBuffer(ofs, config_->module_name());
  if (config_->target() != kARM32M) {
    CodeBenchmarkInitWeight(ofs, config_->module_name());
  }
  CodeBenchmarkInference(ofs, config_->module_name());
  CodeBenchmarkPrintOutputs(ofs, config_->module_name());
  CodeBenchmarkFreeResourse(ofs, config_->module_name(), inputs_num);
  ofs.close();
  return RET_OK;
}
}  // namespace mindspore::lite::micro
