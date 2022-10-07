import pandas as pd

# Read Year 2022 - January
chrome_list_df_jan = pd.read_csv('google-telemetry-202201.csv', usecols=["origin"])
print(f"Size of google data frame Jan: {len(chrome_list_df_jan.axes[0])}")

#Feb
chrome_list_df_feb = pd.read_csv('google-telemetry-202202.csv', usecols=["origin"])
print(f"Size of google data frame Feb: {len(chrome_list_df_feb.axes[0])}")

#March
chrome_list_df_mar = pd.read_csv('google-telemetry-202203.csv', usecols=["origin"])
print(f"Size of google data frame March: {len(chrome_list_df_mar.axes[0])}")

#April
chrome_list_df_apr = pd.read_csv('google-telemetry-202204.csv', usecols=["origin"])
print(f"Size of google data frame April: {len(chrome_list_df_apr.axes[0])}")

#May
chrome_list_df_may = pd.read_csv('google-telemetry-202205.csv', usecols=["origin"])
print(f"Size of google data frame May: {len(chrome_list_df_may.axes[0])}")

#June
chrome_list_df_jun = pd.read_csv('google-telemetry-202206.csv', usecols=["origin"])
print(f"Size of google data frame June: {len(chrome_list_df_jun.axes[0])}")

#July
chrome_list_df_jul = pd.read_csv('google-telemetry-202207.csv', usecols=["origin"])
print(f"Size of google data frame July: {len(chrome_list_df_jul.axes[0])}")

#Aug
chrome_list_df_aug = pd.read_csv('google-telemetry-202208.csv', usecols=["origin"])
print(f"Size of google data frame August: {len(chrome_list_df_aug.axes[0])}")

#consolidate all data and keep the latest domain data only
# function to get the union of 2 dfs.
def output_common_domains(df1, df2):
   intersected_df = pd.merge(df1,df2, how='inner', on=['origin'])
   intersected_df.to_csv("intersected_list_of_domains.csv", index=False)
   sum_of_indexes = len(df1.axes[0]) + len(df2.axes[0])
   print(f"total Size of the 2 google data is: {sum_of_indexes}")
   print(f"Size of intersected google data is: {len(intersected_df.axes[0])}")

#Main program
print("Size of intersected google data for Jan and Feb")
output_common_domains(chrome_list_df_feb, chrome_list_df_jan)
output_common_domains(chrome_list_df_mar, chrome_list_df_feb)
