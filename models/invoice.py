
from odoo.exceptions import ValidationError

from odoo import api, fields, models

class Invoice(models.Model):
    _name = 'clinic.invoice'
    _rec_name = 'patient_id'

    patient_id=fields.Many2one('clinic.patient',string='Patient')
    treatment_ids=fields.Many2many('clinic.treatment',string='Treatment')
    total_amount=fields.Float(compute='_compute_total_amount')
    status=fields.Selection([
        ('draft','Draft'),
        ('paid','Paid'),
        ('cancel','Cancel'),
    ],default='draft')
    active=fields.Boolean(default=True)

    @api.depends('treatment_ids.cost')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount=sum(rec.treatment_ids.mapped('cost'))

    ref=fields.Char(default='New',readonly=True)

    @api.model
    def create(self,vals):
        res=super(Invoice,self).create(vals)
        if res.ref=='New':
            res.ref=self.env['ir.sequence'].next_by_code('invoice_seq')
            return res



    # def action_draft(self):
    #     for rec in self:
    #         rec.status='draft'

    def action_paid(self):
        for rec in self:
            rec.status='paid'

    def action_cancel(self):
        for rec in self:
            rec.status='cancel'

    @api.constrains('treatment_ids')
    def _check_treatment_ids(self):
        for rec in self:
            if not rec.treatment_ids:
                raise ValidationError("You cannot create an invoice without a treatment")