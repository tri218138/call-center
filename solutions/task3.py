"""
Task 3: Scheduling CSR for 1 week, maximize workload fairness
"""
import itertools
from pathlib import Path

import numpy as np

from task3_domain import CsrRequirePerDayDetails, ShiftSpanDetail, RawSchedule, ProblemInput


def main():
    csr_day_file = Path("./../data/json/days.json")
    csr_requirement_per_day = CsrRequirePerDayDetails.from_json_file(csr_day_file)

    shifts_detail_file = Path("./../data/json/shifts.json")
    shifts_detail = ShiftSpanDetail.from_json_file(shifts_detail_file)

    output2_file = Path("./../data/json/output2.json")
    raw_schedules = RawSchedule.from_json_file(output2_file)

    solve_lp_problem(
        ProblemInput(
            num_of_csr_i=raw_schedules.num_of_csr,
            num_of_day_per_week_j=csr_requirement_per_day.num_of_day_per_week,
            num_of_shifts_k=shifts_detail.num_of_available_shifts,
            num_of_period_per_day_t=csr_requirement_per_day.num_of_period_per_day_t,
        )
    )


def solve_lp_problem(problem_input: ProblemInput):
    """
    The variables would be structured into a 1D array, as follows:
    [x_{1,1,1} ; x_{1,1,2} ; ... ; x{1,2,1} ; x{1,2,2} ; ... ; x_{2,1,1} ; x_{2,1,2} ; ... ]

    :return:
    """

    coefficients_c = np.ones(problem_input.num_of_optimized_vars)

    a_ub, b_ub = get_matrix_for_condition_one_shift_per_day(problem_input)
    a_ub, b_ub = get_matrix_for_condition_one_day_off_per_week(problem_input)


def get_matrix_for_condition_one_shift_per_day(
    problem_input: ProblemInput,
) -> [np.ndarray, np.ndarray]:
    """
    :param problem_input:

    :return: A_ub & b_ub
    """
    in_eq_constraint_matrix = np.zeros(
        (
            problem_input.num_of_csr_i * problem_input.num_of_day_per_week_j,
            problem_input.num_of_optimized_vars,
        )
    )

    for processing_row, (csr_i, day_j) in enumerate(
        itertools.product(
            range(problem_input.num_of_csr_i), range(problem_input.num_of_day_per_week_j)
        )
    ):
        for shift_k in range(problem_input.num_of_shifts_k):
            optimized_var_loc = convert_i_j_k_to_1d_arr_loc(csr_i, day_j, shift_k, problem_input)

            in_eq_constraint_matrix[processing_row, optimized_var_loc] = 1

    in_eq_constraint_vector = np.ones(
        problem_input.num_of_csr_i * problem_input.num_of_day_per_week_j
    )

    return in_eq_constraint_matrix, in_eq_constraint_vector


def get_matrix_for_condition_one_day_off_per_week(
    problem_input: ProblemInput,
) -> [np.ndarray, np.ndarray]:
    """
    :param problem_input:

    :return: A_ub & b_ub
    """
    in_eq_constraint_matrix = np.zeros(
        (
            problem_input.num_of_csr_i,
            problem_input.num_of_optimized_vars,
        )
    )

    for processing_row, csr_i in enumerate(range(problem_input.num_of_csr_i)):
        for day_j, shift_k in itertools.product(
            range(problem_input.num_of_day_per_week_j), range(problem_input.num_of_shifts_k)
        ):
            optimized_var_loc = convert_i_j_k_to_1d_arr_loc(csr_i, day_j, shift_k, problem_input)
            in_eq_constraint_matrix[processing_row, optimized_var_loc] = 1

    in_eq_constraint_vector = np.repeat(
        problem_input.num_of_day_per_week_j - 1, problem_input.num_of_csr_i
    )

    return in_eq_constraint_matrix, in_eq_constraint_vector


def get_matrix_for_condition_csr_num_required_per_period(
    problem_input: ProblemInput,
) -> [np.ndarray, np.ndarray]:
    """
    Because we can only do ≤ inequality, we will perform inverse (-1)
    :param problem_input:

    :return: A_ub & b_ub
    """

    in_eq_constraint_matrix = np.zeros(
        (
            problem_input.num_of_csr_i,
            problem_input.num_of_optimized_vars,
        )
    )

    for processing_row, (day_j, period_t) in enumerate(
        itertools.product(
            range(problem_input.num_of_day_per_week_j), range(problem_input.num_of_period_per_day_t)
        )
    ):
        for csr_i, shift_k in itertools.product(
            range(problem_input.num_of_day_per_week_j), range(problem_input.num_of_shifts_k)
        ):
            optimized_var_loc = convert_i_j_k_to_1d_arr_loc(csr_i, day_j, shift_k, problem_input)
            in_eq_constraint_matrix[processing_row, optimized_var_loc] = 1

    in_eq_constraint_vector = np.repeat(
        problem_input.num_of_day_per_week_j - 1, problem_input.num_of_csr_i
    )

    return in_eq_constraint_matrix, in_eq_constraint_vector


def convert_i_j_k_to_1d_arr_loc(
    csr_i: int, day_j: int, shift_k: int, problem_input: ProblemInput
) -> int:
    return (
        (csr_i * problem_input.num_of_day_per_week_j * problem_input.num_of_shifts_k)
        + (day_j * problem_input.num_of_shifts_k)
        + shift_k
    )


if __name__ == "__main__":
    main()
