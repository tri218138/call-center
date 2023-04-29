import subprocess
import sys
from solutions import task1 as sol_task1, task2 as sol_task2, task3 as sol_task3
from evaluation import task1 as eval_task1, task2 as eval_task2, task3 as eval_task3, task4 as eval_task4
import pathlib

HOME_PATH = pathlib.Path(__file__).parent

def run_test():
    program = [eval_task1, eval_task2, eval_task3]
    for idx, prog in enumerate(program):
        print(f"Evaluating the ouput of task{idx + 1} from output/output{idx + 1}.json")
        prog.main(HOME_PATH / "output" / f"output{idx + 1}.json")
        print("============================================")

    try:
        print(f"Evaluating the ouput of task{4} from output/output{4}.json")
        eval_task4.main(HOME_PATH / "output" / f"output{4}_{sys.argv[2]}.json")
        print("============================================")
    except:
        print("Check your command line")
def main():
    program = [sol_task1, sol_task2, sol_task3]
    for idx, prog in enumerate(program):
        print(f"Checking the output of task{idx + 1} from output/output{idx + 1}.json")
        prog.main()
        print("============================================")

if __name__ == '__main__':
    print("""
    To run solve tasks:    python run.py
    To run validate tasks: python run.py test
                           python run.py test merge
                           python run.py test balance
                           python run.py test mod
    """)
    if "test" in sys.argv:
        run_test()
    else:
        main()