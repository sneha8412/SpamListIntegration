# This file aims to take the intersection of the deny list with edge telemetry and 
# deny list intersection with the chrome data and then find the intersection
# between the two files for to see what is the overlap of domains. subtract that 
# from the total number of intersects found in deny + Edge and  Deny + Chrome.

import pandas as pd
from urllib.parse import urlparse

# formats:
# bing spam list: google.com (does not have www)
# Deny list: www.google.com 
# Telemetry: com.google.www (reversed)

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

def PrintDataframe(df):
    for index, row in df.iterrows():
        print(row)

# Find intersection of deny edge and deny chrome domains.
def deny_intersection(edge_deny_df, chrome_deny_df):
    merged_df = pd.merge(edge_deny_df, chrome_deny_df, how='inner', on=['NormalizedDomain'])
    merged_df.drop_duplicates() # removes dupes
    print(f"intersection of deny_intersect_for_chrome_edge_domains df Size: {len(merged_df.axes[0])}")
    merged_df.to_csv("deny_intersect_for_chrome_edge_domains.csv", index=False, columns =['NormalizedDomain', 'origin'])
    return merged_df

# Main Program 

# Work with Edge deny intersect list, normalize and print.
edge_deny_intersect_df = pd.read_csv('Edge_deny_intersect_only_domains.csv', usecols=['NormalizedDomain'])
print(f"Size of Edge deny intersect only data frame: {len(edge_deny_intersect_df.axes[0])}")

# Read the chrome deny intersect list.
print("Read deny list dataframe")
chrome_deny_list_df = pd.read_csv('chrome_deny_intersect_only_domains.csv', usecols=['NormalizedDomain', 'origin'])
print(f"Size of existing chrome only DenyList intersect data frame: {len(chrome_deny_list_df.axes[0])}")

deny_intersection(edge_deny_intersect_df, chrome_deny_list_df)

