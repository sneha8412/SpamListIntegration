import pandas as pd

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

def concat_all_chrome_data(df_list):
   consolidated_chrome_data = pd.concat(df_list, axis=0)
   consolidated_chrome_data.to_csv("consolidated_chrome_data.csv", index=False, columns =['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
   print(f"total length of the chrome consolidated file is: {len(consolidated_chrome_data.axes[0])}")
   return consolidated_chrome_data

def grouping_data_for_final_df(chrome_latest):
   chrome_latest_data = chrome_latest.groupby(['origin', 'accept', 'deny', 'ignore', 'dismiss']) ['month'].max() #agg({'month':max})
   #chrome_latest_data['month'].groupby('origin', group_keys=False).nlargest()
   #chrome_latest_data.last()
   #print(f"total length of the chrome latest file is: {len(chrome_latest_data.axes[0])}")
   #chrome_latest_data.drop_duplicates()
   #chrome_latest_data.reset_index()
   chrome_latest_data.to_csv("latest_chrome_data.csv", index=False, header=True)
   print(chrome_latest_data)
  
   return chrome_latest_data

#main  Program
# Read Year 2022 - January
chrome_list_df_jan = pd.read_csv('google-telemetry-202201.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_feb = pd.read_csv('google-telemetry-202202.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_mar = pd.read_csv('google-telemetry-202203.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_apr = pd.read_csv('google-telemetry-202204.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_may = pd.read_csv('google-telemetry-202205.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_jun = pd.read_csv('google-telemetry-202206.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_jul = pd.read_csv('google-telemetry-202207.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_list_df_aug = pd.read_csv('google-telemetry-202208.csv', usecols=['origin', 'accept', 'deny', 'ignore', 'dismiss'])

# add months to all data frames
jan_df = add_month_to_data_frame(chrome_list_df_jan, 1)
feb_df = add_month_to_data_frame(chrome_list_df_feb, 2)
mar_df = add_month_to_data_frame(chrome_list_df_mar, 3)
apr_df = add_month_to_data_frame(chrome_list_df_apr, 4)
may_df = add_month_to_data_frame(chrome_list_df_may, 5)
jun_df = add_month_to_data_frame(chrome_list_df_jun, 6)
jul_df = add_month_to_data_frame(chrome_list_df_jul, 7)
aug_df = add_month_to_data_frame(chrome_list_df_aug, 8)

chrome_month_jan = pd.read_csv('chrome_jan.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_feb = pd.read_csv('chrome_feb.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_mar = pd.read_csv('chrome_mar.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_apr = pd.read_csv('chrome_apr.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_may = pd.read_csv('chrome_may.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_jun = pd.read_csv('chrome_jun.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_jul = pd.read_csv('chrome_jul.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])
chrome_month_aug = pd.read_csv('chrome_aug.csv', usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])

chrome_data_to_append = [chrome_month_feb, chrome_month_mar, chrome_month_apr, chrome_month_may, chrome_month_jun, chrome_month_jul, chrome_month_aug]

concat_all_chrome_data(chrome_data_to_append)

chrome_consolidated_df = pd.read_csv("consolidated_chrome_data.csv", usecols=['origin', 'month', 'accept', 'deny', 'ignore', 'dismiss'])

grouping_data_for_final_df(chrome_consolidated_df)


#  