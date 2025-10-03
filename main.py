"""
Orchestrator: run all stages in order. Outputs CSV at each stage in output/.
Usage: python main.py         # runs full pipeline
       python main.py --stages 1 2   # run selected stages
"""
import argparse
from stage1_extract import run_stage1
from stage2_probabilities import run_stage2
from stage3_estimate_lambda import run_stage3
from stage4_mu_sigma import run_stage4
from stage5_regression import run_stage5


def main(run_stages=None):
    if run_stages is None:
        run_stages = [1,2,3,4,5]
    if 1 in run_stages:
        run_stage1()
    if 2 in run_stages:
        run_stage2()
    if 3 in run_stages:
        run_stage3()
    if 4 in run_stages:
        run_stage4()
    if 5 in run_stages:
        run_stage5()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stages', nargs='*', type=int, help='stages to run (1..5)')
    args = parser.parse_args()
    main(args.stages)