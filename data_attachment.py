def get_data_from_attachment(id, message_id, service):
    return service.users().messages().attachments().get(id=id,userId="me",messageId=message_id).execute()["data"]
