import pandas as pd
from urllib.parse import urlparse
# This file aims to find the common domains in the deny list and the chrome data
# in an attempt to find any domains in the deny list that are redundant or no longer 
# send any notifications.

# formats:
# bing spam list: google.com (does not have www)
# Deny list: www.google.com 
# Telemetry: com.google.www (reversed)
# chrome telemetry: https://www.google.com

def NormalizeDomain(domain):
    #convert ints and floats to string in case there are IP addresses as  
    if(str(domain) == ""):
        return ""

    domain_noprefix = str(domain)
    if domain_noprefix.startswith("https://"):
        domain_noprefix = domain_noprefix.split("https://")[1]
    
    if domain_noprefix.startswith("http://"):
        domain_noprefix = domain_noprefix.split("http://")[1]

    domain_parts = domain_noprefix.split(".")
    domain_parts.sort()

    if ("www" in domain_parts):
        domain_parts.remove("www")
    
    normalized_domain_string = '.'.join(domain_parts)
    return normalized_domain_string  

def PrintDataframe(df):
    for index, row in df.iterrows():
        print(row)

# Find intersection of deny list with the old chrome  data. 
def old_chrome_deny_intersection(old_chrome_df, deny_df):
    merged_df = pd.merge(old_chrome_df, deny_df, how='inner', on=['NormalizedDomain'])
    merged_df.drop_duplicates() # removes dupes
    print(f"intersection of chrome and deny list Domains Size: {len(merged_df.axes[0])}")
    merged_df.to_csv("old_chrome_deny_intersect_only_domains.csv", index=False, columns =['NormalizedDomain', 'origin'])
    return merged_df

# Main Program 

# Work with old google telemetry, normalize and print.
print("Read old google list dataframe")
old_chrome_list_df = pd.read_csv('old_chrome_domain_with_score.csv', usecols=["origin"])
old_chrome_list_df.drop_duplicates()
print(f"Size of old chrome data frame: {len(old_chrome_list_df.axes[0])}")
old_chrome_list_df['NormalizedDomain'] = old_chrome_list_df['origin'].map(NormalizeDomain)
print(f"Size of old google data frame: after normalization {len(old_chrome_list_df.axes[0])}")

# Read the deny list, normalize the domain for comparison with Chrome data.
print("Read deny list dataframe")
deny_list_df = pd.read_csv('production_domains.txt', names=["SpamDomain"])
deny_list_df.drop_duplicates()
print(f"Size of existing DenyList data frame: {len(deny_list_df.axes[0])}")
deny_list_df['NormalizedDomain'] = deny_list_df['SpamDomain'].map(NormalizeDomain)
print(f"Size of existing DenyList data frame: after normalization {len(deny_list_df.axes[0])}")

old_chrome_deny_intersection(old_chrome_list_df, deny_list_df)

