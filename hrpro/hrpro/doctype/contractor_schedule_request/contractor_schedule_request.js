// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contractor Schedule Request', {
	refresh: function(frm) {
		if(!frappe.user.has_role('HOD')){
			frm.toggle_display(['unregistered'])
		}
	},
	start_date: function(frm) {
		if(frm.doc.start_date){
		frappe.call({
			method: 'erpnext.payroll.doctype.payroll_entry.payroll_entry.get_end_date',
			args: {
				frequency: "Monthly",
				start_date: frm.doc.start_date
			},
			callback: function (r) {
				if (r.message) {
					frm.set_value('end_date', r.message.end_date);
					if(frm.doc.contractor && frm.doc.plant){
						frm.trigger('check_availability')
				}
				}
			}
		});
	}
	},
	contractor(frm){
		if(frm.doc.start_date && frm.doc.end_date && frm.doc.plant){
				frm.trigger('check_availability')
		}
	},
	plant(frm){
		if(frm.doc.start_date && frm.doc.end_date && frm.doc.contractor){
				frm.trigger('check_availability')
		}
	},
	check_availability(frm){
		frappe.call({
			method:"hrpro.hrpro.doctype.contractor_schedule_request.contractor_schedule_request.get_count",
			args:{
				"contractor":frm.doc.contractor,
				"plant":frm.doc.plant,
				"start_date":frm.doc.start_date,
				"end_date":frm.doc.end_date
			},
			callback(r){
				frm.set_value('registered',r.message[0])
				frm.set_value('available',r.message[1])
				frm.set_value('wc_registered_count',r.message[2])
				frm.set_value('wc_available_count',r.message[3])
				frm.save()
			}
		})
	},
	validate(frm){
		if(!frm.doc.__islocal){
			if(!frm.doc.unregistered){
		if((frm.doc.manpower_count).length > 0){
			var count = 0
			$.each(frm.doc.manpower_count,function(i,v){
				count = count + v.manpower_count
			})
		if(count > frm.doc.available){
			frappe.throw('Requested Count cannot be greater than RC Available Count. Kindly raise unregistered request seperately')
		}
		if(count > frm.doc.wc_available_count){
			frappe.throw('Requested Count cannot be greater than WC Available Count. Kindly raise unregistered request seperately')
		}
		}
	}
}
}
});
