# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime,timedelta,date,time
import datetime as dt
from datetime import date
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr

class LapseELLeaveBalance(Document):
    pass

@frappe.whitelist()
def leave_allocation():
    start_date = date(date.today().year, 1, 1)
    end_date = date(date.today().year, 12, 31)
    leave_type = "Earned Leave"
    carry_forward= 1
    employee = frappe.db.sql("""SELECT * FROM `tabEmployee` WHERE status="Active" """,as_dict=True)
    for emp in employee:
        unused_leaves=0
        if not frappe.db.exists("""SELECT * FROM `tabLeave Allocation` WHERE docstatus='1' and employee ='%s' and from_date = '%s' and to_date='%s' """%(emp.name,start_date,end_date)):
            from erpnext.hr.doctype.leave_allocation.leave_allocation import get_carry_forwarded_leaves
            unused_leaves = get_carry_forwarded_leaves(emp.name,leave_type,start_date,carry_forward)
            category = frappe.get_all("Category",{"earned_leave":1},["name","annual_el_count","max_leaves_allowed","max_encashment_allowed"])
            if category:
                for cat in category:
                    total_leave = unused_leaves + cat.annual_el_count
                    if total_leave <= cat.max_leaves_allowed:
                        allocated_leave = total_leave
                        lapse = 0
                    else:
                        allocated_leave = cat.max_leaves_allowed
                        lapse = total_leave - cat.max_leaves_allowed
                    leave = frappe.new_doc("Leave Allocation")
                    leave.update({
                        "employee": emp.name,
                        "from_date": start_date,
                        "to_date": end_date,
                        "leave_type": "Earned Leave",
                        "new_leaves_allocated": allocated_leave
                    })
                    leave.save(ignore_permissions=True)
                    leave.submit()
                    frappe.db.commit()
                    earned_leave = frappe.db.exists("Earned Leave Balance", {"employee": emp.name},["name"])
                    if not earned_leave:
                        el_balance = frappe.new_doc("Earned Leave Balance")
                        el_balance.update({
                            "employee": emp.name,
                            "last_update_date": today(),
                            "annual_credit": cat.annual_el_count,
                            "unused_leave": unused_leaves,
                            "total_allocated": allocated_leave,
                            "lapse_leave": lapse
                        })
                        el_balance.save(ignore_permissions=True)
                        frappe.db.commit()
                    else:
                        el_balance = frappe.get_doc("Earned Leave Balance", earned_leave)
                        el_balance.update({
                            "employee": emp.name,
                            "last_update_date": today(),
                            "annual_credit": cat.annual_el_count,
                            "unused_leave": unused_leaves,
                            "total_allocated": allocated_leave,
                            "lapse_leave": lapse
                        })
                        el_balance.save(ignore_permissions=True)
                        frappe.db.commit()