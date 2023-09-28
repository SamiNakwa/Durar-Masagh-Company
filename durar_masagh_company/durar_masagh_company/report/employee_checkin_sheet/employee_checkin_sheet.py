# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta
from frappe.utils import  getdate
from datetime import date



def execute(filters=None):
	columns, data = get_columns(filters), get_datas(filters)
	return columns, data



def get_columns(filters=None):
	
	return [
		_("Date") + ":Date:100",
		_("Day") + ":Data:150",
		_("Attendance") + ":Data:100",
		_("Checkin Status") + ":Check:50",
		_("First Check-In Time") + ":Time:150",
		_("Last Check-Out Time") + ":Time:150",
        _("Lunch Break") + ":Duration:100",
	    _("Shift Start Time") + ":Time:125",
	    _("Shift End Time") + ":Time:125",
	    _("Hour To Work") + ":Duration:100",
        _("Working Time") + ":Duration:100",
	    _("Over Time/Less Time") + ":Duration:100",
		_("Down Fall Time") + ":Duration:100",
		_("Overtime Rate Calculation(SAR)") + ":Currency:150",
		_("Deduction Rate(SAR)") + ":Currency:150"
	]

def get_datas(filters=None):

	db_filters = {
		'employee':filters.employee,
		'time': ['between', [filters.from_date, filters.to_date]]
	}
	checkin_data = frappe.db.get_all('Employee Checkin', filters=db_filters, fields=['*'], order_by='time asc')
	
	attendance_list = frappe.db.get_all('Attendance', 
									 filters=[
										 ['employee', '=', filters.employee],
										 ['attendance_date', 'between', [filters.from_date, filters.to_date]],
										 ['docstatus', '=', 1]
									],
									fields=['attendance_date', 'status']
									)

	holiday, is_eligible, overtime_rate, default_shift = frappe.db.get_value('Employee', filters.employee, ['holiday_list','is_eligible','overtime_fixed_rate', 'default_shift'] )

	shift_type = frappe.db.get_list('Shift Type',
								 filters={
									 'name':default_shift
								 },
								 fields=['*']
								 )

	holiday_list = frappe.db.get_all(
		'Holiday',
		filters={
			'parent':holiday,
			'parenttype': "Holiday List"
		},
		pluck='holiday_date'
	)

	if not checkin_data:
		frappe.msgprint(f'There is no checkin data for this employee {filters.employee} for this dates from date {filters.from_date} & to date {filters.to_date}')
		return []
	
	structure_data = get_structure_data(checkin_data)
	list_of_dates = get_dates(filters.from_date, filters.to_date)
	data = []
	for date in list_of_dates:
		temp = []
		temp.append(date)

		day = get_day(date)
		temp.append(day)

		temp.append(get_attendance_status(date, attendance_list, holiday_list, structure_data))
		temp.append(is_checkin_there(date, structure_data))
		
		frist_in, last_out, diff, = get_in_and_out_time(structure_data.get(date, []))
		temp.append(frist_in)
		temp.append(last_out)
		temp.append(60*60)

		shift_start, shift_end = get_shift_time_data(structure_data.get(date, []), filters.employee,shift_type,day)
		temp.append(shift_start)
		temp.append(shift_end)

		hour_work = get_hour_work(shift_start,shift_end)
		temp.append(hour_work)
		temp.append(diff)


		is_holiday = getdate(date) in holiday_list

		if is_holiday:
			over_time = 0  
		else:
			over_time = get_over_time(diff, hour_work)

		temp.append(over_time)
		dwon_fall_time = get_down_fall_time(shift_start,shift_end,frist_in,last_out)
		temp.append(dwon_fall_time)

		over_time_rate = get_overtime_fixed_rate(overtime_rate,over_time,is_eligible)
		temp.append(over_time_rate)

		deduction_rate = get_deduction_rate(overtime_rate,dwon_fall_time)
		temp.append(deduction_rate)

		data.append(temp)
	
	return data

	for key, value in structure_data.items():
		temp = []

		temp.append(key)

		frist_in, last_out, diff, = get_in_and_out_time(value)
		
		temp.append(frist_in)
		temp.append(last_out)
		temp.append(60*60)

		shift_start, shift_end = get_shift_time_data(value, filters.employee)
		temp.append(shift_start)
		temp.append(shift_end)

		hour_work = get_hour_work(shift_start,shift_end)
		temp.append(hour_work)
		temp.append(diff)

		over_time = get_over_time(diff,hour_work)
		temp.append(over_time)

		shift_start = ensure_timedelta(shift_start)
	

		dwon_fall_time = get_down_fall_time(shift_start,shift_end,frist_in,last_out)
		temp.append(dwon_fall_time)

		data.append(temp)

	return data


def is_checkin_there(date, checkin_data):

	if checkin_data.get(date):
		return 1
	else:
		return 0


def get_attendance_status(date, attendance_list,holiday_list, checkin_data):
	if attendance_list:
		for atte in attendance_list:
			if atte.get('attendance_date') == getdate(date):
				if atte.get('status') == 'Present':
					return "P"
				if atte.get('status') == 'Absent':
					return "A"
				if atte.get('status') == 'On Leave':
					return "L"
				if atte.get('status') == 'Half Day':
					return "HD"
				if atte.get('status') == 'Work From Home':
					return "WH"
				
	if checkin_data.get('date'):
		return "P"
	if getdate(date) in holiday_list:
		return "H"	

	return "A"
				
   
def ensure_timedelta(time_value):
    if isinstance(time_value, str):
        time_format = "%H:%M:%S"
        
        try:
            time_value = datetime.strptime(time_value, time_format) - datetime.strptime("00:00:00", time_format)
        except ValueError:
            time_value = None  
    elif isinstance(time_value, timedelta):
        pass
    else:
        time_value = None
    
    return time_value

def get_in_and_out_time(value):

	if value:
		frist_in = value[0].get('time').strftime("%H:%M:%S")
		last_out = value[-1].get('time').strftime("%H:%M:%S")
		diff = (value[-1].get('time') - value[0].get('time')).total_seconds() - (60 * 60)
	else:
		frist_in = last_out = None
		diff = 0

	return frist_in, last_out, diff,

def get_structure_data(checkin_data):

	data = {}
	for ec in checkin_data:
		if data.get(str(ec.get('time').date())):
			data.get(str(ec.get('time').date())).append(ec)
		else:
			data[str(ec.get('time').date())] = [ec]
	
	return data


def get_shift_time_data(checkin_data, employee,shift_type, day):
	if shift_type and shift_type[0]:
		shift_type = shift_type[0]
		if day == 'Saturday':
			if shift_type.get('is_saturday_eligible'):
				shift_start = shift_type.get('saturday_shift_start_time')
				shift_end = shift_type.get('saturday_shift_end_time')
				return shift_start, shift_end

	  	
	

	try:
		shift_start = checkin_data[0].get('shift_start').time()
		shift_start = timedelta(
								hours=shift_start.hour,
								minutes=shift_start.minute,
								seconds=shift_start.second
								)
		shift_end = checkin_data[0].get('shift_end').time()
		shift_end = timedelta(
								hours=shift_end.hour,
								minutes=shift_end.minute,
								seconds=shift_end.second
								)
	except:
		shift_doc = get_current_shift_details(employee)
		if shift_doc:
			shift_start, shift_end = shift_doc
		else:
			frappe.throw("There is no shift assigned for a employee")

	return shift_start, shift_end



def get_current_shift_details(employee):
	
	shift_type = frappe.db.get_value('Employee', employee, 'default_shift')
	
	if shift_type:
		shift_doc = frappe.db.get_value('Shift Type', shift_type, ['start_time', 'end_time'])
		return shift_doc
	else:
		return False
	

def get_hour_work(shift_start,shift_end):
		hour_work = shift_end - shift_start
		
		return hour_work.seconds - 3600

def get_over_time(diff,hour_work):
	#if diff is not None and hour_work is not None:
	diff_minutes = diff 
	hour_work_minutes = hour_work   
	over_time = diff_minutes - hour_work_minutes
	return over_time

def get_down_fall_time(shift_start, shift_end, frist_in, last_out):
	frist_in = ensure_timedelta(frist_in)
	last_out = ensure_timedelta(last_out)
	mg = timedelta()
	eg = timedelta()

	if frist_in and last_out:
		if shift_start < frist_in:
			mg = frist_in - shift_start

		if shift_end > last_out:
			eg = shift_end - last_out


	downf_fall_time = mg + eg
	return downf_fall_time.seconds

def get_dates(from_date,to_date):
    date_format = "%Y-%m-%d"
    from_dates = datetime.strptime(from_date,date_format)
    to_dates = datetime.strptime(to_date,date_format)

    date_list = []

    current_date = from_dates
    while current_date <= to_dates:
        date_list.append(current_date.strftime(date_format))
        current_date += timedelta(days=1)

    return date_list

def get_overtime_fixed_rate(overtime_rate,over_time,is_eligible):
	if is_eligible:
		hour_to_minutes = over_time/60
		if hour_to_minutes > 15:
			overtime_fixed_rate = overtime_rate * (hour_to_minutes/60)
			return overtime_fixed_rate

def get_deduction_rate(overtime_rate,dwon_fall_time):
	seconds_to_hour = dwon_fall_time/3600
	hour_to_minutes = seconds_to_hour	
	detuction = overtime_rate * hour_to_minutes
	return detuction

def get_day(date):
	dates = getdate(date)
	day_name = dates.strftime("%A")
	return day_name


	
	
		




