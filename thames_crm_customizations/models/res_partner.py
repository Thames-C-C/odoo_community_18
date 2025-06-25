from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Add company_currency_id to be used by monetary fields
    company_currency_id = fields.Many2one(
        related='company_id.currency_id',
        string="Company Currency",
        readonly=True,
        store=True,
    )

    # --- CUSTOMER FINANCIAL DATA ---
    x_cheque_limit = fields.Monetary(
        string='Cheque Limit',
        currency_field='company_currency_id',
    )
    x_credit_limit = fields.Monetary(
        string='Credit Limit',
        currency_field='company_currency_id',
    )
    x_credit_balance = fields.Monetary(
        string='Credit Balance',
        currency_field='company_currency_id',
    )
    x_security_cheque_amount = fields.Monetary(
        string='Security Cheque Amount',
        currency_field='company_currency_id',
    )
    x_bank_guarantee_amount = fields.Monetary(
        string='Bank Guarantee Amount',
        currency_field='company_currency_id',
    )
    x_total_exposure = fields.Monetary(
        string='Total Exposure',
        currency_field='company_currency_id',
        compute='_compute_total_exposure',
        store=True,
    )
    x_due_invoices_amount = fields.Monetary(
        string='Due Invoices Amount',
        currency_field='company_currency_id',
    )
    x_overdue_invoices_amount = fields.Monetary(
        string='Overdue Invoices Amount',
        currency_field='company_currency_id',
    )

    # --- OTHER CUSTOM FIELDS ---
    x_customer_classification = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ], string='Customer Classification')
    x_customer_since = fields.Date(string='Customer Since')
    x_last_activity_date = fields.Date(string='Last Activity Date')
    x_primary_contact_person = fields.Char(string='Primary Contact Person')
    x_secondary_contact_person = fields.Char(string='Secondary Contact Person')
    x_business_segment = fields.Char(string='Business Segment')
    x_delivery_route_code = fields.Char(string='Delivery Route Code')
    x_is_tax_exempt = fields.Boolean(string='Is Tax Exempt')
    x_tax_exemption_number = fields.Char(string='Tax Exemption Number')
    x_customer_notes = fields.Text(string='Customer Notes')
    x_preferred_communication = fields.Selection([
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('sms', 'SMS')
    ], string='Preferred Communication')

    @api.depends('x_credit_balance', 'x_security_cheque_amount', 'x_bank_guarantee_amount')
    def _compute_total_exposure(self):
        for partner in self:
            partner.x_total_exposure = partner.x_credit_balance + partner.x_security_cheque_amount + partner.x_bank_guarantee_amount 