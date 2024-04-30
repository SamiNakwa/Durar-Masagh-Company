
import frappe
from hrms.hr.doctype.attendance_request.attendance_request import AttendanceRequest
from frappe.utils import add_days, date_diff, getdate
from datetime import datetime



class CustomAttendanceRequest(AttendanceRequest):

    def validate(self):
       super().validate()
       self.validate_attendance_status()
    

    def validate_attendance_status(self):
        data = frappe.db.get_all('Attendance',
                                 filters={
                                    'employee': self.employee,
                                    'attendance_date':['between',[self.from_date,self.to_date]],
                                    'docstatus':1
                                },
                                fields=['name','attendance_date','status'],
                                order_by='attendance_date asc'
                                )
        avoid_date = []                        
        for d in data:
            if d.status != 'Absent':
                avoid_date.append(d)
        
        if avoid_date:
            length = len(avoid_date)
            if length == 1:
                error_message = f"For date <b>{avoid_date[0].attendance_date}</b> the status was <b>{avoid_date[0].status}</b> so you can't raise attendance request. please select corerect from date and to date <hr>Note: You can raise attendance for only <b>Absent</b> or <b>New Attendance</b>"
                frappe.throw(error_message)
            else:
                error_msg = f"You can raise Attendance for only <b>Absent</b> or <b>New Attendance</b>. But below mentioned dates had these status <br><br><table>"

                for avoid in avoid_date:
                    error_msg += f'''
                                <tr>
                                    <td>{avoid.attendance_date}</td>
                                    <td>{avoid.status}</td>
                                </tr>
                                '''
                error_msg += '</table>'
                frappe.throw(error_msg)


    def on_submit(self):
        self.update_and_create_attendance()
           
    def update_and_create_attendance(self):
         
        data = frappe.db.get_all('Attendance',
                                 filters={
                                    'employee': self.employee,
                                    'attendance_date':['between',[self.from_date,self.to_date]],
                                    'docstatus':1
                                },
                                fields=['name','attendance_date','status'],
                                order_by='attendance_date asc'
                                )
        
        if data: 
            struct_date = get_attendance_structure_date(data)
            request_days = date_diff(self.to_date, self.from_date) + 1
            for number in range(request_days):
                attendance_date = add_days(self.from_date, number)

                date_obj = datetime.strptime(attendance_date, '%Y-%m-%d').date()
                
                is_attendance_already_created = check_attendance_already_created(struct_date,date_obj)
                skip_attendance = self.validate_if_attendance_not_applicable(attendance_date)

                if is_attendance_already_created and not skip_attendance:
                    attendance_details = struct_date.get(date_obj)
                    if self.reason == 'Work From Home':
                        status = 'Work From Home'
                    else:
                        status = 'Present'
                    frappe.db.set_value('Attendance', attendance_details.name, 'status', status)
                        
                elif not skip_attendance:
                    self.create_single_attendance(attendance_date=attendance_date)
        else:
            self.create_attendance()

        return data
    
    def create_single_attendance(self, attendance_date=None):
        if attendance_date:
            attendance = frappe.new_doc("Attendance")
            attendance.employee = self.employee
            attendance.employee_name = self.employee_name
            if self.half_day and date_diff(getdate(self.half_day_date), getdate(attendance_date)) == 0:
                attendance.status = "Half Day"
            elif self.reason == "Work From Home":
                attendance.status = "Work From Home"
            else:
                attendance.status = "Present"
            attendance.attendance_date = attendance_date
            attendance.company = self.company
            attendance.attendance_request = self.name
            attendance.save(ignore_permissions=True)
            attendance.submit()
        

def check_attendance_already_created(struct_date, date_obj):
    
    if struct_date.get(date_obj):
        return True
    else:
        return False
        

        
def get_attendance_structure_date(data):
    data_dict = {}
    for d in data:
        data_dict[d.attendance_date] = d
    return data_dict
        
