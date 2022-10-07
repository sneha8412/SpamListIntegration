import pandas as pd
import time

# formats:
# bing spam list: google.com (does not have www)
# Deny list: www.google.com 
# Telemetry: com.google.www (reversed)


def NormalizeDomain(domain):
    #print(f"NormalizeDomain:{domain}")
    
    #convert ints and floats to string in case there are IP addresses as  
    if(str(domain) == ""):
        return ""

    domain_parts = str(domain).split(".")
    domain_parts.sort()

    if ("www" in domain_parts):
        domain_parts.remove("www")
    
    normalized_domain_string = '.'.join(domain_parts)
    return normalized_domain_string  

def PrintDataframe(df):
    for index, row in df.iterrows():
        print(row)

# Main Program
start_time = time.time()

# Work with Bing Spam list, normalize the domains and print.
spam_list_df = pd.read_csv('all_bing_spam_domains.csv', usecols=['SpamDomain', 'etldDomain'])
print(f"Size of Spam list data frame: {len(spam_list_df.axes[0])}")
spam_list_df['NormalizedDomain'] = spam_list_df['SpamDomain'].map(NormalizeDomain)
print(f"Size of Spam list data frame: after normalization {len(spam_list_df.axes[0])}")
#PrintDataframe(df)

# Work with Edge telemetry, normalize and print.
telemetry_df = pd.read_csv('edge_telemetry_all_domains.csv', usecols=['Origin'])
print(f"Size of Telemetry data frame: {len(telemetry_df.axes[0])}")
telemetry_df['NormalizedDomain'] = telemetry_df['Origin'].map(NormalizeDomain)
print(f"Size of Telemetry data frame after normalization: {len(telemetry_df.axes[0])}")

# Merge the normalized Bing Spam List with Edge telemetry using inner join.
merged_df = pd.merge(spam_list_df, telemetry_df, how='inner', on=['NormalizedDomain'])
merged_df.drop_duplicates() # removes dupes
#print(f"Printing Merged DataFrame: Spammy Notification Domains")
#PrintDataframe(merged_df)
print(f"Spammy Notification Domains Size: {len(merged_df.axes[0])}")

# Read the deny list.
print("Read deny list dataframe")
deny_list_df = pd.read_csv('production_domains.txt', names=["SpamDomain"])
deny_list_df.drop_duplicates()
print(f"Size of existing DenyList data frame: {len(deny_list_df.axes[0])}")

# Update deny list with spammy notification domains
print("Concatenate: Deny list data frame + Spammy notificaton domains")
frames_to_concat = [ deny_list_df, merged_df[["SpamDomain"]] ] # put the frames to union in a array
concat_deny_list_df = pd.concat(frames_to_concat)
concat_deny_list_df.drop_duplicates() # remove dupes if any
#PrintDataframe(concat_deny_list_df)
print(f"Final Deny List DataFrame size: {len(concat_deny_list_df.axes[0])}")

# Write final deny list to file.
print(f"Writing final deny list dataframe to file")
concat_deny_list_df.to_csv("final_deny_list_domains.csv", index=False, header=None)

# Size of additional entries added to Deny list
print(f"Size of additional items added to deny list: {len(concat_deny_list_df.axes[0]) - len(deny_list_df.axes[0])}")

# print time taken for the process.
print(f"Total processing time (seconds): {time.time() - start_time}")




  