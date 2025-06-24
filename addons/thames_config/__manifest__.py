# -*- coding: utf-8 -*-
{
    'name': "Thames ERP Configuration",
    'summary': "Installs all required modules for the Thames ERP project.",
    'author': "Your Company Name",
    'website': "https://www.thameserp.com",
    'category': 'Uncategorized',
    'version': '1.0',
    # List of all required applications plus our customizations
    'depends': [
        'crm',
        'sale_management',
        'website',
        'stock',
        'account', # This is the technical name for the Invoicing app
        'thames_crm_customizations', # Your customizations module
    ],
    'installable': True,
    'application': True,
}