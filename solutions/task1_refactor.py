from functools import reduce
from typing import List, Dict, Optional
import numpy as np
import pandas as pd
from scipy.optimize import linprog

from solutions.task1_refactor_domain import CSRInquiries, ShiftsDetail


def solve(
    shifts_detail: ShiftsDetail, csr_inquiries: CSRInquiries
) -> Dict[str, List[Optional[str]]]:
    coefficients_c = np.ones(shifts_detail.num_of_shifts)
    q1_result = [
        min_csr_of_a_day(coefficients_c, csr_inquiries, shifts_detail, day_j).x
        for day_j in range(csr_inquiries.num_of_days)
    ]

    # q1_csr = q1_show["Total"].max()
    # q1_show = show_pandas(q1_result, shifts_detail.columns, csr_inquiries.columns)


    # q1_schedule = (
    #     q1_show.apply(lambda row: label_shift_to_employee(row, q1_csr), axis=1)
    #     .set_axis([f"NV{i}" for i in range(1, q1_csr + 1)], axis=1)
    #     .T
    # )

    # q1_dict = q1_schedule.T.to_dict()
    # q1_output = {employee: [shift[s] for s in shift.keys()] for employee, shift in q1_dict.items()}
    # q1_output

    return {}


def min_csr_of_a_day(
    coefficients_c: np.ndarray, csr_inquiries: CSRInquiries, shifts_detail: ShiftsDetail, day_j: int
):
    constraint_matrix, constraint_vector = constraint_min_CSR_of_a_period(
        csr_inquiries, shifts_detail, day_j
    )
    return linprog(coefficients_c, constraint_matrix, constraint_vector, integrality=3)


def constraint_min_CSR_of_a_period(
    csr_inquiries: CSRInquiries, shifts_detail: ShiftsDetail, at: int
):
    constraint_matrix = -1 * shifts_detail._shifts_detail
    constraint_vector = -1 * csr_inquiries._csr_inquiries[at]
    return constraint_matrix.T, constraint_vector


def show_pandas(result, col, row):
    stat = pd.DataFrame(np.array(result), columns=col, index=row, dtype=int)
    stat["Total"] = stat.sum(axis=1)
    return stat


def label_shift_to_employee(row: pd.Series, min_csr: int):
    label = [[name] * x for x, name in zip(row, row.index[:-1])] + [(min_csr - row[-1]) * [None]]
    return pd.Series(reduce(lambda pre, cur: pre + cur, label, []))
