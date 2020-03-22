def get_message_info(id, service):
    '''
    Возвращает следующего рода объект:
    {
      "id": string,
      "threadId": string,
      "labelIds": [
        string
      ],
      "snippet": string,
      "historyId": unsigned long,
      "internalDate": long,
      "payload": {
        "partId": string,
        "mimeType": string,
        "filename": string,
        "headers": [
          {
            "name": string,
            "value": string
          }
        ],
        "body": users.messages.attachments Resource,
        "parts": [
          (MessagePart)
        ]
      },
      "sizeEstimate": integer,
      "raw": bytes
    }'''
    return service.users().messages().get(userId="me", id=id).execute()