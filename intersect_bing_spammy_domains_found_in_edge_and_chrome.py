from urllib.parse import urlparse
import pandas as pd
# This file aims to find the common domains that exist in the edge and chrome 
# spammy domains identified via bing spam. Identify all the domains to be added to the 
# deny list that don't already exist.

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
def find_intersection(telemetry_df, chrome_list_df):
    merged_df = pd.merge(chrome_list_df, telemetry_df, how='inner', on=['NormalizedDomain'])
    merged_df.drop_duplicates(inplace=True) # removes dupes
    print(f"merged Notification Domains Size: {len(merged_df.axes[0])}")
    
    del merged_df["origin"]

    merged_df.to_csv("intersected_list_of_edge_and_chrome_domains.csv", index=False)
    print(f"Intersected Notification Domains Size: {len(merged_df.axes[0])}")

    return merged_df

# Get domains in edge that does not intersect with chrome.
def edge_only(telemetry_df, chrome_list_df):

    telemetry_df = telemetry_df[['NormalizedDomain', 'Origin']]
    chrome_list_df = chrome_list_df[['NormalizedDomain', 'origin']]

    merged_df = telemetry_df.merge(chrome_list_df, how='left', indicator=True)

    bing_edge_only_df = merged_df[merged_df['_merge'] == 'left_only']

    print(f"Edge Only Domains Size: {len(bing_edge_only_df.axes[0])}")

    bing_edge_only_df.to_csv("bing_spammy_edge_only_domains.csv", index=False, columns =['NormalizedDomain', 'Origin'])

    return bing_edge_only_df

# Get domains in chrome that does not intersect with edge.
def chrome_only(telemetry_df, chrome_list_df):

    telemetry_df = telemetry_df[['NormalizedDomain', 'Origin']]
    chrome_list_df = chrome_list_df[['NormalizedDomain', 'origin']]

    merged_df = chrome_list_df.merge(telemetry_df, how='left', indicator=True)

    bing_chrome_only_df = merged_df[merged_df['_merge'] == 'left_only']

    print(f"Edge Only Domains Size: {len(bing_chrome_only_df.axes[0])}")

    bing_chrome_only_df.to_csv("bing_spammy_chrome_only_domains.csv", index=False, columns =['NormalizedDomain', 'origin'])

    return bing_chrome_only_df


# Main Program 

# Read bing_spammy_domains_found_in_edge_telemetry.csv.
telemetry_df = pd.read_csv('bing_spammy_domains_found_in_edge_telemetry.csv', usecols=['Origin', 'NormalizedDomain'])
print(f"Size of Telemetry data frame: {len(telemetry_df.axes[0])}")

# Read the 'bing_spammy_domains_found_in_chrome_latest.csv'
print("Read google list dataframe")
chrome_df = pd.read_csv('bing_spammy_domains_found_in_chrome_latest.csv', usecols=["origin", "NormalizedDomain"])
print(f"Size of google latest data frame: {len(chrome_df.axes[0])}")

# Get the intersection between the 2 files.
merged_df = find_intersection(telemetry_df, chrome_df)

edge_only_df = edge_only(telemetry_df, chrome_df)

chrome_only_df= chrome_only(chrome_df, telemetry_df)
