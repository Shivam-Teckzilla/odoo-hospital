from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    # to add chatter
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"
    _order = 'id desc'  # to give ascending(asc) and descending(desc) order

    name = fields.Char(string="Name", tracking=True)  # tracking use to track data in chatter field
    date_of_birth = fields.Date(string='Date of birth', )
    is_birthday = fields.Boolean(string='Is Birthday', compute='_compute_is_birthday')
    age = fields.Integer(string="Age", tracking=True,
                         compute='_compute_age',
                         search="_search_age",
                         inverse='_inverse_compute_age')  # compute use to define method and we cannot use compute in search view
    # (compute) and it will not accept manually entry
    # (compute) and it is not store in database
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('other', 'Other')], string="Gender", tracking=True)
    # to archive th field
    active = fields.Boolean(string="Active", default=True, tracking=True)
    ref = fields.Char(string="Reference")
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string='Tags')
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    # variable(display_name) name should be same method(_compute_display_name) name any thing
    display_name = fields.Char(string="Name", compute='_compute_display_name')
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')
    appointment_ids = fields.One2many("hospital.appointment", "patient_id", string="Appointments")

    parent = fields.Char(string="parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status")
    parent_name = fields.Char(string="Parent Name")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="WebSite")

    @api.depends('date_of_birth')
    def _compute_age(self):  # this filed depends on up to  (@api.depends('date_of_birth') ) decorator
        # if singleton error show use for loop and iterate
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)
        return

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    # to override create method
    @api.model
    def create(self, vals):
        # to set a default value
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    # to override write method
    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('ref', 'name')
    def _compute_display_name(self):
        for patient in self:
            patient.display_name = str(patient.ref) + " " + str(patient.name)

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_(' the entered date not accepted'))

    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #     for rec in self:
    #         rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        appointment_group = self.env['hospital.appointment'].read_group(domain=[],
                                                                        fields=['patient_id'], groupby=['patient_id'])
        for appointment in appointment_group:
            patient_id = appointment.get('patient_id')[0]
            patient_rec = self.browse(patient_id)
            patient_rec.appointment_count = appointment['patient_id_count']
            self -= patient_rec
        self.appointment_count = 0

    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_(' you cant delete a patient with appointment !!'))

    def action_test(self):
        print("Click M e")

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    def action_view_appointment(self):
        return {
            'name': _('Appointment'),
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }
