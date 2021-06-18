# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.hr.utils import get_holidays_for_employee
from datetime import datetime,timedelta,date,time
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr

class ShiftSchedule(Document):
    def on_submit(self):
        sas = frappe.get_all("Shift Assignment",{'shift_schedule':self.name,'docstatus':'0'})
        for sa in sas:
            doc = frappe.get_doc('Shift Assignment',sa.name)
            doc.submit()
            frappe.db.commit()
        frappe.msgprint('Shift Schedule Approved Successfully')

    @frappe.whitelist()
    def validate_employees(self):
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])
        # dates = self.get_dates()
        err_list = ""
        for pp in pps:
            if pp[0] != 'ID':
                if pp[0]:
                    if not pp[1]:
                        err_list +='<li>Employe Name should not be Empty. </li>'
                    if not pp[2]:
                        err_list +='<li>Department should not be Empty. </li>'
                    if not pp[3]:
                        err_list +='<li>Category should not be Empty. </li>'
                    if not pp[4]:
                        err_list +='<li>Date should not be Empty. </li>'
                    if not pp[5]:
                        err_list +='<li>Shift Group should not be Empty. </li>'
                    if not pp[6]:
                        err_list +='<li>Shift should not be Empty. </li>'
                    # if not pp[7]:
                    # 	err_list +='<li>Boarding Point should not be Empty. </li>'
                    if not frappe.db.exists("Employee",{'name':pp[0],'status':'Active'}):
                        err_list +='<li><font color="red"><b>%s</b></font> is not an Active Employee. </li>'%(pp[0])
                    else:
                        if self.department != frappe.db.get_value("Employee",pp[0],"department"):
                            err_list += '<li><font color="red"><b>%s</b></font> doesnot belongs to <b>%s</b> department. </li>'%(pp[0],self.department)
                        else:
                            if pp[6]:
                                # for date in dates:
                                sa = frappe.db.exists('Shift Assignment',{'employee':pp[0],'start_date':pp[4],'docstatus':['!=','2']})
                                if sa:
                                    err_list += '<li>%s department have already allocated shift for <font color="red"><b>%s</b></font> for the date %s </li>'%(frappe.db.get_value("Shift Assignment",sa,"department"),pp[0],pp[4])
                            else:
                                err_list += '<li>Shift value missing for <font color="red"><b>%s</b></font> in the upload sheet.</li>'%(pp[0])
                else:
                    li = [pp[1],pp[2],pp[3],pp[4],pp[5],pp[6]]
                    if len(li) != 7:
                        err_list += '<li>ID should not be Empty.</li>'

        return err_list

    # def get_dates(self):
    # 	"""get list of dates in between from date and to date"""
    # 	no_of_days = date_diff(add_days(self.to_date, 1), self.from_date)
    # 	dates = [add_days(self.from_date, i) for i in range(0, no_of_days)]
    # 	return dates

    @frappe.whitelist()
    def show_csv_data(self):
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])
        data_list = ''
        for pp in pps:
            if pp[0] == 'ID':
                data_list += "<tr><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td></tr>"%(pp[0],pp[1],pp[2],pp[3],pp[4],pp[5],pp[6])
            else:
                data_list += "<tr><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td></tr>"%(pp[0],pp[1],pp[2],pp[3],pp[4],pp[5],pp[6])

        return data_list

    @frappe.whitelist()
    def show_summary(self):
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])
        data = ''
        officer_1 = 0
        officer_2 = 0
        officer_3 = 0
        staff_1 = 0
        staff_2 = 0
        staff_3 = 0
        retainer_1 = 0
        retainer_2 = 0
        retainer_3 = 0
        trainee_1 = 0
        trainee_2 = 0
        trainee_3 = 0 
        for pp in pps:
            if pp[3] == 'Officer':
                if pp[6] == "1":
                    officer_1 +=1
                elif pp[6] == "2":
                    officer_2 +=1
                elif pp[6] == "3":
                    officer_3 +=1
            if pp[3] == 'Staff':
                if pp[6] == "1":
                    staff_1 +=1
                elif pp[6] == "2":
                    staff_2 +=1
                elif pp[6] == "3":
                    staff_3 +=1
            if pp[3] == 'Retainer':
                if pp[6] == "1":
                    retainer_1 +=1
                elif pp[6] == "2":
                    retainer_2 +=1
                elif pp[6] == "3":
                    retainer_3 +=1
            if pp[3] == 'Trainee':
                if pp[6] == "1":
                    trainee_1 +=1
                elif pp[6] == "2":
                    trainee_2 +=1
                elif pp[6] == "3":
                    trainee_3 +=1
        total = officer_1+officer_2+officer_3+staff_1+staff_2+staff_3+retainer_1+retainer_2+retainer_3+trainee_1+trainee_2+trainee_3
        data += """
            <td style="background-color:#f0b27a; border: 1px solid black">Shift</td><td style="background-color:#f0b27a ; border: 1px solid black">1</td><td style="background-color:#f0b27a; border: 1px solid black">2</td><td style="background-color:#f0b27a; border: 1px solid black">3</td><td style="background-color:#f0b27a ; border: 1px solid black">Total</td>
            </tr>
            <tr>
                <th style = 'border: 1px solid black'>Officer</th><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style="background-color:#58d68d ; border: 1px solid black">%s</td>
            </tr>
            <tr>
                <th style = 'border: 1px solid black'>Staff</th><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style="background-color:#58d68d ; border: 1px solid black">%s</td>
            </tr>
            <tr>
                <th style = 'border: 1px solid black'>Retainer</th><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td>
            </tr>
            <tr>
                <th style = 'border: 1px solid black'>Trainee</th><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td>
            </tr>
            <tr>
                <td style="background-color:#58d68d; border: 1px solid black">Total</td><td style="background-color:#58d68d; border: 1px solid black">%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td>
            </tr>"""%(officer_1,officer_2,officer_3,(officer_1+officer_2+officer_3),staff_1,staff_2,staff_3,(staff_1+staff_2+staff_3),retainer_1,retainer_2,retainer_3,(retainer_1+retainer_2+retainer_3),trainee_1,trainee_2,trainee_3,(trainee_1+trainee_2+trainee_3),(officer_1+staff_1+retainer_1+trainee_1),(officer_2+staff_2+retainer_2+trainee_2),(officer_3+staff_3+retainer_3+trainee_3),total)

        return data


@frappe.whitelist()
def create_shift_assignment(file,from_date,to_date,name):
    filepath = get_file(file)
    pps = read_csv_content(filepath[1])
    for pp in pps:
        if pp[6] != 'Shift':
            if pp[6]:
                shift_date = datetime.strptime(pp[4],'%d-%m-%Y')
                if pp[6] != 'WO':
                    if not frappe.db.exists("Shift Assignment",{'employee':pp[0],'start_date':shift_date,'end_date':shift_date,'docstatus':['in',[0,1]]}):
                        doc = frappe.new_doc("Shift Assignment")
                        doc.employee = pp[0]
                        doc.shift_type = pp[6]
                        doc.start_date = shift_date
                        doc.end_date = shift_date
                        doc.shift_schedule = name
                        doc.save(ignore_permissions=True)
                        frappe.db.commit()
                elif pp[6] == 'WO':
                    if frappe.db.exists("Holiday List",{'name':pp[0]}):
                        holiday = frappe.get_doc("Holiday List", pp[0])
                        holiday.append("holidays",{
                            "holiday_date":pp[4],
                            "weekly_off":1,
                            "description":"Week Off"
                        })
                        holiday.save(ignore_permissions=True)
                        frappe.db.commit()
                    else:
                        start_date = date(date.today().year, 1, 1)
                        end_date = date(date.today().year, 12, 31)
                        holiday = frappe.new_doc("Holiday List")
                        holiday.holiday_list_name = pp[0]
                        holiday.from_date = start_date
                        holiday.to_date = end_date
                        holiday.append("holidays",{
                            "holiday_date":pp[4],
                            "weekly_off":1,
                            "description":"Week Off"
                        })
                        holiday.save(ignore_permissions=True)
                        frappe.db.commit()
                        frappe.db.set_value('Employee',pp[0],"holiday_list",pp[0])
    frappe.msgprint('Shift Schedule uploaded successfully')    

@frappe.whitelist()
def get_template():
    args = frappe.local.form_dict

    if getdate(args.from_date) > getdate(args.to_date):
        frappe.throw(_("To Date should be greater than From Date"))

    w = UnicodeWriter()
    w = add_header(w)

    try:
        w = add_data(w, args)
    except Exception as e:
        frappe.clear_messages()
        frappe.respond_as_web_page("Holiday List Missing", html=e)
        return	

    # write out response as a type csv
    frappe.response['result'] = cstr(w.getvalue())
    frappe.response['type'] = 'csv'
    frappe.response['doctype'] = "Shift Assignment"

def add_header(w):
    w.writerow(["ID", "Name", "Department","Category","Date","Shift Group","Shift"])
    return w

def add_data(w, args):
    data = get_data(args)
    writedata(w, data)
    return w

@frappe.whitelist()
def get_data(args):
    dates = get_dates(args)
    employees = get_active_employees(args)
    holidays = get_holidays_for_employees([employee.name for employee in employees], args["from_date"], args["to_date"])
    data = []
    for date in dates:
        for employee in employees:
            if getdate(date) < getdate(employee.date_of_joining):
                continue
            if employee.relieving_date:
                if getdate(date) > getdate(employee.relieving_date):
                    continue
            employee_holiday_list = get_holiday_list_for_employee(employee.name)
            row = [
                employee.name, employee.employee_name, employee.department,employee.category,date,employee.shift_group,employee.default_shift
            ]
            if date in holidays[employee_holiday_list]:
                row[6] =  "Holiday"
            data.append(row)
    return data

def get_holidays_for_employees(employees, from_date, to_date):
    holidays = {}
    for employee in employees:
        holiday_list = get_holiday_list_for_employee(employee)
        holiday = get_holidays_for_employee(employee, getdate(from_date), getdate(to_date))
        if holiday_list not in holidays:
            holidays[holiday_list] = holiday

    return holidays

def writedata(w, data):
    for row in data:
        w.writerow(row)

def get_dates(args):
    """get list of dates in between from date and to date"""
    no_of_days = date_diff(add_days(args["to_date"], 1), args["from_date"])
    dates = [add_days(args["from_date"], i) for i in range(0, no_of_days)]
    return dates

def get_active_employees(args):
    employees = frappe.db.get_all('Employee',
        fields=['name', 'employee_name', 'department', 'date_of_joining', 'company', 'relieving_date','default_shift','category','shift_group'],
        filters={
            'docstatus': ['<', 2],
            'status': 'Active',
            'department': (args["department"]).replace("1","&")
        }
    )
    return employees

# @frappe.whitelist()
# def shift_wise_count(doc):
# 	employee_type = ["BC","WC","CL","NT","FT"]
# 	data = "<table class='table table-bordered'><tr><td colspan='2' style='background-color:#f0b27a'><center>Shift 1</center></td><td colspan='2' style='background-color:#f0b27a'><center>Shift 2</center></td><td colspan='2' style='background-color:#f0b27a'><center>Shift 3</center></td><td colspan='2' style='background-color:#f0b27a'><center>Shift PP1</center></td><td colspan='2' style='background-color:#f0b27a'><center>Shift PP2</center></td><td colspan='2' style='background-color:#f0b27a'><center>Total Head Count</center></td></tr>"
# 	for emp_type in employee_type:
# 		s1 = 0
# 		s2 = 0
# 		s3 = 0
# 		spp1 = 0
# 		spp2 = 0
# 		shift1 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '1' and docstatus != 2 and start_date = '%s' and employee_type = '%s' "%(doc.from_date,emp_type),as_dict=True)
# 		shift2 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '2' and docstatus != 2 and start_date = '%s' and employee_type = '%s' "%(doc.from_date,emp_type),as_dict=True)
# 		shift3 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '3' and docstatus != 2 and start_date = '%s' and employee_type = '%s' "%(doc.from_date,emp_type),as_dict=True)
# 		shiftpp1 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = 'PP1' and docstatus != 2 and start_date = '%s' and employee_type = '%s' "%(doc.from_date,emp_type),as_dict=True)
# 		shiftpp2 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = 'PP2' and docstatus != 2 and start_date = '%s' and employee_type = '%s' "%(doc.from_date,emp_type),as_dict=True)
# 		if shift1:
# 			s1 = shift1[0].count
# 		if shift2:
# 			s2 = shift2[0].count
# 		if shift3:
# 			s3 = shift3[0].count
# 		if shiftpp1:
# 			spp1 = shiftpp1[0].count
# 		if shiftpp2:
# 			spp2 = shiftpp2[0].count
# 		total = s1+s2+s3+spp1+spp2
# 		data += '<tr><td style="background-color:#58d68d">%s</td><td>%s</td><td style="background-color:#58d68d">%s</td><td>%s</td><td style="background-color:#58d68d">%s</td><td>%s</td><td style="background-color:#58d68d">%s</td><td>%s</td><td style="background-color:#58d68d">%s</td><td>%s</td><td style="background-color:#58d68d">%s</td><td>%s</td></tr>'%(emp_type,s1,emp_type,s2,emp_type,s3,emp_type,spp1,emp_type,spp2,emp_type,total)
# 	sf1 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '1' and docstatus != 2 and start_date = '%s' "%(doc.from_date),as_dict=True)
# 	sf2 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '2' and docstatus != 2 and start_date = '%s' "%(doc.from_date),as_dict=True)
# 	sf3 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '3' and docstatus != 2 and start_date = '%s' "%(doc.from_date),as_dict=True)
# 	sfpp1 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = 'PP1' and docstatus != 2 and start_date = '%s' "%(doc.from_date),as_dict=True)
# 	sfpp2 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = 'PP2' and docstatus != 2 and start_date = '%s' "%(doc.from_date),as_dict=True)

# 	data += '<tr><td style="background-color:#f0b27a">Total</td><td>%s</td><td style="background-color:#f0b27a">Total</td><td>%s</td><td style="background-color:#f0b27a">Total</td><td>%s</td><td style="background-color:#f0b27a">Total</td><td>%s</td><td style="background-color:#f0b27a">Total</td><td>%s</td><td style="background-color:#f0b27a">Total</td><td>%s</td></tr>'%(sf1[0].count,sf2[0].count,sf3[0].count,sfpp1[0].count,sfpp2[0].count,sf1[0].count+sf2[0].count+sf3[0].count+sfpp1[0].count+sfpp2[0].count)
# 	data = data + '</table>' 
# 	return data


# @frappe.whitelist()
# def shift_employees(doc,shift):
# 	shift_emp = frappe.db.sql("select employee,employee_name from `tabShift Assignment` where shift_type = '%s' and docstatus != 2 and start_date = '%s' "%(shift,doc.from_date),as_dict=True)
# 	data = "<table class='table table-bordered'><tr><td style='background-color:#f0b27a'><center>S.No</center></td><td colspan='2' style='background-color:#f0b27a'><center>Shift %s</center></td></tr>"%(shift)
# 	if shift_emp:
# 		i = 1
# 		for s in shift_emp:
# 			data += '<tr><td style="background-color:#f0b27a">%s</td><td style="background-color:#58d68d">%s</td><td>%s</td></tr>'%(i,s.employee,s.employee_name)
# 			i += 1
# 	else:
# 		data += '<tr><td></td><td></td></tr>'
# 	data = data + '</table>'
# 	return data