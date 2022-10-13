
import pandas as pd

# This file aims to find the top domains from the list of top-1m.csv in the new domains
# that will be added to the deny list. 

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

# Find intersection of new deny list (created with bing spam filter) with the top 10k data 
def edge_deny_intersection_10k(top_10k_sites_df, deny_df):
    merged_df = pd.merge(top_10k_sites_df, deny_df, how='inner', on=['NormalizedDomain'])
    merged_df.drop_duplicates(inplace=True) # removes dupes
    print(f"intersection of top 10k sites and new deny list Domains Size: {len(merged_df.axes[0])}")
    #merged_df.to_csv("top_10ksites_found_in_denylist.csv", index=False, header=True, columns =['rank', 'Origin'])
    return merged_df

# Remove top 100 sites from the new deny list (created with bing spam filter).
def remove_top_100_sites_from_deny(deny_to_add, top_100_sites):
    deny_to_add = deny_to_add[['NormalizedDomain', 'origin']]
    deny_to_add.rename(columns = {"origin": "Origin"}, inplace=True)
    top_100_sites = top_100_sites[['NormalizedDomain', 'Origin']]
  
    print("top 100 sites with Origin + Normalized Domain")
    print(top_100_sites)

    merged_df = deny_to_add.merge(top_100_sites, how='left', indicator=True)
    print(f"Size of the new deny list WITH the top 100 domains: {len(merged_df.axes[0])}")

    deny_with_no_top_sites_df = merged_df[merged_df['_merge'] == 'left_only']
    del deny_with_no_top_sites_df["NormalizedDomain"]
    del deny_with_no_top_sites_df["_merge"]
    #deny_with_no_top_sites_df.dropna(inplace=True)
    print(f"Size of deny list WITHOUT top 100 domains: {len(deny_with_no_top_sites_df.axes[0])}")
    print(deny_with_no_top_sites_df)

    #deny_with_no_top_sites_df.to_csv("deny_list_after_top100_domains_removed.csv", index=False, columns=['origin'])
    return deny_with_no_top_sites_df

# compare the new deny list (one without the top 100 sites) with the existing deny list
# to keep only unique domains
#TODO Fix the format of the concat_deny_list_df csv. 
def update_deny_list_with_new_entries(deny_without_top, existing_deny):
    print(f"size of the deny list to add: {len(deny_without_top.axes[0])}")
    #del deny_without_top['NormalizedDomain']

    print("deny list without top sites")
    print(deny_without_top)

    print("existing deny list")
    print(existing_deny)
    
    frames_to_concat = [existing_deny, deny_without_top ] # put the frames to union in a array
    concat_deny_list_df = pd.concat(frames_to_concat)
    concat_deny_list_df.drop_duplicates(inplace=True) # remove dupes if any
    concat_deny_list_df.dropna(inplace=True)
    print(f"Final Deny List DataFrame size: {len(concat_deny_list_df.axes[0])}")
    print(f"Size of additional items added to deny list: {len(concat_deny_list_df.axes[0]) - len(existing_deny.axes[0])}")
    
    print("deny list with top 100 removed and concatened with existing deny list:")
    print(concat_deny_list_df)
    return concat_deny_list_df

# Main Program 

# Work with top 1 million site csv, create new file with right header names. 
header_list = ["rank", "Origin"]
top_df = pd.read_csv('top-1m.csv', names=header_list)
top_10k = top_df.head(10000) # return the top 10k rows
top_10k.to_csv("top_10k_sites_with_header.csv", index=False, columns=['rank','Origin'])
print(f"Size of top 1 mil data frame: {len(top_df.axes[0])}")

top_100_df = top_df.head(100) # gets the top 100 domain
top_100_df.to_csv("top_100_sites_with_header.csv", index=False, columns=['rank','Origin'])
top_100_with_header_df =  pd.read_csv('top_100_sites_with_header.csv', usecols=['rank','Origin'])
top_100_with_header_df['NormalizedDomain'] = top_100_df['Origin'].map(NormalizeDomain)

# Read the deny list.
print("Read deny list dataframe")
deny_list_df = pd.read_csv('bing_spam_original_domains_from_edge_tobe_added_to_denylist.csv', usecols=['origin'])
deny_list_df['NormalizedDomain'] = deny_list_df['origin'].map(NormalizeDomain)
print(f"Size of DenyList after bing spam match: {len(deny_list_df.axes[0])}")

# Read Existing deny_list.
existing_deny_df = pd.read_csv('production_domains.txt',  names=["Origin"])
print(f"Size of existing DenyList data frame: {len(existing_deny_df.axes[0])}")

print("deny list produced after merging spam + telemetry")
print(deny_list_df)

print("top 100 sites list with header")
print(top_100_with_header_df)

deny_with_no_top_sites_df = remove_top_100_sites_from_deny(deny_list_df, top_100_with_header_df)

final_deny_list = update_deny_list_with_new_entries(deny_with_no_top_sites_df, existing_deny_df)
final_deny_list.to_csv('final_deny_list_without_dupes_and_top_sites.csv', index=False )


