import json
import pathlib

HOME_PATH = pathlib.Path(__file__).parent.parent

with open(HOME_PATH / 'data' / 'json' / 'days.json', 'r') as f:
    days = json.load(f)

with open(HOME_PATH / 'data' / 'json' / 'shifts.json', 'r') as f:
    shifts = json.load(f)

with open(HOME_PATH / 'data' / 'json' / 'week.json', 'r') as f:
    week = json.load(f)



def main(path = HOME_PATH / 'output' / "output1.json"):

    with open(path, "r") as f:
        output1 = json.load(f)

    J = days.keys()
    K = shifts.keys()
    I = output1.keys()
    for i in I:
        for idx, k in enumerate(output1[i]):
            if k is None: continue
            for t, binary in enumerate(shifts[k]):
                if binary == 1:
                    days[week[str(idx)]][t] -= 1
            # print(days)
    ret = True
    for j in J:
        for idx, val in enumerate(days[j]):
            if val > 0:
                ret = False
                print(f"A result is incorrect because CSR does not enough at {j}, shift {idx}-th")
    if ret:
        print("Conclusion: A result is correct")
    else:
        print("Conclusion: Some day of week does not have enough CSR")

if __name__ == "__main__":
    main(HOME_PATH / 'output' / "output1.json")