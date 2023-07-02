from erpnext.stock.doctype.delivery_trip.delivery_trip import DeliveryTrip
import frappe
from durar_masagh_company.whatsapp import send_whatsapp_message, get_only_number

# is_doc_new = False
class CustomDeliveryTrip(DeliveryTrip):

    def before_submit(self):
        self.validate_delivery_trip()


    def validate_delivery_trip(self):
        if self.delivery_status == 'Not Delivered':
             frappe.throw("You Can't Submit The Form Before Deliver")
    

    def before_save(self):
        self.send_whatsapp_message_to_driver()
    

    def send_whatsapp_message_to_driver(self):
        try:
            is_local = getattr(self, '__islocal')
            if is_local:
                if self.employee:
                    whatsapp_message = frappe.get_doc('Whatsapp Message', 'Delivery Trip - Assign To Driver Notification')
                    user = frappe.db.get_value('Employee', self.employee, 'user_id')
                    numbers = [frappe.db.get_value('User', user, 'mobile_no')]
                    numbers = get_only_number(numbers)
                    doc_dict = self.as_dict()
                    doc_dict['doc_url'] = frappe.utils.get_url() + self.get_url()
                    body = whatsapp_message.message.format(**doc_dict)
                    send_whatsapp_message(to=numbers, body=body)
                    frappe.msgprint('Whatsapp Notification Send To The Driver')
                else:
                    frappe.msgprint("Employee Not Mapped To The Driver So We Can't Send Notification")

                
        except AttributeError as ex:
            frappe.log_error(str(ex), 'Delivery Trip - Driver Notification | Not A Critical Issue')

    @frappe.whitelist()
    def get_driver_details(self):
        if self.driver:
            doc = frappe.get_doc('Driver', self.driver)
            return doc
        return {}


    @frappe.whitelist()
    def sent_delivery_status_update_message(self):
        whatsapp_message = frappe.get_doc('Whatsapp Message', 'Delivery Trip Driver Status Update Notification')

        user_list = frappe.get_all("Has Role", filters={"role":("in", ['Fleet Manager'])}, pluck='parent')
        numbers = frappe.db.get_list('User', pluck='mobile_no', filters={
                                        'name': ['in', user_list]
                                    })
        numbers = get_only_number(numbers)
        doc_dict = self.as_dict()
        doc_dict['doc_url'] = frappe.utils.get_url() + self.get_url()
        body = whatsapp_message.message.format(**doc_dict)

        send_whatsapp_message(to=numbers, body=body)

        