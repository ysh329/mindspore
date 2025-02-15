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
#include <sys/stat.h>
#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include "common/common_test.h"
#include "include/api/types.h"
#include "minddata/dataset/include/execute.h"
#include "minddata/dataset/include/transforms.h"
#include "minddata/dataset/include/vision.h"
#ifdef ENABLE_ACL
#include "minddata/dataset/include/vision_ascend.h"
#endif
#include "minddata/dataset/kernels/tensor_op.h"
#include "include/api/model.h"
#include "include/api/serialization.h"
#include "include/api/context.h"

using namespace mindspore;
using namespace mindspore::dataset;
using namespace mindspore::dataset::vision;

class TestZeroCopy : public ST::Common {
 public:
  TestZeroCopy() {}
};

constexpr auto resnet_file = "/home/workspace/mindspore_dataset/mindir/resnet50/resnet50_imagenet.mindir";
constexpr auto image_path = "/home/workspace/mindspore_dataset/imagenet/imagenet_original/val/n01440764/";
constexpr auto aipp_path = "./data/dataset/aipp_resnet50.cfg";

size_t GetMax(mindspore::MSTensor data);
std::string RealPath(std::string_view path);
DIR *OpenDir(std::string_view dir_name);
std::vector<std::string> GetAllFiles(std::string_view dir_name);

TEST_F(TestZeroCopy, TestMindIR) {
#ifdef ENABLE_ACL
    // Set context
    mindspore::GlobalContext::SetGlobalDeviceTarget(mindspore::kDeviceTypeAscend310);
    mindspore::GlobalContext::SetGlobalDeviceID(0);
    auto model_context = std::make_shared<ModelContext>();
    ModelContext::SetInsertOpConfigPath(model_context,aipp_path);
    // Define model
    auto graph = mindspore::Serialization::LoadModel(resnet_file, mindspore::ModelType::kMindIR);
    mindspore::Model resnet50(mindspore::GraphCell(graph),model_context);
    // Build model
    ASSERT_TRUE(resnet50.Build() == kSuccess);
    // Get model info
    std::vector<mindspore::MSTensor> model_inputs =resnet50.GetInputs();
    ASSERT_EQ(model_inputs.size(), 1);
    // Define transform operations
    std::shared_ptr<TensorTransform> decode(new vision::Decode());
    std::shared_ptr<TensorTransform> resize(new vision::Resize({256}));
    std::shared_ptr<TensorTransform> center_crop(new vision::CenterCrop({224,224}));
    mindspore::dataset::Execute Transform({decode,resize,center_crop},MapTargetDevice::kAscend310);
    size_t count=0;
    // Read images
    std::vector<std::string> images =GetAllFiles(image_path);
    for(const auto &image_file:images){
        // prepare input
        std::vector<mindspore::MSTensor> inputs;
        std::vector<mindspore::MSTensor> outputs;
        std::shared_ptr<mindspore::dataset::Tensor> de_tensor;
        mindspore::dataset::Tensor::CreateFromFile(image_file, &de_tensor);
        auto image = mindspore::MSTensor(std::make_shared<mindspore::dataset::DETensor>(de_tensor));
        // Apply transform on images
        Status rc = Transform(image, &image);
        ASSERT_TRUE(rc == kSuccess);
        inputs.push_back(image);
        // infer
        ASSERT_TRUE(resnet50.Predict(inputs, &outputs)==kSuccess);
        if(GetMax(outputs[0])==0){
          ++count;
        }
        Transform.DeviceMemoryRelease();
    }
    ASSERT_GE(static_cast<double>(count)/images.size()*100.0, 20.0);
#endif
}

size_t GetMax(mindspore::MSTensor data) {
  float max_value = -1;
  size_t max_idx = 0;
  const float *p = reinterpret_cast<const float *>(data.MutableData());
  for (size_t i = 0; i < data.DataSize() / sizeof(float); ++i) {
    if (p[i] > max_value) {
      max_value = p[i];
      max_idx = i;
    }
  }
  return max_idx;
}

std::string RealPath(std::string_view path) {
  char real_path_mem[PATH_MAX] = {0};
  char *real_path_ret = realpath(path.data(), real_path_mem);
  if (real_path_ret == nullptr) {
    return "";
  }
  return std::string(real_path_mem);
}

DIR *OpenDir(std::string_view dir_name) {
  // check the parameter !
  if (dir_name.empty()) {
    return nullptr;
  }
  std::string real_path = RealPath(dir_name);

  // check if dir_name is a valid dir
  struct stat s;
  lstat(real_path.c_str(), &s);
  if (!S_ISDIR(s.st_mode)) {
    return nullptr;
  }

  DIR *dir;
  dir = opendir(real_path.c_str());
  if (dir == nullptr) {
    return nullptr;
  }
  return dir;
}

std::vector<std::string> GetAllFiles(std::string_view dir_name) {
  struct dirent *filename;
  DIR *dir = OpenDir(dir_name);
  if (dir == nullptr) {
    return {};
  }
  /* read all the files in the dir ~ */
  std::vector<std::string> res;
  while ((filename = readdir(dir)) != nullptr) {
    std::string d_name = std::string(filename->d_name);
    // get rid of "." and ".."
    if (d_name == "." || d_name == ".." || filename->d_type != DT_REG)
      continue;
    res.emplace_back(std::string(dir_name) + "/" + filename->d_name);
  }

  std::sort(res.begin(), res.end());
  return res;
}
