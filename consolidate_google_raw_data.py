import pandas as pd
# This file aims to create a csv file that has the latest domains and data on older 
# domains in the chrome data on notifications from Jan to Aug.

# Add a new month column to all the data frames and populate the value based on the numerical
# value of that month. This value is constant for all the origins in a given df.
def add_month_to_data_frame(df, month):
   chrome_dfs_dict = { "chrome_jan":chrome_list_df_jan,
      "chrome_feb":chrome_list_df_feb,
      "chrome_mar": chrome_list_df_mar, 
      "chrome_apr":chrome_list_df_apr,
      "chrome_may" :chrome_list_df_may, 
      "chrome_jun":chrome_list_df_jun , 
      "chrome_jul":chrome_list_df_jul,
      "chrome_aug": chrome_list_df_aug }

   print(f"Size of google data frame of month {month}: {len(df.axes[0])}")
   #insert a new column in the data frame with the respective month as integer.
   df.insert(1, "month", month)
   for key, value in chrome_dfs_dict.items():
      if str(value) == str(df):
         value.to_csv("./{}.csv".format(key), index=False, columns =['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
   return df

# Concatenate all the new data frames that now have the month column, to create one large csv to work on.
def concat_all_chrome_data(df_list):
   consolidated_chrome_data = pd.concat(df_list, axis=0)
   consolidated_chrome_data.to_csv("consolidated_chrome_data.csv", index=False, columns =['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
   print(f"total length of the chrome consolidated file is: {len(consolidated_chrome_data.axes[0])}")
   return consolidated_chrome_data

# Process the consolidated csv file to only keep the latest values for every origin.
def grouping_data_for_final_df(chrome_latest):
   chrome_latest_data = chrome_latest.sort_values(by=['month'], ascending=False)
   chrome_latest_data_sorted = chrome_latest_data.groupby(['origin'], as_index=False).first()
   print(f"total length of the chrome latest file is: {len(chrome_latest_data_sorted.axes[0])}")
   #print(chrome_latest_data_sorted)
   del chrome_latest_data_sorted['month']
   chrome_latest_data_sorted.to_csv("latest_chrome_data.csv", index=False, header=True)
   return chrome_latest_data_sorted

#main  Program
#Read the original csv and create data frames
chrome_list_df_jan = pd.read_csv('google-telemetry-202201.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_feb = pd.read_csv('google-telemetry-202202.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_mar = pd.read_csv('google-telemetry-202203.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_apr = pd.read_csv('google-telemetry-202204.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_may = pd.read_csv('google-telemetry-202205.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_jun = pd.read_csv('google-telemetry-202206.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_jul = pd.read_csv('google-telemetry-202207.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_aug = pd.read_csv('google-telemetry-202208.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])

# add months to all data frames
add_month_to_data_frame(chrome_list_df_jan, 1)
add_month_to_data_frame(chrome_list_df_feb, 2)
add_month_to_data_frame(chrome_list_df_mar, 3)
add_month_to_data_frame(chrome_list_df_apr, 4)
add_month_to_data_frame(chrome_list_df_may, 5)
add_month_to_data_frame(chrome_list_df_jun, 6)
add_month_to_data_frame(chrome_list_df_jul, 7)
add_month_to_data_frame(chrome_list_df_aug, 8)

# read the newly created csvs that also have the month, to be able to concatenate.
chrome_month_jan = pd.read_csv('chrome_jan.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_feb = pd.read_csv('chrome_feb.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_mar = pd.read_csv('chrome_mar.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_apr = pd.read_csv('chrome_apr.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_may = pd.read_csv('chrome_may.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_jun = pd.read_csv('chrome_jun.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_jul = pd.read_csv('chrome_jul.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_aug = pd.read_csv('chrome_aug.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])

# Concatenate the csvs into one large csv file.
chrome_data_to_append = [chrome_month_feb, chrome_month_mar, chrome_month_apr, chrome_month_may, chrome_month_jun, chrome_month_jul, chrome_month_aug]
concat_all_chrome_data(chrome_data_to_append)

# Read the newly formed concatenated csv and Create chrome latest csv from it.
chrome_consolidated_df = pd.read_csv("consolidated_chrome_data.csv", usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
grouping_data_for_final_df(chrome_consolidated_df)
