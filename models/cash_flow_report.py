from odoo import models, fields

class CashFlowPreviewLine(models.TransientModel):
    _name = 'cash.flow.preview.line'
    _description = 'Cash Flow Preview Line'

    name = fields.Char(string="Label")
    amount = fields.Float(string="Amount")
    sequence = fields.Integer(string="Sequence")
    report_id = fields.Many2one('cash.flow.report', string="Wizard") 

