from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Add your new field here
    account_type = fields.Selection([
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ], string='Account Type', default='standard')