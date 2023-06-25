# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address
from frappe.utils.data import get_datetime


class VehicleMaintenanceSchedule(Document):
		
	def submit(self):
		if self.docstatus == 0:
			self.docstatus = 1
		self.insurance_date_checking()

		if self.carbon_check or self.vehicle_passing or self.insurance_renewal:
			self.update_vehicle_regulatory_data()
		self.save()

		self.validate_is_tyre_changed()
	
	def after_insert(self):
		if self.docstatus == 0:
			self.vehicle_maintenance_notifcation()

	def insurance_date_checking(self):
		if self.insurance_renewal:
			if not bool(self.start_date) or not bool(self.end_date):
				frappe.throw("Make sure you filled <b>Start Date</b> and <b>End Date</b>\nif not please provide respective date")

	def update_vehicle_regulatory_data(self):
		vehicle = frappe.get_doc('Vehicle', self.vehicle)
		if self.carbon_check:
			vehicle.carbon_check_date = get_datetime(self.date).date()
		if self.vehicle_passing:
			vehicle.last_vehicle_passing = get_datetime(self.date).date()
		if self.insurance_renewal:
			vehicle.start_date = self.start_date
			vehicle.end_date = self.end_date
		vehicle.save()


	def validate_is_tyre_changed(self):
		
		if self.is_tyre_changed:
			pass
	
	
	@frappe.whitelist()
	def get_vehicle_details(self):
		tyre = frappe.db.get_list('Vehicle Tyre Details',
									filters={
										'parent': self.vehicle,
										'parenttype': 'Vehicle'
									},
									pluck='tyre_position'
								)
		service = frappe.get_list(
					'Vehicle Service Type',
					filters={
						'is_tyre':0
					},
					pluck='name'
				)

		data = {
			'tyre': tyre,
			'service': service
		}

		return data

	@frappe.whitelist()
	def vehicle_maintenance_notifcation(self, throw_if_missing=False):
		doc = self.as_dict()
		email_template = frappe.get_doc("Email Template", "Vehicle Maintenance Schedule Notification")
		doc['site_url'] = frappe.utils.get_url() + f"/app/vehicle-maintenance-schedule/{self.name}"
		message = frappe.render_template(email_template.response, doc)
		recipients = frappe.get_all("Has Role", filters={"role":("in", ['Fleet Manager', 'Fleet User'])}, pluck='parent')
		recipients = list(set([email for email in recipients if validate_email_address(email, throw=False)]))
		try:
			frappe.sendmail(
				recipients= recipients,
				subject=email_template.subject + f" | {self.vehicle}",
				message=message,
			)
		except Exception as ex:
			frappe.msgprint(f"Please contact Administrator or Check 'Email Account' settings \n {ex}")


		