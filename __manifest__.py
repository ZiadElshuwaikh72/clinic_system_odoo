{
    'name': "Clinics System",
    'version': '17.0.0.1.0',
    'summary': ' management system clinics',
    'author': "Ziad Ahmed",
    'category': 'Custom',
    'license': 'LGPL-3',
    'depends': ['base','account','mail','contacts'

                ],
    'data':
        [
            # 'security/security.xml',
            'security/ir.model.access.csv',
            'data/sequence.xml',
            # 'data/data.xml',
        'views/base_menu.xml',
        'views/appointment_view.xml',
        'views/department_view.xml',
        'views/doctor_view.xml',
        'views/invoice_view.xml',
        'views/patient_view.xml',
        'views/treatment_view.xml',
        'reports/invoice_report.xml'

    ],
# 'images': ['static/Images/icon.png'],
    'assets':{
        'web.assets_backend':[

        ],
        'web.report_assets_common': [

        ]
    },
    'application': True,
    'installable': True,
}
