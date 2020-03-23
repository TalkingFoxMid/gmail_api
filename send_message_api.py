import base64
from base64 import urlsafe_b64encode
from email import encoders
from email.mime.application import MIMEApplication
import re
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from data_attachment import get_data_from_attachment


def create_messageK(sender, to, subject, message_text):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message.attach(MIMEText("HOLLAHOLLA", "plain"))
    fp = open("/home/talkingfox/Downloads/alggeom01.pdf", 'rb')
    attach = (MIMEApplication(fp.read(), 'pdf'))
    attach.add_header('Content-Disposition', 'attachment', filename="rowbow")
    message.attach(attach)
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
        'raw': raw_message.decode("utf-8")
    }


def create_message(message_to_copy, sender, to, subject, message_text, service):
    """Create a message for an email.
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.
    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    # message.attach(MIMEText(message_text, "plain"))
    for i in message_to_copy.attachments:
        mime_type = i.mime_type.split("/")
        if mime_type[0] in ["multipart"] or i.part_id == '0':
            continue
        print(i.part_id)
        if i.data == None:
            data = get_data_from_attachment(i.attachment_id, i.message_id, service)
        else:
            data = i.data
        attach = (MIMEBase(mime_type[0], mime_type[1]))
        attach.set_payload(base64.urlsafe_b64decode(data))
        encoders.encode_base64(attach)
        print(data)
        # attach = MIMEAudio(base64.urlsafe_b64decode(data), 'mp3')
        if(i.data == None):
            attach.add_header('Content-Disposition', 'attachment', filename=i.name[0])
        message.attach(attach)
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
        'raw': raw_message.decode("utf-8")
    }


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
        message = (service.users().messages().send(userId="me", body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    # except errors.HttpError, error:
    except:
        print('An error occurred: %s')


def send_message_brief(to, msg, service):
    raw_msg = create_message(msg, "knmatmeh@gmail.com", to, msg.subject, msg.text, service)
    send_message(service, "me", raw_msg)
