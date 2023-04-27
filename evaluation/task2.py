import json

with open("output\output2.json", "r") as f:
    output2 = json.load(f)

I = output2.keys()

ret = True
for i in I:
    haveBreak = False
    for k in output2[i]:
        if k is None:
            haveBreak = True
    ret = ret and haveBreak

if ret:
    print("A result is correct")
else:
    print("Some CSR does not have a break day")
