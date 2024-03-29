# Source code for Q2: Minimum CSRs for a week

# Import libraries
import json
from math import ceil
from typing import List, Dict, Optional
import pathlib
from solutions.utility import write_output_to_file
# try:
#     from solutions.utility import write_output_to_file
# except:
#     from utility import write_output_to_file

HOME_PATH = pathlib.Path(__file__).parent.parent

def solve(CSR_by_shift: Dict[str, List[Optional[str]]]):
    ######################################################################################

    # Set total working days per week
    nd = len(list(CSR_by_shift.values())[0])

    ######################################################################################

    # Calculate max number of CSR for a day
    CSRs = list(CSR_by_shift.keys())
    max_nc = len(CSRs)

    ######################################################################################

    # Calculate number of CSR each day & total empty slot
    nc = [0] * nd
    ne = 0
    for j in range(0, nd):
        empty_slot = [CSR for CSR in CSRs if CSR_by_shift[CSR][j] == None]
        ne += len(empty_slot)
        nc[j] = max_nc - len(empty_slot)

    ######################################################################################

    # Calculate additional number of CSR to ensure every CSR has at least 1 day off each week
    x = max(0, int(ceil((max_nc - ne) / (nd - 1))))

    ######################################################################################

    # Generate output
    ## update new number of CSR
    max_nc += x

    ## create new CSR list
    CSR_by_week = CSR_by_shift
    ## add x new CSRs to list
    for cnt in range(1, x + 1):
        CSR_name = "NV" + str(int(CSRs[-1][2:]) + 1)
        CSR_by_week[CSR_name] = [None] * nd
        CSRs.append(CSR_name)

    ## arrange day off
    first_off_of_day = 0
    r_CSRs = CSRs[::-1]
    for j in range(0, nd):
        empty_slot = max_nc - nc[j]

        # move shift down
        if first_off_of_day + empty_slot <= max_nc:
            for i in range(0, max_nc - first_off_of_day - empty_slot):
                CSR = r_CSRs[i]
                ref_CSR = r_CSRs[i + empty_slot]
                CSR_by_week[CSR][j] = CSR_by_week[ref_CSR][j]
        else:
            for i in range(max_nc - first_off_of_day, 2 * max_nc - first_off_of_day - empty_slot):
                CSR = r_CSRs[i]
                ref_CSR = r_CSRs[i + (first_off_of_day + empty_slot) - max_nc]
                CSR_by_week[CSR][j] = CSR_by_week[ref_CSR][j]

        # add 'None' to appropriate slot
        for i in range(0, empty_slot):
            off_CSR = CSRs[(first_off_of_day + i) % max_nc]
            CSR_by_week[off_CSR][j] = None

        first_off_of_day = (first_off_of_day + empty_slot) % max_nc

    return CSR_by_week


def main():
    # Import data
    
    file = open(HOME_PATH / "output" / "output1.json")
    CSR_by_shift = json.load(file)

    CSR_by_week = solve(CSR_by_shift)

    ######################################################################################

    write_output_to_file(HOME_PATH / "output" / "output2.json", CSR_by_week)

if __name__ == "__main__":
    main()
