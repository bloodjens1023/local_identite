import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def envoie_email(destinataire, sujet, corp):
    # Paramètres Gmail
    email_sender = 'bloodjens32@gmail.com'
    email_receiver = destinataire

    # Création du message
    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = sujet

    # Corps du message
    body = corp
    message.attach(MIMEText(body, 'html'))

    # Connexion au serveur SMTP de Gmail
    server = smtplib.SMTP('live.smtp.mailtrap.io', 587)
    server.starttls()
    server.login("api", "f7f08a46eabb0d519d2a23fafb01149b")

    # Envoi de l'e-mail
    text = message.as_string()
    server.sendmail(email_sender, email_receiver, text)
    print("sms envoyer")
    # Fermeture de la connexion
    server.quit()
    
    
envoie_email("hasiniainafanomezantsoa32@gmail.com","test","tay be miboretaka")