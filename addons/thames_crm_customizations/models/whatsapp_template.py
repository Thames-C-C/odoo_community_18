from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)

class WhatsAppTemplate(models.Model):
    _name = 'whatsapp.template'
    _description = 'WhatsApp Message Template'
    _order = 'name'

    name = fields.Char(string="Template Name", required=True)
    body_text = fields.Text(string="Body")
    language = fields.Char(string="Language", required=True)
    status = fields.Char(string="Status", readonly=True)
    category = fields.Char(string="Category")
    components_json = fields.Text(string="Components JSON", readonly=True)

    def action_sync_templates_from_meta(self):
        """
        Connects to the Meta API to fetch all approved message templates
        and creates/updates them in Odoo.
        """
        params = self.env['ir.config_parameter'].sudo()
        access_token = params.get_param('meta.whatsapp.api_token')
        waba_id = params.get_param('meta.whatsapp.business_account_id') # We need the WhatsApp Business Account ID for this
        api_version = params.get_param('meta.whatsapp.api_version', 'v18.0')

        if not all([access_token, waba_id]):
            raise UserError(_("Meta WhatsApp API is not fully configured for template sync. Please set 'meta.whatsapp.api_token' and 'meta.whatsapp.business_account_id' in System Parameters."))

        api_url = f"https://graph.facebook.com/{api_version}/{waba_id}/message_templates"
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            response = requests.get(api_url, headers=headers, timeout=15)
            response.raise_for_status()
            templates_data = response.json().get('data', [])
            
            _logger.info(f"Found {len(templates_data)} templates from Meta.")

            for template_data in templates_data:
                existing_template = self.search([('name', '=', template_data['name']), ('language', '=', template_data['language'])])
                
                vals = {
                    'name': template_data['name'],
                    'language': template_data['language'],
                    'status': template_data['status'],
                    'category': template_data['category'],
                    'components_json': str(template_data['components']),
                    'body_text': next((comp['text'] for comp in template_data['components'] if comp['type'] == 'BODY'), '')
                }

                if existing_template:
                    existing_template.write(vals)
                else:
                    self.create(vals)
        
        except requests.exceptions.HTTPError as e:
            _logger.error(f"Failed to fetch templates from Meta API (HTTPError): {e.response.text}")
            raise UserError(_("Meta API Error: %s", e.response.text))
        except Exception as e:
            _logger.error(f"An unexpected error occurred during template sync: {e}")
            raise UserError(_("An unexpected error occurred: %s", e))
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Template synchronization complete.'),
                'type': 'success',
                'sticky': False,
            }
        }