import json
from collections import defaultdict
from dataclasses import field, dataclass
from pathlib import Path
from typing import Optional, List, Dict

import numpy as np


class CsrRequirePerDayDetails:
    def __init__(self, input_file: Path):
        with open(input_file, "r") as input_json:
            parsed_input = json.load(input_json)
            self._day_of_week_names = list(parsed_input.keys())
            self._csr_requirements_per_day = np.array(list(parsed_input.values()))

    @staticmethod
    def from_json_file(file_name: Path):
        return CsrRequirePerDayDetails(file_name)

    @property
    def num_of_day_per_week(self) -> int:
        return self._csr_requirements_per_day.shape[0]

    @property
    def num_of_period_per_day(self) -> int:
        return self._csr_requirements_per_day.shape[1]

    def get_vector_of_day_and_require_csr(self) -> np.ndarray:
        """
        :return: a 1D vector,  No.CSR major
        """
        return self._csr_requirements_per_day.flatten()

    def get_day_of_week_names(self) -> List[str]:
        return self._day_of_week_names


class ShiftSpanDetail:
    def __init__(self, input_file: Path):
        with open(input_file, "r") as input_file:
            parsed_input: Dict[str, List[int]] = json.load(input_file)

            self._shift_names = parsed_input.keys()
            self._period_detail_matrix = np.array(list(parsed_input.values()))

    @staticmethod
    def from_json_file(file_name: Path):
        return ShiftSpanDetail(file_name)

    @property
    def num_of_available_shifts(self) -> int:
        return self._period_detail_matrix.shape[0]

    def get_shift_names(self) -> List[str]:
        return list(self._shift_names)

    def check_for_spanning(self, shift_k: int, period_t: int) -> bool:
        return self._period_detail_matrix[shift_k, period_t]


class RawSchedule:
    def __init__(self, input_file: Path):
        with open(input_file, "r") as input_json:
            self._input_schedule: Dict[str, List[Optional[str]]] = json.load(input_json)

    @staticmethod
    def from_json_file(file_name: Path):
        return RawSchedule(file_name)
    
    

    def __repr__(self):
        return str(self._input_schedule)

    def get_csr_names(self) -> List[str]:
        return list(self._input_schedule.keys())

    @property
    def num_of_csr(self) -> int:
        return len(self._input_schedule)

    def get_list_of_required_csr_per_shift_nc_k(self, shift_names: List[str]) -> List[int]:
        """
        :param shift_names: The order of appearing in input
                is also the order of appearing for output
        :return:
        """
        _csr_counter_per_shift = defaultdict(int)

        for employee_schedule in self._input_schedule.values():
            for shift in employee_schedule:
                if shift:
                    _csr_counter_per_shift[shift] += 1

        return [_csr_counter_per_shift[shift] for shift in shift_names]


@dataclass
class ProblemInput:
    num_of_csr_i: int = field(init=False)
    num_of_day_per_week_j: int = field(init=False)
    num_of_shifts_k: int = field(init=False)
    num_of_period_per_day_t: int = field(init=False)

    shift_span_detail: ShiftSpanDetail
    csr_requirement_detail: CsrRequirePerDayDetails
    raw_schedules: RawSchedule

    required_csr_per_shift_nc_k: List[int] = field(init=False)

    num_of_optimized_vars: int = field(init=False)

    def __post_init__(self):
        self.num_of_csr_i = self.raw_schedules.num_of_csr
        self.num_of_day_per_week_j = self.csr_requirement_detail.num_of_day_per_week
        self.num_of_shifts_k = self.shift_span_detail.num_of_available_shifts
        self.num_of_period_per_day_t = self.csr_requirement_detail.num_of_period_per_day

        self.required_csr_per_shift_nc_k = (
            self.raw_schedules.get_list_of_required_csr_per_shift_nc_k(
                self.shift_span_detail.get_shift_names()
            )
        )

        self.num_of_optimized_vars = (
            self.num_of_csr_i * self.num_of_day_per_week_j * self.num_of_shifts_k
        )
