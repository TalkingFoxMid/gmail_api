from base64 import urlsafe_b64encode
from email.mime.text import MIMEText


def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.
    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    encoded_message = urlsafe_b64encode(message.as_bytes())
    return {'raw': encoded_message.decode()}

# https://developers.google.com/gmail/api/guides/sending
def send_message(service, user_id, message):
    """Send an email message.
    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.
    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    # except errors.HttpError, error:
    except:
        print('An error occurred: %s')
def send_message_brief(to, text, service):
    raw_msg = create_message("knmatmeh@gmail.com", to, "Рассылка", text)
    send_message(service, "me", raw_msg)