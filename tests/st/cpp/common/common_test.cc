/**
 * Copyright 2020 Huawei Technologies Co., Ltd
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
#include "common/common_test.h"
#include "include/api/context.h"

#ifdef __cplusplus
#if __cplusplus
extern "C" {
#endif
#endif

namespace ST {
static std::string GetEnv(const std::string &envvar) {
  const char *value = std::getenv(envvar.c_str());
  if (value == nullptr) {
    return "";
  }

  return std::string(value);
}

void Common::SetUpTestCase() {}

void Common::TearDownTestCase() {}

void Common::SetUp() {}

void Common::TearDown() {}

void Common::ReadFile(const char *file, size_t *size, char **buf) {
  ASSERT_NE(nullptr, file);
  ASSERT_NE(nullptr, size);
  ASSERT_NE(nullptr, buf);
  std::string path = std::string(file);
  std::ifstream ifs(path);
  ASSERT_EQ(true, ifs.good());
  ASSERT_EQ(true, ifs.is_open());

  ifs.seekg(0, std::ios::end);
  *size = ifs.tellg();
  *buf = new char[*size];

  ifs.seekg(0, std::ios::beg);
  ifs.read(*buf, *size);
  ifs.close();
}

void Common::ContextAutoSet() {
  auto device_target = GetEnv("DEVICE_TARGET");
  if (device_target.empty()) {
    device_target = mindspore::kDeviceTypeAscend310;  // default is 310
  }

  auto device_id_str = GetEnv("DEVICE_ID");
  if (device_id_str.empty()) {
    device_id_str = "0";  // default is 0
  }
  uint32_t device_id = std::strtoul(device_id_str.c_str(), nullptr, 10);

  mindspore::GlobalContext::SetGlobalDeviceTarget(device_target);
  mindspore::GlobalContext::SetGlobalDeviceID(device_id);
}
}  // namespace ST

#ifdef __cplusplus
#if __cplusplus
}
#endif
#endif
