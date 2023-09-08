# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeTaskManagement(Document):
	
	@frappe.whitelist()
	def get_current_employee(self):
		user = frappe.session.user

		data = frappe.db.get_value('Employee', {'user_id':user}, 'name')

		if data:
			return {'employee': data}
		else:
			return False