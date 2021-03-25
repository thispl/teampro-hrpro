# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.csvutils import read_csv_content


class ComplianceDocuments(Document):
    def before_submit(self):
        validate_pf(self.pf_csv,self.start_date)
        validate_esi(self.esi_csv,self.start_date)
    
    def on_submit(self):
        ss_list = frappe.db.sql("""select name,pf_non_compliance,esi_non_compliance from `tabSalary Slip` where start_date = %s """,(self.start_date),as_dict=True)
        for ss in ss_list:
            if ss.pf_non_compliance or ss.esi_non_compliance:
                frappe.db.set_value("Salary Slip",ss.name,"non_compliance",1)
            else:
                frappe.db.set_value("Salary Slip",ss.name,"non_compliance",0)



# @frappe.whitelist()
# def validate_csv(pf_csv,esi_csv,start_date):
#     validate_pf(pf_csv,start_date)
#     validate_esi(esi_csv,start_date)


def validate_pf(pf_csv,start_date):	
    from frappe.utils.file_manager import get_file
    _file = frappe.get_doc("File", {"file_url": pf_csv})
    filepath = get_file(pf_csv)
    pps = read_csv_content(filepath[1])
    ss_list = []
    emp_list = []
    for pp in pps:
        emp = frappe.db.exists("Employee",{"uan":pp[0]})
        if emp:
            ss = frappe.db.get_value("Salary Slip",{"employee":emp,"start_date":start_date})
            pf = frappe.db.get_value("Salary Detail", {'abbr': 'PF', 'parent':ss }, ['amount'])
            if pf:
                rpf = pf - 5
                if frappe.db.get_value("Salary Slip",ss,["pf_paid"]) == 0:
                    frappe.db.set_value("Salary Slip",ss,"pf_paid",pp[6])
                    if float(pp[6]) < rpf:
                        frappe.db.set_value("Salary Slip",ss,"pf_non_compliance",1)
                elif frappe.db.get_value("Salary Slip",ss,["pf_paid"]) > 0:
                    if frappe.db.get_value("Salary Slip",ss,["pf_non_compliance"]):
                        apf = frappe.db.get_value("Salary Slip",ss,["pf_paid"])+float(pp[6])
                        if apf < rpf:
                            frappe.db.set_value("Salary Slip",ss,"pf_non_compliance",1)
                            frappe.db.set_value("Salary Slip",ss,"pf_paid",apf)
                        else:
                            frappe.db.set_value("Salary Slip",ss,"pf_non_compliance",0)
                            frappe.db.set_value("Salary Slip",ss,"pf_paid",apf)

def validate_esi(esi_csv,start_date):	
    from frappe.utils.file_manager import get_file
    _file = frappe.get_doc("File", {"file_url": esi_csv})
    filepath = get_file(esi_csv)
    pps = read_csv_content(filepath[1])
    ss_list = []
    emp_list = []
    for pp in pps:
        emp = frappe.db.exists("Employee",{"esi_ip_no":pp[0]})
        if emp:
            ss = frappe.db.get_value("Salary Slip",{"employee":emp,"start_date":start_date})
            esi = frappe.db.get_value("Salary Detail", {'abbr': 'ESI', 'parent':ss }, ['amount'])
            if esi:
                resi = esi - 5
                pp3 = float(pp[3])*0.0075
                if frappe.db.get_value("Salary Slip",ss,["esi_paid"]) == 0:
                    frappe.db.set_value("Salary Slip",ss,"esi_paid",pp3)
                    if pp3 < resi:
                        frappe.db.set_value("Salary Slip",ss,"esi_non_compliance",1)
                elif frappe.db.get_value("Salary Slip",ss,["esi_paid"]) > 0:
                    if frappe.db.get_value("Salary Slip",ss,["esi_non_compliance"]):
                        aesi = frappe.db.get_value("Salary Slip",ss,["esi_paid"])+pp3
                        frappe.errprint(aesi)
                        frappe.errprint(resi)
                        if aesi < resi:
                            frappe.db.set_value("Salary Slip",ss,"esi_non_compliance",1)
                            frappe.db.set_value("Salary Slip",ss,"esi_paid",aesi)
                        else:
                            frappe.db.set_value("Salary Slip",ss,"esi_non_compliance",0)
                            frappe.db.set_value("Salary Slip",ss,"esi_paid",aesi)