import pandas as pd
import csv

def FindTopMatchingDomainNamesInPolicy(writer, top_list_row):

    top_domain_name = top_list_row[1]
    top_domain_name_parts = top_domain_name.split(".")
    top_domain_name_parts.sort()

    with open('first_iteration_sneha.csv', mode='r', encoding="utf8") as csv_file_policy:
        csv_reader_policy = csv.reader(csv_file_policy, delimiter=",")
        
        for policy_row in csv_reader_policy:
            #print("policy row domain:" + str(policy_row[0]))
            policy_domain_name_parts = policy_row[0].split(".")
            
            if ("www" in policy_domain_name_parts):
                policy_domain_name_parts.remove("www")

            policy_domain_name_parts.sort()

            if (top_domain_name_parts == policy_domain_name_parts):
                print("found matching policy domain:" + str(policy_row[0]))
                writer.writerow(policy_row)
                return True

# Main program
with open('top-1m.csv', mode='r', encoding="utf8") as csv_file:
    # csv_reader = csv.DictReader(csv_file)
    csv_reader = csv.reader(csv_file, delimiter=",") 

    with open('domain-matches.csv', mode="w", encoding='UTF8') as f:
        writer = csv.writer(f)
        header = ["Origin","SumInstanceCount","SumGestureCount","SumNoGestureCount", "SumDeniedActionCount","SumDismissedCount","SumIgnoredCount","SumGrantedActionCount","DeniedPercent","NoGesturePercent"]
        writer.writerow(header)

        for top_list_row in csv_reader:
            #print("top_list_row" + str(top_list_row[0]) + str(top_list_row[1]))
            FindTopMatchingDomainNamesInPolicy(writer, top_list_row)

