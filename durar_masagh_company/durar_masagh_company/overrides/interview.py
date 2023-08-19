import frappe
from erpnext.hr.doctype.interview.interview import Interview


class CustomInterview(Interview):


    @frappe.whitelist()
    def get_applicant_name(self):
        try:
            applicant_name = frappe.db.get_value('Job Applicant', self.job_applicant, 'applicant_name')
            return applicant_name
        except:
            return None