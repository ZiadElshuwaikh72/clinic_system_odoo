from odoo import models, fields,api

class Doctor(models.Model):
    _name = 'clinic.doctor'

    name = fields.Char(required=True)
    phone = fields.Char(required=True)
    email = fields.Char()
    specialization= fields.Selection([
        ('general', 'General Practitioner'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedics', 'Orthopedics'),
        ('neurology', 'Neurology'),
        ('dentistry', 'Dentistry'),
        ('ophthalmology', 'Ophthalmology'),
        ('psychiatry', 'Psychiatry'),
        ('surgery', 'Surgery'),
        ('gynecology', 'Gynecology'),
        ('urology', 'Urology'),
        ('radiology', 'Radiology'),
        ('anesthesiology', 'Anesthesiology'),
    ],required=True)

    patient_ids=fields.One2many('clinic.patient','doctor_id')
    department_id=fields.Many2one('clinic.department')
    appointment_ids=fields.One2many('clinic.appointment','doctor_id')
    active=fields.Boolean(default=True)

    ref=fields.Char(default='New',readonly=True)

    @api.model
    def create(self,vals):
        res = super(Doctor, self).create(vals)
        if res.ref=='New':
            res.ref=self.env['ir.sequence'].next_by_code('doctor_seq')
            return res