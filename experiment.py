import pandas as pd

def NormalizeDomain(domain1):
    #print(f"NormalizeDomain:{domain1}")
    
    if(str(domain1) == ""):
        return ""

    domain1_parts = str(domain1).split(".")
    domain1_parts.sort()

    if ("www" in domain1_parts):
        domain1_parts.remove("www")
    
    normalized_domain_string = '.'.join(domain1_parts)
    return normalized_domain_string  

def PrintDataframe(df):
    for index, row in df.iterrows():
        print(row)


# work with Bing Spam list
df = pd.read_csv('all_bing_spam_domains_test.csv', usecols=['SpamDomain', 'etldDomain'])
df['NormalizedDomain'] = df['SpamDomain'].map(NormalizeDomain)
print(f"Size of Span list data frame: {df.size}")
#PrintDataframe(df)

# Work with Edge telemerry
df2 = pd.read_csv('edge-permission-telemetry.csv', usecols=['Origin'])
df2['NormalizedDomain'] = df2['Origin'].map(NormalizeDomain)
print(f"Size of Telemetry data frame: {df2.size}")

#Merge Span List normalized with Edge telemetry Normalized
merged_df = pd.merge(df, df2, how='inner', on=['NormalizedDomain'])
merged_df.drop_duplicates() # removes dupes

print(f"Printing Merged DataFrame")
PrintDataframe(merged_df)
print(f"Merged Data Frame Size: {merged_df.size}")

# Read the deny list
print("Read deny list dataframe")
deny_list_df = pd.read_csv('production_domains.txt', names=["DenyOrigin"])
deny_list_df.drop_duplicates()

print("Concat deny list data frame")
frames = [ merged_df, deny_list_df ]
concat_deny_list_df = pd.concat(frames)
concat_deny_list_df.drop_duplicates() # remove dupes
PrintDataframe(concat_deny_list_df)
print(f"Merged Data Frame Size: {concat_deny_list_df.size}")








  