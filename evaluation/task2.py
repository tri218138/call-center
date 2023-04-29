import json
import pathlib

HOME_PATH = pathlib.Path(__file__).parent.parent

def main(path = HOME_PATH / "output" / "output2.json"):

    with open(path, "r") as f:
        output2 = json.load(f)

    I = output2.keys()

    ret = True
    for i in I:
        haveBreak = False
        for k in output2[i]:
            if k is None:
                haveBreak = True
        if not haveBreak:
            print(f"CSR {i} does not have a day off")
        ret = ret and haveBreak

    if ret:
        print("Conclusion: A result is correct")
    else:
        print("Conclusion: Some CSR does not have a break day")

if __name__ == "__main__":
    main(HOME_PATH / "output" / "output2.json")