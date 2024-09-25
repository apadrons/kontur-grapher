import pandas as pd
import math

file_path_depth_seconds = ("./data/3481AI_NB_Ramp Rt 52-NB to New Rd-NB/Depth in Seconds/3481AI_NB_Ramp Rt 52-NB to "
                           "New Rd_Sec02.csv")


def header_cleaner_csv(file_path):
    with open(file_path_depth_seconds, 'r') as file:
        lines = file.readlines()

    with open(file_path_depth_seconds, 'w') as new_file:
        for line in lines[15:]:
            new_file.write(line)
            print(line)


def file_cleanup (df,portion,initial_distance):
    df = df[['0', '-1.968504', '1.968504']]
    df['Adj Distance'] = df_depth_seconds.apply(lambda row: row['0'] + initial_distance, axis=1)

    columns = ['0', 'Adj Distance', '-1.968504', '1.968504']
    df = df[columns]
    df.columns = ['initial_distance', 'adj_distance', 'channel_2', 'channel_18']

    return df


def add_adj_thickness(df,depth_core,core_location):
    updated_dielectric = dielectric_calculator(df,depth_core,core_location)
    df['adj_lwp_thick(in)'] = df.apply(lambda row: (
            SPEED_LIGHT / math.sqrt(updated_dielectric) * (row['time(s)'] * NANO_SECONDS) / 2), axis=1)
    return df

def dielectric_calculator(df, depth_core, core_location):
    closest_index = (df['adj_distance'] - depth_core_left).abs().idxmin()
    closest_row = df.iloc[closest_index]
    return (closest_row['time(s)'] * NANO_SECONDS) * SPEED_LIGHT / (2 * depth_core_left)

df_depth_seconds = pd.read_csv(file_path_depth_seconds)

PORTION = '0'
INITIAL_DISTANCE = 1000
DIELECTRIC_LEFT = 5 #standarized_dialectric
DIELECTRIC_RIGHT = 5 #standarized_dialectric
SPEED_LIGHT = 11.8028527 #speed of light in nanoseconds
NANO_SECONDS =  1.0e9

depth_core_left = 15
core_location_left = 1450
depth_core_right = 20
core_location_right = 1450



df_depth_seconds = file_cleanup(df_depth_seconds,PORTION,INITIAL_DISTANCE)

print(df_depth_seconds)

df_channel_1 = df_depth_seconds[['adj_distance','channel_2']]
df_channel_2 = df_depth_seconds[['adj_distance','channel_18']]

df_channel_1.columns = ['adj_distance','time(s)']
df_channel_2.columns = ['adj_distance','time(s)']

df_channel_1['lwp_thickness(in)'] = df_channel_1.apply(lambda row:(
            SPEED_LIGHT / math.sqrt(DIELECTRIC_LEFT) * (row['time(s)'] * NANO_SECONDS) / 2), axis =1)
df_channel_2['rwp_thickness(in)'] = df_channel_2.apply(lambda row:(
            SPEED_LIGHT / math.sqrt(DIELECTRIC_RIGHT) * (row['time(s)'] * NANO_SECONDS) / 2), axis =1)



closest_index_left = (df_channel_1['adj_distance'] - depth_core_left).abs().idxmin()
closest_index_right = (df_channel_2['adj_distance'] - depth_core_right).abs().idxmin()

closest_row_left = df_channel_1.iloc[closest_index_left]
closest_row_right = df_channel_2.iloc[closest_index_right]

updated_dielectric_left =  (closest_row_left['time(s)'] * NANO_SECONDS) * SPEED_LIGHT / ( 2 * depth_core_left )
updated_dielectric_right =  (closest_row_right['time(s)'] * NANO_SECONDS) * SPEED_LIGHT / ( 2 * depth_core_right)

print(updated_dielectric_right)

df_channel_1['adj_lwp_thick(in)'] = df_channel_1.apply(lambda row:(
            SPEED_LIGHT / math.sqrt(updated_dielectric_left) * (row['time(s)'] * NANO_SECONDS) / 2), axis =1)
df_channel_2['adj_rwp_thick(in)'] = df_channel_2.apply(lambda row:(
            SPEED_LIGHT / math.sqrt(updated_dielectric_right) * (row['time(s)'] * NANO_SECONDS) / 2), axis =1)

start_data = 1200
end_data = 1750

df_channel_1 = df_channel_1[(df_channel_1['adj_distance'] >= start_data) & (df_channel_1['adj_distance'] <= end_data)]
df_channel_2 = df_channel_2[(df_channel_2['adj_distance'] >= start_data) & (df_channel_2['adj_distance'] <= end_data)]

stats_channel_1 = {
    '90 Percentile': df_channel_1['adj_lwp_thick(in)'].quantile(0.90) ,
    '10 Percentile': df_channel_1['adj_lwp_thick(in)'].quantile(0.10) ,
    'Average': df_channel_1['adj_lwp_thick(in)'].mean(),
    'Standard Deviation': df_channel_1['adj_lwp_thick(in)'].std(),
}
stats_channel_2 = {
    '90 Percentile': df_channel_2['adj_rwp_thick(in)'].quantile(0.90) ,
    '10 Percentile': df_channel_2['adj_rwp_thick(in)'].quantile(0.10) ,
    'Average': df_channel_2['adj_rwp_thick(in)'].mean(),
    'Standard Deviation': df_channel_2['adj_rwp_thick(in)'].std(),
}

print(stats_channel_1)