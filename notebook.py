from pathlib import Path
from solutions.task1_domain import ReadJson, CSRInquiries, ShiftsDetail
from solutions import task1, task2, task3
import numpy as np
from functools import reduce

read_json = ReadJson(Path("data/json"))
shifts_dict = read_json.read_shifts()
day_dict = read_json.read_days()

# %%
shifts_detail = ShiftsDetail(shifts_dict)
csr_inquiries = CSRInquiries(day_dict)

# %%
coefficients_c = np.ones(shifts_detail.num_of_shifts)

# %%
stat = [
    (2 if day_j < 5 else 1) * task1.min_csr_of_a_day(coefficients_c, csr_inquiries, shifts_detail, day_j) 
    for day_j in range(csr_inquiries.num_of_days)
]
stat

# %%
min_total_csr = max([reduce(lambda pre, cur: pre + cur, days, 0) for days in stat])

# %%
employee_assignment = np.array(
    [task1.label_shift_to_employee(shift, shifts_detail.columns, min_total_csr) for shift in stat]
).T.tolist()

# %%
schedule = {f"NV{i}": em for i, em in enumerate(employee_assignment)}
schedule

# %%
# schedule = task2.solve(schedule)
# schedule

# %%
task3.solve(shifts_dict, day_dict, schedule)

# %% [markdown]
# Failed miserably :>>>

# %%
import math

table_1 = {
    name: [math.ceil(period / 2) if name != "Saturday" else period for period in shift]
    for name, shift in day_dict.items() if name != "Sunday"
}
table_1

# %%
import math

table_2 = {
    name: [math.ceil(period / 2) if name != "Sunday" else period for period in shift]
    for name, shift in day_dict.items() if name != "Saturday"
}
table_2

# %%
schedule_1 = task1.solve(shifts_dict, table_1)
schedule_1

# %%
schedule_2 = task1.solve(shifts_dict, table_2)
schedule_2

# %%
schedule_1 = task2.solve(schedule_1)
schedule_1

# %%
schedule_1 = task3.solve(shifts_dict, table_1, schedule_1)
schedule_1

# %%
schedule_2 = task2.solve(schedule_2)
schedule_2

# %%
schedule_2 = task3.solve(shifts_dict, table_2, schedule_2)
schedule_2

# %%
# add sunday col to schedule_1
schedule_1 = { employee: shift + [None] for employee, shift in schedule_1.items()}
schedule_1

# %%
# add saturday col to schedule_1
offset = len(schedule_2.keys())
for employee, shift in schedule_2.items():
    shift.insert(-1, None)
schedule_2 = {f"NV{int(employee[-1])+ offset}": shift for employee, shift in schedule_2.items()}
schedule_2

# %%
merge = list(schedule_1.items()) + list(schedule_2.items())
merge = {employee: shift for employee, shift in merge}
merge

from solutions.utility import write_output_to_file
write_output_to_file("output\output4_merge.json", merge)

# %%
balance = task3.solve(shifts_dict, day_dict, merge)
write_output_to_file("output\output4_balance.json", balance)
# %%
from solutions import task3_mod

new_shift_dict = shifts_dict.copy()
new_shift_dict['C0'] = [0] * len(list(shifts_dict.values())[0])

task3_mod.solve(shifts_dict, day_dict, merge)
write_output_to_file("output\output4_mod.json", balance)
# %%



