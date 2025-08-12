import requests
from datetime import datetime
from odoo import models, api
from odoo.exceptions import UserError

class IdenfitLeaveSync(models.Model):
    _name = "idenfit.leave.sync"
    _description = "İdenfit izin senkronizasyonu"

    @api.model
    def sync_leaves_from_idenfit(self):
        token = "Bearer YOUR_ACCESS_TOKEN"
        url = "https://integration.idenfit.com/graphql"

        query = """
        {
          filterLeaveRequests(criteria: {leaveRequestStatus: "APPROVED"}) {
            id
            leaveType { name }
            employee { identityNumber firstName lastName }
            beginLeaveRequestDay { date }
            endLeaveRequestDay { date }
            explanation
          }
        }
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': token,
            'origin': 'https://integration.idenfit.com',
        }

        response = requests.post(url, json={'query': query}, headers=headers)
        if response.status_code != 200:
            raise UserError(f"API Error: {response.text}")

        data = response.json().get("data", {}).get("filterLeaveRequests", [])
        for leave in data:
            emp = self.env['hr.employee'].search([('identification_id', '=', leave["employee"]["identityNumber"])], limit=1)
            if not emp:
                continue

            start_date = datetime.strptime(leave['beginLeaveRequestDay']['date'], "%Y-%m-%d")
            end_date = datetime.strptime(leave['endLeaveRequestDay']['date'], "%Y-%m-%d")

            # Takvim etkinliği oluşturma
            self.env['calendar.event'].create({
                'name': f"{emp.name} - {leave['leaveType']['name']}",
                'start': start_date,
                'stop': end_date,
                'allday': True,
                'attendee_ids': [(4, emp.user_id.partner_id.id)] if emp.user_id and emp.user_id.partner_id else [],
            })
