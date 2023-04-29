"""
Task 3: Scheduling CSR for 1 week, maximize workload fairness
"""
import itertools
import json
import math
import pathlib
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from scipy.optimize import OptimizeResult, linprog
from solutions.task3_domain import CsrRequirePerDayDetails, ProblemInput, RawSchedule, ShiftSpanDetail
from solutions.utility import write_output_to_file
# try:
#     from solutions.task3_domain import CsrRequirePerDayDetails, ProblemInput, RawSchedule, ShiftSpanDetail
#     from solutions.utility import write_output_to_file
# except:
#     from task3_domain import CsrRequirePerDayDetails, ProblemInput, RawSchedule, ShiftSpanDetail
#     from utility import write_output_to_file

def main():
    HOME_PATH = pathlib.Path(__file__).parent.parent

    csr_day_file_path = HOME_PATH / "data" / "json" / "days.json"
    # print(csr_day_file_path)
    with open(csr_day_file_path) as csr_day_file:
        csr_requirement_per_day = json.load(csr_day_file)

    shifts_detail_file_path = HOME_PATH / "data" / "json" / "shifts.json"
    with open(shifts_detail_file_path) as shifts_detail_file:
        shifts_detail = json.load(shifts_detail_file)

    output2_file_path = HOME_PATH / "output" / "output2.json"
    with open(output2_file_path) as quiz_2_solution_file:
        solution_2_schedule = json.load(quiz_2_solution_file)

    result_dict = solve(shifts_detail, csr_requirement_per_day, solution_2_schedule)

    # with open(HOME_PATH / "output" / "output3.json", "w") as output_json_file:
    #     json.dump(result_dict, output_json_file)

    write_output_to_file(HOME_PATH / "output" / "output3.json", result_dict)


def solve(
    shifts_detail: Dict[str, List[int]],
    days_dict: Dict[str, List[int]],
    solution_2_schedule: Dict[str, List[Optional[str]]],
):
    """
    The variables would be structured into a 1D array, as follows:
    [x_{1,1,1} ; x_{1,1,2} ; ... ; x{1,2,1} ; x{1,2,2} ; ... ; x_{2,1,1} ; x_{2,1,2} ; ... ]

    :return:
    """
    problem_input = ProblemInput(
        shift_span_detail=ShiftSpanDetail(shifts_detail),
        csr_requirement_detail=CsrRequirePerDayDetails(days_dict),
        raw_schedules=RawSchedule(solution_2_schedule),
    )

    coefficients_c = np.ones(problem_input.num_of_optimized_vars)

    a_ub1, b_ub1 = get_matrix_for_condition_one_shift_per_day(problem_input)
    a_ub2, b_ub2 = get_matrix_for_condition_one_day_off_per_week(problem_input)
    a_ub3, b_ub3 = get_matrix_for_condition_csr_num_required_per_period(problem_input)
    a_ub4, b_ub4 = get_matrix_for_condition_csr_must_be_scheduled_fairly(problem_input)

    total_a_ub = np.concatenate((a_ub1, a_ub2, a_ub3, a_ub4))
    total_b_ub = np.concatenate((b_ub1, b_ub2, b_ub3, b_ub4))

    result = linprog(coefficients_c, total_a_ub, total_b_ub, integrality=1)
    # print(result)

    return convert_result_to_dict(result, problem_input)


def get_matrix_for_condition_one_shift_per_day(
    problem_input: ProblemInput,
) -> tuple[np.ndarray, np.ndarray]:
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
) -> tuple[np.ndarray, np.ndarray]:
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
) -> tuple[np.ndarray, np.ndarray]:
    """
    Because we can only do ≤ inequality, we will perform inverse (-1)
    :param problem_input:

    :return: A_ub & b_ub
    """

    in_eq_constraint_matrix = np.zeros(
        (
            problem_input.num_of_day_per_week_j * problem_input.num_of_period_per_day_t,
            problem_input.num_of_optimized_vars,
        )
    )

    for processing_row, (day_j, period_t) in enumerate(
        itertools.product(
            range(problem_input.num_of_day_per_week_j),
            range(problem_input.num_of_period_per_day_t),
        )
    ):
        for csr_i, shift_k in itertools.product(
            range(problem_input.num_of_csr_i), range(problem_input.num_of_shifts_k)
        ):
            period_is_spanned = problem_input.shift_span_detail.check_for_spanning(
                shift_k, period_t
            )
            if not period_is_spanned:
                continue

            optimized_var_loc = convert_i_j_k_to_1d_arr_loc(csr_i, day_j, shift_k, problem_input)
            in_eq_constraint_matrix[processing_row, optimized_var_loc] = -1

    in_eq_constraint_vector = -(
        problem_input.csr_requirement_detail.get_vector_of_day_and_require_csr()
    )

    return in_eq_constraint_matrix, in_eq_constraint_vector


def get_matrix_for_condition_csr_must_be_scheduled_fairly(
    problem_input: ProblemInput,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Because we can only do ≤ inequality, we will perform inverse (-1)
    :param problem_input:

    :return: A_ub & b_ub
    """

    num_of_total_required_csr_nc = problem_input.num_of_csr_i

    in_eq_constraint_matrix_upper_bound = np.zeros(
        (
            problem_input.num_of_shifts_k * problem_input.num_of_csr_i,
            problem_input.num_of_optimized_vars,
        )
    )

    in_eq_constraint_vector = []

    for processing_row, (shift_k, csr_i) in enumerate(
        itertools.product(range(problem_input.num_of_shifts_k), range(problem_input.num_of_csr_i))
    ):
        num_of_csr_for_shift_nc_k = problem_input.required_csr_per_shift_nc_k[shift_k]
        upper_bound = math.ceil(num_of_csr_for_shift_nc_k / num_of_total_required_csr_nc)

        for day_j in range(problem_input.num_of_day_per_week_j):
            optimized_var_loc = convert_i_j_k_to_1d_arr_loc(csr_i, day_j, shift_k, problem_input)
            in_eq_constraint_matrix_upper_bound[processing_row, optimized_var_loc] = 1

        in_eq_constraint_vector.append(upper_bound)

    in_eq_constraint_matrix_lower_bound = np.zeros(
        (
            problem_input.num_of_shifts_k * problem_input.num_of_csr_i,
            problem_input.num_of_optimized_vars,
        )
    )

    for processing_row, (shift_k, csr_i) in enumerate(
        itertools.product(range(problem_input.num_of_shifts_k), range(problem_input.num_of_csr_i))
    ):
        num_of_csr_for_shift_nc_k = problem_input.required_csr_per_shift_nc_k[shift_k]
        lower_bound = math.floor(num_of_csr_for_shift_nc_k / num_of_total_required_csr_nc)

        for day_j in range(problem_input.num_of_day_per_week_j):
            optimized_var_loc = convert_i_j_k_to_1d_arr_loc(csr_i, day_j, shift_k, problem_input)
            in_eq_constraint_matrix_lower_bound[processing_row, optimized_var_loc] = -1

        in_eq_constraint_vector.append(-lower_bound)

    in_eq_constraint_matrix = np.vstack(
        (in_eq_constraint_matrix_upper_bound, in_eq_constraint_matrix_lower_bound)
    )

    return in_eq_constraint_matrix, np.array(in_eq_constraint_vector)


def convert_i_j_k_to_1d_arr_loc(
    csr_i: int, day_j: int, shift_k: int, problem_input: ProblemInput
) -> int:
    return (
        (csr_i * problem_input.num_of_day_per_week_j * problem_input.num_of_shifts_k)
        + (day_j * problem_input.num_of_shifts_k)
        + shift_k
    )


def convert_result_to_dict(
    result: OptimizeResult, problem_input: ProblemInput
) -> Dict[str, List[Optional[str]]]:
    # print(result.x)
    dataframe_result = convert_to_pandas(result.x, problem_input)

    result_dict = {}
    transpose_result = dataframe_result.transpose()
    for column in transpose_result:
        result_dict[column] = [
            None if item == "" else item for item in transpose_result[column].values
        ]

    return result_dict


def convert_to_pandas(solution: np.ndarray, problem_input: ProblemInput) -> pd.DataFrame:
    reshaped: np.ndarray = solution.reshape(
        (
            problem_input.num_of_csr_i,
            problem_input.num_of_day_per_week_j,
            problem_input.num_of_shifts_k,
        )
    )

    csr_names = problem_input.raw_schedules.get_csr_names()
    shift_names = problem_input.shift_span_detail.get_shift_names()
    day_of_week_names = problem_input.csr_requirement_detail.get_day_of_week_names()

    parsed_result = pd.DataFrame(
        "",
        index=csr_names,
        columns=day_of_week_names,
    )

    for index_combination in np.argwhere(reshaped != 0):
        csr_i, day_j, shift_k = tuple(index_combination)
        parsed_result.iloc[csr_i, day_j] = shift_names[shift_k]

    return parsed_result


if __name__ == "__main__":
    main()
