# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta




def execute(filters=None):
	
	columns, data = get_columns(filters), get_datas(filters)
	return columns, data


def get_columns(filters=None):

	return [
		{
			"label": _("Vehicle No"),
			"fieldname": "vehicle_no",
			"fieldtype": "Data",
			"width": 150,
			"align":"center"
		},
		{
			"label": _("Driver Name"),
			"fieldname": "driver_name",
			"fieldtype": "Data",
			"width": 250,
			"align":"center"
		},
		{
			"label": _("Start Odometer"),
			"fieldname": "start_odometer",
			"fieldtype": "Int",
			"width": 150,
			# "align": "center"
		},
		{
			"label": _("End Odometer"),
			"fieldname": "end_odometer",
			"fieldtype": "Int",
			"width": 150,
			# "align": "center"
		},
		{
			"label": _("Distance Travelled(Kms)"),
			"fieldname": "distance_travelled",
			"fieldtype": "Int",
			"width": 200,
			# "align": "center"
		}
	]


def get_datas(filters=None):
	


	vehicle_list = frappe.db.get_all('Vehicle',fields=['license_plate', 'employee'])

	vehicle_datas = frappe.db.get_all('Vehicle Log',
								    filters=[									
									  	['date', 'between', [filters.date, filters.date]]
									],
									fields=['*'],
									)

	if not vehicle_datas:
		frappe.msgprint(f'No vehicle log data available for the selected date: {filters.date}')
	data = []
	for d in vehicle_list:
		temp = []
		temp.append(d.license_plate)

		temp.append(d.employee)
		
		if get_vehicle_log_datas(vehicle_datas, d) == None:
			end = None
			start = None
		else:
			end, start = get_vehicle_log_datas(vehicle_datas, d)
		temp.append(end)
		temp.append(start)

		distance = get_distance(start, end)
		temp.append(distance)

		data.append(temp)
		
	return data
def get_vehicle_log_datas(vehicle_datas, d):

	i = 0
	for date in vehicle_datas:
		if d.license_plate == date.license_plate:
			
			last_odometer = date.last_odometer
			start_odometer = date.odometer
			return last_odometer, start_odometer
		else:
			i += 1
	
	return None
	
		

def get_distance(start, end):

	if  start == None and end == None:
		return None
	
	else:
		distance_travelled = start - end

		return distance_travelled
		
