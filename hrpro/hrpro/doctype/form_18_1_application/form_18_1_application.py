# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

import frappe, json
from frappe.model.document import Document
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day

class Form18_1Application(Document):
	pass

@frappe.whitelist()
def get_present_days(employee,request_date):
    compensatory_off=[]
    overtime=[]
    holiday_list = get_holidays_for_employee(employee,request_date)
    if holiday_list:
        for holiday in holiday_list:
            frappe.errprint(holiday)
            attendance = frappe.db.sql("""SELECT * FROM `tabAttendance` WHERE employee='%s' and 
            attendance_date='%s' and status='Present' and compensatory_off='0' """%(employee,holiday),as_dict=True)
            # frappe.errprint(attendance)
            compensatory_off.append(attendance)
    timesheet = frappe.db.sql("""SELECT * FROM `tabTimesheet` WHERE employee='%s' and start_date>='%s' and 
    end_date<='%s' and docstatus=1 """%(employee,request_date,request_date),as_dict=True)
    if timesheet:
        for ot_sheet in timesheet:
            frappe.errprint(ot)
            overtime.append(ot_sheet)
    return compensatory_off,overtime


def get_holidays_for_employee(employee, request_date):
        holiday_list = get_holiday_list_for_employee(employee)
        holidays = frappe.db.sql_list('''select holiday_date from `tabHoliday`
            where
                parent=%(holiday_list)s
                and holiday_date >= %(start_date)s
                and holiday_date <= %(end_date)s''', {
                    "holiday_list": holiday_list,
                    "start_date": request_date,
                    "end_date": request_date
                })

        holidays = [cstr(i) for i in holidays]

        return holidays

@frappe.whitelist()
def create_comp_off(employee,request_date,comp_off):
    # frappe.errprint(comp_off)
    comp_off = json.loads(comp_off)
    for comp in comp_off:
        frappe.errprint(comp)
        if comp['__checked'] == 1:
            frappe.errprint(comp)
            compensatory = frappe.new_doc("Compensatory Leave Request")
            compensatory.employee = employee
            compensatory.leave_type = "Compensatory Off"
            compensatory.work_from_date = comp['attendance_date']
            compensatory.work_end_date = comp['attendance_date']
            compensatory.reason = "Compensatory Off"
            compensatory.save(ignore_permissions = True)
            frappe.db.commit()
            frappe.db.set_value('Attendance',comp['id'],"compensatory_off",1)

@frappe.whitelist()
def check_employee(employee):
	employee = frappe.db.get_value("Employee",{"status":"Active","employee":employee},["form_18_1_applicable"])
	return employee