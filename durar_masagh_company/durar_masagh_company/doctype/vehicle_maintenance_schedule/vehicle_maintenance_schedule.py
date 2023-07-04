# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address
from frappe.utils.data import get_datetime, getdate
from datetime import datetime
from durar_masagh_company.whatsapp import send_whatsapp_message, get_only_number


class VehicleMaintenanceSchedule(Document):
		
	def submit(self):
		if self.docstatus == 0:
			self.docstatus = 1
		self.insurance_date_checking()

		if self.carbon_check or self.vehicle_passing or self.insurance_renewal:
			self.update_vehicle_regulatory_data()
		
		self.validate_vehicle_details_and_update()
		self.save()
		
	
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


	def validate_vehicle_details_and_update(self):
		global vehicle_doc
		vehicle_doc = frappe.get_doc('Vehicle', self.vehicle)

		vms_date = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
		vms_date = vms_date.date()

		# Check Is Tyre Changed
		if self.is_tyre_changed:
			for tyre in vehicle_doc.tyre:
				for service in self.maintenance_details:
					if tyre.tyre_position == service.product_or_service:
						tyre.last_changed_date = vms_date
						tyre.odo_meter = vehicle_doc.last_odometer
		
		# Insurance Renewal
		if self.insurance_renewal:
			if getdate(self.start_date) < getdate(self.end_date):
				vehicle_doc.start_date = self.start_date
				vehicle_doc.end_date = self.end_date
			else:
				frappe.throw('Insurance Renewal Start Date Should Not Be Greater Than End Date')

		# Carbon Check
		if self.carbon_check:
			vehicle_doc.carbon_check_date = vms_date
		
		# Vehicle Passing
		if self.vehicle_passing:
			self.last_vehicle_passing = vms_date

		# check Batery is Changed
		if self.is_battery_changed:
			vehicle_doc.battery_date = vms_date
			vehicle_doc.battery_warranty_date = self.battery_warranty_date
		
		vehicle_doc.save()
	
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
		self.send_vms_status_whatsapp_message()
		# doc = self.as_dict()
		# email_template = frappe.get_doc("Email Template", "Vehicle Maintenance Schedule Notification")
		# doc['site_url'] = frappe.utils.get_url() + f"/app/vehicle-maintenance-schedule/{self.name}"
		# message = frappe.render_template(email_template.response, doc)
		# recipients = frappe.get_all("Has Role", filters={"role":("in", ['Fleet Manager', 'Fleet User'])}, pluck='parent')
		# recipients = list(set([email for email in recipients if validate_email_address(email, throw=False)]))
		# try:
		# 	frappe.sendmail(
		# 		recipients= recipients,
		# 		subject=email_template.subject + f" | {self.vehicle}",
		# 		message=message,
		# 	)
		# except Exception as ex:
		# 	frappe.msgprint(f"Please contact Administrator or Check 'Email Account' settings \n {ex}")


	def send_vms_status_whatsapp_message(self):
		whatsapp_message = frappe.get_doc('Whatsapp Message', 'VMS - Status Notification')
		if self.workflow_state in ['Scheduled', 'Completed', 'Cancelled']:
			# CEO Number
			user_list = frappe.get_all("Has Role", filters={"role":("in", ['CEO'])}, pluck='parent')
			numbers = frappe.db.get_list('User', pluck='mobile_no', filters={
											'name': ['in', user_list]
										})
			# Driver Number
			user = frappe.db.get_value('Employee', self.employee, 'user_id')
			user_number = frappe.db.get_value('User', user, 'mobile_no')

			numbers.append(user_number)
	
		else:
			# Fleet Manager
			user_list = frappe.get_all("Has Role", filters={"role":("in", ['Fleet Manager'])}, pluck='parent')
			numbers = frappe.db.get_list('User', pluck='mobile_no', filters={
											'name': ['in', user_list]
										})
			
		numbers = get_only_number(numbers)
		doc_dict = self.as_dict()
		doc_dict['doc_url'] = frappe.utils.get_url() + self.get_url()
		body = whatsapp_message.message.format(**doc_dict)
		send_whatsapp_message(to=numbers, body=body)