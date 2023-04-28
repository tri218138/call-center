import json
import task1, task2, task3
import math
import numpy as np
import pathlib
from typing import Dict, List, Optional

def solve(
    shifts_dict: Dict[str, List[int]], day_dict: Dict[str, List[int]]
) -> Dict[str, List[Optional[str]]]:
    table_1 = {
        name: [math.ceil(period / 2) if name != "Saturday" else period for period in shift]
        for name, shift in day_dict.items() if name != "Sunday"
    }
    print("# Monday - Saturday")
    print(table_1)


    table_2 = {
        name: [math.floor(period / 2) if name != "Sunday" else period for period in shift]
        for name, shift in day_dict.items() if name != "Saturday"
    }

    print("#Monday - Friday, Sunday")
    print(table_2)

    schedule_1 = task1.solve(shifts_dict, table_1)
    schedule_1 = task2.solve(schedule_1)
    schedule_1 = task3.solve(shifts_dict, table_1, schedule_1)
    schedule_1 = { employee: shift + [None] for employee, shift in schedule_1.items()}


    schedule_2 = task1.solve(shifts_dict, table_2)
    schedule_2 = task2.solve(schedule_2)
    schedule_2 = task3.solve(shifts_dict, table_2, schedule_2)
    offset = len(schedule_2.keys()) + 1
    for employee, shift in schedule_2.items():
        shift.insert(-1, None)
    schedule_2 = {f"NV{int(employee[-1])+ offset}": shift for employee, shift in schedule_2.items()}

    merge = list(schedule_1.items()) + list(schedule_2.items())
    return {employee: shift for employee, shift in merge}

def main():
    HOME_PATH = pathlib.Path(__file__).parent.parent

    csr_day_file_path = HOME_PATH / "data" / "json" / "days.json"
    print(csr_day_file_path)
    with open(csr_day_file_path) as csr_day_file:
        day_dict = json.load(csr_day_file)

    shifts_detail_file_path = HOME_PATH / "data" / "json" / "shifts.json"
    with open(shifts_detail_file_path) as shifts_detail_file:
        shifts_dict = json.load(shifts_detail_file)

    merge = solve(shifts_dict, day_dict)

    with open(HOME_PATH / "output" / "output4.json", "w") as f:
        json.dump(merge, f, indent=None)

    ## read the file contents and modify them (each NV on 1 line)
    with open(HOME_PATH / "output" / "output4.json", "r") as f:
        contents = f.read()
        # Replace newlines with ',\n' except for lines that contain a list value
        contents = contents.replace("], ", "],\n\t")
        contents = contents.replace("{", "{\n\t")
        contents = contents.replace("]}", "]\n}")
        # print(contents)

    ## overwrite the file with the modified contents
    with open(HOME_PATH / "output" / "output4.json", "w") as f:
        f.write(contents)

    K = shifts_dict.keys()
    I = merge.keys()
    freq = {}
    for k in K:
        freq[k] = np.zeros(len(I))

    for idx, i in enumerate(I):
        for k in merge[i]:
            if k is None: continue
            freq[k][idx] += 1
    # print(freq)
    F = freq.keys()
    ret = True
    for f in F:
        min_val = np.min(freq[f])
        max_val = np.max(freq[f])
        if abs(max_val - min_val) > 1:
            ret = False

    if ret:
        print("A result is correct")
    else:
        print("Some CSR does not have a break day")

if __name__ == "__main__":
    main()