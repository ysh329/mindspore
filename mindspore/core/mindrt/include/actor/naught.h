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

#ifndef MINDSPORE_CORE_MINDRT_INCLUDE_ACTOR_NAUGHT_H
#define MINDSPORE_CORE_MINDRT_INCLUDE_ACTOR_NAUGHT_H

#include <memory>

namespace mindspore {

class Naught;
class ActorBase;

typedef std::shared_ptr<Naught> UniqueNaught;
typedef std::shared_ptr<Naught> SharedNaught;
typedef std::string BusString;

// Lite , start from Naught
class Naught {
 public:
  virtual ~Naught() {}
};

};  // namespace mindspore

#endif
