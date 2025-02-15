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
#include "debug/rdr/mem_address_recorder.h"
#include <fstream>
#include <sstream>
#include <utility>
#include "backend/kernel_compiler/kernel.h"

namespace mindspore {
namespace {
std::string MemInfo2String(const std::string &label, const AddressPtrList &info) {
  std::ostringstream ss;
  ss << label << " " << info.size() << std::endl;
  for (size_t i = 0; i < info.size(); i++) {
    if (info[i] != nullptr) {
      ss << "&" << info[i]->addr << " #" << info[i]->size << std::endl;
    }
  }
  return ss.str();
}
}  // namespace
MemAddressRecorder &MemAddressRecorder::Instance() {
  static MemAddressRecorder recorder;
  return recorder;
}

void MemAddressRecorder::SaveMemInfo(const std::string &op_name, const GPUMemInfo &mem_info) {
  std::lock_guard<std::mutex> lock(mtx_);
  std::ostringstream mem_info_stream;
  auto inputs = mem_info.inputs_;
  mem_info_stream << op_name << std::endl;
  mem_info_stream << MemInfo2String("kernel_inputs", *inputs);
  auto workspaces = mem_info.workspaces_;
  mem_info_stream << MemInfo2String("kernel_workspaces", *workspaces);
  auto outputs = mem_info.outputs_;
  mem_info_stream << MemInfo2String("kernel_outputs", *outputs);
  mem_info_stream << std::endl;
  std::string mem_info_str = mem_info_stream.str();
  mem_info_container_[op_name] = mem_info_str;
}

void MemAddressRecorder::Export() {
  auto realpath = GetFileRealPath();
  if (!realpath.has_value()) {
    return;
  }
  std::lock_guard<std::mutex> lock(mtx_);
  std::string file_path = realpath.value() + ".txt";
  ChangeFileMode(file_path, S_IRWXU);
  std::ofstream fout(file_path);
  if (!fout.is_open()) {
    MS_LOG(WARNING) << "Open file for saving gpu memory information failed. File path: '" << file_path << "'.";
    return;
  }
  for (auto &info : mem_info_container_) {
    fout << info.second;
  }
  fout.close();
  ChangeFileMode(file_path, S_IRUSR);
}
}  // namespace mindspore
