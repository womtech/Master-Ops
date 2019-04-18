import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailHandler:

	def EmailSender( RECIPIENT, SUBJECT, MSG ):

		SENDER = 'info@mymangoapp.com'
		SENDERNAME = 'My Mango App'
		USERNAME_SMTP = "AKIAIG73GCVAG36FF7WQ"
		PASSWORD_SMTP = "AonUFA0FYO7Cx2PNuc8LQ79gd0F7npISHeAVuF2R+gWi"
		HOST = "email-smtp.us-west-2.amazonaws.com"
		PORT = 587
		#SUBJECT = 'Important - New Update Is Available Of My Mango App'
		#BODY_TEXT = getNonHTMLBody()
		#BODY_HTML = getHTMLBody()
		MSG = MIMEMultipart('alternative')
		MSG['Subject'] = SUBJECT
		MSG['From'] = email.utils.formataddr((SENDERNAME, SENDER))
		MSG['To'] = RECIPIENT

		#part1 = MIMEText(BODY_TEXT, 'plain')
		#part2 = MIMEText(BODY_HTML, 'html')

		#MSG.attach(part1)
		#MSG.attach(part2)

	# Try to send the message.
		try:
			server = smtplib.SMTP(HOST, PORT)
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login(USERNAME_SMTP, PASSWORD_SMTP)
			server.sendmail(SENDER, RECIPIENT, MSG.as_string())
			server.close()
		except Exception as e:
			return False
		else:
			return True

