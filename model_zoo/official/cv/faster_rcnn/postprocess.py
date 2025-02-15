# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""post process for 310 inference"""
import argparse
import numpy as np
from pycocotools.coco import COCO

from src.config import config
from src.util import coco_eval, bbox2result_1image, results2json

dst_width = 1280
dst_height = 768

parser = argparse.ArgumentParser(description="FasterRcnn inference")
parser.add_argument("--ann_file", type=str, required=True, help="ann file.")
parser.add_argument("--img_path", type=str, required=True, help="image file path.")
args = parser.parse_args()

def get_eval_result(ann_file):
    """ get evaluation result of faster rcnn"""
    max_num = 128
    result_path = "./result_Files/"

    outputs = []

    dataset_coco = COCO(ann_file)
    img_ids = dataset_coco.getImgIds()

    for img_id in img_ids:
        file_id = str(img_id).zfill(12)

        bbox_result_file = result_path + file_id + "_0.bin"
        label_result_file = result_path + file_id + "_1.bin"
        mask_result_file = result_path + file_id + "_2.bin"

        all_bbox = np.fromfile(bbox_result_file, dtype=np.float32).reshape(80000, 5)
        all_label = np.fromfile(label_result_file, dtype=np.int32).reshape(80000, 1)
        all_mask = np.fromfile(mask_result_file, dtype=np.bool_).reshape(80000, 1)

        all_bbox_squee = np.squeeze(all_bbox)
        all_label_squee = np.squeeze(all_label)
        all_mask_squee = np.squeeze(all_mask)

        all_bboxes_tmp_mask = all_bbox_squee[all_mask_squee, :]
        all_labels_tmp_mask = all_label_squee[all_mask_squee]

        if all_bboxes_tmp_mask.shape[0] > max_num:
            inds = np.argsort(-all_bboxes_tmp_mask[:, -1])
            inds = inds[:max_num]
            all_bboxes_tmp_mask = all_bboxes_tmp_mask[inds]
            all_labels_tmp_mask = all_labels_tmp_mask[inds]

        outputs_tmp = bbox2result_1image(all_bboxes_tmp_mask, all_labels_tmp_mask, config.num_classes)
        outputs.append(outputs_tmp)

    eval_types = ["bbox"]
    result_files = results2json(dataset_coco, outputs, "./results.pkl")
    coco_eval(result_files, eval_types, dataset_coco, single_result=False)

if __name__ == '__main__':
    get_eval_result(args.ann_file)
