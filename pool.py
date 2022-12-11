#Returns 88dhgzEuTX.... internal address and extrapolates operator address and ERG value based on simple blockchain heuristic when supplied a block-hash
#------------------------------------------------------------
from colorama import init, Fore, Back, Style #for colored CLI text (colors = coolness ^ 10)
init() #initialize colorama 
import requests 
import json 
import random #for rotating cheesy intro
import sys #for args and early script terimination, if no arg supplied
import time #sleep to avoid globalist rate-limiting scum

#colorama test/reference
#print(Fore.RED + 'text')
#print(Back.GREEN + 'and with a green background')
#print(Style.BRIGHT + 'and in dim text')
#print(Style.RESET_ALL)
#print('back to normal now')
#print(f"This is {Fore.GREEN}color{Style.RESET_ALL}!") 
#print("This is "+Fore.GREEN+"color"+Style.RESET_ALL+"!")

print(Fore.RED + "  ____________________________")
print(Fore.RED + " [--"+Fore.CYAN+" Ergo PoolOp Sniff v0.1"+Fore.RED+" --]")
print(Fore.RED + " ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
cheesy_intro = [" --------- meep meep ----------", " ------- Praise Kushti -------", " --- sniff sniff... you smell that? it's data... ---", " -- Buy me a beer: XMR: 87YqHTqUGqgJzVoKg5XCUtM3yisn7ygFkXhoDgs2CcDFLKs4BZfqenrGNemRa6rNUhLYBcS8Wc6ahDPdNtoKJw8EDNUra53"]
print(Fore.GREEN + random.choice(cheesy_intro))
print(Style.RESET_ALL)
print("  -- Input a block-hash arg at runtime (e.g. "+Fore.CYAN+"pool.py def6f75737e7db171cde4f3814fd1960b63a21c51f9503c04a6ff902548152d3"+Style.RESET_ALL+") ")
print("  -- Returns 88dhgzEuTX.... internal address and extrapolates operator address (and its' balance) based on simple blockchain heuristic :) ")
print("  -- Known Limitations: if the internal [88..] address does not have outgoing tx's on page 1 (20tx's) it will not find the operator address! ")
print("  -- Methodology may not be 100% accurate, though appears to be so far...")

#state-of-the-art anti-anti-scraping technology
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
url = "https://api.ergoplatform.com/api/v1/blocks/" 
# Check if an argument was supplied
if len(sys.argv) < 2:
    # If no argument was supplied, print an error message
    print("Error: Please supply a block-hash argument")
    sys.exit() #exit()
hash = sys.argv[1]
     
print("Looking Up Pool Operator Address for Ergo Block Hash [ "+Fore.YELLOW+" "+hash+Style.RESET_ALL+" ]...");
print("")
# Send a request to the URL and get the response
response = requests.get(url+hash, headers)


#STEP 1: BLOCK HASH --> BLOCK/"88" ADDRESS
json_response = json.loads(response.text)
block = json_response["block"]["header"]["height"]
op88 = str(json_response["block"]["blockTransactions"][0]["outputs"][1]["address"])
print("Sniffing "+Fore.GREEN+"Block #"+str(block)+Style.RESET_ALL+ " for 88dhgzEuTX... address....")
print("")
print("Internal 88... Found! "+Fore.GREEN+op88+Style.RESET_ALL)
print("")
time.sleep(1)

# STEP 2 88 ADDRESS TO POOL OP #
#url = "https://api.ergoplatform.com/api/v1/addresses/"+op88+"/transactions?fromHeight="+str(block-1)+"&toHeight="+str(block+1)
url = "https://api.ergoplatform.com/api/v1/addresses/"+op88+"/transactions"
response = requests.get(url, headers)
json_response = json.loads(response.text)
n = len(json_response["items"])
if(n >= 20):
    print(Fore.CYAN+"Parsing "+Fore.GREEN+"top "+str(n)+Style.RESET_ALL+" tx's from "+Fore.GREEN+op88+Style.RESET_ALL)
else:
    print(Fore.CYAN+"Parsing "+Fore.GREEN+"all "+str(n)+Style.RESET_ALL+" tx's from "+Fore.GREEN+op88+Style.RESET_ALL)
found = False
pool_op = ""
for i in range(n):
    #print("item #"+str(i)+":") #DEBUGGING
    #print("tx-id :"+str(json_response["items"][i]["id"])) #DEBUGGING
    noutputs = len(json_response["items"][i]["outputs"])
    output = str(json_response["items"][i]["outputs"][noutputs-1]["address"])
    #print(output)
    if(output.startswith("88") == False):
        #print("output :"+output) #DEBUGGING
        found = True
        pool_op = output
time.sleep(1)
if(not found):
    print(Fore.RED+"Pool Operator Address Not Found! "+Style.RESET_ALL+" - try again when [88...] has outgoing tx within top-20 tx's...")
    sys.exit() #no point running balance-checks on non-existent address; kill script
else:
    print(Fore.CYAN+"Found "+Fore.RED+" Pool Op "+Fore.GREEN+pool_op+Style.RESET_ALL+"!")
    print(Fore.CYAN+"Checking "+Fore.GREEN+pool_op+Style.RESET_ALL+" balance....")
    
# STEP 3 FETCH POOL OP BALANCE #
url = "https://api.ergoplatform.com/api/v1/addresses/"+pool_op+"/balance/confirmed"
response = requests.get(url, headers)
json_response = json.loads(response.text)
balance = (json_response["nanoErgs"]/1000000000) #convert nano erg to erg
print(Fore.RED+"Pool Op "+Fore.GREEN+pool_op+Style.RESET_ALL+" balance = "+Fore.CYAN+str(balance)+" ERG"+Style.RESET_ALL+"!")
