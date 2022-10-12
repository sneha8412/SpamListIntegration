import pandas as pd
from urllib.parse import urlparse
# This file aims to find the common domains in the deny list and the edge Telemetry
# in an attempt to find any domains in the deny list that are redundant or no longer 
# send any notifications.

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

# Find intersection of new edge list with the top 1 million data 
def edge_deny_intersection(top_sites_df, deny_df):
    merged_df = pd.merge(top_sites_df, deny_df, how='inner', on=['NormalizedDomain'])
    merged_df.drop_duplicates(inplace=True) # removes dupes
    print(f"intersection of top 1 million and deny list Domains Size: {len(merged_df.axes[0])}")
    merged_df.reset_index()
    merged_df.to_csv("top_10ksites_found_in_denylist.csv", index=False, header=True, columns =['rank', 'Origin'])
    return merged_df

# Main Program 

# Work with top 1 million site csv, create new file with right header names. 
header_list = ["rank", "Origin"]
top_df = pd.read_csv('top-1m.csv', names=header_list)
top_10k = top_df.head(10000) # return the top 10k rows
top_10k.to_csv("top_10k_sites_with_header.csv", index=False, columns=['rank','Origin'])
print(f"Size of top 1 mil data frame: {len(top_df.axes[0])}")

# Read the new top-1m_sites_with_header.csv
top_1m_with_header_df =  pd.read_csv('top_10k_sites_with_header.csv', usecols=['rank','Origin'])
top_1m_with_header_df['NormalizedDomain'] = top_1m_with_header_df['Origin'].map(NormalizeDomain)

# Read the deny list.
print("Read deny list dataframe")
deny_list_df = pd.read_csv('bing_spam_domains_from_edge_tobe_added_to_denylist.csv', usecols=['origin'])
deny_list_df['NormalizedDomain'] = deny_list_df['origin'].map(NormalizeDomain)
print(f"Size of existing DenyList data frame: {len(deny_list_df.axes[0])}")

edge_deny_intersection(top_1m_with_header_df, deny_list_df)


