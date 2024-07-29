#utils
import re
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
    
    subject = "Email Verification"
    body = f"Please verify your email address by clicking the link below:\n\n{verification_link}"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = user.email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        server.login(from_email, from_email_password)
        text = msg.as_string()
        server.sendmail(from_email, user.email, text)
        server.quit()
        return True, "Verification email sent successfully"
    except Exception as e:
        logging.error(f"Failed to send verification email: {e}")
        return False, str(e)
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

