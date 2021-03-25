// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Approval', {
	refresh: function(frm) {
		frm.disable_save()
	},
	attendance_date(frm){
		if(frm.doc.plant){
			frm.trigger('fetch')
		}
	},
	department(frm){
		if(frm.doc.attendance_date){
		if(frm.doc.plant){
			frm.trigger('fetch')
		}
	}
	},
	plant(frm){
		if(frm.doc.attendance_date){
		if(frm.doc.plant){
			frm.trigger('fetch')
		}
	}
	},
	fetch(frm){
		if (frm.doc.plant != "TPL (All Plants)"){
		frappe.call({
			method:"hrpro.hrpro.doctype.attendance_approval.attendance_approval.get_attendance",
			args:{
				"attendance_date":frm.doc.attendance_date,
				"department":frm.doc.department,
				"plant":frm.doc.plant
			},
			freeze:true,
			freeze_message:"Loading",
			callback(r){
				frm.clear_table('ot_child')
				frm.refresh_field('ot_child')
				$.each(r.message,function(i,v){
					frm.add_child('ot_child',{
						employee : v.employee,
						employee_name : v.employee_name,
						attendance : v.name,
						department:v.department,
						contractor:v.contractor,
						shift : v.shift,
						in : v.in,
						out : v.out,
						total_working_hours : v.total_working_hours,
						extra_hours : v.extra_hours,
						approved_ot_hours : v.approved_ot_hours

					})
					frm.refresh_field('ot_child')
				})
			}
		})
	}
	else{
		frappe.msgprint("Please select only one Plant")
	}
	},
	submit(frm){
		frappe.call({
			method:"hrpro.hrpro.doctype.attendance_approval.attendance_approval.update_attendance",
			args:{
				table:frm.doc.ot_child,
				date:frm.doc.attendance_date
			},
			callback(r){
				if(r.message){
				frm.clear_table("ot_child")
				frm.refresh_field('ot_child')
				frappe.msgprint("Attendance Submitted Successfully")
				}
			}
		})
	}
});
frappe.ui.form.on('OT Child', {
	in(frm,cdt,cdn){
		let row = frappe.get_doc(cdt, cdn);
		if(row.in && row.out && row.shift){
		calculate_hours(frm,row,cdt,cdn)
		}
	},
	out(frm,cdt,cdn){
		let row = frappe.get_doc(cdt, cdn);
		if(row.in && row.out && row.shift){
		calculate_hours(frm,row,cdt,cdn)
		}
	},
	shift(frm,cdt,cdn){
		let row = frappe.get_doc(cdt, cdn);
		if(row.in && row.out && row.shift){
		calculate_hours(frm,row,cdt,cdn)
		}
	}
	
});
let calculate_hours = function(frm,row,cdt,cdn){
	frappe.call({
		method:"hrpro.hrpro.doctype.attendance_approval.attendance_approval.calculate_hours",
		args:{
			row:row,
		},
		callback(r){
			frappe.model.set_value(cdt,cdn,"total_working_hours",r.message.twh)
			frappe.model.set_value(cdt,cdn,"extra_hours",r.message.ot)
			frappe.model.set_value(cdt,cdn,"approved_ot_hours",r.message.ot)
		}
	})
}
