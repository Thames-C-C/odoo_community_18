{
    'name': "Thames ERP Configuration",
    'summary': "Installs all the required modules for the Thames ERP project.",
    'description': """
        This module acts as the master configuration for any new Thames ERP deployment.
        Installing this single module will automatically install all other required apps.
    """,
    'author': "Your Company Name",
    'website': "https://www.thameserp.com",
    'category': 'Uncategorized',
    'version': '1.0',

    # List the technical names of the apps you installed.
    'depends': [
        'base',
        'crm',
        'sale_management',
        'stock',
        'account',
    ],

    'data': [
        'views/res_partner_views.xml',
    ],

    'installable': True,
    'application': True,
}