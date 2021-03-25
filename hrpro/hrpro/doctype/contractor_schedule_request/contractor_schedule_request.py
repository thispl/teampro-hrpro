# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import datetime
from frappe.model.document import Document

class ContractorScheduleRequest(Document):
    def on_submit(self):
        csa = frappe.db.exists("Contractor Schedule Approval",{"start_date":self.start_date,"contractor":self.contractor})
        if not csa:
            doc = frappe.new_doc('Contractor Schedule Approval')
            doc.contractor = self.contractor
            doc.start_date = self.start_date
            doc.end_date = self.end_date
            doc.registered = self.registered
            doc.wc_registered_count = self.wc_registered_count
            for s in self.manpower_count:
                doc.append("manpower_count",{
                    'department' : self.department,
                    'plant' : self.plant,
                    'shift_type':s.shift_type,
                    'contract_type':s.contract_type,
                    'manpower_count':s.manpower_count
                })
            doc.save(ignore_permissions=True)
            frappe.db.commit()
        else:
            doc = frappe.get_doc('Contractor Schedule Approval',csa)
            doc.contractor = self.contractor
            doc.start_date = self.start_date
            doc.end_date = self.end_date
            doc.registered = self.registered
            doc.wc_registered_count = self.wc_registered_count
            for s in self.manpower_count:
                doc.append("manpower_count",{
                    'department' : self.department,
                    'plant' : self.plant,
                    'shift_type':s.shift_type,
                    'contract_type':s.contract_type,
                    'manpower_count':s.manpower_count
                })
            doc.save(ignore_permissions=True)
            frappe.db.commit()

@frappe.whitelist()
def get_count(contractor,plant,start_date,end_date):
    con = frappe.get_doc('Contractor',contractor)
    for c in con.rc_child:
        if c.plant == plant:
            reg_count = c.max
    csrs = frappe.db.sql("""select name from `tabContractor Schedule Request` where start_date between %s and %s and contractor = %s and plant = %s""",(start_date,end_date,contractor,plant),as_dict=True)
    av_count = 0
    for csr in csrs:
        cs = frappe.get_all('Manpower Count',{'parent':csr.name},['*'])
        for c in cs:
            av_count = av_count + c["manpower_count"]
    a_count = reg_count-av_count
    wcs = frappe.get_doc("Contractor",contractor)
    end_d = datetime.strptime(end_date, '%Y-%m-%d')
    wc_count = 0
    for wc in wcs.wc_child:
        if end_d.date() < wc.to:
            wc_count = wc_count + int(wc.persons_covered)
    wcsrs = frappe.db.sql("""select name from `tabContractor Schedule Request` where start_date between %s and %s and contractor = %s """,(start_date,end_date,contractor),as_dict=True)
    av_count_wc = 0
    for wcsr in wcsrs:
        wcs = frappe.get_all('Manpower Count',{'parent':wcsr.name},['*'])
        for wc in wcs:
            av_count_wc = av_count_wc + wc["manpower_count"]
    av_wc_count = wc_count-av_count_wc
    return reg_count,a_count,wc_count,av_wc_count
