import csv
import pandas as pd

# formats:
# bing spam list: google.com (does not have www)
# Deny list: www.google.com 
# Telemetry: com.google.www (reversed)

# intersect function to check which subdomains in the Bing spam are present in the Edge Permissions telemetry and
# create a new list.
def FindNotificationSendingDomainsInBingSpamList(bing_spam_domains_csv_file_path, edge_notification_sending_domains_dict):
    #create a new file with intersected data
    notification_sending_domains_in_bing_dict = {}
    with open(bing_spam_domains_csv_file_path, mode='r', encoding='utf8') as csv_file_policy:
        csv_reader_policy = csv.reader(csv_file_policy, delimiter=",")

        for domain_row in csv_reader_policy:
            #print(f"FindNotificationSendingDomainsInBingSpamList: Reading bing spam list domain: {domain_row}")
            sub_domain_name = domain_row[0]
            eTLD_name = domain_row[1]
            # check if the sub domain is  == to eTLD in bing spam list
            if sub_domain_name == eTLD_name and DomainExists(sub_domain_name, edge_notification_sending_domains_dict):
                #print(f"FindNotificationSendingDomainsInBingSpamList: Found Spammy Notification Sending Domain: {sub_domain_name}")
                notification_sending_domains_in_bing_dict[sub_domain_name] = 1
    print("FindNotificationSendingDomainsInBingSpamList: notification_sending_domains_in_bing_dict created ")
    return notification_sending_domains_in_bing_dict

# create a dictionary with the orgins in the edge permission telemetry to make it less expensive to read. 
def ReadNotificationSendingDomainsFromEdgeTelemetry(edge_telemetry_csv_file_path):
    edge_notification_sending_domains_dict = {}

    with open(edge_telemetry_csv_file_path, mode='r', encoding='utf8') as csv_file_policy:
        csv_reader_policy = csv.reader(csv_file_policy, delimiter=",")

        for domain_row in csv_reader_policy:
            #print(f"ReadNotificationSendingDomainsFromEdgeTelemetry: Reading Edge Telemetry Domain: {domain_row}")
            origin = domain_row[0]
            edge_notification_sending_domains_dict[origin] = 1
    
    print("ReadNotificationSendingDomainsFromEdgeTelemetry: edge_notification_sending_domains_dict created ")
    return  edge_notification_sending_domains_dict

# union function : to add these bing spam domains in the deny_list if it doesn't already exist.
def MergeSpamDomainNamesInDenyList(deny_list_file_path, notification_sending_domains_in_bing_dict):
    current_deny_list_domains_dict = {}

    # cache all existing domains in the current deny list into a dict
    with open(deny_list_file_path, mode='r', encoding="utf8") as csv_file_policy:
        csv_reader_policy = csv.reader(csv_file_policy)
        
        for deny_list_domain in csv_reader_policy:
            #print(f"MergeSpamDomainNamesInDenyList: Reading Deny List Domain: {deny_list_domain}")

            domain_name = deny_list_domain[0]
            current_deny_list_domains_dict[domain_name] = 1

    # merge the spam list domains into current deny list by adding those domains that don't already exist in current deny list
    with open(deny_list_file_path, mode='a+', encoding="utf8") as dentListTextFile:

        for spam_notification_domain in notification_sending_domains_in_bing_dict:
            #print(f"MergeSpamDomainNamesInDenyList: Reading Spammy Notification sending Domain: {spam_notification_domain}")

            if not DomainExists(spam_notification_domain, current_deny_list_domains_dict):
                #print(f"MergeSpamDomainNamesInDenyList: Adding new domain to current deny list: {spam_notification_domain}")
                dentListTextFile.write(f"\n{spam_notification_domain}")
    print(f"MergeSpamDomainNamesInDenyList: Added new domain to current deny list")

def DomainExists(domain_name, dict):
    for item in dict:
        if AreDomainsEqual(item, domain_name):
            return True
    return False


def AreDomainsEqual(domain1, domain2):

    domain1_parts = domain1.split(".")
    domain1_parts.sort()
    if ("www" in domain1_parts):
        domain1_parts.remove("www")

    domain2_parts = domain2.split(".")
    domain2_parts.sort()
    if ("www" in domain2_parts):
        domain2_parts.remove("www")

    return domain1_parts == domain2_parts

# Main program
edge_telemetry_file_path = 'edge-permission-telemetry.csv'
bing_spam_list_file_path = 'all_bing_spam_domains.csv'
deny_list_file_path = 'production_domains.txt'

edge_notification_sending_domains_dict = ReadNotificationSendingDomainsFromEdgeTelemetry(edge_telemetry_file_path)
notification_sending_domains_in_bing_dict = FindNotificationSendingDomainsInBingSpamList(bing_spam_list_file_path, edge_notification_sending_domains_dict)
MergeSpamDomainNamesInDenyList(deny_list_file_path, notification_sending_domains_in_bing_dict)  
