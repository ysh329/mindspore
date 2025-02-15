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
#ifndef MINDSPORE_CCSRC_DEBUG_RDR_BASE_RECORDER_H_
#define MINDSPORE_CCSRC_DEBUG_RDR_BASE_RECORDER_H_
#include <memory>
#include <string>
#include <sstream>
#include <chrono>
#include <iomanip>
#include "debug/common.h"
#include "debug/env_config_parser.h"
#include "mindspore/core/utils/log_adapter.h"

const int maxTagLength = 32;
namespace mindspore {
class BaseRecorder {
 public:
  BaseRecorder() : module_(""), tag_(""), directory_(""), filename_(""), timestamp_("") {}
  BaseRecorder(const std::string &module, const std::string &tag) : module_(module), tag_(tag), filename_("") {
    directory_ = mindspore::EnvConfigParser::GetInstance().rdr_path();

    if (tag.length() > maxTagLength) {
      tag_ = tag.substr(0, maxTagLength);
      MS_LOG(WARNING) << "The tag length is " << tag.length() << ", exceeding the limit " << maxTagLength
                      << ". It will be intercepted as '" << tag_ << "'.";
    }

    std::string err_msg = module_ + ":" + tag_ + " set filename failed.";
    if (!filename_.empty() && !Common::IsFilenameValid(filename_, maxFilenameLength, err_msg)) {
      filename_ = "";
    }

    auto sys_time = std::chrono::system_clock::now();
    auto t_time = std::chrono::system_clock::to_time_t(sys_time);
    std::tm *l_time = std::localtime(&t_time);
    if (l_time == nullptr) {
      timestamp_ = "";
    } else {
      std::stringstream ss;
      ss << std::put_time(l_time, "%Y%m%d%H%M%S");
      timestamp_ = ss.str();
    }
  }
  virtual ~BaseRecorder() {}

  std::string GetModule() const { return module_; }
  std::string GetTag() const { return tag_; }
  std::string GetTimeStamp() const { return timestamp_; }
  std::optional<std::string> GetFileRealPath(const std::string &suffix = "");

  void SetDirectory(const std::string &directory);
  void SetFilename(const std::string &filename);
  void SetModule(const std::string &module) { module_ = module; }
  virtual void Export() {}

 protected:
  std::string module_;
  std::string tag_;
  std::string directory_;
  std::string filename_;
  std::string timestamp_;  // year,month,day,hour,minute,second
  std::string delimiter_{"."};
};
using BaseRecorderPtr = std::shared_ptr<BaseRecorder>;
}  // namespace mindspore
#endif  // MINDSPORE_CCSRC_DEBUG_RDR_BASE_RECORDER_H_
