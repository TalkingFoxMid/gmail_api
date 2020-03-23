from get_message_info import get_message_info
import re
class Attachment:
    def __init__(self, attachment,id):
        self.text = attachment
        self.message_id = id
        self.part_id = attachment['partId']
        self.name = re.findall('name="(.+?)"',attachment["headers"][0]["value"])
        self.mime_type = attachment["mimeType"]
        print(attachment["body"])
        if "attachmentId" in attachment["body"]:
            self.attachment_id = attachment["body"]["attachmentId"]
        else:
            self.attachment_id = None
            print(self.mime_type)
        print(attachment)



class Message:
    def __init__(self, id, service):
        message_info = get_message_info(id, service)
        self.subject = re.findall("'name': 'Subject', 'value': '(.+?)'",str(message_info))[0]
        self.id = id
        self.text = message_info["snippet"]
        if "parts" in message_info["payload"]:
            self.attachments = [Attachment(i, id) for i in message_info["payload"]["parts"]]
        else:
            self.attachments = []

def get_new_messages(historyId, service):
    '''Возвращает пару: массив входящих сообщений и historyId,
    начиная с которого будут приходить новые события'''

    response = service.users().history().list(userId="me", startHistoryId=historyId).execute()
    if "history" in response:
        events = response["history"]
    else:
        events = []
    new_messages = [event["messagesAdded"][0]['message'] for event in events if "messagesAdded" in event]
    inbox_unread_messages = [Message(msg["id"], service) for msg in new_messages if "INBOX" in msg["labelIds"]]
    return (inbox_unread_messages, response["historyId"])
