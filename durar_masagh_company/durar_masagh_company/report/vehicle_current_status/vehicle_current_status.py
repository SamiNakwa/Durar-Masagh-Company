# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
import requests
import numpy as np
from frappe import _
import copy
from datetime import datetime, timedelta
import json


def execute(filters=None):
	columns, data = get_columns(filters=filters), get_datas(filters=filters)
	return columns, data


def get_columns(filters=None):
	
	return [
		_("Vehicle") + ":Link/Vehicle:100",
		_("Ignition") + ":Check:50",
		_("Speed") + ":Data:100",
		_("Distance") + ":Int:100",
        _("Latitude") + ":Data:100",
        _("Longitude") + ":Data:100",
        _("Track Date Time") + ":Data:100",
        _("Expiry Date") + ":Date:100",
        _("Weight") + ":Int:100",
		_("Location") + ":Data:250",
		_("Active")+ ":Int:10",
		_("In-Active")+ ":Int:10"
	]


def get_datas(filters=None):

	# query_filter = get_query_filter(filters=None)

	try:
		doc = frappe.get_doc('Fleet Management API')
		response = requests.get(doc.arabitra_url)
	except Exception as ex:
		frappe.log_error(message=str(ex), title="Arabitra API schedule job - In Report (Vehicle Current Status)")
		frappe.msgprint("<b>Arabitra API</b> is not working please check the Arabitra or please check sometime later")
		return [[]]
	
	if response.status_code == 200 and response.json().get('data'):
		vehicle_data = response.json().get('data')
		structured_data = []
		temp = []
		for vehicle in vehicle_data:
			temp.append(vehicle.get('vehicleNo'))
			temp.append(int(vehicle.get('ignition', 0)))
			temp.append(float(vehicle.get('speed', 0)))
			temp.append(float(vehicle.get('distance', 0)))
			temp.append(vehicle.get('latitude'))
			temp.append(vehicle.get('longitude'))
			temp.append(vehicle.get('TrackDateTime'))
			temp.append(vehicle.get('expiryDate'))
			temp.append(vehicle.get('weight', 0))
			temp.append(vehicle.get('location'))
			if int(vehicle.get('ignition', 0)):
				temp.append(1)
				temp.append(0)
			else:
				temp.append(0)
				temp.append(1)

			structured_data.append(temp)
			temp = []
	else:
		frappe.msgprint("Arabitra return no value ")
		return [[]]
	
	
	vechicle_array = np.array(structured_data)
	vechicle_array_T = vechicle_array.T
	vehicle_name = vechicle_array_T[0]
	vechicle_array_ignition = vechicle_array_T[1]
	

	if filters.get('vehicle'):
		return vechicle_array[(vehicle_name==filters.get('vehicle'))].tolist()


	if filters.get('ignition') == 'All':
		return structured_data
	elif filters.get('ignition') == 'Yes':
		return vechicle_array[(vechicle_array_ignition==1)].tolist()
	elif filters.get('ignition') == 'No':
		return vechicle_array[(vechicle_array_ignition==0)].tolist()
	else:
		frappe.throw(f"Hi Mr {frappe.session.user}, Please select any one filter")


