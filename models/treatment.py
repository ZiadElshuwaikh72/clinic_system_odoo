from odoo import models, fields, api

class Treatment(models.Model):
    _name = 'clinic.treatment'

    name = fields.Char(string='Treatment Name', required=True)
    appointment_id=fields.Many2one('clinic.appointment',string='Appointment')
    description=fields.Char()
    cost=fields.Float()
    patient_id=fields.Many2one('clinic.patient',string='Patient')
    active = fields.Boolean(default=True)

    ref=fields.Char(default='New',readonly=True)

    @api.model
    def create(self,vals):
        res=super(Treatment,self).create(vals)
        if res.ref=='new':
            res.ref=self.env['ir.sequence'].next_by_code('treat_seq')
            return res

