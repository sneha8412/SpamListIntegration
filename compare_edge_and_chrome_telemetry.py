from urllib.parse import urlparse
import pandas as pd
# This file aims to find the common domains that exist in the edge and chrome 
# telemetry. The larger the intersect the more confidence we can develop in using 
# edge Telemetry. 

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

# Find intersection of chrome with the edge telemtry data.
def merge_edge_and_chrome_intersection(edge_df, chrome_df):
    merged_df = pd.merge(chrome_list_df, telemetry_df, how='inner', on=['NormalizedDomain'])
    merged_df.drop_duplicates() # removes dupes
    print(f"merged Notification Domains Size: {len(merged_df.axes[0])}")
    
    del merged_df["origin"]

    merged_df.to_csv("intersected_list_of_edge_and_chrome_domains.csv", index=False)
    print(f"Intersected Notification Domains Size: {len(merged_df.axes[0])}")

    return merged_df

# Get data in edge that does not intersect with chrome
def edge_only(edge_df, intersect_df):

    edge_df = edge_df[['NormalizedDomain', 'Origin']]
    intersect_df = intersect_df[['NormalizedDomain', 'Origin']]

    edge_df.to_csv("edge_df.csv", index=False)
    intersect_df.to_csv("edge_chrome_intersect_df.csv", index=False)

    merged_df = edge_df.merge(intersect_df, how='left', indicator=True)

    edge_only_df = merged_df[merged_df['_merge'] == 'left_only']

    print(f"Edge Only Domains Size: {len(edge_only_df.axes[0])}")

    edge_only_df.to_csv("edge_only_domains.csv", index=False, columns =['NormalizedDomain', 'Origin'])

    return edge_only_df


# Main Program 

# Work with edge telemetry, normalize and print.
telemetry_df = pd.read_csv('edge_telemetry_all_domains.csv', usecols=['Origin'])
print(f"Size of Telemetry data frame: {len(telemetry_df.axes[0])}")
telemetry_df['NormalizedDomain'] = telemetry_df['Origin'].map(NormalizeDomain)
print(f"Size of Telemetry data frame: after normalization {len(telemetry_df.axes[0])}")

# Read the google telemetry, normalize and print.
print("Read google list dataframe")
chrome_list_df = pd.read_csv('latest_chrome_data.csv', usecols=["origin"])
print(f"Size of google latest data frame: {len(chrome_list_df.axes[0])}")
chrome_list_df['NormalizedDomain'] = chrome_list_df['origin'].map(NormalizeDomain)
print(f"Size of google data frame: after normalization {len(chrome_list_df.axes[0])}")

merged_df = merge_edge_and_chrome_intersection(telemetry_df, chrome_list_df)

edge_only_df = edge_only(telemetry_df, merged_df)
