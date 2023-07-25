# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from durar_masagh_company.whatsapp import send_whatsapp_message

class WhatsappMessage(Document):
	
	def on_trash(self):
		
		if self.is_standard:
			frappe.throw("You Can't Delete This Message")


@frappe.whitelist()
def sent_test_whatsapp_message(number=None, message=None):
	try:
		send_whatsapp_message(to=[number], body=message)
		return True
	except:
		return False