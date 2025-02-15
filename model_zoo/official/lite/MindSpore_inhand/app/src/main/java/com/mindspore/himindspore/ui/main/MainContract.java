/**
 * Copyright 2021 Huawei Technologies Co., Ltd
 * <p>
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * <p>
 * http://www.apache.org/licenses/LICENSE-2.0
 * <p>
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.mindspore.himindspore.ui.main;

import com.mindspore.customview.tablayout.listener.CustomTabEntity;
import com.mindspore.himindspore.net.FileDownLoadObserver;
import com.mindspore.himindspore.net.UpdateInfoBean;

import java.io.File;
import java.util.ArrayList;

public interface MainContract {

    interface View  {
        void showUpdateResult(UpdateInfoBean object);

        void showFail(String s);
    }

    interface Presenter  {
        ArrayList<CustomTabEntity> getTabEntity();

        void getUpdateInfo();

        void downloadApk(String destDir, String fileName, FileDownLoadObserver<File> fileDownLoadObserver);
    }


}
