import pandas as pd

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

# Find intersection of deny list with the chrome telemtry data. 
def chrome_deny_intersection(chrome_df, deny_df):
    merged_df = pd.merge(deny_df, chrome_df, how='inner', on=['NormalizedDomain'])
    merged_df.drop_duplicates() # removes dupes
    print(f"intersection of chrome and deny list Domains Size: {len(merged_df.axes[0])}")
    merged_df.to_csv("chrome_deny_intersect_only_domains.csv", index=False, columns =['NormalizedDomain', 'origin'])
    return merged_df

# Main Program 

# Work with google telemetry, normalize and print.
print("Read google list dataframe")
chrome_list_df = pd.read_csv('latest_chrome_data.csv', usecols=["origin"])
print(f"Size of google Aug data frame: {len(chrome_list_df.axes[0])}")
chrome_list_df['NormalizedDomain'] = chrome_list_df['origin'].map(NormalizeDomain)
print(f"Size of google data frame: after normalization {len(chrome_list_df.axes[0])}")

# Read the deny list, normailize the domain for comparison with Chrome data.
print("Read deny list dataframe")
deny_list_df = pd.read_csv('production_domains.txt', names=["SpamDomain"])
print(f"Size of existing DenyList data frame: {len(deny_list_df.axes[0])}")
deny_list_df['NormalizedDomain'] = deny_list_df['SpamDomain'].map(NormalizeDomain)
print(f"Size of existing DenyList data frame: after normalization {len(deny_list_df.axes[0])}")

chrome_deny_intersection(chrome_list_df, deny_list_df)

