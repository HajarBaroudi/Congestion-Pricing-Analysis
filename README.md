# Congestion Pricing Analysis

# Overview 
This program analyzes the effects of the Manhattan congestion pricing, which took effect on January 5th, 2025, on 60th Street and below. The goal of the policy was to reduce overall traffic in the area in an attempt to reduce the negative externalities caused by vehicles. The program separately compares vehicle and MTA traffic from 2023-2024 to 2025-2026 based on data sets from NYC Open Data.

# Development
The program uses pandas to narrow the vehicle data to the Manhattan area affected by the congestion pricing. For both the vehicle data set and the MTA data sets, it calculates the percentage of change, confirming its statistical significance through a Welch’s t-test (p < 0.05) using SciPy. It then generates a histogram and boxplot utilizing Matplotlib, representative of the vehicle data set, and a histogram to visualize the comparison of the two MTA data sets. Additionally, it compares the percentage of change of vehicle traffic during hours when peak pricing is in effect vs off-peak hours.

# Findings
The overall vehicle traffic following the congestion pricing policy increased by 27.8%, with a slightly larger increase during off-peak pricing of 30.3% compared to the increase during peak pricing of 27.5%. However, the difference in traffic between peak and off-peak hours appears to be too marginal for a definitive conclusion. MTA ridership has also shown an overall, although smaller, increase of 11.5%. Taking everything into consideration, although there has been a clear statistically significant increase in traffic in the area focused on vehicles, a causal connection between the increase and the policy cannot be drawn based on the information extracted alone.

