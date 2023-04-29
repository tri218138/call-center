import subprocess
import sys

def run_test():
    for i in range(1, 4):
        print(f"Evaluating the ouput of task{i} from output/output{i}.json")
        subprocess.call(['python', f'task{i}.py'], cwd="evaluation")
        print("============================================")

def main():
    for i in range(1, 4):
        print(f"Checking the output of task{i} from output/output{i}.json")
        subprocess.call(['python', f'task{i}.py'], cwd = "solutions")
        print("============================================")

if __name__ == '__main__':
    print("""
    To run solve tasks:    python run.py
    To run validate tasks: python run.py test
    """)

    if "test" in sys.argv:
        run_test()
    else:
        main()