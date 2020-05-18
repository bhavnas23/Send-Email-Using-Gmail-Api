# Send-Email-Using-Gmail-Api
This package uses Gmail API to send mails automatically.

For the program to run the app needs authorisation to send emails on behalf of another email id. The authorisation can be obtained from this link: https://developers.google.com/gmail/api/auth/about-auth. This will generate a .json file which should be kept along with other .py files. Rename this file to credentials.json

Steps:
 1. Run "python setup.py install" to install required packages.
 2. Run TryGmailApi.py file.
 3. If running for the first time, the user will be asked to register and login. Allow the app to have permissions to send emails. This step generated token.pickle file
 4. It will then ask for receiver's id (multiple ids should be separated using ';'), subject and body of the email.
 5. Click Send to send the email.
 
Future Scope:
 1. Add attachment, Bcc and Cc fields.
 2. Mail scheduling
 3. Change sender's email id.
