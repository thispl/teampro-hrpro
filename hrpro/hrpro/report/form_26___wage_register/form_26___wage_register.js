// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Form 26 - Wage Register"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -9),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), 21),
			"reqd": 1
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname": "docstatus",
			"label": __("Document Status"),
			"fieldtype": "Select",
			"options": ["Draft", "Submitted", "Cancelled"],
			"default": "Draft"
		},
		{
			"fieldname": "subcontractor_id",
			"label": __("SubContractor ID"),
			"fieldtype": "Link",
			"options": "Subcontractor"

		},
		{
			"fieldname": "job_order_name",
			"label": __("Job Order Name"),
			"fieldtype": "Link",
			"options": "Job Order",
		}
	]
};
