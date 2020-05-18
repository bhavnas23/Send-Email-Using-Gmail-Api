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
import time
from tkinter import Tk, Entry, Label, Button, StringVar, END, Toplevel, Message, RAISED, messagebox
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

    #displays error window
    def winError(self, errorMsg):
        subScreen = Toplevel(self.screen)
        #subScreen.geometry("150x90")
        subScreen.title("Error:")
        Label(subScreen, text=errorMsg, fg="red").pack()
        Button(subScreen, text="OK", command=subScreen.destroy).pack()

    #displays Redirect window
    def winRedirect(self):
        subScreen = Toplevel(self.screen)
        subScreen.geometry("300x90")
        subScreen.title("Error:")
        Label(subScreen, text="You are not regstered!! Click OK to register",
              fg="red").pack()
        Button(subScreen, text="OK", command=subScreen.destroy).pack()

    #displays succes window
    def winSuccess(self):
        subScreen = Toplevel(self.screen)
        subScreen.geometry("150x90")
        subScreen.title("Error:")
        Label(subScreen, text="Mail Sent Successfully",
              fg="red").pack()
        Button(subScreen, text="OK", command=subScreen.destroy).pack()

    #program begins here
    def winStart(self):
        self.receiverId=StringVar()
        self.subject=StringVar()
        self.body=StringVar()        

        Label(text="To *").place(x=15, y=70)
        Label(text="Subject *").place(x=15, y=140)
        Label(text="Body *").place(x=15, y=210)


        Entry(self.screen, textvariable=self.receiverId, width=75).place(x=15, y=100)
        Entry(self.screen, textvariable=self.subject, width=75).place(x=15, y=170)
        self.body = ScrolledText(self.screen, height=10, width=55)
        self.body.place(x=15, y=240)
        try:
            self.creds=self.validateCreds()
            try:
                self.validateFields()
            except Exception as e:
                print(messagebox.showerror("Error", e))
        except Exception as e:
            print(messagebox.showerror("Error", e))
        
            

    #validate credentials and token files
    def validateCreds(self):
        creds=None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
            return creds
        # If there are no (valid) credentials available, let the user log in.
        #cont="cancel"
        cont=False
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                cont=True
                return creds               
            else:
                #self.winRedirect()
                cont = messagebox.askokcancel("Registration", "You are not registered!! Click OK to register Cancel to Quit")
                print(cont)
        #print("hi"+cont)
        if cont==True:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
            return creds
        else:
            self.screen.destroy()            
            raise Exception("Program Quit" )
        

    #validae fields
    def validateFields(self):

        #Entry(self.screen, textvariable=self.receiverId, width=75).place(x=15, y=100)
        #Entry(self.screen, textvariable=self.subject, width=75).place(x=15, y=170)
        #self.body = ScrolledText(self.screen, height=10, width=55)
        #self.body.place(x=15, y=240)
        #self.body=st.get(1.0, END)

            
        receiverIdTxt=""
        subjectTxt=""
        bodyTxt=""
        def register():
            receiverIdTxt=self.receiverId.get()
            subjectTxt=self.subject.get()
            bodyTxt=self.body.get(1.0, END)

            #validating one or many email ids
            regex = '(([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)(\s*;\s*|\s*$))+'
            if re.fullmatch(regex, receiverIdTxt) is None:#len([re.search(regex, receiverIdTxt)])!=len(receiverIdTxt.split(';')):
                    self.winError("Invalid Email Id")
            else:
                self.winSendMail(receiverIdTxt, subjectTxt, bodyTxt)

        Button(self.screen, text="Send", width=7, bg="gray", command=register).place(x=15, y=430)

    #Create and Send Email
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
    
