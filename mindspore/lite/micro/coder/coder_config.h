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

#ifndef MINDSPORE_LITE_MICRO_CODER_CONFIG_H
#define MINDSPORE_LITE_MICRO_CODER_CONFIG_H

#include <string>

namespace mindspore::lite::micro {
enum Target { kX86 = 0, kARM32M = 1, kARM32A = 2, kARM64 = 3, kAllTargets = 4, kTargetUnknown = 99 };
enum CodeMode { Inference = 0, Train = 1, Code_Unknown = 99 };

inline const char *EnumNameTarget(Target target) {
  switch (target) {
    case kX86:
      return "kX86";
    case kARM32M:
      return "kARM32M";
    case kARM32A:
      return "kARM32A";
    case kARM64:
      return "kARM64";
    case kAllTargets:
      return "kAllTargets";
    default:
      return "kTargetUnknown";
  }
}

inline const char *EnumNameCodeMode(CodeMode codeMode) {
  switch (codeMode) {
    case Inference:
      return "Inference";
    case Train:
      return "Train";
    default:
      return "Code_Unknown";
  }
}

class Configurator {
 public:
  static Configurator *GetInstance() {
    static Configurator configurator;
    return &configurator;
  }

  void set_module_name(const std::string &module_name) { module_name_ = module_name; }
  std::string module_name() const { return module_name_; }

  void set_code_path(const std::string &code_path) { code_path_ = code_path; }
  std::string code_path() const { return code_path_; }

  void set_target(Target target) { target_ = target; }
  Target target() const { return target_; }

  void set_code_mode(CodeMode code_mode) { code_mode_ = code_mode; }
  CodeMode code_mode() const { return code_mode_; }

  void set_debug_mode(bool debug) { debug_mode_ = debug; }
  bool debug_mode() const { return debug_mode_; }

  void set_support_parallel(bool parallel) { support_parallel_ = parallel; }
  bool support_parallel() const { return support_parallel_; }

 private:
  Configurator() = default;
  ~Configurator() = default;

  std::string module_name_;
  std::string code_path_;
  Target target_{kTargetUnknown};
  CodeMode code_mode_{Code_Unknown};
  bool support_parallel_{false};
  bool debug_mode_{false};
};
}  // namespace mindspore::lite::micro

#endif  // MICRO_CODER_CONFIG_H
