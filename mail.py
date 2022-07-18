'''----------------Test Report Mail------------------------------
Here, The results of the attacks are mailed to the intended destination
By accessing the generated attack result as input to the below defined function
'''

#Importing required libraries to interact with the target site and to use smtp
import re
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

def result_mail(result_file_path):
    
    target_site = os.getenv('TARGET_SITE')
    
    # getting the from-address from .env file
    fromaddr = os.getenv('FROMADDR')

    # verifying whether the input - validity 
    #input destination address
    toaddr =input("Enter Destination email address: ")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    if(re.fullmatch(regex, toaddr)):
        print("Sending email...")
    else:
        print("Invalid Email")
        quit() 

    # masking the user entered password 
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
    attachment = open(result_file_path, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % result_file_path)

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
    os.remove(result_file_path)

    #Printing the confirmation
    print("Mail sent")

    time.sleep(3)

