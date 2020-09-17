#!/usr/bin/env python
# coding: utf-8

# In[21]:


import email, getpass, imaplib, os, mailparser
from datetime import date
import wikiquote

import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

rcvr = "hilali.murto@gmail.com"
user = "nooziapp@gmail.com"
pwd = "Noozi135$"
#pwd = getpass.getpass()


# In[22]:


# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
m.select("INBOX")# here you a can choose a mail box like INBOX instead

# use m.list() to get all the mailboxes


# In[23]:


today = date.today()
thedate = today.strftime("%d-%b-%Y")

#to be used in IMAP filter
trd = ("SENTON ",thedate)
trd2 = ''.join(map(str, trd))


# In[24]:


resp, items = m.search(None, (trd2)) # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items = items[0].split() # getting the mails id


# In[25]:


#empty list that will contain html data from all specified emails
html_list = []

for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1] # getting the mail content
    mail = mailparser.parse_from_bytes(email_body) # parsing the mail content to get a mail object
    
    #pull html data, concatenate it into a string, add it to html_list[], then adding space
    b = mail.text_html
    b_1 = ''.join(map(str, b))
    html_list.append(b_1)
    html_list.append("\n\n")


# In[26]:


#concatenates list into string
html = ''.join(map(str, html_list))

#writes string to html
with open((thedate+'.html'), 'w',encoding = 'utf-8') as file:
    file.write(html)


# In[27]:


# Create email body strin
quote = wikiquote.quote_of_the_day()
a, b = quote
email_body = ("\""+ a + "\" — " + b)

subject = "Your Daily Roundup ☕"
body = (email_body)
sender_email = user
receiver_email = rcvr
password = pwd

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

fn = str(thedate+'.html')

filename = fn  # In same directory as script

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)


# In[ ]:




