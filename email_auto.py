import smtplib, ssl
import time
import random
from imap_tools import MailBox, AND
import imap_tools

sleeping_time = 10   #in seconds

gmail_server = "smtp.gmail.com"
gmail_port = 465

def send_mail(sender_mail, password,my_server,my_port, receiver_mail, send_from_gmail):
    context = ssl.create_default_context()
    if(send_from_gmail):
        smtp_server = gmail_server
        port = gmail_port
        try:
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_mail, password)
                server.sendmail(sender_mail, receiver_mail, select_msg())
                print("Mail sent from " + sender_mail + " to " + receiver_mail)
        except:
            print("Fail sending mail from " + sender_mail + " to " + receiver_mail)

    else:
        smtp_server = my_server
        port = my_port
        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(sender_mail, password)
                server.sendmail(sender_mail, receiver_mail, select_msg())
                print("Mail sent from " + sender_mail + " to " + receiver_mail)
        except:
            print("Fail sending mail from " + sender_mail + " to " + receiver_mail)

def star_mail(email,password):
    try:
        with MailBox('imap.gmail.com').login(email, password, initial_folder='INBOX') as mailbox:
            flags = (imap_tools.MailMessageFlags.ANSWERED, imap_tools.MailMessageFlags.FLAGGED)
            mailbox.flag(mailbox.fetch(AND(seen=False), limit=2, reverse=True), flags, True)
        print(email+" emails are stared")
    except:
        print(email + " emails could not stared this time")

def select_msg():
    try:
        message_subject = random.choice(mail_texts_list).split()[0]
    except:
        message_subject = "Regarding Your concern"
    try:
        message_content = random.choice(mail_texts_list)
    except:
        message_content = "I will be able to proceed as you requested. Thank you."

    message = """\
Subject:""" + message_subject + """\n\n""" + message_content
    print("----------------")
    print(message)
    print("----------------")

    return message


gmails = open("gmails.txt","r").read().split("\n")
gmail_list =[]
for i in range(0,len(gmails)):
    if(gmails[i]!=""):
        gmail_list.append(gmails[i].split())

print(gmail_list)

my_mails = open("my_mails.txt","r").read().split("\n")
my_mail_list =[]
for i in range(0,len(my_mails)):
    if (my_mails[i] != ""):
        my_mail_list.append(my_mails[i].split())

print(my_mail_list)

mail_texts_list = open("text_for_mail.txt","r", encoding="utf8").read().split("\n\n")

while(True):
    for i in range(0,len(my_mail_list)):
        for j in range(0,len(gmail_list)):
            send_mail(my_mail_list[i][0],my_mail_list[i][1],my_mail_list[i][2],my_mail_list[i][3],gmail_list[j][0],False)
            time.sleep(10)
            star_mail(gmail_list[j][0],gmail_list[j][1])
            time.sleep(5)
            send_mail(gmail_list[j][0],gmail_list[j][1],"not used","not used",my_mail_list[i][0],True)
            time.sleep(sleeping_time)


print("THE END")






