from odoo import models, fields

class BankBookPreviewLine(models.TransientModel):
    _name = 'bank.book.preview.line'
    _description = 'Bank Book Preview Line'
    _order = 'ldate'

    wizard_id = fields.Many2one('account.bank.book.report', string="Wizard")
    account_id = fields.Many2one('account.account', string="Account")
    ldate = fields.Date(string="Date")
    lcode = fields.Char(string="Journal")
    lname = fields.Char(string="Label")
    lref = fields.Char(string="Ref")
    partner_name = fields.Char(string="Partner")
    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")
    balance = fields.Float(string="Balance")
