from odoo import models,fields,api

class Patient(models.Model):
    _name = 'clinic.patient'
    _inherit=['mail.thread', 'mail.activity.mixin']

    name=fields.Char(required=True,tracking=True)
    ref=fields.Char(default='New',readonly=True)
    birth_date=fields.Date(tracking=True)
    gender=fields.Selection([
        ('male','Male'),
        ('female','Female')
    ])
    address=fields.Char(tracking=True)
    phone=fields.Char(tracking=True)
    active=fields.Boolean(default=True)

    doctor_id=fields.Many2one('clinic.doctor',required=True)
    appointment_ids=fields.One2many('clinic.appointment','patient_id')
    invoice_ids=fields.One2many('clinic.invoice','patient_id')
    treatment_ids=fields.One2many('clinic.treatment','patient_id')

    appointment_count=fields.Integer(compute='_compute_appointment_count')

    #method related with sequence
    @api.model
    def create(self,vals):
        res = super(Patient,self).create(vals)
        if res.ref=='New':
            res.ref=self.env['ir.sequence'].next_by_code('patient_seq')
        return res

    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count=self.env['clinic.appointment'].search_count([('patient_id','=',rec.id)])

    # method related smart buttons
    def action_view_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'clinic.appointment',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
        }

    def action_view_treatments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Treatments',
            'res_model': 'clinic.treatment',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
        }