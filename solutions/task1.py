import cplex
from docplex.mp.model import Model

# load data
import json
with open('./data/json/days.json', 'r') as f:
    days = json.load(f)

with open('./data/json/shifts.json', 'r') as f:
    shifts = json.load(f)

# read data
J = days.keys()
K = shifts.keys()

# model
model = Model(name='Q1')

# result
result = []
maxCSR = 0

for j in J:
    # variables
    x = {}
    for k in K:
        x[k] = model.integer_var(
            lb=0, ub=cplex.infinity, name='x_{}'.format(k))

    # objective
    model.minimize(sum([x[k] for k in K]))

    # constraints
    for t in range(13):
        sum_t = sum([shifts[k][t]*x[k] for k in K])
        model.add_constraint(sum_t >= days[j][t])

    # solve
    solution = model.solve()

    result.append([x[k].solution_value for k in K])
    maxCSR = max(maxCSR, int(model.objective_value))

    model.clear()

# output
assign = {}
for csr in range(1, maxCSR + 1):
    assign['NV{}'.format(csr)] = []

for j in range(len(J)):
    csr = 1
    for k in range(len(result[j])):
        for res in range(int(result[j][k])):
            assign['NV{}'.format(csr)].append('C{}'.format(k + 1))
            csr += 1
    while csr <= maxCSR:
        assign['NV{}'.format(csr)].append(None)
        csr += 1

output = json.dumps(assign)

with open("output\output1.json", "w") as outfile:
    outfile.write(output)
