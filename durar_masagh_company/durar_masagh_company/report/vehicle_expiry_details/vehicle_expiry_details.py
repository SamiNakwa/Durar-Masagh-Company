# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _
from datetime import datetime, timedelta


def execute(filters=None):
	columns, data = get_columns(filters=None), get_datas(filters=None)
	return columns, data

def get_columns(filters=None):

	return [
		{
			"label": _("Vehicle"),
			"fieldname": "vehicle",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": _("Branch"),
			"fieldname": "branch",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Insurance Expiry Date"),
			"fieldname": "insurance_expiry_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Insurance Description"),
			"fieldname": "insurance_description",
			"fieldtype": "data",
			"width": 280,
			"align": "center"
		},
		{
			"label": _("Battery Expiry Date"),
			"fieldname": "battery_expiry_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Battery Expiry Description"),
			"fieldname": "battery_expiry_description",
			"fieldtype": "data",
			"width": 280,
			"align": "center"
		},
		{
			"label": _("Carbon Check Expiry"),
			"fieldname": "carbon_check_expiry",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Carbon Check Description"),
			"fieldname": "carbon_check_description",
			"fieldtype": "data",
			"width": 280,
			"align": "center"
		},
		{
			"label": _("Last Vehicle Passing"),
			"fieldname": "last_vehicle_passing",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Vehicle Passing Description"),
			"fieldname": "vehicle_passing_description",
			"fieldtype": "data",
			"width": 280,
			"align": "center"
		},
		{
			"label": _("Oil Changeing Expiry "),
			"fieldname": "oil_changeing_expiry",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Oil Changeing Description"),
			"fieldname": "oil_changeing_description",
			"fieldtype": "data",
			"width": 280,
			"align": "center"
		},
	]	



def get_datas(filters=None):

	vehicle_list = frappe.db.get_all('Vehicle',fields=['*'])

	current_date = get_current_date()
	expiry_details = get_data(vehicle_list, current_date)

	data = []
	for value in expiry_details:
		temp = []
		if value[3] or value[5] or value[7] or value[9] or value[11]:
			temp.append(value[0])
			temp.append(value[1])
			temp.append(value[2])
			temp.append(value[3])
			temp.append(value[4])
			temp.append(value[5])
			temp.append(value[6])
			temp.append(value[7])
			temp.append(value[8])
			temp.append(value[9])
			temp.append(value[10])
			temp.append(value[11])

			data.append(temp)
	return data			
	# 	temp.append(key.name)
	# 	temp.append(key.end_date)

	# 	insurance_expiry = get_insurance_expiry(key, current_date)
	# 	temp.append(insurance_expiry)

	# 	temp.append(key.battery_warranty_date)

	# 	battery_expiry_date = get_battery_expiry_date(key, current_date)
	# 	temp.append(battery_expiry_date)

	# 	temp.append(key.carbon_check_date)

	# 	carbon_check_expiry = get_carbon_check(key, current_date)
	# 	temp.append(carbon_check_expiry)

	# 	temp.append(key.last_vehicle_passing)

	# 	last_vehicle = last_vehicle_passing(key, current_date)
	# 	temp.append(last_vehicle )

	# 	temp.append(key.oil_change_date)

	# 	oil_change_date = get_oil_changeing_expiry(key, current_date)
	# 	temp.append(oil_change_date)

	# 	data.append(temp)
	
	# return data


def get_insurance_expiry(key, current_date):
	
	if key.end_date != None:		
		date2 = key.end_date
		days_difference = (date2 - current_date).days

		if days_difference > 0 and days_difference > 15:
			return None
		elif days_difference < 0:
			msg = f"The Insurance Expired {abs(days_difference)} Days Ago"
					
			return msg
		else:
			msg = f"The Insurance will Expire In {days_difference} Days"
			return msg
	else:
		return None
	

def get_battery_expiry_date(key, current_date):

	if key.battery_warranty_date:
		date2 = key.battery_warranty_date
		days_difference = (date2 - current_date).days

		if days_difference > 0 and days_difference > 15:
			return None
		elif days_difference < 0:
			return (f"The Battery Expired {abs(days_difference)} Days Ago")
		else:
			return (f"The Battery will Expire In {days_difference} Days")
	else:
		return None
	
	
def get_carbon_check(key, current_date):

	if key.carbon_check_date:
		carbon_ckeck = key.carbon_check_date + timedelta(days=180)
		days_difference = (carbon_ckeck - current_date).days

		if days_difference > 0 and days_difference > 15:
			return None
		elif days_difference < 0:
			return (f"The Carbon Expired {abs(days_difference)} Days Ago")
		else:
			return (f"The Carbon will Expire In {days_difference} Days")
	else:
		return None	
	
	
def last_vehicle_passing(key, current_date):

	if key.last_vehicle_passing != None:
		last_vehicle_passing = key.last_vehicle_passing + timedelta(days=90)
		days_difference = (last_vehicle_passing - current_date).days

		if days_difference > 0 and days_difference > 15:
			return None
		elif days_difference < 0:
			return (f"The Vehicle Passing Expired {abs(days_difference)} Days Ago")
		else:
			return (f"The Vehicle Passing will Expire In {days_difference} Days")
	else:
		return None	
	
	
def get_oil_changeing_expiry(key, current_date):

	if key.oil_change_date != None:	
		oil_change_date = key.oil_change_date + timedelta(days=90)
		days_difference = (oil_change_date - current_date).days

		if days_difference > 0 and days_difference > 15:
			return None
		elif days_difference < 0:
			return (f"The Oil Expired {abs(days_difference)} Days Ago")
		else:
			return (f"The Oil will Expire In {days_difference} Days")
	else:
		return None	
	
	
def get_current_date():

	date = datetime.now()
	today_date = date.date()
	return today_date


def get_data(vehicle_list, current_date):

	datas = []
	for key in vehicle_list:
		temp = []
		temp.append(key.name)
		temp.append(key.branch)
		temp.append(key.end_date)

		insurance_expiry = get_insurance_expiry(key, current_date)
		temp.append(insurance_expiry)

		temp.append(key.battery_warranty_date)

		battery_expiry_date = get_battery_expiry_date(key, current_date)
		temp.append(battery_expiry_date)

		temp.append(key.carbon_check_date)

		carbon_check_expiry = get_carbon_check(key, current_date)
		temp.append(carbon_check_expiry)

		temp.append(key.last_vehicle_passing)

		last_vehicle = last_vehicle_passing(key, current_date)
		temp.append(last_vehicle )

		temp.append(key.oil_change_date)

		oil_change_date = get_oil_changeing_expiry(key, current_date)
		temp.append(oil_change_date)

		datas.append(temp)

	return datas

	

	

		



		




