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

# Main Program 

# Work with Edge telemetry, normalize and print.
telemetry_df = pd.read_csv('edge_telemetry_all_domains.csv', usecols=['Origin'])
print(f"Size of Telemetry data frame: {len(telemetry_df.axes[0])}")
telemetry_df['NormalizedDomain'] = telemetry_df['Origin'].map(NormalizeDomain)
print(f"Size of Telemetry data frame: after normalization {len(telemetry_df.axes[0])}")

# Read the deny list.
print("Read deny list dataframe")
deny_list_df = pd.read_csv('production_domains.txt', names=["SpamDomain"])
print(f"Size of existing DenyList data frame: {len(deny_list_df.axes[0])}")
# Work with Deny list, normalize and print
deny_list_df['NormalizedDomain'] = deny_list_df['SpamDomain'].map(NormalizeDomain)
print(f"Size of existing DenyList data frame: after normalization {len(deny_list_df.axes[0])}")

# Find union with the edge telemtry data
merged_df = pd.merge(deny_list_df, telemetry_df, how='inner', on=['NormalizedDomain'])
merged_df.drop_duplicates() # removes dupes
#print(f"Printing Merged DataFrame: Deny list Notification Domains that are present in Edge telemetry")
print(f"Spammy Notification Domains Size: {len(merged_df.axes[0])}")

# Find the union between edge elemetry and Deny list 


