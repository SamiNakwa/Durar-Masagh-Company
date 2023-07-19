# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VehicleServiceType(Document):
	
	def validate(self):
		# self.check_dupliate_check_box_entry()
		pass

	
	def check_dupliate_check_box_entry(self):

		checkbox = [self.is_tyre, self.is_battery]

		if checkbox.count(1) > 1:
			frappe.throw('You Should Check Only One Service Type', 'Dublicate Checkbox Entry')



