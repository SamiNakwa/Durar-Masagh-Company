import frappe
import requests
from frappe.utils import add_days, getdate, now, get_datetime
import time
from frappe.utils import datetime
import numpy as np
from durar_masagh_company.durar_masagh_company.overrides.vehicle import get_coordinates_list
import json
from datetime import timedelta

def get_arabitra_data():
    try:
        doc = frappe.get_doc('Fleet Management API')
        response = requests.get(doc.arabitra_url)

        if response.status_code == 200:
            vehicle_data = response.json().get('data')
            # create_vehicle(vehicle_data)
            for data in vehicle_data:
                new_doc = frappe.new_doc("Vehicle Arabitra Logs")
                new_doc.vehicle = data.get('vehicleNo')
                new_doc.latitude = data.get('latitude')
                new_doc.longitude = data.get('longitude')
                new_doc.track_date_time = data.get('TrackDateTime')
                new_doc.location = data.get('location')
                new_doc.ignition = int(data.get('ignition'))
                new_doc.distance = float(data.get('distance'))
                new_doc.expiry_date = data.get('expiryDate')
                new_doc.weight = data.get('weight')
                new_doc.speed = float(data.get('speed'))
                try:
                    new_doc.insert()
                except Exception as ex:
                    frappe.log_error(str(ex), 'Arabitra API Vehicle Not Found')
                    # create_vehicle(data)

    except Exception as ex:
        frappe.log_error(message=str(ex), title="Arabitra API schedule job")

def create_vehicle(data):
    new_doc = frappe.new_doc("Vehicle")
    new_doc.license_plate = data.get('vehicleNo')
    new_doc.make = "TATA"
    new_doc.model = "Dost+"
    new_doc.last_odometer = float(data.get('distance'))
    new_doc.uom = "Litre"
    new_doc.tyre_durability = 2000

    new_doc.insert()


def update_vehicle_logs():
    '''
    This cron triggers daily at 00:00:00 so we have to take the yesterday date data and update
    '''
    try:
        yesterday = add_days(getdate(), -1)
        start_date = datetime.datetime.combine(yesterday, datetime.datetime.min.time())
        end_date = datetime.datetime.combine(yesterday, datetime.datetime.max.time())

        filters = {
                "creation": ["between", [start_date, end_date]]
            }
        keys = ['vehicle', 'latitude', 'longitude', 'track_date_time', 'distance']
        arabitra_logs = frappe.db.get_list(
                'Vehicle Arabitra Logs',
                fields=keys,
                filters=filters,
                as_list=True
            )
        
        location_data = frappe.db.get_list(
            'Location',
            filters={
                'date': ['=', yesterday]
            },
            pluck='name'
        )

        arabitra_logs = np.array(arabitra_logs)
        arabitra_logs_T = arabitra_logs.T
        vehicles = arabitra_logs_T[0]

        for vehicle in list(set(vehicles)):
            currect_vehicle_logs = arabitra_logs[vehicles==vehicle]
            currect_vehicle_logs = [dict(zip(keys, vals)) for vals in currect_vehicle_logs]
            if currect_vehicle_logs:
                create_location_tracker(vehicle, yesterday, currect_vehicle_logs, location_data)
                vehicle_logs_update(currect_vehicle_logs[0], yesterday)
            else:
                continue
    except IndexError as ex:
        frappe.log_error(str(frappe.get_traceback()), "Vehicle Update Daily Task - Insuficient Data")
    except Exception:
        frappe.log_error(str(frappe.get_traceback()), "Vehicle Logs Update - Critical Error")

def create_location_tracker(vehicle, yesterday, currect_vehicle_logs, location_data):
    try:
        name = str(yesterday) + ' ' + vehicle
        if name in location_data:
            doc = frappe.get_doc('Location', name)
            # doc.location = frappe.as_json(get_coordinates_list(currect_vehicle_logs))
            doc.location = json.dumps(get_coordinates_list(currect_vehicle_logs), separators=(',', ':'))
            doc.save()
        else:
            if currect_vehicle_logs:
                latest_log = currect_vehicle_logs[0]
                doc = frappe.new_doc('Location')
                doc.location_name = name
                doc.latitude = latest_log.get('latitude')
                doc.longitude = latest_log.get('longitude')
                doc.vehicle = vehicle
                doc.date = yesterday
                # doc.location = frappe.as_json(get_coordinates_list(currect_vehicle_logs))
                doc.location = json.dumps(get_coordinates_list(currect_vehicle_logs), separators=(',', ':'))
                doc.insert()
    except Exception as ex:
        frappe.log_error(message=str(ex), title="Location update daily scheduler")

def vehicle_logs_update(vehicle, date):
    try:
        vehicle_doc = frappe.get_doc('Vehicle', vehicle.get('vehicle'))
        doc = frappe.new_doc('Vehicle Log')
        doc.license_plate = vehicle_doc.license_plate
        doc.employee = vehicle_doc.employee
        doc.model = vehicle_doc.model
        doc.make = vehicle_doc.make
        doc.date = date
        doc.odometer = vehicle.get('distance')
        doc.last_odometer = vehicle_doc.last_odometer

        doc.insert()
        doc.submit()

    except Exception as ex:
        frappe.log_error(message=str(ex), title="Vehicle logs update daily scheduler")


def remove_unwanted_data():
    today = getdate()
    doc = frappe.get_doc("Fleet Management API")
    n_date_before = get_datetime(today) - timedelta(days=doc.data_duration)
    try:
        frappe.db.delete('Vehicle Arabitra Logs', {
            'track_date_time':["<", str(n_date_before)]
        })
    except Exception as ex:
        frappe.log_error(message=str(ex), title="Vehicle logs - Remove Unwanted Data")

   
