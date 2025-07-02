from odoo import models, fields, api, _
from odoo.exceptions import UserError

class WhatsappMassMessageWizard(models.TransientModel):
    _name = 'whatsapp.mass.message.wizard'
    _description = 'Send WhatsApp Message to Many'

    template_id = fields.Many2one('whatsapp.template', required=True)
    recipient_type = fields.Selection([
        ('individual', 'Selected Customers'),
        ('all', 'All Customers'),
    ], default='individual', required=True)
    partner_ids = fields.Many2many('res.partner', string="Recipients")
    preview = fields.Text("Preview", compute='_compute_preview')

    @api.depends('template_id', 'partner_ids')
    def _compute_preview(self):
        for wizard in self:
            if wizard.template_id and wizard.partner_ids:
                wizard.preview = wizard.template_id.body_text.format(
                    name=wizard.partner_ids[0].name
                )
            else:
                wizard.preview = ''

    def action_send_messages(self):
        if self.recipient_type == 'all':
            partners = self.env['res.partner'].search([('x_whatsapp_no', '!=', False)])
        else:
            partners = self.partner_ids

        for partner in partners:
            message = self.template_id.body_text.format(name=partner.name)
            self.env['whatsapp.compose.message'].create({
                'partner_id': partner.id,
                'message': message,
            }).action_send_message()
        return {'type': 'ir.actions.act_window_close'} 