import pandas as pd

# Convert the edge_permissions telemtry to contain only origin, discard akll other
# columns
# Telemetry: com.google.www (reversed) 
# need to unreverse it first 
# run the executable for the bloom filter 
# pass the arguments  

def reverse_domain(domain):
    #convert ints and floats to string in case there are IP addresses as  
    if(str(domain) == ""):
        return ""

    domain_parts = str(domain).split(".")
    #domain_parts.sort()
    reversed_domain = domain_parts[::-1]

    reversed_domain_string = '.'.join(reversed_domain)
    return reversed_domain_string 
   
#Main Program
#read the edhe telemetry csv.
telemetry_df = pd.read_csv('edge_telemetry_all_domains.csv', usecols=['Origin'])
print(f"Size of Telemetry data frame: {len(telemetry_df.axes[0])}")
telemetry_df['ReversedDomain'] = telemetry_df['Origin'].map(reverse_domain)
#drop nan values if any
telemetry_df.dropna(inplace=True)
# write to csv
telemetry_df.to_csv("reversed_edge_telemetry_all_domains.csv", index=False, columns=["ReversedDomain"])

