import pathlib
HOME_PATH = pathlib.Path(__file__).parent.parent.parent
from solutions.utility import write_output_to_file

default = {
    "Monday":   [6, 9, 9, 8, 3, 3, 7, 8, 8, 5, 3, 3, 2],
    "Tuesday":  [6, 10, 7, 7, 3, 4, 7, 5, 9, 5, 3, 4, 3],
    "Wednesday":[7, 9, 9, 6, 3, 4, 6, 8, 7, 4, 3, 3, 3],
    "Thursday": [6, 9, 8, 6, 4, 4, 5, 8, 7, 5, 4, 3, 4],
    "Friday":   [6, 7, 8, 7, 3, 5, 6, 7, 6, 5, 3, 3, 3],
    "Saturday": [6, 9, 9, 4, 3, 3, 4, 5, 5, 5, 3, 3, 2],
    "Sunday":   [5, 7, 6, 5, 4, 3, 4, 5, 6, 5, 3, 3, 3]
}

def generate_data():
    new_data = default
    for key in new_data:
        for idx, value in enumerate(new_data[key]):
            new_data[key][idx] = value * 1
    return new_data

def main():
    write_output_to_file(HOME_PATH / "data" / "json" / "days.json", generate_data())