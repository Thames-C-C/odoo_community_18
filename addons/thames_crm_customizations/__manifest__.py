{
    'name': 'Thames CRM Customizations',
    'version': '1.0',
    'summary': 'Adds a large number of custom fields to the Partner/Customer form.',
    'author': 'Thames C&C Ltd',
    'depends': ['base', 'account', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/whatsapp_template_views.xml',
        'wizards/whatsapp_compose_message_view.xml',
        'wizards/whatsapp_mass_message_wizard_view.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
} 