import datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment", domain=[('state', '=', 'draft')])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    # to get default method
    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        return res

    def action_cancel(self):
        if self.appointment_id.booking_date == fields.Date.today():
            raise ValidationError(_("sorry"))
        line_id = self.env.context.get('active_id')
        appointment_id = self.env['hospital.appointment'].search([('id', '=', line_id)])
        appointment_id.state = 'cancel'
        # to use reload  the page
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
