from odoo import api, fields, models

class Department(models.Model):
    _name = 'clinic.department'


    name = fields.Selection([
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
    ], string="Department Name", required=True)
    doctor_ids=fields.One2many('clinic.doctor','department_id')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name is already in use.')
    ]
    active=fields.Boolean(default=True)

    ref=fields.Char(default="New",readonly=True)

    @api.model
    def create(self,vals):
        res=super(Department,self).create(vals)
        if res.ref=='New':
            res.ref=self.env['ir.sequence'].next_by_code('dept_seq')
            return res