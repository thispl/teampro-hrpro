// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Swapping', {
	// refresh: function(frm) {

	// }
	shift_date:function(frm){
		frappe.call({
			method: 'hrpro.hrpro.doctype.shift_swapping.shift_swapping.allocated_shift',
			args: {
				employee: frm.doc.employee,
				shift_date: frm.doc.shift_date
			},
			callback: function (r) {
				if (r.message) {
					frm.set_value('shift_type', r.message);
				}
			}
		});
	},
	swap_to:function(frm){
		// frappe.call({
		// 	method: 'hrpro.hrpro.doctype.shift_swapping.shift_swapping.shift_details',
		// 	args: {
		// 		employee: frm.doc.employee,
		// 		shift_date: frm.doc.shift_date,
		// 		swap_to: frm.doc.swap_to
		// 	},
		// 	callback: function (r) {
		// 		if (r.message) {
					// $.each(r.message, function(i, d) {
					// 	frm.add_child('item', {
					// 		salary_slip: d.salary_slip,
					// 		month: d.month,
					// 		year:d.year,
					// 		basic_and_da:d.basic + d.da,
					// 		pf: d.pf,
					// 		esi: d.esi,
					// 		pt: d.pt,
					// 		bonus: d.bonus
					// 	});
					// 	frm.refresh_field('item');
					// })
		// 		}
		// 	}
		// });
	}
});
