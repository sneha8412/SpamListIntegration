import pandas as pd
import time

# formats:
# bing spam list: google.com (does not have www)
# Deny list: www.google.com 
# Telemetry: com.google.www (reversed) (only reverse this one)
# chrome: https://www.google.com

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

# Main Program
start_time = time.time()

# Work with Bing Spam list, normalize the domains and print.
spam_list_df = pd.read_csv('all_bing_spam_domains.csv', usecols=['SpamDomain', 'etldDomain'])
print(f"Size of Spam list data frame: {len(spam_list_df.axes[0])}")
spam_list_df['NormalizedDomain'] = spam_list_df['SpamDomain'].map(NormalizeDomain)
print(f"Size of Spam list data frame: after normalization {len(spam_list_df.axes[0])}")
#PrintDataframe(df)

# Work with chrome latest data, normalize and print.
chrome_df = pd.read_csv('latest_chrome_data.csv', usecols=['origin'])
print(f"Size of Telemetry data frame: {len(chrome_df.axes[0])}")
chrome_df['NormalizedDomain'] = chrome_df['origin'].map(NormalizeDomain)
print(f"Size of Telemetry data frame after normalization: {len(chrome_df.axes[0])}")

# Merge the normalized Bing Spam List with latest chrome data using inner join.
merged_df = pd.merge(spam_list_df, chrome_df, how='inner', on=['NormalizedDomain'])
merged_df.drop_duplicates() # removes dupes
#print(f"Printing Merged DataFrame: Spammy Notification Domains")
#PrintDataframe(merged_df)
merged_df.to_csv("bing_spammy_domains_found_in_chrome_latest.csv", index=False)
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
print(f"Final Deny List DataFrame size: {len(concat_deny_list_df.axes[0])}")

# Write final deny list to file.
print(f"Writing final deny list dataframe to file")
concat_deny_list_df.to_csv("final_deny_list_domains_with_only_chrome_latest.csv", index=False, header=None)

# Size of additional entries added to Deny list
print(f"Size of additional items added to deny list: {len(concat_deny_list_df.axes[0]) - len(deny_list_df.axes[0])}")

# print time taken for the process.
print(f"Total processing time (seconds): {time.time() - start_time}")




  