import pandas as pd

def NormalizeDomain(domain):
    #print(f"NormalizeDomain:{domain}")
    
    #convert ints and floats to string in case there are IP addresses as  
    if(str(domain) == ""):
        return ""

    domain1_parts = str(domain).split(".")
    domain1_parts.sort()

    if ("www" in domain1_parts):
        domain1_parts.remove("www")
    
    normalized_domain_string = '.'.join(domain1_parts)
    return normalized_domain_string  

# Work with Edge telemetry, normalize and print.
telemetry_df = pd.read_csv('edge_telemetry_all_domains.csv', usecols=['Origin' , 'SumInstanceCount'])
telemetry_df['NormalizedDomain'] = telemetry_df['Origin'].map(NormalizeDomain)
print(f"Size of Edge Telemetry data frame after normalization: {len(telemetry_df.axes[0])}")
print("Edge telemetry")
print(telemetry_df)

# Read the new deny list.
print("Read deny list dataframe")
deny_list_df = pd.read_csv('final_deny_list_with_label_filter_without_dupes.csv', usecols=['Origin'])
deny_list_df.drop_duplicates(inplace=True)
deny_list_df['NormalizedDomain'] = telemetry_df['Origin'].map(NormalizeDomain)
print(f"Size of existing DenyList data frame: {len(deny_list_df.axes[0])}")
print('deny list df')
print( deny_list_df
)
# Merge the normalized Bing Spam List with Edge telemetry using inner join.
merged_df =  pd.merge(deny_list_df, telemetry_df, how='inner', on=['NormalizedDomain'])
merged_df.drop_duplicates(inplace=True) # removes dupes
print("merged df")
print(merged_df)
merged_df.to_csv("bing_spam_denylist_and_telemetry_notification_sum_count.csv", index=False)
print(f"size of Spammy Notification Domains found in Edge telemetry: {len(merged_df.axes[0])}")

merged_final_df = pd.read_csv('bing_spam_denylist_and_telemetry_notification_sum_count.csv', usecols=['Origin_x','SumInstanceCount'])
merged_final_df.to_csv('bing_final_spam_denylist_and_telemetry_notification_sum_count.csv', index=False)


sorted_df = pd.read_csv('bing_final_spam_denylist_and_telemetry_notification_sum_count.csv', usecols=['Origin_x','SumInstanceCount'])
sorted_by_sum_instance_count = sorted_df.sort_values(by='SumInstanceCount', ascending=False)
print('sorted df')
print(sorted_by_sum_instance_count)
sorted_by_sum_instance_count.to_csv('sorted_edge_telemetry_bing_deny_list_intersection.csv', index=False)
