from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # === Fields from your list ===
    # General & Branch Info
    x_cust_code = fields.Char('Customer Code')
    x_branch_name = fields.Char('Branch Name')
    x_branch_code = fields.Char('Branch Code')
    x_params = fields.Char('Params')
    # Contact Holders
    x_holder1 = fields.Char('Holder 1')
    x_holder2 = fields.Char('Holder 2')
    x_holder3 = fields.Char('Holder 3')
    # Status & Category
    x_account_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_hold', 'On Hold'),
    ], string='Account Status', default='active')
    x_payment_method = fields.Char('Payment Method')
    x_business_category = fields.Char('Business Category')
    x_business_type = fields.Char('Business Type')
    # Mailing
    x_mailing_code = fields.Char('Mailing Code')
    x_mail_shot = fields.Boolean('Mail Shot')
    x_vat_exempt = fields.Boolean('VAT Exempt')
    # Banking & Financial
    x_bank_sort_code = fields.Char('Bank Sort Code')
    x_bank_acc_no = fields.Char('Bank Account No.')
    x_ledger_account = fields.Char('Ledger Account')
    x_settlement_terms_desc = fields.Char('Settlement Terms Description')
    # Credit Control
    x_cheque_limit = fields.Monetary('Cheque Limit', currency_field='currency_id')
    x_iou_limit = fields.Monetary('IOU Limit', currency_field='currency_id')
    x_total_limit = fields.Monetary('Total Limit', currency_field='currency_id')
    x_credit_check = fields.Boolean('Credit Check Required')
    # Discounts
    x_trade_discount_cc = fields.Float('Trade Discount (CC %)')
    x_trade_discount_del = fields.Float('Trade Discount (DEL %)')
    x_settlement_discount = fields.Float('Settlement Discount %')
    x_hierarchy_discount = fields.Float('Hierarchy Discount %')
    # History & Routing
    x_date_opened = fields.Date('Date Opened')
    x_notes_legacy = fields.Text('Legacy Notes')
    x_route = fields.Char('Route')
    x_drop_number = fields.Integer('Drop Number')
    x_last_visit = fields.Date('Last Visit Date')
    # Legacy Sales Values
    x_ty_sales_value = fields.Monetary('This Year Sales Value', currency_field='currency_id')
    x_ly_sales_value = fields.Monetary('Last Year Sales Value', currency_field='currency_id')
    x_av_sales_value = fields.Monetary('Average Sales Value', currency_field='currency_id')
    # Legacy Track & Trace
    x_tpd_eoid = fields.Char('Legacy TPD EOID')
    x_tpd_fid = fields.Char('Legacy TPD FID')