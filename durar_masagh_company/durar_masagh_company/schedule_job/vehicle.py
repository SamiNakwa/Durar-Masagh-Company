import frappe
from frappe.utils import datetime, add_days, validate_email_address

today = datetime.datetime.today().date()

def regulatory_compliance_checking():
    
    vehicles = frappe.db.get_list('Vehicle', fields=['*'])
    
    subject_html = '''<div class="ql-editor read-mode"><p><strong>Vehicle Regulatory Compliance:</strong></p>'''
    head_html = subject_html + '''<table class="table table-bordered"><tbody><tr><td data-row="row-t3od"><strong>Vehicle</strong></td><td data-row="row-t3od"><strong>Details</strong></td></tr>'''
    is_sendable = False
    for vehicle in vehicles:
        content = ''
        insurance = insurance_checking(vehicle)
        carbon = carbon_checking(vehicle)
        vehicle_passing = vehicle_passing_checking(vehicle)
        
        if insurance or carbon or vehicle_passing:
            if insurance:
                content = f"For Insurance Renewal {insurance} "
            if carbon:
                if content:
                    content += ('& ' + f"For Carbon Testing {carbon} ")
                else:
                    content = f"For Carbon Testing {carbon} "
            if vehicle_passing:
                if content:
                    content += ('& ' + f"For Vehicle Passing {vehicle_passing} ")
                else:
                    content = f"For Vehicle Passing {vehicle_passing}"
            site_url= frappe.utils.get_url() + f"/app/vehicle/{vehicle.get('name')}"        

            head_html += f'''<tr><td data-row="row-pbhk"><span style="background-color: rgb(255, 255, 255); font-size: 12px; color: rgb(51, 60, 68);"><a href="{site_url}">{vehicle.get('name')}</a></span></td><td data-row="row-pbhk">{content}</td></tr>'''
            content = ''
            is_sendable = True
    message = head_html + '''</tbody></table></div>'''
    if is_sendable:
        send_regulatory_compliance_notification(message)

def insurance_checking(vehicle):
    end_date = vehicle.get('end_date')
    no_of_days = end_date - today
    return fifteen_one_week_one_day_check(no_of_days.days)

def carbon_checking(vehicle):
    '''
    Every 6 months have to take the carbon checking
    '''
    last_carbon_check_date = vehicle.get('carbon_check_date')
    if last_carbon_check_date:
        next_carbon_check = add_days(vehicle.get('carbon_check_date'), 6*30)
        no_of_days = next_carbon_check - today
        return fifteen_one_week_one_day_check(no_of_days.days)
    else:
        return None
    
def vehicle_passing_checking(vehicle):
    '''
    Every year we have to do vehicle passing checking with the goverment.
    taking common year day count 365
    '''
    last_vehicle_passing = vehicle.get('last_vehicle_passing')
    if last_vehicle_passing:
        vehicle_passing_date = add_days(vehicle.get('last_vehicle_passing'), 365)
        no_of_days = vehicle_passing_date - today
        return fifteen_one_week_one_day_check(no_of_days.days)
    else:
        return None

def fifteen_one_week_one_day_check(no_of_days):
    '''
    Checking whether the day lenth with in 15 days or one week or daily
    '''
    if no_of_days == 15:
        return '15 Days Left'
    elif no_of_days == 7:
        return '7 Days Left'
    elif no_of_days < 7:
        return f'{no_of_days} Days Left'
    return None


def send_regulatory_compliance_notification(message):
    recipients = frappe.get_all("Has Role", filters={"role":("in", ['Fleet Manager', 'Fleet User'])}, pluck='parent')
    recipients = list(set([email for email in recipients if validate_email_address(email, throw=False)]))
    try:
        frappe.sendmail(
            recipients= recipients,
            subject='Regulatory Compliance Notification',
            message=message,
        )
    except Exception as ex:
        frappe.msgprint(f"Please contact Administrator or Check 'Email Account' settings \n {ex}")