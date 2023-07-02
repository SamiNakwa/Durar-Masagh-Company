# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WhatsappMessage(Document):
	
	def on_trash(self):
		
		if self.is_standard:
			frappe.throw("You Can't Delete This Message")
