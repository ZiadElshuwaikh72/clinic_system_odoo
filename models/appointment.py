from odoo import fields, models,api
from datetime import datetime, timedelta

from odoo.exceptions import ValidationError


class Appointment(models.Model):
    _name = 'clinic.appointment'

    doctor_id = fields.Many2one('clinic.doctor')
    patient_id=fields.Many2one('clinic.patient')
    date_time=fields.Datetime(required=True,string='Appointment Date',default=fields.Datetime.now)
    status=fields.Selection([
        ('new','New'),
        ('confirmed','Confirmed'),
        ('done','Done'),
        ('cancelled','Cancelled'),
    ],default='new',string='Appointment Status')

    treatment_ids=fields.One2many('clinic.treatment','appointment_id')
    active=fields.Boolean(default=True)

    ref=fields.Char(default="New",readonly=True)

    @api.model
    def create(self,vals):
        res=super(Appointment,self).create(vals)
        if res.ref=='New':
            res.ref=self.env['ir.sequence'].next_by_code('appoint_seq')
            return res

    # def action_new(self):
    #     for rec in self:
    #         rec.status = 'new'

    def action_confirmed(self):
        for rec in self:
            rec.status = 'confirmed'

    def action_done(self):
        for rec in self:
            rec.status = 'done'

    def action_cancelled(self):
        for rec in self:
            rec.status = 'cancelled'


    @api.constrains('doctor_id','date_time')
    def _check_doctor_availability(self):
        for rec in self:
            existing=self.search([
                ('doctor_id','=',rec.doctor_id.id),
                ('date_time','=',rec.date_time),
                ('id','!=',rec.id)
            ])
            if existing:
                raise ValidationError('This doctor already has an appointment at this time')


    @api.constrains('date_time')
    def _check_date_time(self):
        for rec in self:
            if rec.date_time<fields.Datetime.now():
                    raise ValidationError("Appointment Date cannot be in the past")

    def unlink(self):
        for rec in self:
            if rec.status=='confirmed':
                raise ValidationError('you cannot delete confirmed appointments')
        return super(Appointment, self).unlink()