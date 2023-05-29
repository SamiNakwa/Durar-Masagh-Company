import frappe
from erpnext.hr.doctype.vehicle.vehicle import Vehicle


class CustomVehicle(Vehicle):
    
    @frappe.whitelist()
    def get_arabitra_data(self):
        arabitra = frappe.get_last_doc('Vehicle Arabitra Logs', filters={"vehicle": self.name})
        return arabitra.as_dict()