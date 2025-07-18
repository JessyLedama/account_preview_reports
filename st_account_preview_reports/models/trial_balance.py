from odoo import models, fields

class TrialBalancePreviewLine(models.TransientModel):
    _name = 'trial.balance.preview.line'
    _description = 'Trial Balance Preview Line'
    _order = 'code'

    wizard_id = fields.Many2one('account.balance.report', string="Wizard")
    code = fields.Char(string="Account Code")
    name = fields.Char(string="Account Name")
    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")
    balance = fields.Float(string="Balance")
