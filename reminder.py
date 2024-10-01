#!/usr/bin/python3
import os
import smtplib # used for sending emails using SMTP
from email.mime.text import MIMEText # alllows you to create email messages that contain text
from datetime import datetime, timedelta # datetime - provide functions to work with dates and times, timedelta - useful for calcultaing days
import csv # handles reading Comma-Seperated Values files
import tkinter as tk

def send_email(client_name, to_email): #function that accepts a recipient's email addess and name of client
    from_email = "alphonseoketch2004@gmail.com" #
    password = os.getenv("EMAIL_PASSWORD")

    subject = "Subscription RenewalReminder"
    body = f"Dear {client_name},\n\nYour subscription is about to expire, Please update it to avoid interruptions."

    msg = MIMEText(body) #create email message using the body text
    msg['Subject'] = subject #sets email's subject field
    msg['From'] = from_email #specifies the sender;s email address
    msg['To'] = to_email #specifies recipient's email address

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server: #creates a secure connection to Gmail
        server.login(from_email, password)
        server.sendemail(from_email, to_email, msg.as_string())
    print(f"Reminder set to {client_name} ({to_email})")


def check_subscriptions():
    today = datetime.now().date() #stores the current date without the time
    reminder_period = timedelta(days=7)

    with open('clients.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            client_name = row['name']
            email = row['email']
            subscription_end = datetime.strptime(row['subscription_end'], "%Y-%m-%d").date()

            if today >= subscription_end - reminder_period:
                send_email(client_name, email)

import tkinter as tk

def send_reminder():
    check_subscriptions()
    print("Reminder Sent!")

root = tk.Tk()
root.title("Subscription Reminder App")

btn = tk.Button(root, text="Send Reminder", command=send_reminder)
btn.pack(pady=20)

root.mainloop()
