import json
import numpy as np
import pathlib
from evaluation import task1 as eval_task1, task2 as eval_task2, task3 as eval_task3

HOME_PATH = pathlib.Path(__file__).parent.parent

def main(path = HOME_PATH / "output" / "output4_balance.json"):
    program = [eval_task1, eval_task2, eval_task3]
    for idx, prog in enumerate(program):
        print(f"Task {idx + 1}:", end = ' ')
        prog.main(path)
    
    print("Task 4:")
    with open(path, "r") as f:
        output4 = json.load(f)
    I = output4.keys()
    ret = True
    for idx, i in enumerate(I):
        if output4[i][-1] is not None and output4[i][-2] is not None:
            print(f"CSR {idx} does not have a day off at weekend")
            ret = False
    if ret:
        print("Conclusion: A result is correct")
    else:
        print("Conclusion: Some CSR does not have a day off at weekend")
if __name__ == "__main__":
    main()