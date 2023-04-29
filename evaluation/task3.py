import json
import numpy as np
import pathlib

HOME_PATH = pathlib.Path(__file__).parent.parent

with open(HOME_PATH / 'data' / 'json' / 'shifts.json', 'r') as f:
    shifts = json.load(f)

def main(path = HOME_PATH / 'output' / "output1.json"):
    with open(path, "r") as f:
        output3 = json.load(f)
    K = shifts.keys()
    I = output3.keys()
    freq = {}
    for k in K:
        freq[k] = np.zeros(len(I))

    for idx, i in enumerate(I):
        for k in output3[i]:
            if k is None: continue
            freq[k][idx] += 1
    # print(freq)
    F = freq.keys()
    ret = True
    for f in F:
        min_val = np.min(freq[f])
        max_val = np.max(freq[f])
        # print(min_val, max_val)
        if abs(max_val - min_val) > 1:
            ret = False
            print(f"The schedule of shift {f} is not fair at some CSR")

    if ret:
        print("Conclusion: A result is correct")
    else:
        print("Conclusion: Some CSR does not have a fair schedule with another")

if __name__ == "__main__":
    main(HOME_PATH / 'output' / "output3.json")