# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from datetime import datetime
from datetime import timedelta, time,date
from frappe.utils.data import add_days

class AttendanceApproval(Document):
    pass

@frappe.whitelist()
def calculate_hours(row):
    time_list = []
    ot = ""
    s_list = ["C Shift","Night Shift"]
    r = json.loads(row)
    in_time = datetime.strptime(r['in'], '%H:%M:%S')
    out_time = datetime.strptime(r['out'], '%H:%M:%S')
    if r["department"] != "SECURITY - TPL":
        if r["shift"] not in ["C Shift","Night Shift"]:
            total_twh = datetime.strptime(str(out_time - in_time), '%H:%M:%S')
        else:
            o_time = (add_days(out_time,1))
            total_twh = datetime.strptime(str(o_time - in_time), '%H:%M:%S')
        max_twh = datetime.strptime('08:00', '%H:%M')
        if total_twh > max_twh:
            ot = total_twh - max_twh
        return {"twh":str(total_twh.time()),"ot":str(ot)}
    if r["department"] == "SECURITY - TPL":
        if r["shift"] != "Night Shift":
            total_twh = datetime.strptime(str(out_time - in_time), '%H:%M:%S')
        else:
            o_time = (add_days(out_time,1))
            total_twh = datetime.strptime(str(o_time - in_time), '%H:%M:%S')
        max_twh = datetime.strptime('12:00', '%H:%M')
        if total_twh > max_twh:
            ot = total_twh - max_twh
        return {"twh":str(total_twh.time()),"ot":str(ot)}

@frappe.whitelist()
def get_attendance(attendance_date,plant,department=None):
    if department:
        att_list = frappe.db.sql("""Select * from `tabAttendance` where attendance_date = %s and docstatus = 0 and plant = %s and department = %s and owner = 'Administrator' """,(attendance_date,plant,department),as_dict=True)
        return att_list
    elif not department:
        att_list = frappe.db.sql("""Select * from `tabAttendance` where attendance_date = %s and docstatus = 0 and plant = %s and owner = 'Administrator' """,(attendance_date,plant),as_dict=True)
        return att_list

@frappe.whitelist()
def update_attendance(table,date):
    table = json.loads(table)
    for t in table:
        att = frappe.get_doc("Attendance",t["attendance"])
        att.out = t["out"]
        att.shift = t["shift"]
        att.extra_hours = t["extra_hours"]
        att.total_working_hours = t["total_working_hours"]
        att.approved_ot_hours = t["approved_ot_hours"]
        att.save(ignore_permissions=True)
        att.submit()
        frappe.db.commit()
        frappe.db.set_value("Attendance",att.name,"in",t["in"])
        doc = frappe.new_doc("Timesheet")
        doc.employee = t["employee"]
        ot = t["approved_ot_hours"]
        if ot:
            ftr = [3600,60,1]
            hr = sum([a*b for a,b in zip(ftr, map(int,ot.split(':')))])
            ot_time = datetime.strptime(date+' '+t['approved_ot_hours'], '%Y-%m-%d %H:%M:%S')
            out = datetime.strptime(date+' '+t['out'], '%Y-%m-%d %H:%M:%S')
            f_time = out - ot_time
            from_time = datetime.strptime(date+' '+str(f_time), '%Y-%m-%d %H:%M:%S')
            doc.append("time_logs",{
                "activity_type":"Overtime",
                "hours":hr/3600,
                "from_time":from_time,
                "to_time":out
            })
            doc.save(ignore_permissions=True)
            doc.submit()
            frappe.db.commit()
    return "ok"