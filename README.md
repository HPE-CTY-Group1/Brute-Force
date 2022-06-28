# BruteForce-Attack
This repository contains an Automation Script written in Python Programming language to Automate Brute-Force Attack. 

The Vulnerable web app used is "DVWA". "DVWA" can either be accessed by Metasploitable virtual machine or by runing a docker container. 

In order to make the script usable interms of both virtualization and containerization, only the URL of DVWA web app is directly used as the target site in the brute_force.py file 

After illegally obtaining the username and password , they are written to a text file. Then text-file is mailed to intended recipient.


Pre-requisite:-

Keep the target webapp(DVWA) runing either by containerization(DOCKER) or Virtualization(Metasploitable)
