import json

with open('./data/json/days.json', 'r') as f:
    days = json.load(f)

with open('./data/json/shifts.json', 'r') as f:
    shifts = json.load(f)

with open('./data/json/week.json', 'r') as f:
    week = json.load(f)

with open("output\output1.json", "r") as f:
    output1 = json.load(f)
# print(days)
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
    print("A result is correct")