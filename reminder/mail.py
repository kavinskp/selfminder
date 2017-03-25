from django.core.mail import send_mail

from selfminder import settings


def sendEmail( datas):
    subject = datas['subject']
    message = datas['message']
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [datas['email']], fail_silently=False)