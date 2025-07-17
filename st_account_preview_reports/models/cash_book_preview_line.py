from odoo import models, fields

class CashBookPreviewLine(models.TransientModel):
    _name = 'cash.book.preview.line'
    _description = 'Cash Book Preview Line'
    _order = 'ldate'

    wizard_id = fields.Many2one('account.cash.book.report', string="Wizard")
    account_id = fields.Many2one('account.account', string="Account")
    ldate = fields.Date(string="Date")
    lcode = fields.Char(string="Journal")
    lname = fields.Char(string="Label")
    lref = fields.Char(string="Ref")
    partner_name = fields.Char(string="Partner")
    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")
    balance = fields.Float(string="Balance")
