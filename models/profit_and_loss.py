from odoo import models, fields

class AccountPreviewLine(models.TransientModel):
    _name = 'profit.and.loss'
    _description = 'P&L Report Preview Line'

    name = fields.Char()
    code = fields.Char()
    debit = fields.Float()
    credit = fields.Float()
    balance = fields.Float()
    sequence = fields.Integer()
    report_id = fields.Many2one('financial.report', string="P&L Preview Report")
