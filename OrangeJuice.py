# You are a Floridian orange grower and orange juice provider
# You need to make 600,000 gallons of orange juice next month
# Your juice must meet your rigorous consistency requirements:
#     Brix/Acid ratio between 11.5 and 12.5
#     Acid level between 0.75% and 1%
#     Astringency below 4
#     Colour between 4.5 and 5.5

# 40% of your juice must come from Florida
# to ensure you keep getting your tax break

# QUESTION
# What is the lowest cost you can make juice that meets the above requirements?

# RESOURCE
# OrangeJuiceBlending.csv contains supplier/juice details

import pulp
import pandas as pd

target_volume = 600
Florida_tax_break = 0.4

# Read supplier details into Pandas dataframe
df = pd.read_csv("OrangeJuiceBlending.csv")

# Create a dictionary of decision variables, one for each supplier
x = pulp.LpVariable.dicts("x", df.index, lowBound=0)

# create our model as a minimize problem
mod = pulp.LpProblem("Budget", pulp.LpMinimize)

# ---- Objective function -----
mod += sum([(x[idx] * df['Price (per 1K Gallons)'][idx]) +
        (x[idx] * df['Shipping'][idx]) for idx in df.index])

# ---- Constraints ------
# Can't order more than available
for idx in df.index:
    mod += x[idx] <= df['Qty Available (1,000 Gallons)'][idx]

# Florida tax break
florida_index = df.index[df['Region'] == 'Florida'].tolist()[0]
mod += x[florida_index] >= (target_volume * Florida_tax_break), "Florida"

# Astringency
mod += sum([x[idx] * df['Astringency (1-10 Scale)'][idx]
    for idx in df.index]) / target_volume <= 4, "Astringency"

# BAR greater than 11.5
mod += sum([x[idx] * df['Brix / Acid Ratio'][idx]
    for idx in df.index]) / target_volume >= 11.5, "BAR Lower"
# BAR less than than 12.5
mod += sum([x[idx] * df['Brix / Acid Ratio'][idx]
    for idx in df.index]) / target_volume <= 12.5, "BAR Upper"

# Acid greater than 0.75%
mod += sum([x[idx] * df['Acid (%)'][idx]
    for idx in df.index]) / target_volume >= 0.0075, "Acid Lower"
# Acid less than than 1%
mod += sum([x[idx] * df['Acid (%)'][idx]
    for idx in df.index]) / target_volume <= 0.01, "Acid Upper"

# Color greater than 4.5
mod += sum([x[idx] * df['Color (1-10 Scale)'][idx]
    for idx in df.index]) / target_volume >= 4.5, "Colour Lower"
# Color less than than 5.5
mod += sum([x[idx] * df['Color (1-10 Scale)'][idx]
    for idx in df.index]) / target_volume <= 5.5, "Colour Upper"

# Budget sum
mod += sum([x[idx] for idx in df.index]) == target_volume, "Required Volume"

# ---- Finish -----
# Write the problem to a document
mod.writeLP("Orange.lp")

# Run the solver
mod.solve()

# Print the status i.e. whether the algorithm found a solution
print("Status:", pulp.LpStatus[mod.status])

# Print the variable names and values
for v in mod.variables():
    print(v.name, "=", v.varValue)

# Print the objective value
print("Total cost =", pulp.value(mod.objective))