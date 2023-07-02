from erpnext.stock.doctype.delivery_trip.delivery_trip import DeliveryTrip
import frappe
from durar_masagh_company.whatsapp import send_whatsapp_message, get_only_number

class CustomDeliveryTrip(DeliveryTrip):

    def before_submit(self):
        self.validate_delivery_trip()


    def validate_delivery_trip(self):
        if self.delivery_status == 'Not Delivered':
             frappe.throw("You Can't Submit The Form Before Deliver")
    


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

        