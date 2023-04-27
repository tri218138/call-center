import json
import numpy as np

with open("output\output3.json", "r") as f:
    output3 = json.load(f)

with open('./data/json/shifts.json', 'r') as f:
    shifts = json.load(f)

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

if ret:
    print("A result is correct")
else:
    print("Some CSR does not have a break day")

