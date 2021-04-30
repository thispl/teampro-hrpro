// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PF Report"] = {
	"filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": [frappe.datetime.add_months(frappe.datetime.get_today())],
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": [frappe.datetime.add_months(frappe.datetime.get_today())],
            "reqd": 1
        },
    ],

onload : function(report) {
	report.page.add_inner_button(__('Download TXT File'), function() {
        values = []
        columns = []
        report_data = report.data
        // console.log(report_data)
        for(i=0;i< report_data.length;i++){
            values.push(Object.values(report_data[i]))
        }
        
        window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s&column=%(column)s&value=%(value)s', {
			cmd: "hrpro.hrpro.report.pf_report.pf_report.get_template",
            column: columns,
            value: values,
		});
        
	})
}
};