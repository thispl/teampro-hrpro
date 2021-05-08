# -*- coding: utf-8 -*-
# Copyright (c) 2019, VHRS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import frappe,os,base64
import requests
import datetime
import json,calendar
from datetime import datetime,timedelta,date,time
import datetime as dt
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from frappe.desk.notifications import delete_notification_count_for
from frappe import _
import xml.etree.ElementTree as ET


class MissPunchApplication(Document):
    def on_submit(self):
        if self.status == "Approved By HR":
            frappe.db.set_value("Attendance",self.attendance,"in_time",self.in_time)
            frappe.db.set_value("Attendance",self.attendance,"out_time",self.in_time)
            frappe.db.set_value("Attendance",self.attendance,"qr_scan_time",self.in_time)
            frappe.db.set_value("Attendance",self.attendance,"status","Present")