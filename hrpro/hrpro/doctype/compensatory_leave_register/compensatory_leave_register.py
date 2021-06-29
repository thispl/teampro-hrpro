# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

import frappe, json
from frappe.model.document import Document
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day

class CompensatoryLeaveRegister(Document):
    pass

@frappe.whitelist()
def get_present_days(employee,from_date,to_date):
    compensatory_off=[]
    holiday_list = get_holidays_for_employee(employee,from_date,to_date)
    for holiday in holiday_list:
        frappe.errprint(holiday)
        attendance = frappe.db.sql("""SELECT * FROM `tabAttendance` WHERE employee='%s' and 
        attendance_date='%s' and status='Present' and compensatory_off='0' """%(employee,holiday),as_dict=True)
        # frappe.errprint(attendance)
        compensatory_off.append(attendance)
    return compensatory_off


def get_holidays_for_employee(employee, from_date, to_date):
        holiday_list = get_holiday_list_for_employee(employee)
        holidays = frappe.db.sql_list('''select holiday_date from `tabHoliday`
            where
                parent=%(holiday_list)s
                and holiday_date >= %(start_date)s
                and holiday_date <= %(end_date)s''', {
                    "holiday_list": holiday_list,
                    "start_date": from_date,
                    "end_date": to_date
                })

        holidays = [cstr(i) for i in holidays]

        return holidays

@frappe.whitelist()
def create_comp_off(employee,from_date,to_date,comp_off):
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
            frappe.throw("Compensatory Leave Request Raised for Approval")