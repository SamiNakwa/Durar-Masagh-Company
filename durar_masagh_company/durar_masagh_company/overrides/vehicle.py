import frappe
from frappe.exceptions import DoesNotExistError
from frappe.utils import datetime
from erpnext.setup.doctype.vehicle.vehicle import Vehicle
import json

class CustomVehicle(Vehicle):

    def validate(self):
        self.tyre_dublicate_entry_validate()


    def tyre_dublicate_entry_validate(self):
        tyre_list = []
        for tyre in self.tyre:
            if tyre.tyre_position not in tyre_list:
                tyre_list.append(tyre.tyre_position)
            else:
                frappe.throw('Dublicate Entry In Tyre Details')

    @frappe.whitelist()
    def get_arabitra_data(self):
        try:
            arabitra = frappe.get_last_doc('Vehicle Arabitra Logs', filters={"vehicle": self.name})
            return arabitra.as_dict()
        except DoesNotExistError:
            return {}
    
    @frappe.whitelist()
    def sync_live_location(self):
        today = datetime.datetime.today().date()
        start_date = datetime.datetime.combine(today, datetime.datetime.min.time())
        end_date = datetime.datetime.combine(today, datetime.datetime.max.time())

        filters = {
            "vehicle": f"{self.name}",
            "creation": ["between", [start_date, end_date]]
        }

        arabitra_logs = frappe.db.get_list(
            'Vehicle Arabitra Logs',
            fields=['*'],
            filters=filters
        )

        if arabitra_logs:
            name = str(today)+ ' ' + self.name
            if not frappe.db.exists('Location', name):
                latest_log = arabitra_logs[0]
                doc = frappe.new_doc('Location')
                doc.location_name = name
                doc.latitude = latest_log.get('latitude')
                doc.longitude = latest_log.get('longitude')
                doc.vehicle = self.name
                doc.date = today
                # doc.location = frappe.as_json(get_coordinates_list(arabitra_logs))
                doc.location = json.dumps(get_coordinates_list(arabitra_logs), separators=(',', ':'))
                doc.insert()
            else:
                doc = frappe.get_doc('Location', name)
                # doc.location = frappe.as_json(get_coordinates_list(arabitra_logs))
                doc.location = json.dumps(get_coordinates_list(arabitra_logs), separators=(',', ':'))
                doc.save()

            return "Location sync successful"
        else:
            return "There is no Arabitra logs for this vehicle please check"
        

def get_coordinates_list(arabitra_logs):
    recent_log = arabitra_logs[0]
    location = {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {},
                            "geometry": {
                                "type": "LineString",
                                "coordinates": []
                            }
                        },
                        {
                            "type": "Feature",
                            "properties": {},
                            "geometry": {
                                "type": "Point",
                                "coordinates": [recent_log.get('longitude'), recent_log.get('latitude')]
                            }
                        }
                    ]
                }
    list_of_coordinates = []
    for log in arabitra_logs:
        temp = []
        temp.append(log.get('longitude'))
        temp.append(log.get('latitude'))
        list_of_coordinates.append(temp)
        temp = []
    location['features'][0]['geometry']['coordinates'] = list_of_coordinates
    return location