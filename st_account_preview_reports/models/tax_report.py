from odoo import models, fields


class TaxReportPreviewLine(models.TransientModel):
    _name = 'tax.report.preview.line'
    _description = 'Tax Report Preview Line'
    _order = 'type, name'

    wizard_id = fields.Many2one('kit.account.tax.report', string="Wizard")
    type = fields.Selection([('sale', 'Sale'), ('purchase', 'Purchase')], string='Type')
    name = fields.Char(string='Tax Name')
    net = fields.Float(string='Net')
    tax = fields.Float(string='Tax')
