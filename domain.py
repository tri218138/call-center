import json
from collections import defaultdict
from dataclasses import field, dataclass
from pathlib import Path
from typing import Optional, List, Dict

import numpy as np
import pandas as pd


class CSRInquiries:
    def __init__(self, table: Dict[str, List[int]]):
        self._days_name = list(table.keys())
        self._crs_inquiries = np.array(list(table.values()))

    @staticmethod
    def read_json(input_file: Path):
        with open(input_file, "r") as input_json:
            parsed_input: Dict[str, List[int]] = json.load(input_json)
            return CSRInquiries(parsed_input)

    @property
    def num_of_days(self) -> int:
        return self._crs_inquiries.shape[0]

    @property
    def num_of_period_per_day(self) -> int:
        return self._crs_inquiries.shape[1]

    @property
    def columns(self) -> List[str]:
        return self._days_name

    def to_dataframe(self):
        return pd.DataFrame(self._crs_inquiries.transpose(), columns=self._days_name)

    def vectorize(self) -> np.ndarray:
        """
        :return: a 1D vector,  No.CSR major
        """
        return self._crs_inquiries.flatten()

    def exclude(self, days: List[str]):
        return CSRInquiries(
            {s: v for s, v in zip(self._days_name, self._crs_inquiries) if s not in days}
        )


class ShiftsDetail:
    def __init__(self, table: Dict[str, List[int]]):
        self._shifts_name = list(table.keys())
        self._shifts_detail = np.array(list(table.values()))

    @staticmethod
    def read_json(input_file: Path):
        with open(input_file, "r") as input_json:
            parsed_input: Dict[str, List[int]] = json.load(input_json)
            return ShiftsDetail(parsed_input)

    @property
    def num_of_shifts(self) -> int:
        return self._shifts_detail.shape[0]

    @property
    def columns(self) -> List[str]:
        return self._shifts_name

    def to_dataframe(self):
        return pd.DataFrame(self._shifts_detail.transpose(), columns=self._shifts_name)

    def at(self, shift_k, period_t) -> bool:
        return self._shifts_detail[shift_k, period_t] == 1


class Schedule:
    def __init__(self, table: Dict[str, List[int]]):
        self._csr_name = list(table.keys())
        self._schedule = np.array(list(table.values()))

    @staticmethod
    def read_json(input_file: Path):
        with open(input_file, "r") as input_json:
            parsed_input: Dict[str, List[int]] = json.load(input_json)
            return Schedule(parsed_input)

    def __repr__(self):
        return str(self._schedule)

    @property
    def num_of_csr(self) -> int:
        return len(self._schedule)

    @property
    def num_of_days(self) -> int:
        return self._schedule.shape[1]


# class ProblemInput:
#     def __init__(
#         self,
#         crs_inquiries: CSRInquiries,
#         shifts_detail: ShiftsDetail,
#         schedules: Schedule or None = None,
#     ):
#         self.crs_inquiries = crs_inquiries
#         self.shifts_detail = shifts_detail
#         self.schedules = schedules

#         self.num_of_csr_i: int = 0 if self.schedules is None else self.schedules.num_of_csr
#         self.num_of_days_j: int = self.crs_inquiries.num_of_days
#         self.num_of_shifts_k: int = self.shifts_detail.num_of_shifts
#         self.num_of_period_per_day_t: int = field(init=False)
