#from __future__ import print_function
import pickle
import os
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
#from email.mime.audio import MIMEAudio
#from email.mime.base import MIMEBase
#from email.mime.image import MIMEImage
#from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from apiclient import errors

from tkinter import Tk, Entry, Label, Button, StringVar, END, Toplevel
from tkinter.scrolledtext import ScrolledText
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

class app:
    def __init__(self, root):
        self.screen=root
        self.screen.geometry("500x500")
        self.screen.title("Send Email")
        self.winStart()
    
    def winError(self, errorMsg):
        subScreen = Toplevel(self.screen)
        #subScreen.geometry("150x90")
        subScreen.title("Error:")
        Label(subScreen, text=errorMsg, fg="red").pack()
        Button(subScreen, text="OK", command=subScreen.destroy).pack()
        
    def winRedirect(self):
        subScreen = Toplevel(self.screen)
        subScreen.geometry("300x90")
        subScreen.title("Error:")
        Label(subScreen, text="You are not regstered!! Click OK to register",
              fg="red").pack()
        Button(subScreen, text="OK", command=subScreen.destroy).pack()

    def winSuccess(self):
        subScreen = Toplevel(self.screen)
        subScreen.geometry("150x90")
        subScreen.title("Error:")
        Label(subScreen, text="Mail Sent Successfully",
              fg="red").pack()
        Button(subScreen, text="OK", command=subScreen.destroy).pack()

        
    def winStart(self):
        self.receiverId=StringVar()
        self.subject=StringVar()
        self.body=StringVar()        

        Label(text="To *").place(x=15, y=70)
        Label(text="Subject *").place(x=15, y=140)
        Label(text="Body *").place(x=15, y=210)

        self.creds=self.validateCreds()
        self.validateFields()

    def validateCreds(self):
        creds=None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                self.winRedirect()
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        #print("creds: "+creds)
        return creds

    def validateFields(self):

        Entry(self.screen, textvariable=self.receiverId, width=75).place(x=15, y=100)
        Entry(self.screen, textvariable=self.subject, width=75).place(x=15, y=170)
        self.body = ScrolledText(self.screen, height=10, width=55)
        self.body.place(x=15, y=240)
        #self.body=st.get(1.0, END)

            
        receiverIdTxt=""
        subjectTxt=""
        bodyTxt=""
        def register():
            receiverIdTxt=self.receiverId.get()
            subjectTxt=self.subject.get()
            bodyTxt=self.body.get(1.0, END)

            #validating one or many email ids
            if receiverIdTxt=='' or receiverIdTxt[-1]!=';':
                receiverIdTxt+=';'

            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3};$'
            
            if re.search(regex,receiverIdTxt)is None:
                self.winError("Invalid Email Id")
            else:
                self.winSendMail(receiverIdTxt, subjectTxt, bodyTxt)

        Button(self.screen, text="Send", width=7, bg="gray", command=register).place(x=15, y=430)

    def winSendMail(self, to, subject, body):        
        service = build('gmail', 'v1', credentials=self.creds)

        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        try:
            msg=create_message("me", to, subject, body)
            message = send_message(service, "me", msg)
            self.winSuccess()       
        except Exception as e: 
            self.winError("Message not delivered:" + str(e))
            
        

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_msg =  base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {'raw': raw_msg.decode("utf-8")}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: ' + str(error))
        raise error

if __name__ == '__main__':
    root=Tk()
    top=app(root)
    root.mainloop()
    
