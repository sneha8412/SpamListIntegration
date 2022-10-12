import pandas as pd
from urllib.parse import urlparse
# This file aims to find the common domains that exist in the chrome old and new
# telemetry. The old data was used to add the domains to the deny list previously.  

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

# Find intersection of old and new chrome data.
def intersect_old_and_new_data(old_df, new_df):
    merged_df = pd.merge(new_df, old_df, how='inner', on=['NormalizedDomain'])
    merged_df.drop_duplicates(inplace=True) # removes dupes
    print(f"merged Notification Domains Size: {len(merged_df.axes[0])}")
    
    # del merged_df["origin"]

    merged_df.to_csv("intersected_old_and_new_chrome_domains.csv", index=False)
    print(f"Intersected Notification Domains Size: {len(merged_df.axes[0])}")

    return merged_df

# # Get data in edge that does not intersect with chrome
# def edge_only(edge_df, intersect_df):

#     edge_df = edge_df[['NormalizedDomain', 'Origin']]
#     intersect_df = intersect_df[['NormalizedDomain', 'Origin']]

#     edge_df.to_csv("edge_df.csv", index=False)
#     intersect_df.to_csv("edge_chrome_intersect_df.csv", index=False)

#     merged_df = edge_df.merge(intersect_df, how='left', indicator=True)

#     edge_only_df = merged_df[merged_df['_merge'] == 'left_only']

#     print(f"Edge Only Domains Size: {len(edge_only_df.axes[0])}")

#     edge_only_df.to_csv("edge_only_domains.csv", index=False, columns =['NormalizedDomain', 'Origin'])

#     return edge_only_df


# Main Program 

# Work with edge telemetry, normalize and print.
old_chrome_df = pd.read_csv('old_chrome_domain_with_score.csv', usecols=['origin'])
print(f"Size of old chrome data frame: {len(old_chrome_df.axes[0])}")
old_chrome_df['NormalizedDomain'] = old_chrome_df['origin'].map(NormalizeDomain)
print(f"Size of old chrome data frame: after normalization {len(old_chrome_df.axes[0])}")

# Read the google telemetry, normalize and print.
print("Read new google lattest dataframe")
new_chrome_df = pd.read_csv('latest_chrome_data.csv', usecols=["origin"])
print(f"Size of google latest data frame: {len(new_chrome_df.axes[0])}")
new_chrome_df['NormalizedDomain'] = new_chrome_df['origin'].map(NormalizeDomain)
print(f"Size of latest google data frame: after normalization {len(new_chrome_df.axes[0])}")

merged_df = intersect_old_and_new_data(old_chrome_df, new_chrome_df)

#edge_only_df = edge_only(old_chrome_df, merged_df)
