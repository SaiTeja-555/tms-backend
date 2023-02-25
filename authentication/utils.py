from concurrent.futures import thread
from django.core.mail import EmailMessage
import threading

class EmailThread(threading.Thread):

    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:

    @staticmethod
    def send_mail(data):
        print("sending mail.................")
        email = EmailMessage(
            subject = data['email_subject'],
            body = data['email_body'],
            to =[data['to_email']]
            
        )
        EmailThread(email).start()