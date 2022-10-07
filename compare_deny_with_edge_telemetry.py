import pandas as pd

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

# Find intersection of deny with the Edge permissions telemtry data 
def edge_deny_intersection(edge_df, deny_df):
    merged_df = pd.merge(deny_df, edge_df, how='inner', on=['NormalizedDomain'])
    merged_df.drop_duplicates() # removes dupes
    print(f"intersection of Edge and deny list Domains Size: {len(merged_df.axes[0])}")
    merged_df.to_csv("Edge_deny_intersect_only_domains.csv", index=False, columns =['NormalizedDomain', 'Origin'])
    return merged_df

# Main Program 

# Work with Edge telemetry, normalize and print.
telemetry_df = pd.read_csv('edge_telemetry_all_domains.csv', usecols=['Origin'])
print(f"Size of Edge Telemetry data frame: {len(telemetry_df.axes[0])}")
telemetry_df['NormalizedDomain'] = telemetry_df['Origin'].map(NormalizeDomain)
print(f"Size of Edge Telemetry data frame: after normalization {len(telemetry_df.axes[0])}")

# Read the deny list.
print("Read deny list dataframe")
deny_list_df = pd.read_csv('production_domains.txt', names=["SpamDomain"])
print(f"Size of existing DenyList data frame: {len(deny_list_df.axes[0])}")
deny_list_df['NormalizedDomain'] = deny_list_df['SpamDomain'].map(NormalizeDomain)
print(f"Size of existing DenyList data frame: after normalization {len(deny_list_df.axes[0])}")

edge_deny_intersection(telemetry_df, deny_list_df)


