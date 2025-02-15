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
#include "debug/rdr/task_debug_info_recorder.h"
#include "runtime/device/ascend/tasksink/task_generator.h"

namespace mindspore {
void TaskDebugInfoRecorder::Export() {
  auto realpath = GetFileRealPath(std::to_string(graph_id_));
  if (!realpath.has_value()) {
    return;
  }
  std::string file_path = realpath.value() + ".ir";
  device::ascend::tasksink::TaskGenerator::DumpTaskInfo(file_path, task_debug_info_);
}
}  // namespace mindspore
