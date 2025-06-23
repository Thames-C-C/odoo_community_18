# -*- coding: utf-8 -*-
{
    'name': "Thames Config and Customizations", # You can rename this
    'summary': "Adds custom fields and installs all required modules.",
    'author': "Your Company Name",
    'website': "https://www.thameserp.com",
    'category': 'Uncategorized',
    'version': '1.0',

    'depends': [
        'base',
        'crm',
        'sale_management',
        'stock',
    ],

    # ADD THIS 'data' SECTION
    'data': [
        # 'security/ir.model.access.csv', # Good practice, but we'll skip for now
        'views/res_partner_views.xml',
    ],

    'installable': True,
    'application': True,
}