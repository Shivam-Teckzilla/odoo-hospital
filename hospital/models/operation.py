from odoo import api, fields, models, _


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    _log_access = False
    _rec_name = 'operation_name'

    doctor_id = fields.Many2one('res.users', string="Doctor")
    operation_name = fields.Char(string="Name")
    reference_record = fields.Reference(selection=[('hospital.patient', 'Patient'),
                                                   ('hospital.appointment', 'Appointment')], string="Record")
    sequence = fields.Integer(string="Sequence", default=10)

    # to store created value in db
    @api.model
    def name_create(self, name):
        record = self.create({'operation_name': name})
        return record.id, record.display_name
