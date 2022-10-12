import pandas as pd
import time
# This file aims find the domains from the Bing spam list, which have "Spam" and
# "Crush" labels, in the Edge Permissions telemetry. By doing so we will identify the
# the spammy domains that send notifications. We will add these domains to the 
# existing deny list. 

# formats:
# bing spam list: google.com (does not have www)
# Deny list: www.google.com 
# Telemetry: com.google.www (reversed) (only reverse this one)

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

# Work with Edge telemetry, normalize and print.
telemetry_df = pd.read_csv('edge_telemetry_all_domains.csv', usecols=['Origin'])
telemetry_df['NormalizedDomain'] = telemetry_df['Origin'].map(NormalizeDomain)
print(f"Size of Telemetry data frame after normalization: {len(telemetry_df.axes[0])}")

# Work with Bing Spam list, normalize the domains and print.
spam_list_df = pd.read_csv('all_bing_spam_domains.csv', usecols=['SpamDomain', 'etldDomain', 'SpamLabel'])
print(f"Size of Spam list data frame: {len(spam_list_df.axes[0])}")
spam_list_df['NormalizedDomain'] = spam_list_df['SpamDomain'].map(NormalizeDomain)
print(f"Size of Spam list data frame: after normalization {len(spam_list_df.axes[0])}")

# Get the domains from the bing spam that have Spam and Crush Label only. 
result_spam_df = spam_list_df.query("SpamLabel == 'Spam'")
print(f"size of domains with spam label {len(result_spam_df.axes[0])}")
result_crush_df = spam_list_df.query("SpamLabel == 'Crush'")
print(f"size of domains with Crush label {len(result_crush_df.axes[0])}")
df_to_concat = [ result_spam_df, result_crush_df[["SpamDomain"]] ]
result_df = pd.concat(df_to_concat) # gets all rows with "Spam" label
print(f"size of the result of domains with spam and crush combined labels {len(result_df.axes[0])} ")

# Merge the normalized Bing Spam List with Edge telemetry using inner join.
merged_df =  pd.merge(result_df, telemetry_df, how='inner', on=['NormalizedDomain'])
merged_df.drop_duplicates(inplace=True) # removes dupes
merged_df["SpamDomain"].to_csv("bing_spam_domains_from_edge_tobe_added_to_denylist.csv", index=False, header=['origin'])
merged_df.to_csv("bing_spammy_domains_in_edge_telemetry.csv", index=False)
print(f"Spammy Notification Domains Size with Crush and Spam label: {len(merged_df.axes[0])}")

# Read the deny list.
print("Read deny list dataframe")
deny_list_df = pd.read_csv('production_domains.txt', names=["SpamDomain"])
deny_list_df.drop_duplicates(inplace=True)
print(f"Size of existing DenyList data frame: {len(deny_list_df.axes[0])}")

# Update deny list with spammy notification domains
print("Concatenate: Deny list data frame + Spammy notificaton domains")
frames_to_concat = [ deny_list_df, merged_df[["SpamDomain"]] ] # put the frames to union in a array
concat_deny_list_df = pd.concat(frames_to_concat)
concat_deny_list_df.drop_duplicates(inplace=True) # remove dupes if any
print(f"Final Deny List DataFrame size: {len(concat_deny_list_df.axes[0])}")

# Write final deny list to file.
print(f"Writing final deny list dataframe to file")
concat_deny_list_df.to_csv("final_deny_list_domains.csv", index=False, header=None)

# Size of additional entries added to Deny list
print(f"Size of additional items added to deny list: {len(concat_deny_list_df.axes[0]) - len(deny_list_df.axes[0])}")

# print time taken for the process.
print(f"Total processing time (seconds): {time.time() - start_time}")

# TODO: exclude IP address from the bing spam list for comparision.
# TODO : Drop any rows that are empty


  