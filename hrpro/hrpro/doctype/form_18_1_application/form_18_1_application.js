// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Form 18_1 Application', {
	// refresh: function(frm) {

	// }
	employee:function(frm){
		if(frm.doc.employee){
			frappe.call({
				"method":"hrpro.hrpro.doctype.form_18_1_application.form_18_1_application.check_employee",
				"args":{
					"employee":frm.doc.employee
				},
				callback: function(r){
					// console.log(r.message)
					if(r.message==0){
						frappe.validated = false;
						frappe.msgprint("This Employee not under the 18(1) Condition")
						frm.set_value('employee','')
					}
				}
			})	
		}
	},
	get_details:function(frm){
		if (frm.doc.request_date){
			frappe.call({
				"method":"hrpro.hrpro.doctype.form_18_1_application.form_18_1_application.get_present_days",
				"args":{
					"employee":frm.doc.employee,
					"request_date":frm.doc.request_date
				},
				callback: function(r){
					console.log(r.message[0][0])
					$.each(r.message[0], function(i, d) {
						let row = frm.add_child("compensatory_details");
						row.id = d.name;
						row.attendance_date = d.attendance_date;
						row.status = d.status;
						row.shift = d.shift;
						row.check_in = d.in_time;
						row.check_out = d.out_time;						
					});
					refresh_field("compensatory_details");
					$.each(r.message[1], function(i, d) {
						let row = frm.add_child("overtime_details");
						row.id = d.name;
						row.date = d.start_date;
						row.total_hours = d.total_hours;
					});
					refresh_field("overtime_details");
				}
			})
		}
	},
	request_date(frm) {
		var today = new Date()
		today.setDate(today.getDate() - 90);
		var dd = today.getDate();
        var mm = today.getMonth(); 
        var yyyy = today.getFullYear();
        if(dd<10) 
            {
                dd='0'+dd;
            } 
            
        if(mm<10) 
            {
                mm='0'+mm;
            } 
        today = yyyy+'-'+mm+'-'+dd;
		console.log(today)
		console.log(frm.doc.request_date)
		if (frm.doc.request_date < today){
		    frappe.validated = false;
		    frappe.msgprint("Compensatory Off request must be raise within 90days for the Worked on Holidays")
			frm.set_value('request_date','')
		} 
	},
	create_comp_off(frm){
		if(frm.doc.compensatory_details){
			frappe.call({
				"method":"hrpro.hrpro.doctype.form_18_1_application.form_18_1_application.create_comp_off",
				"args":{
					"employee":frm.doc.employee,
					"request_date":frm.doc.request_date,
					"comp_off":frm.doc.compensatory_list
				},
				callback: function(r){
					console.log(r.message)
				}
			})
		}
	}
});