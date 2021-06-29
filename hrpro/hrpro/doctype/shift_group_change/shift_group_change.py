# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ShiftGroupChange(Document):
	def on_submit(self):
		frappe.db.set_value("Employee",self.employee,"shift_group",self.group_change_to)
		frappe.msgprint("Successfully Shift Group Changed")

	def on_cancel(self):
		if self.present_group:
			frappe.db.set_value("Employee",self.employee,"shift_group",self.present_group)
			frappe.msgprint("Successfully Shift Group Cancelled")
		else:
			frappe.db.set_value("Employee",self.employee,"shift_group","")
			frappe.msgprint("Successfully Shift Group Cancelled")