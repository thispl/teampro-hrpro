# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ContractorEmployee(Document):
	def on_submit(self):
		doc = frappe.new_doc("Employee")
		doc.salutation = self.salutation
		doc.first_name = self.first_name
		doc.middle_name = self.last_name
		doc.gender = self.gender
		doc.date_of_joining = self.date_of_joining
		doc.date_of_birth = self.date_of_birth
		doc.marital_status = self.marital_status
		doc.blood_group = self.blood_group
		doc.cell_number = self.cell_number
		doc.personal_email = self.personal_email
		doc.contractor_id = self.contractor_id
		doc.flat = self.flat
		doc.flat_name = self.flat_name
		doc.street_road = self.street_road
		doc.area_locality = self.area_locality
		doc.village_town_city = self.village_town_city
		doc.district = self.district
		doc.state = self.state
		doc.pin_code = self.pin_code
		doc.pf_number = self.pf_number
		doc.esi_ip_no = self.esi_ip_no
		doc.uan = self.uan
		doc.aadhar_number = self.aadhar_number
		doc.flags.ignore_mandatory = True
		doc.save(ignore_permissions=True)
		frappe.db.commit()
