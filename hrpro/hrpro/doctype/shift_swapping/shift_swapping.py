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
	shift = frappe.get_value("Shift Assignment",{"employee":employee},["shift_type"])
	return shift