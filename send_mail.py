import smtplib
from email.mime.text import MIMEText

def send_mail(customer, storelocation, rating, comments):
    port = 2552
    smtp_server = 'smtp.mailtrap.io'
    login = 'c2fa9c3c33c34d'
    password = '1edd91283eec97'
    message = f"<h3>New feedback submission</h3><ul><li>Customer: {customer}</li><li>Store Location: {storelocation}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></h3>"

    sender_email = 'email@sender.com'
    receiver_email = 'email@receiver.com'
    msg =MIMEText(message, 'html')
    msg['Subject'] = 'Customer Review Feeback'
    msg['From'] = sender_email
    msg['To'] = receiver_email


    #SENDING

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
