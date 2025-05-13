{
    'name': 'Account Preview Reports',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Adds Preview to Accounting Reports',
    'author': 'SIMI Technologies',
    'website': 'https://simitechnologies.co.ke',
    'depends': ['account', 'base_accounting_kit'],
    'data': [
        'security/ir.model.access.csv',

        'views/profit_and_loss.xml',
        'views/bank_book_preview.xml',
        'views/cash_book_preview.xml',
        'views/day_book_preview.xml',

        'wizards/profit_and_loss.xml',
        'wizards/cash_flow_statement_wizard.xml',
        'wizards/bank_book.xml',
        'wizards/cash_book.xml',
        'wizards/day_book.xml',
    ],
    'installable': True,
    'application': True,
}
