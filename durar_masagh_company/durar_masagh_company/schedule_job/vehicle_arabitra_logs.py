import frappe
import requests
# from frappe.utils.data import get_datetime

def get_arabitra_data():
    doc = frappe.get_doc('Fleet Management API')
    response = requests.get(doc.arabitra_url)

    if response.status_code == 200:
        vehicle_data = response.json().get('data')
        create_vehicle(vehicle_data)
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

            new_doc.insert()

def create_vehicle(vehicle_data):
    for data in vehicle_data:
        new_doc = frappe.new_doc("Vehicle")
        new_doc.license_plate = data.get('vehicleNo')
        new_doc.make = "TATA"
        new_doc.model = "Dost+"
        new_doc.last_odometer = int(eval(data.get('distance')))
        new_doc.uom = "Litre"
        new_doc.insert()
