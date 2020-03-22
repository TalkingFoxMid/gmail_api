from get_message_info import get_message_info


class Message:
    def __init__(self, id, service):
        message_info = get_message_info(id, service)
        self.id = id
        self.text = message_info["snippet"]

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
