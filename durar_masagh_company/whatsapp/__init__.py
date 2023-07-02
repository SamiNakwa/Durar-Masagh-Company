import frappe
from twilio.rest import Client
from twilio.base import values


def send_whatsapp_message(to:list=None, body:str='No Message', media_url=values.unset):
    
    try:
        twilio = frappe.get_doc('Twilio Settings')
        account_sid = twilio.account_sid
        auth_token = twilio.auth_token
        from_ = twilio.whatsapp_number

        if twilio.is_active:
            client = Client(account_sid, auth_token)
            
            if to:
                for num in to:
                    try:
                        client.messages.create(
                                    from_=f'whatsapp:{from_}',
                                    body=body,
                                    to=f'whatsapp:{num}',
                                    media_url=media_url
                                )
                    except Exception as ex:
                        frappe.log_error(str(ex), "Whatsapp error")
                        continue
        else:
            frappe.log_error("Whatsapp is not active ", "Twilio Inactive")
    except Exception as ex:
        frappe.log_error(str(ex), "Whatsapp error")


def get_only_number(numbers):
    
    return [num for num in numbers if num is not None]