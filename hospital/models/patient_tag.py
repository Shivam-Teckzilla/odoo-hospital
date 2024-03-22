from odoo import api, fields, models, _


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tags"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string='color')
    color2 = fields.Char(string='color 2')

    _sql_constraints = [
        ('unique_tag_name', 'unique (name)', 'Each name must be unique.'),
    ]

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (Copy)", self.name)
        return super(PatientTag, self).copy(default=default)
