# BruteForce-Attack
This repository contains an Automation Script written in Python Programming language to Automate Brute-Force Attack and SQLi 

The Vulnerable web app used is "DVWA" for Brute-force and "Mutillidae" for SQLi


Pre-requisite & Run-time requirements:-

1. Keep the target webapp(DVWA,Mutillidae) runing either by containerization(DOCKER) or Virtualization(Metasploitable)
2. usernames/password files should be in same dir.
3. python module to mail the result(of brute-force) should be in same directory.



Result handling:-

1. Output of brute-force loaded into .txt file and mailed to intended recipient
2. Output of SQLi attack is directly launched on a browser
3. Traces of output-file(if generated like in brute-force) is removed

