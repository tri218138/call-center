# Source code for Q2: Minimum CSRs for a week

# Import libraries
import json
from math import ceil

# Import data
file = open('../data/json/output1.json')
CSR_by_shift = json.load(file)

# Set total working days per week
nd = 7

# Calculate max number of CSR for a day
CSRs = CSR_by_shift.keys()
max_nc = len(CSRs)

# Calculate number of CSR each day & total empty slot
nc = [0]*7
ne = 0
for j in range(0,nd):
    empty_slot = [CSR for CSR in CSRs if CSR_by_shift[CSR][j] == None]
    ne += len(empty_slot)
    nc[j] = max_nc - len(empty_slot)
print(nc)

# Calculate additional number of CSR to ensure every CSR has at least 1 day off each week
x = max(0, int(ceil((max_nc-ne)/(nd-1))))
print(x)

# Generate output
max_nc += x
nc = [y+x for y in nc]
day_off = [0]*nd
CSR_by_week = CSR_by_shift
