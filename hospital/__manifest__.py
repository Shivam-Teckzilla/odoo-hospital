{
    'name': 'Hospital Management',
    'version': '1.2',
    'summary': 'hospital Management System',
    'sequence': -100,
    'description': """Hospital Management System""",
    'category': 'Education',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['base', 'mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/cancel_appointment_view.xml',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/gender_patient_view.xml',
        'views/appointment_patient_view.xml',
        'views/patient_tag_view.xml',
        'views/playground_view.xml',
        'views/res_config_settings_views.xml',
        'views/operation_view.xml',
        'reports/templet.xml',
        'reports/appointment.xml',

        # 'reports/patient_card.xml',

    ],
    'demo': [],
    'assets': {
        'web.report_assets_common': [
            'hospital/static/src/scss/**/*'
        ]
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
