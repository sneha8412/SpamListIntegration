from pandas import  DataFrame
from urllib.parse import urlparse

# df1 = DataFrame({'col1':[1,2,3], 'col2':[2,3,4]})
# df2 = DataFrame({'col1':[4,2,5], 'col2':[6,3,5]})


# print(df2[~df2.isin(df1).all(1)])
# print(df2[(df2!=df1)].dropna(how='all'))
# print(df2[~(df2==df1)].dropna(how='all'))

def NormalizeDomain(domain):
    #convert ints and floats to string in case there are IP addresses as  
    if(str(domain) == ""):
        return ""

    domain_noprefix = str(domain)
    if domain_noprefix.startswith("https://"):
        domain_noprefix = domain_noprefix.split("https://")[1]
    
    if domain_noprefix.startswith("http://"):
        domain_noprefix = domain_noprefix.split("http://")[1]

    #domain_parts = domain_noprefix.split(".")
    #domain_parts.sort()

    reversed_domain = ".".join(domain_noprefix.split(".")[::-1])
    print(reversed_domain)
    return reversed_domain

    # if ("www" in domain_parts):
    #     domain_parts.remove("www")
    
    # normalized_domain_string = '.'.join(domain_parts)
    # print(normalized_domain_string)
    # return normalized_domain_string  

# NormalizeDomain('com.gmail.google') #edge
# NormalizeDomain('https://google.gmail.com') #chrome

# NormalizeDomain('gmail.com.google') #edge
# NormalizeDomain('https://google.gmail.com') #chrome

A = urlparse('https://google.gmail.com')
print(A.netloc)

B = urlparse('com.gmail.google')
print(B.netloc)

C = urlparse('gmail.com.google')
print(C.netloc)

D = urlparse('www.gmail.com')
print(D.netloc)

E = urlparse('gmail.com')
print(E.netloc)

E = urlparse('https://www.gmail.com')
print(E.netloc)
