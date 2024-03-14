import smtplib
import mimetypes
from email.message import EmailMessage
from email.utils import make_msgid
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import os
from myconstants import ATTACHMENT_PATH, EMAIL, PASSWORD

#an easy function to attach images. just pass the emailmessage() instance, the name of the file and the directory to find it.

def attach_image(email, filename, dirname):
  if dirname == None:
    with open(filename, 'rb') as image:
      image_data = image.read()
      email.attach(MIMEImage(image_data, name=filename))

  else:
    with open(f'{dirname}/{filename}') as image:
      image_data = image.read()
      email.attach(MIMEImage(image_data, name=filename))

#the same as mentioned above, but for other common file types such as txt, pdf, etc.
      
def attach_file(email, filename, dirname):
  if dirname == None:
    attachment = MIMEBase('application', "octet-stream")
    attachment.set_payload(open(filename, "rb").read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
    email.attach(attachment)

  else:
    attachment = MIMEBase('application', "octet-stream")
    attachment.set_payload(open(f'{dirname}/{filename}', "rb").read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
    email.attach(attachment)

#define the email message

message = '''
<html>
  <head></head>
  <body>
    <p style="font-size: 16px;">
    Hello!<br/><br/>

    Dear customer,<br/><br/>

    This is an example of message that could be sent to you!<br/><br/>

    Sincerely,<br/><br/>

    </p>
  <img src="cid:{image_cid}" width="552">
  </body>
</html>
'''

#destination emails are extracted from emails.txt file

file = open('emails.txt', 'r')
recipients = file.readlines()
for i in range(len(recipients)):
  recipients[i] = recipients[i].strip(' ,;<>\n')
file.close()

#carboncopy emails are extracter from carboncopy.txt file

file = open('carboncopy.txt', 'r')
carboncopy = file.readlines()
for i in range(len(carboncopy)):
  carboncopy[i] = carboncopy[i].strip(' ,;<>\n')
file.close()

email = EmailMessage()
email['From'] = f'Your Name <{EMAIL}>'
email['To'] = ','.join(recipients)
email['Cc'] = ','.join(carboncopy)
email['Subject'] = 'Email Subject'
email.set_content(message)

image_cid = make_msgid(domain='exampledomain.com')

#here an example footer gif is sent in the body of the email

email.add_alternative(message.format(image_cid=image_cid[1:-1]), subtype='html')

with open('giphy.gif', 'rb') as gif:
  email.get_payload()[1].add_related(gif.read(), maintype='image', subtype='gif', cid=image_cid)

#in this example, each file in your attatchment directory is sent to the senders in emails.txt.
#if there is need to also delete the file after sending it, just uncomment the os.remove commented line.

files = os.listdir(ATTACHMENT_PATH)
files = sorted(files)

for filename in files:
  attach_file(email, filename, ATTACHMENT_PATH)
  #os.remove(f'{ATTACHMENT_PATH}/filename')

#in this example, outlook is the mail platform i have been using, but if you must log in through another platform,
#just change it in the parameter field.

smtp = smtplib.SMTP('smtp-mail.outlook.com', port=587)
smtp.starttls()
smtp.login(EMAIL, PASSWORD)
smtp.sendmail(EMAIL, recipients+carboncopy, email.as_string())
smtp.quit()