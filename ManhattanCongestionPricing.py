#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 15:04:19 2026

@author: hajarbaroudi
"""
# setup
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd

file_path = '/Users/hajarbaroudi/Downloads/Automated_Traffic_Volume_Counts_20260619.csv'
df = pd.read_csv(file_path, na_values=['NA'])


#narrow data
manhattan = df[df['Boro'] == 'Manhattan'].copy()

coords = manhattan['WktGeom'].str.extract(
    r'POINT \(([-\d.]+) ([-\d.]+)\)'
)

manhattan['Y'] = coords[1].astype(float)

region = manhattan[manhattan['Y'] <= 219334.4].copy()
prev_years = region[(region['Yr'] == 2024) | (region['Yr'] == 2023)].copy()
during_years = region[(region['Yr'] == 2025) | (region['Yr'] == 2026)].copy()

# average volume of traffic prev_years vs during_years
prev_vol = prev_years['Vol'].str.replace(',', '').astype(int)
prev_mean = prev_vol.mean()
during_vol = during_years['Vol'].str.replace(',', '').astype(int)
during_mean = during_vol.mean()

percentage_of_change = ((during_mean - prev_mean) / prev_mean) * 100

print('Overall Vehicle traffic change: ', f"{percentage_of_change:.3f}%")

# t - test
prev_sd = prev_vol.std(ddof = 0)
during_sd = during_vol.std(ddof = 0)
t_stat, p_value = stats.ttest_ind(prev_vol, during_vol, equal_var = False)

# box-plot
prev_median = prev_vol.median()
during_median = during_vol.median()

prev_q1 = prev_vol.quantile(.25)
prev_q2 = prev_vol.quantile(.5)
prev_q3 = prev_vol.quantile(.75)

during_q1 = during_vol.quantile(.25)
during_q2 = during_vol.quantile(.5)
during_q3 = during_vol.quantile(.75)

plt.boxplot([prev_vol, during_vol], labels = ['Before', 'After'])
plt.title('Traffic Volume') 
plt.ylabel('Volume')

plt.show()

# histogram
plt.hist(prev_vol, bins = 100, alpha = 0.5, label = 'Before')
plt.hist(during_vol, bins = 100, alpha = 0.5, label = 'After')

plt.title('Traffic Volume') 
plt.xlabel('Volume')
plt.ylabel('Number of hourly observations')
plt.legend()
plt.show()

# peak hours vs off peak
region['date'] = pd.to_datetime(region[['Yr', 'M', 'D']].rename(columns = {'Yr':'year', 'M': 'month', 'D': 'day'}))
region['day_of_week'] = region['date'].dt.day_name()
region['weekend'] = region['date'].dt.dayofweek >= 5

weekend_peak = (region['weekend'] == True) & (region['HH'] >= 9) & (region['HH'] <= 21)
weekday_peak = (region['weekend'] == False) & (region['HH'] >= 5) & (region['HH'] <= 21)



region['timing'] = 'offPeak'
region.loc[weekend_peak, 'timing'] = 'peak'
region.loc[weekday_peak, 'timing'] = 'peak'

prev_years = region[(region['Yr'] == 2024) | (region['Yr'] == 2023)].copy()
during_years = region[(region['Yr'] == 2025) | (region['Yr'] == 2026)].copy()

prev_peak = prev_years[prev_years['timing'] == 'peak']
during_peak = during_years[during_years['timing'] == 'peak']

prev_peak_vol = prev_peak['Vol'].str.replace(',', '').astype(int)
prev_peak_mean = prev_peak_vol.mean()
during_peak_vol = during_peak['Vol'].str.replace(',', '').astype(int)
during_peak_mean = during_peak_vol.mean()

prev_offPeak = prev_years[prev_years['timing'] == 'offPeak']
during_offPeak = during_years[during_years['timing'] == 'offPeak']

prev_offPeak_vol = prev_offPeak['Vol'].str.replace(',', '').astype(int)
prev_offPeak_mean = prev_offPeak_vol.mean()
during_offPeak_vol = during_offPeak['Vol'].str.replace(',', '').astype(int)
during_offPeak_mean = during_offPeak_vol.mean()

peak_percentage_of_change = ((during_peak_mean - prev_peak_mean) / prev_peak_mean) * 100
offPeak_percentage_of_change = ((during_offPeak_mean - prev_offPeak_mean) / prev_offPeak_mean) * 100

print('Vehicle trafffic change during peak hours: ', f"{peak_percentage_of_change:.3f}%")
print('Vehicle trafffic change during peak hours: ', f"{offPeak_percentage_of_change:.3f}%")

# 2023 - 2024 MTA ridership
file_path = '/Users/hajarbaroudi/Downloads/MTA_Subway_Hourly_Ridership__2020-2024_20260622.csv'
df = pd.read_csv(file_path, na_values=['NA'])
df['ridership'] = df['ridership'].str.replace(',', '').astype(int)

df['transit_timestamp'] = pd.to_datetime(df['transit_timestamp'])
df['date'] = df['transit_timestamp'].dt.date

prev_ridership = (df.groupby(df['transit_timestamp'].dt.date)['ridership'].sum())
mean_prev_ridership = prev_ridership.mean()

#2025 - 2026 MTA ridership
file_path = '/Users/hajarbaroudi/Downloads/MTA_Subway_Hourly_Ridership__Beginning_2025_20260622.csv'
df = pd.read_csv(file_path, na_values=['NA'])
df['ridership'] = df['ridership'].str.replace(',', '').astype(int)

df['transit_timestamp'] = pd.to_datetime(df['transit_timestamp'])
df['date'] = df['transit_timestamp'].dt.date

during_ridership = (df.groupby(df['transit_timestamp'].dt.date)['ridership'].sum())
mean_during_ridership = during_ridership.mean()

#change and significance
ridership_percentage_of_change = ((mean_during_ridership - mean_prev_ridership) / mean_prev_ridership) * 100
print('Overall MTA ridership change: ', f"{ridership_percentage_of_change:.3f}%")

prev_ridership_sd = prev_ridership.std(ddof = 0)
during_ridership_sd = during_ridership.std(ddof = 0)
ridership_t_stat, ridership_p_value = stats.ttest_ind(prev_ridership, during_ridership, equal_var = False)

#histogram
plt.figure()
plt.hist(prev_ridership, bins = 50, alpha = 0.5, label = 'Before')
plt.hist(during_ridership, bins = 50, alpha = 0.5, label = 'After')

plt.title('MTA Ridership') 
plt.xlabel('Ridership')
plt.ylabel('Number of Days')
plt.legend()
plt.show()



















    




