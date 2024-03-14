This is a simple email-assembling code to make repetitive email sending process easier and faster.


It is not meant to be the final automated version as every system will most likely organize files and destination emails differently, as well as amount of files to be attached and so forth.
Therefore, this program was made with purpose of offering tools to automate each individual case of manual email sending.

The code was made using simple python and smtplib, as well as other email assembling imports like MIMEBase and MIMEImage. For my testing I used Outlook as email sending platform. Make sure to insert your platform of use before testing the code. (There are comments in the .py file that may explait it better)

Aside from that, make sure to edit the myconstants.py file to put your own credentials when using this code, it serves as a way to avoid exposing the credentials when using / editing this code.
