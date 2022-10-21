
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


# Find intersection of new deny list (created with bing spam filter) with the top 10k data 
def toplist_and_bloom_intersection(top_sites_df, bloom_df):
    merged_df = pd.merge(top_sites_df, bloom_df, how='inner', on=['Origin'])
    merged_df.drop_duplicates(inplace=True) # removes dupes
    print(f"intersection of toplist 1 mil sites and bloom false positives list Domains Size: {len(merged_df.axes[0])}")
    return merged_df

# Main Program 

# Work with top 1 million site csv, create new file with right header names. 
header_list = ["rank", "Origin"]
top_df = pd.read_csv('top-1m.csv', names=header_list)
top_df.to_csv("top_1m_sites_with_header.csv", index=False, columns=['rank','Origin'])
top_1m_with_header_df = pd.read_csv('top_1m_sites_with_header.csv', usecols=['rank', 'Origin'])
#top_1m_with_header_df['NormalizedDomain'] = top_df['Origin'].map(NormalizeDomain)
print("Top 1m sites with header")
print(top_df)

# Read the deny list (without the crush_zh_cn filter).
print("Read bloom flase positives list")
bloom_list_df = pd.read_csv('bloom_filter_false_positives_output.txt', names=['Origin'])
bloom_list_df.to_csv("bloom_false_positives_with_header.csv", index=False, columns=['Origin'])
bloom_list_with_header =  pd.read_csv('bloom_false_positives_with_header.csv', usecols=['Origin'])
#bloom_list_df['NormalizedDomain'] = bloom_list_df['Origin'].map(NormalizeDomain)
print(f"Size of bloom false positives: {len(bloom_list_df.axes[0])}")
print(bloom_list_df)

toplist_and_bloom_intersect_df = toplist_and_bloom_intersection(top_1m_with_header_df, bloom_list_with_header)
print(toplist_and_bloom_intersect_df)
toplist_and_bloom_intersect_df.to_csv('top_sites_found_in_bloom_filter.csv', index=False, columns=['rank', 'Origin'])

