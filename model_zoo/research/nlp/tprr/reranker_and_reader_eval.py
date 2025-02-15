# Copyright 2021 Huawei Technologies Co., Ltd
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
"""main file"""

from mindspore import context
from src.rerank_and_reader_utils import get_parse, cal_reranker_metrics, select_reader_dev_data
from src.reranker_eval import rerank
from src.reader_eval import read
from src.hotpot_evaluate_v1 import hotpotqa_eval
from src.build_reranker_data import get_rerank_data


def rerank_and_retriever_eval():
    """main function"""
    context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")
    parser = get_parse()
    args = parser.parse_args()

    if args.get_reranker_data:
        get_rerank_data(args)

    if args.run_reranker:
        rerank(args)

    if args.cal_reranker_metrics:
        total_top1_pem, _, _ = \
            cal_reranker_metrics(dev_gold_file=args.dev_gold_file, rerank_result_file=args.rerank_result_file)
        print(f"total top1 pem: {total_top1_pem}")

    if args.select_reader_data:
        select_reader_dev_data(args)

    if args.run_reader:
        read(args)

    if args.cal_reader_metrics:
        metrics = hotpotqa_eval(args.reader_result_file, args.dev_gold_file)
        for k in metrics:
            print(f"{k}: {metrics[k]}")


if __name__ == "__main__":
    rerank_and_retriever_eval()
