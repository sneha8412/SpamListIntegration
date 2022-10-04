import pandas as pd
import time

def NormalizeDomain(domain):
    #print(f"NormalizeDomain:{domain1}")
    
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

start_time = time.time()

# Work with Bing Spam list, normalize the domains and print.
spam_list_df = pd.read_csv('all_bing_spam_domains.csv', usecols=['SpamDomain', 'etldDomain'])
spam_list_df['NormalizedDomain'] = spam_list_df['SpamDomain'].map(NormalizeDomain)
print(f"Size of Spam list data frame: {spam_list_df.size}")
#PrintDataframe(df)

# Work with Edge telemetry, normalize and print.
telemetry_df = pd.read_csv('edge-permission-telemetry.csv', usecols=['Origin'])
telemetry_df['NormalizedDomain'] = telemetry_df['Origin'].map(NormalizeDomain)
print(f"Size of Telemetry data frame: {telemetry_df.size}")

# Merge the normalized Bing Spam List with Edge telemetry using inner join.
merged_df = pd.merge(spam_list_df, telemetry_df, how='inner', on=['NormalizedDomain'])
merged_df.drop_duplicates() # removes dupes
#print(f"Printing Merged DataFrame: Spammy Notification Domains")
#PrintDataframe(merged_df)
print(f"Spammy Notification Domains Size: {merged_df.size}")

# Read the deny list.
print("Read deny list dataframe")
deny_list_df = pd.read_csv('production_domains.txt', names=["SpamDomain"])
deny_list_df.drop_duplicates()
print(f"Size of existing DenyList data frame: {deny_list_df.size}")

# Update deny list with spammy notification domains
print("Concatenate: Deny list data frame + Spammy notificaton domains")
frames_to_concat = [ deny_list_df, merged_df[["SpamDomain"]] ] # put the frames to union in a array
concat_deny_list_df = pd.concat(frames_to_concat)
concat_deny_list_df.drop_duplicates() # remove dupes if any
#PrintDataframe(concat_deny_list_df)
print(f"Final Deny List DataFrame size: {concat_deny_list_df.size}")

# Write final deny list to file.
print(f"Writing final deny list dataframe to file")
concat_deny_list_df.to_csv("final_deny_list_domains.csv", index=False, header=None)

# Size of additional entries added to Deny list
print(f"Size of additional items added to deny list: {concat_deny_list_df.size - deny_list_df.size}")

# print time taken for the process.
print(f"Total processing time (seconds): {time.time() - start_time}")




  