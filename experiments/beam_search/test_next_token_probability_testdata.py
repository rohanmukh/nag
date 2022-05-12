# Copyright 2017 Rice University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import argparse
import sys
import os

from program_helper.infer_model_helper import InferModelHelper
from utilities.basics import conditional_director_creator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

NUM_DATA = 100
SKIP_DATA = 0
BEAM_WIDTH = 10
SEED = 500


def test_next_token_probability(_clargs):
    conditional_director_creator(clargs.temp_result_path)
    dump_data_path = os.path.join(_clargs.temp_result_path, 'test_data')
    conditional_director_creator(dump_data_path)

    infer_model = InferModelHelper(model_path=_clargs.continue_from,
                                   seed=SEED,
                                   beam_width=BEAM_WIDTH,
                                   max_num_data=NUM_DATA,
                                   depth=None,
                                   visibility=_clargs.visibility
                                   )

    infer_model.read_and_dump_data(filepath=_clargs.filepath,
                                   data_path=dump_data_path,
                                   )

    avg_prob_dict = infer_model.get_next_token(
        data_path=dump_data_path,
        categories=['concept', 'api', 'type', 'clstype', 'var', 'op', 'method']
        )


    for cat in avg_prob_dict.keys():
        print("The average probability for {} is {}".format(cat, avg_prob_dict[cat]))
    infer_model.close()

# %%
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--python_recursion_limit', type=int, default=10000,
                        help='set recursion limit for the Python interpreter')
    parser.add_argument('--continue_from', type=str, default='save',
                        help='ignore config options and continue training model checkpointed here')
    # parser.add_argument('--data', default='../data_extraction/data_reader/data')
    parser.add_argument('--filepath', default=None)
    parser.add_argument('--temp_result_path', type=str, default='results/test_next_tokem/')
    parser.add_argument('--visibility', type=float, default=1.00)


    clargs = parser.parse_args()
    sys.setrecursionlimit(clargs.python_recursion_limit)

    test_next_token_probability(clargs)
