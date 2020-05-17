from setuptools import setup, find_packages

setup(
    name='TryGmailApi',
    version='0.1.0',
    description='Send Emails Automtically',
    author='Bhavna Soni',
    author_email='bhavna.soni108@gmail.com',
    packages=find_packages(include=['TryGmailApi']),
    python_requires='>=3.5.2',
    install_requires=[
        'pickle',
        'os',
        'googleapiclient.discovery',
        'google_auth_oauthlib.flow',
        'google.auth.transport.requests',
        'base64',
        'email',
        'mimetypes',
        'apiclient',
        'tkinter',
        're'
        ],
    entry_points={
        "gui_scripts":[
            "baz = TryGmailApi:__main__"
        ]
    }
)
