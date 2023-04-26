import json
from collections import defaultdict
from dataclasses import field, dataclass
from pathlib import Path
from typing import Optional, List, Dict, TextIO

import numpy as np
import pandas as pd


class CSRInquiries:
    """
    The matrix, required number of CSR for a shift, in a day
    """

    def __init__(self, table: Dict[str, List[int]]):
        self._day_names = list(table.keys())
        self._csr_inquiries = np.array(list(table.values()))

    @staticmethod
    def read_json(input_file: Path):
        with open(input_file, "r") as input_json:
            parsed_input: Dict[str, List[int]] = json.load(input_json)
            return CSRInquiries(parsed_input)

    @property
    def num_of_days(self) -> int:
        return self._csr_inquiries.shape[0]

    @property
    def day_names(self) -> List[str]:
        return self._day_names

    @property
    def num_of_period_per_day(self) -> int:
        return self._csr_inquiries.shape[1]

    # @property
    # def columns(self) -> List[str]
    #     return self._days_name

    def to_dataframe(self):
        """
        :return: 2D matrix, time period x day of week
        """
        return pd.DataFrame(self._csr_inquiries.transpose(), columns=self._day_names)

    def vectorize(self) -> np.ndarray:
        """
        :return: a 1D vector,  No.CSR major
        """
        return self._csr_inquiries.flatten()

    def exclude(self, days: List[str]):
        return CSRInquiries(
            {s: v for s, v in zip(self._day_names, self._csr_inquiries) if s not in days}
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

    def get_list_of_shift_names(self) -> List[str]:
        return self._shifts_name

    @property
    def columns(self) -> List[str]:
        return self._shifts_name

    def to_dataframe(self):
        return pd.DataFrame(self._shifts_detail.transpose(), columns=self._shifts_name)

    def check_for_spanning(self, shift_k, period_t) -> bool:
        return self._shifts_detail[shift_k, period_t] == 1


class Schedule:
    def __init__(self, table: Dict[str, List[int]]):
        self._csr_name = list(table.keys())
        self._schedule = np.array(list(table.values()))

    @staticmethod
    def from_json(input_file: TextIO):
        parsed_input: Dict[str, List[int]] = json.load(input_file)
        return Schedule(parsed_input)

    def __repr__(self):
        return str(self._schedule)

    @property
    def num_of_csr(self) -> int:
        return len(self._schedule)

    @property
    def num_of_days(self) -> int:
        return self._schedule.shape[1]
    
class ReadJson:
    SHIFT_FILE_NAME = "shifts.json"
    DAY_FILE_NAME = "days.json"
    SCHEDULE_FILE_NAME = "shift.json"

    def __init__(self, data_folder_path: Path) -> None:
        self.data_folder_path = data_folder_path

    def read_shifts(self) -> Dict[str, List[int]]:
        with open(self.data_folder_path / self.SHIFT_FILE_NAME) as input_json:
            return json.load(input_json)
        
    def read_days(self) -> Dict[str, List[int]]:
        with open(self.data_folder_path / self.DAY_FILE_NAME) as input_json:
            return json.load(input_json)
        
    def read_schedule(self) -> Dict[str, List[str]]:
        with open(self.data_folder_path / self.SCHEDULE_FILE_NAME) as input_json:
            return json.load(input_json)
            


class ProblemInput:
    def __init__(
        self,
        csr_inquiries: CSRInquiries,
        shifts_detail: ShiftsDetail,
    ):
        self.csr_inquiries = csr_inquiries
        self.shifts_detail = shifts_detail
        # self.schedules:  = None

        # self.num_of_csr_i: int = 0 if self.schedules is None else self.schedules.num_of_csr
        self.num_of_days_j: int = self.csr_inquiries.num_of_days
        self.num_of_shifts_k: int = self.shifts_detail.num_of_shifts
        self.num_of_period_per_day_t: int = field(init=False)
