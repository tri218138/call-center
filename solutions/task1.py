from functools import reduce
from typing import List, Dict, Optional
import numpy as np
import pandas as pd
from scipy.optimize import linprog
from pathlib import Path

from solutions.task1_domain import CSRInquiries, ShiftsDetail, ReadJson


def solve(
    shifts_dict: Dict[str, List[int]], day_dict: Dict[str, List[int]]
) -> Dict[str, List[Optional[str]]]:
    
    shifts_detail = ShiftsDetail(shifts_dict)
    csr_inquiries = CSRInquiries(day_dict)

    coefficients_c = np.ones(shifts_detail.num_of_shifts)
    stat = [
        min_csr_of_a_day(coefficients_c, csr_inquiries, shifts_detail, day_j).tolist()
        for day_j in range(csr_inquiries.num_of_days)
    ]

    min_total_csr = max([reduce(lambda pre, cur: pre + cur, days, 0) for days in stat])

    employee_assignment = np.array(
        [label_shift_to_employee(shift, shifts_detail.columns, min_total_csr) for shift in stat]
    ).T.tolist()

    return {f"NV{i}": em for i, em in enumerate(employee_assignment)}


def min_csr_of_a_day(
    coefficients_c: np.ndarray, csr_inquiries: CSRInquiries, shifts_detail: ShiftsDetail, day_j: int
) -> np.ndarray:
    constraint_matrix, constraint_vector = constraint_min_CSR_of_a_period(
        csr_inquiries, shifts_detail, day_j
    )
    return (
        linprog(coefficients_c, constraint_matrix, constraint_vector, integrality=3)
        .x.astype(int)
    )

def constraint_min_CSR_of_a_period(
    csr_inquiries: CSRInquiries, shifts_detail: ShiftsDetail, at: int
):
    constraint_matrix = -1 * shifts_detail._shifts_detail
    constraint_vector = -1 * csr_inquiries._csr_inquiries[at]
    return constraint_matrix.T, constraint_vector

def label_shift_to_employee(row: List[int], label: List[str], min_total_csr: int):
    assert len(row) == len(label)
    csr_per_day = reduce(lambda pre, cur: pre + cur, row, 0)
    label = [[name] * x for x, name in zip(row, label)] + [(min_total_csr - csr_per_day) * [None]]
    return reduce(lambda pre, cur: pre + cur, label, [])

if __name__ == "__main__":

    read_json = ReadJson(Path("data/json"))
    shifts_dict = read_json.read_shifts()
    day_dict = read_json.read_days()
    print(solve(shifts_dict, day_dict))
