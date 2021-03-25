// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Compliance Documents', {
	check: function(frm) {
		frappe.call({
			"method":"hrpro.hrpro.doctype.compliance_documents.compliance_documents.validate_csv",
			args:{
				"pf_csv":frm.doc.pf_csv,
				"esi_csv":frm.doc.esi_csv,
				"start_date":frm.doc.start_date
			},
			callback(r){
				// console.log(r.message)
			}
		})
	}
});
