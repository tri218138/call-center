import json
from dataclasses import field, dataclass
from pathlib import Path
from typing import Optional, List, Dict


class CsrRequirePerDayDetails:
    def __init__(self, input_file: Path):
        with open(input_file, "r") as input_json:
            self._input_details: Dict[str, List[int]] = json.load(input_json)

    @staticmethod
    def from_json_file(file_name: Path):
        return CsrRequirePerDayDetails(file_name)

    @property
    def num_of_day_per_week(self) -> int:
        return len(self._input_details)

    @property
    def num_of_period_per_day(self) -> int:
        first_any_day_detail = next(iter(self._input_details.values()))
        return len(first_any_day_detail)


class ShiftSpanDetail:
    def __init__(self, input_file: Path):
        with open(input_file, "r") as input_json:
            self._input_span_detail: Dict[str, List[int]] = json.load(input_json)

    @staticmethod
    def from_json_file(file_name: Path):
        return ShiftSpanDetail(file_name)

    @property
    def num_of_available_shifts(self) -> int:
        return len(self._input_span_detail)


class RawSchedule:
    def __init__(self, input_file: Path):
        with open(input_file, "r") as input_json:
            self._input_schedule: Dict[str, List[Optional[str]]] = json.load(input_json)

        self._available_shifts = set[str]()
        for employee_schedule in self._input_schedule.values():
            for shifts in employee_schedule:
                if shifts:
                    self._available_shifts.add(shifts)

    @staticmethod
    def from_json_file(file_name: Path):
        return RawSchedule(file_name)

    def __repr__(self):
        return str(self._input_schedule)

    @property
    def num_of_csr(self) -> int:
        return len(self._input_schedule)


@dataclass
class ProblemInput:
    num_of_csr_i: int
    num_of_day_per_week_j: int
    num_of_shifts_k: int
    num_of_period_per_day_t: int

    num_of_optimized_vars: int = field(init=False)

    def __post_init__(self):
        self.num_of_optimized_vars = (
            self.num_of_csr_i * self.num_of_day_per_week_j * self.num_of_shifts_k
        )
