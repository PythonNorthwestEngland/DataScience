# In OrangeJuice.py the lowest cost to meet required standards was found
# Your boss now asks you to find a way to reduce costs by 10%

# QUESTION
# What is the lowest you can lower your standards by
# to meet your new target cost?

# RESOURCE
# OrangeJuiceBlending.csv contains supplier/juice details

import pulp
import pandas as pd

target_volume = 600
Florida_tax_break = 0.4
current_cost = 371800 # calculated in OrangeJuice.py
target_cost = current_cost * 0.9 # 90% of optimal cost

# Read data into Pandas dataframe
df = pd.read_csv("OrangeJuiceBlending.csv")

# Create a dictionary of decision variables, one for each supplier
x = pulp.LpVariable.dicts("x", df.index, lowBound=0)

# New decision variables
# percentage we reduce each standard by
x1 = pulp.LpVariable("Astringency Relax", 0, None)
x2 = pulp.LpVariable("BAR Relax", 0, None)
x3 = pulp.LpVariable("Acid Relax", 0, None)
x4 = pulp.LpVariable("Colour Relax", 0, None)

# create our model as a minimize problem
mod = pulp.LpProblem("Degradation", pulp.LpMinimize)

# -----New Objective -----
mod += (x1 + x2 + x3 + x4) / 4

# ---- Old Objective is a New Constraint -----
# Cost must be below target cost
mod += sum([(x[idx] * df['Price (per 1K Gallons)'][idx]) +
        (x[idx] * df['Shipping'][idx])
            for idx in df.index]) <= target_cost

# ---- Constraints ------
# Can't order more than available
for idx in df.index:
    mod += x[idx] <= df['Qty Available (1,000 Gallons)'][idx]

# Florida
florida_index = df.index[df['Region'] == 'Florida'].tolist()[0]
mod += x[florida_index] >= (target_volume * Florida_tax_break), "Florida"

# Astringency
mod += sum([x[idx] * df['Astringency (1-10 Scale)'][idx]
    for idx in df.index]) / target_volume <= (4 * (1 + x1)), "Astringency"

# BAR greater than 11.5
mod += sum([x[idx] * df['Brix / Acid Ratio'][idx]
    for idx in df.index]) / target_volume >= (11.5 * (1 - x2)), "BAR Lower"
# BAR less than than 12.5
mod += sum([x[idx] * df['Brix / Acid Ratio'][idx]
    for idx in df.index]) / target_volume <= (12.5 * (1 + x2)), "BAR Upper"

# Acid greater than 0.75%
mod += sum([x[idx] * df['Acid (%)'][idx]
    for idx in df.index]) / target_volume >= (0.0075 * (1 - x3)), "Acid Lower"
# Acid less than than 1%
mod += sum([x[idx] * df['Acid (%)'][idx]
    for idx in df.index]) / target_volume <= (0.01 * (1 + x3)), "Acid Upper"

# Color greater than 4.5
mod += sum([x[idx] * df['Color (1-10 Scale)'][idx]
    for idx in df.index]) / target_volume >= (4.5 * (1 - x4)), "Colour Lower"

# Color less than than 5.5
mod += sum([x[idx] * df['Color (1-10 Scale)'][idx]
    for idx in df.index]) / target_volume <= (5.5 * (1 + x4)), "Colour Upper"

# Volume sum
mod += sum([x[idx] for idx in df.index]) == target_volume, "Required Volume"

# ---- Finish -----
# Write the problem to a document
mod.writeLP("Orange.lp")

# Run the solver
mod.solve()

# Pritn the status i.e. whether the algorithm found a successful solution
print("Status:", pulp.LpStatus[mod.status])

# Print out the variable values for the solution
for v in mod.variables():
    print(v.name, "=", v.varValue)

# Print the objective value
print("Average standards relaxation =", pulp.value(mod.objective))