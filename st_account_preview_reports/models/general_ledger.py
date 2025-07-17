from odoo import models, fields

class GeneralLedgerPreviewLine(models.TransientModel):
    _name = 'general.ledger.preview.line'
    _description = 'General Ledger Preview Line'
    _order = 'ldate'

    wizard_id = fields.Many2one('account.report.general.ledger', string="Wizard")
    account_code = fields.Char(string="Account Code")
    account_name = fields.Char(string="Account Name")
    ldate = fields.Date(string="Date")
    lcode = fields.Char(string="Journal")
    partner_name = fields.Char(string="Partner")
    lref = fields.Char(string="Reference")
    move_name = fields.Char(string="Move")
    lname = fields.Char(string="Label")
    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")
    balance = fields.Float(string="Balance")
    currency_code = fields.Char(string="Currency")
