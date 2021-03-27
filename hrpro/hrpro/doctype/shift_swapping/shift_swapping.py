# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ShiftSwapping(Document):
	pass

@frappe.whitelist()
def allocated_shift(employee,shift_date):
	shift = frappe.db.sql("""select shift_type,start_date,end_date from `tabShift Assignment` where employee = '%s' and '%s' between start_date and end_date"""%(employee, shift_date),as_dict = 1)
	return shift