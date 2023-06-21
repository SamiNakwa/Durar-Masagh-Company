import frappe
import datetime
import numpy as np

def license_expairy_notification():
    '''
    License and Driver card poth expairy checking here
    '''

    # fields = ['expiry_date', 'driver_card_date', 'name', 'full_name', 'license_number', 'issuing_date']

    
    drivers = frappe.db.get_list('Driver',
                                fields=['*'],
                                filters={
                                    'status': 'Active'
                                },
                                # as_list=True
                                )

    today = datetime.date.today()
    global expairy_vehicle_dict
    expairy_vehicle_dict = {
        'driver_details': []
    }

    for driver in drivers:
        expairy_check_ = expairy_check(driver, today)
        if expairy_check_:
            expairy_vehicle_dict['driver_details'].append(expairy_check_)
    
    if expairy_vehicle_dict.get('driver_details'):
        email_template = frappe.get_doc("Email Template", "License Expairy Notification")
        message = frappe.render_template(email_template.response_html, expairy_vehicle_dict)

        frappe.sendmail(
                    recipients= 'antony15898@gmail.com',
                    subject=email_template.subject,
                    message=message,
                )

def expairy_check(driver, today):

    license_expairy = None
    card_expairy = None
    if driver.get('expiry_date'):
        days = (today - driver.get('expiry_date')).days
        if days == 15:
            license_expairy = days
        elif days == 7:
            license_expairy = days
        elif days < 7 and days >= 0:
            license_expairy = days

    if driver.get('driver_card_date'):
        days = (today - driver.get('driver_card_date')).days
        if days == 15:
            card_expairy = days
        elif days == 7:
           card_expairy = days
        elif days < 7 and days >= 0:
            card_expairy = days

    if card_expairy or license_expairy:

        driver['license_expairy'] = license_expairy
        driver['card_expairy'] = card_expairy

        return driver



    