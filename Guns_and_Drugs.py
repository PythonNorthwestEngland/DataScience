# You are a Columbian gangster who can sell one of two products:
#     Drugs
#     Guns
# Your boss gives you a monthly budget of $1,800 to buy stock
# Your store room has space for 21 cubic meters of product
# 1 gun:
#     takes up 0.5 cubic meters of space,
#     costs $150 to buy,
#     sells for $195
# 1 ton of drugs:
#     takes up 1.5 cubic meters of space,
#     costs $100 to buy,
#     sells for $150

# QUESTION:
# How much of each should we buy each month to maximise our revenue?

import pulp

# create our model as a maximize problem
mod = pulp.LpProblem("Budget", pulp.LpMaximize)

# Decision variables
x1 = pulp.LpVariable("GunNumber", 0, None, pulp.LpInteger)
x2 = pulp.LpVariable("DrugsAmount", 0, None, pulp.LpInteger)

# Objective function
mod += (195 * x1) + (150 * x2), "Maximise sales revenue"

# Constraints
mod += (0.5 * x1) + (1.5 * x2) <= 21, "Space constraint"
mod += (150 * x1) + (100 * x2) <= 1800, "Budget constraint"

# ---- Finish -----
# Write the problem to a document
mod.writeLP("GunsAndDrugs.lp")

# Run the solver
mod.solve()

# Print the status i.e. whether the algorithm found a solution
print("Status:", pulp.LpStatus[mod.status])

# Print the variable names and values
for v in mod.variables():
    print(v.name, "=", v.varValue)

# Print the objective value
print("Revenue =", pulp.value(mod.objective))