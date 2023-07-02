
import frappe
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote
from frappe.utils import datetime, validate_email_address
from durar_masagh_company.whatsapp import send_whatsapp_message, get_only_number

class CustomDeliveryNote(DeliveryNote):

    def on_submit(self):
        # self.notify_driver_and_manager()
        self.send_message_to_wharehouse_manager()

    def notify_driver_and_manager(self):

        url = frappe.utils.get_url() + f"/app/delivery-note/{self.name}"

        email_template = frappe.get_doc("Email Template", "Delivery Note Submit Notification")
        message = frappe.render_template(email_template.response, {'name':self.name, 'url':url})

        recipients = frappe.get_all("Has Role", filters={"role":("in", ['Stock Manager'])}, pluck='parent')
        recipients = list(set([email for email in recipients if validate_email_address(email, throw=False)]))
        try:
            frappe.sendmail(
                recipients= recipients,
                subject='Delivery Trip Notification',
                message=message,
            )
        except Exception as ex:
            frappe.msgprint(f"Please contact Administrator or Check 'Email Account' settings \n {ex}")

    
    def send_message_to_wharehouse_manager(self):
        
        whatsapp_message = frappe.get_doc('Whatsapp Message', 'Delivery Note Notification To WhareHouse Manager')

        user_list = frappe.get_all("Has Role", filters={"role":("in", ['Warehouse Manager'])}, pluck='parent')
        numbers = frappe.db.get_list('User', pluck='mobile_no', filters={
                                        'name': ['in', user_list]
                                    })
        
        numbers = get_only_number(numbers)
        doc_dict = self.as_dict()
        doc_dict['doc_url'] = frappe.utils.get_url() + self.get_url()

        body = whatsapp_message.message.format(**doc_dict)

        send_whatsapp_message(to=numbers, body=body)
