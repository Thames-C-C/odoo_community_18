from odoo import models, fields, _
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Branch & Customer Info
    x_cust_code = fields.Char(string='Customer Code')
    x_branch_name = fields.Char(string='Branch Name')
    x_branch_code = fields.Char(string='Branch Code')
    x_business_category = fields.Selection([
        ('convenience_grocery', 'Convenience Grocery'),
        ('ctn', 'CTN'),
        ('off_licence', 'Off Licence'),
        ('chemists', 'Chemists'),
        ('restaurants', 'Restaurants'),
        ('caterers', 'Caterers'),
        ('bars_and_pubs', 'Bars and Pubs'),
        ('export', 'Export'),
        ('trc_club_members', 'TRC Club Members'),
        ('symbol_group_member', 'Symbol Group Member'),
        ('bv_customer', 'B&V Customer'),
    ], string='Business Category')
    x_business_type = fields.Char(string='Business Type')
    x_params = fields.Char(string='PARAMS')

    # Account Information
    x_account_status = fields.Selection([
        ('live', 'Live'),
        ('potential', 'Potential'),
        ('stopped', 'Stopped'),
        ('deleted', 'Deleted')
    ], string='Account Status')
    x_sales_rep_name = fields.Selection([
        ('ashraf', 'Ashraf'),
        ('charmil', 'CHARMIL'),
        ('dhaval', 'DHAVAL'),
        ('diya_patel', 'DIYA PATEL'),
        ('umang_sahil', 'UMANG / SAHIL')
    ], string='Representative')
    x_payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('credit_card', 'Credit Card'),
        ('delivered', 'Delivered')
    ], string='Payment Method')
    x_date_opened = fields.Date(string='Date Opened')
    x_main_account_ref = fields.Char(string='Main Account')
    x_main_account_branch_name = fields.Char(string='Main Account Branch')
    x_whatsapp_no = fields.Char(string='WhatsApp No')

    # Contact Holders
    x_holder1 = fields.Char(string='Holder 1')
    x_holder2 = fields.Char(string='Holder 2')
    x_holder3 = fields.Char(string='Holder 3')

    # Mailing & VAT
    x_mailing_code = fields.Selection([
        ('birmingham', 'Birmingham'),
        ('bristol', 'Bristol'),
        ('cardiff', 'Cardiff'),
        ('leeds', 'Leeds'),
        ('manchester', 'Manchester'),
        ('stockport', 'Stockport')
    ], string='Mailing Code')
    x_mail_shot = fields.Boolean(string='Mail Shot')
    x_vat_exempt = fields.Selection([
        ('t0', 'Export EU: T0'),
        ('t4', 'Export Non-EU: T4')
    ], string='VAT Exempt')

    # Banking & Settlement
    x_bank_sort_code = fields.Char(string='Bank Sort Code')
    x_bank_acc_no = fields.Char(string='Bank Acc No')
    x_ledger_account_ref = fields.Char(string='Ledger Account')
    x_settlement_terms = fields.Char(string='Settlement Terms')
    x_settlement_terms_desc = fields.Char(string='Settlement Terms Desc')

    # Credit Control
    x_cheque_limit = fields.Float(string='Cheque Limit')
    x_iou_limit = fields.Float(string='IOU Limit')
    x_total_limit = fields.Float(string='Total Limit')
    x_credit_check = fields.Boolean(string='Credit Check')

    # Discounts
    x_trade_discount_cc = fields.Float(string='Trade Discount C&C (%)')
    x_trade_discount_del = fields.Float(string='Trade Discount DEL (%)')
    x_settlement_discount = fields.Float(string='Settlement Discount (%)')
    x_hierarchy_discount = fields.Float(string='Hierarchy Discount (%)')

    # Routing & History
    x_route = fields.Selection([
        ('leeds', 'Leeds'),
        ('london', 'London'),
        ('manchester', 'Manchester'),
        ('rochdale', 'Rochdale'),
        ('birmingham', 'Birmingham')
    ], string='Route')
    x_drop_number = fields.Integer(string='Drop Number')
    x_last_visit = fields.Date(string='Last Visit Date')
    x_container = fields.Selection([
        ('cages', 'Cages'),
        ('pallets', 'Pallets')
    ], string='Container')
    x_dms_customer_type = fields.Selection([
        ('bonded', 'BONDED : Bonded Deliveries'),
        ('dippriv', 'DIPPRIV : Diplomatic Privelage'),
        ('export', 'EXPORT : Export'),
        ('nonbonded', 'NONBONDED : Homeuse Deliveries'),
        ('vforces', 'VFORCES : Visiting Forces')
    ], string='DMS Customer Type')
    x_edi_provider = fields.Selection([
        ('fourth', 'FourthHospitalityEDI'),
        ('pelican', 'PelicanEDI')
    ], string='EDI Provider')


    # Legacy Sales Values
    x_ty_sales_value = fields.Float(string='TY Sales Value')
    x_ly_sales_value = fields.Float(string='LY Sales Value')
    x_av_sales_value = fields.Float(string='AV Sales Value')

    # Tobacco Products Directive (TPD)
    x_tpd_eoid = fields.Char(string='TPD Economic Operator ID')
    x_tpd_fid = fields.Char(string='TPD Facility ID')

    x_legacy_notes = fields.Text(string='Legacy Notes')

    def action_open_whatsapp_wizard(self):
        """
        Opens the wizard to compose a WhatsApp message.
        """
        self.ensure_one()
        if not self.x_whatsapp_no:
            raise UserError("This customer does not have a WhatsApp number.")
            
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'whatsapp.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
                'default_message': f"Hello {self.name}, "
            }
        }