from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AppointmentPatient(models.Model):
    _name = "hospital.appointment"
    # to add chatter
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'ref'  # to  change the model name to actually name also change Many2onne value

    # Many2one field fetch the data to another table and show me the dropdown(comodel_name)
    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Name", tracking=2, ondelete="restrict")
    # default = fields.Datetime.now to use current dat and time
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now, tracking=2)
    # default = fields.Date.context_today to use current date
    booking_date = fields.Date(string='Booking date', tracking=3, default=fields.Date.context_today)
    # to related field fetch data to another model using Many2one
    gender = fields.Selection(related='patient_id.gender', string="Gender", tracking=4)
    ref = fields.Char(string="Reference", tracking=1)
    prescription = fields.Html(string="Prescription", tracking=5)  # to add HTML fields
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low',),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")  # to add priority
    state = fields.Selection([('draft', 'Draft'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')], default="draft", string="Status",
                             required=True)  # to add statusbar
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_line_ids = fields.One2many('hospital.pharmacy.lines', 'appointment_id', string="Pharmacy Lines")
    operation_id = fields.Many2one('hospital.operation', string="Operation")
    progress = fields.Integer(string="Progress", compute="_compute_progress")
    duration = fields.Float(string="Duration")

    company_id = fields.Many2one("res.company", string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    # to use on change
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.amazon.in/?&tag=googhydrabk1-21&ref=pd_sl_7hz2t19t5c_e&adgrpid=155259815513&hvpone=&hvptwo=&hvadid=674842289437&hvpos=&hvnetw=g&hvrand=15274951349850679754&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062215&hvtargid=kwd-10573980&hydadcr=14453_2316415&gad_source=1',
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("you can delete  appointment only  with 'Draft' state"))
        return super(AppointmentPatient, self).unlink()

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = 25
            elif rec.state == 'in_consultation':
                progress = 50
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    def action_share_whatsapp(self):
        if self.patient_id.phone:
            msg = 'Hii %s' % self.patient_id.name
            whatspp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone, msg)
        else:
            raise ValidationError(_("Missing Phone number in patient records"))
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatspp_api_url
        }


class AppointmentPharmacyLines(models.Model):
    _name = "hospital.pharmacy.lines"
    _description = "Appointment Pharmacy Lines "

    product_id = fields.Many2one('product.product')
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    price_subtotal = fields.Monetary(string="Subtotal", compute='_compute_price_subtotal')
    currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')

    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty
