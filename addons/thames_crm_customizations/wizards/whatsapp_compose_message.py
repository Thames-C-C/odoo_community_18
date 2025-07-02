from odoo import models, fields, _, api
from odoo.exceptions import UserError
import requests
import logging
import re
import json

_logger = logging.getLogger(__name__)

class WhatsappComposeMessage(models.TransientModel):
    _name = 'whatsapp.compose.message'
    _description = 'Compose WhatsApp Message'

    template_id = fields.Many2one('whatsapp.template', 'Template', required=True)
    partner_id = fields.Many2one('res.partner', 'Recipient', readonly=True)
    
    preview = fields.Text(string="Preview", compute='_compute_preview', readonly=True)

    @api.depends('template_id', 'partner_id')
    def _compute_preview(self):
        for rec in self:
            if rec.template_id and rec.partner_id and rec.template_id.body_text:
                try:
                    rec.preview = rec.template_id.body_text.format(name=rec.partner_id.name)
                except KeyError:
                    rec.preview = rec.template_id.body_text
            else:
                rec.preview = ""

    def action_send_message(self):
        """
        Sends the selected WhatsApp template to the partner using the Meta Cloud API.
        """
        self.ensure_one()
        if not self.partner_id.x_whatsapp_no:
            raise UserError(_("Recipient %s does not have a WhatsApp number.", self.partner_id.name))

        params = self.env['ir.config_parameter'].sudo()
        access_token = params.get_param('meta.whatsapp.api_token')
        phone_number_id = params.get_param('meta.whatsapp.phone_number_id')
        api_version = params.get_param('meta.whatsapp.api_version', 'v18.0')

        if not all([access_token, phone_number_id]):
            raise UserError(_("Meta WhatsApp API is not configured. Please set 'meta.whatsapp.api_token' and 'meta.whatsapp.phone_number_id' in System Parameters."))

        api_url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"
        
        raw_number = self.partner_id.x_whatsapp_no
        recipient_number = re.sub(r'\D', '', raw_number)
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_number,
            "type": "template",
            "template": {
                "name": self.template_id.name,
                "language": {
                    "code": self.template_id.language
                }
            }
        }
        
        components = []
        try:
            template_components = json.loads(self.template_id.components_json or '[]')
            body_component = next((c for c in template_components if c['type'] == 'BODY'), None)
            
            if body_component and body_component.get('example', {}).get('body_text', [[]])[0]:
                components.append({
                    "type": "body",
                    "parameters": [{"type": "text", "text": self.partner_id.name}]
                })
        except (json.JSONDecodeError, StopIteration, KeyError) as e:
            _logger.info(f"Could not parse components for template '{self.template_id.name}'. Sending without personalization. Error: {e}")

        if components:
            payload['template']['components'] = components
        
        _logger.info(f"Sending WhatsApp template '{self.template_id.name}' to {recipient_number} via Meta API.")

        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            
            response_json = response.json()
            message_id = response_json.get('messages', [{}])[0].get('id')

            _logger.info(f"WhatsApp message sent successfully. Message ID: {message_id}")
            self.partner_id.message_post(body=_("WhatsApp template '%s' sent via Meta.", self.template_id.name))
        
        except requests.exceptions.HTTPError as e:
            _logger.error(f"Failed to send WhatsApp message via Meta API (HTTPError): {e.response.text}")
            raise UserError(_("Meta API Error: %s", e.response.text))
        except requests.exceptions.RequestException as e:
            _logger.error(f"Failed to send WhatsApp message via Meta API (RequestException): {e}")
            raise UserError(_("Connection Error: Could not connect to Meta API. %s", e))
        except Exception as e:
            _logger.error(f"An unexpected error occurred while sending WhatsApp message: {e}")
            raise UserError(_("An unexpected error occurred: %s", e))

        return {'type': 'ir.actions.act_window_close'}