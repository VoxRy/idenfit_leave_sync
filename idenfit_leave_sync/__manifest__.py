{
    'name': 'İdenfit Leave Sync',
    'version': '1.0',
    'summary': 'İdenfit izinlerini Odoo ile senkronize eder',
    'category': 'Human Resources',
    'depends': ['hr_holidays', 'calendar'],
    'data': [
        'data/ir_cron.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
}
