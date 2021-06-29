// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Compensatory Leave Register', {
	// refresh: function(frm) {

	// }
	get_details:function(frm){
		if (frm.doc.from_date && frm.doc.to_date){
			frappe.call({
				"method":"hrpro.hrpro.doctype.compensatory_leave_register.compensatory_leave_register.get_present_days",
				"args":{
					"employee":frm.doc.employee,
					"from_date":frm.doc.from_date,
					"to_date":frm.doc.to_date
				},
				callback: function(r){
					console.log(r.message[0][0])
					$.each(r.message[0], function(i, d) {
						// frm.doc.invoices = frm.doc.invoices.filter(row => row.sales_invoice);
						let row = frm.add_child("compensatory_list");
						row.id = d.name;
						row.attendance_date = d.attendance_date;
						row.status = d.status;
						row.shift = d.shift;
						row.check_in = d.in_time;
						row.check_out = d.out_time;						
					});
					refresh_field("compensatory_list");
				}
			})
		}
	},
	from_date(frm) {
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
		console.log(frm.doc.from_date)
		if (frm.doc.from_date < today){
		    frappe.validated = false;
		    frappe.msgprint("Compensatory Off request must be raise within 90days for the Worked on Holidays")
		} 
	},
	to_date(frm){
		if (frm.doc.from_date){
			if(frm.doc.to_date < frm.doc.from_date){
				frappe.msgprint("To Date cannot be Less then From Date")
				frm.set_value('to_date','')
			}
		}
	},
	create_comp_off(frm){
		if(frm.doc.compensatory_list){
			frappe.call({
				"method":"hrpro.hrpro.doctype.compensatory_leave_register.compensatory_leave_register.create_comp_off",
				"args":{
					"employee":frm.doc.employee,
					"from_date":frm.doc.from_date,
					"to_date":frm.doc.to_date,
					"comp_off":frm.doc.compensatory_list
				},
				callback: function(r){
					console.log(r.message)
				}
			})
		}
	}
});
