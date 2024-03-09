#1........................ SEND OTP
# import requests

# url = "http://gateway.messagecentral.com/verification/v2/verification/send?countryCode=91&customerId=C-AB7C01E4EA1245D&flowType=SMS&mobileNumber=8290486711"

# payload = {}
# headers = {
# 'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLUFCN0MwMUU0RUExMjQ1RCIsImlhdCI6MTY5NzAwNjg2MSwiZXhwIjoxNjk3NjExNjYxfQ.QepTUvyglzeA_MwnzQimUaCYM8rgial-z8SS2YLdRsWGdptPuZQVcYAXLeLmyYwFGllXdH9Uz4iPZ-TGwl_Tmw'
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)

#2.........................VALIDATE OTP

# import requests

# url = "http://gateway.messagecentral.com/verification/v2/verification/validateOtp?countryCode=91&mobileNumber=8290486711&verificationId=36557&customerId=C-AB7C01E4EA1245D&code=1338"

# payload = {}
# headers = {
# 'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLUFCN0MwMUU0RUExMjQ1RCIsImlhdCI6MTY5NzAwNjg2MSwiZXhwIjoxNjk3NjExNjYxfQ.QepTUvyglzeA_MwnzQimUaCYM8rgial-z8SS2YLdRsWGdptPuZQVcYAXLeLmyYwFGllXdH9Uz4iPZ-TGwl_Tmw'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

import requests 

 

url = "https://cpaas.messagecentral.com/auth/v1/authentication/token?country=IN&customerId=C-BCC9B78DE0E742A&key=cGFzc3dvcmQxMjM=&scope=NEW" 

 

payload = {} 

headers = { 

  'accept': '*/*' 

} 

 

response = requests.request("GET", url, headers=headers, data=payload) 

 

print(response.text) 