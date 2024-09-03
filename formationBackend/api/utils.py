#utils
import re
import os
import dns.resolver
import smtplib
import logging
import environ
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from email.mime.image import MIMEImage

env = environ.Env()
environ.Env.read_env()

User = get_user_model()

def validate_email(email):
    if not validate_email_format(email):
        return False, "Invalid email format"
    
    domain = extract_domain(email)
    if not check_mx_records(domain):
        return False, "No MX records found for the domain"
    
    if not smtp_check(email):
        return False, "SMTP check failed; the email address may not exist"
    
    return True, "Email address is valid"

def send_verification_email(user):
    from_email = "allouchhatim@gmail.com"
    from_email_password = env('APP_SMTP_SERVE')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_link = f"{settings.SITE_URL}{reverse('verify_email', kwargs={'uidb64': uid, 'token': token})}"
    
    subject = "Vérification de l'email"
    body = f"""
    <p>Bonjour {user.first_name},</p>
    <p>Merci de vous être inscrit chez nous. Veuillez vérifier votre adresse e-mail en cliquant sur le bouton ci-dessous :</p>
    <p><a href="{verification_link}" style="
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: #ffffff;
        background-color: #007bff;
        text-decoration: none;
        border-radius: 5px;
    ">Vérifier l'email</a></p>
    <p>Si vous n'avez pas créé ce compte, veuillez ignorer cet e-mail.</p>
    <br>
    <p>Cordialement,</p>
    <p>Nom de votre entreprise</p>
    <img src="cid:footer_image" alt="Pied de page">
    """

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = user.email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Joindre l'image du pied de page
    image_path = os.path.join(settings.MEDIA_ROOT, 'footermail.png')
    with open(image_path, 'rb') as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-ID', '<footer_image>')
        msg.attach(img)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Activer la sortie de débogage
        server.starttls()
        server.login(from_email, from_email_password)
        text = msg.as_string()
        server.sendmail(from_email, user.email, text)
        server.quit()
        return True, "E-mail de vérification envoyé avec succès"
    except Exception as e:
        logging.error(f"Échec de l'envoi de l'e-mail de vérification : {e}")
        return False, str(e)
    return True, "E-mail de vérification envoyé avec succès"


def validate_email_format(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def extract_domain(email):
    return email.split('@')[1]

def check_mx_records(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.NXDOMAIN:
        return False
    except dns.exception.DNSException:
        return False

def smtp_check(email):
    from_email = "allouchhatim@gmail.com"
    from_email_password = env('APP_SMTP_SERVE')
    domain = extract_domain(email)
    
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        # mail_server = str(mx_records[0].exchange)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.starttls()
        server.login(from_email, from_email_password)
        server.mail(from_email)
        code, message = server.rcpt(email)
        server.quit()
        
        return code == 250
    except smtplib.SMTPConnectError as e:
        logging.error(f"SMTP connection error: {e}")
        return False
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"SMTP authentication error: {e}")
        return False
    except Exception as e:
        logging.error(f"SMTP error: {e}")
        return False

def send_password_reset_email(user):
    from_email = "allouchhatim@gmail.com"
    from_email_password = env('APP_SMTP_SERVE')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"http://localhost:3000/reset-password-confirm/{uid}/{token}"
    
    subject = "Réinitialisation du mot de passe"
    body = f"""
    <p>Bonjour {user.first_name},</p>
    <p>Vous avez demandé la réinitialisation de votre mot de passe. Veuillez cliquer sur le bouton ci-dessous pour réinitialiser votre mot de passe :</p>
    <p><a href="{reset_link}" style="
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: #ffffff;
        background-color: #007bff;
        text-decoration: none;
        border-radius: 5px;
    ">Réinitialiser le mot de passe</a></p>
    <p>Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet e-mail.</p>
    <br>
    <p>Cordialement,</p>
    <p>Nom de votre entreprise</p>
    <img src="cid:footer_image" alt="Pied de page">
    """

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = user.email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Joindre l'image du pied de page
    image_path = os.path.join(settings.MEDIA_ROOT, 'footermail.png')
    with open(image_path, 'rb') as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-ID', '<footer_image>')
        msg.attach(img)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Activer la sortie de débogage
        server.starttls()
        server.login(from_email, from_email_password)
        text = msg.as_string()
        server.sendmail(from_email, user.email, text)
        server.quit()
        return True, "E-mail de réinitialisation du mot de passe envoyé avec succès"
    except Exception as e:
        logging.error(f"Échec de l'envoi de l'e-mail de réinitialisation du mot de passe : {e}")
        return False, str(e)
