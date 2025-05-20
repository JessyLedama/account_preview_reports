from odoo import models, fields


class PartnerLedgerPreviewLine(models.TransientModel):
    _name = 'partner.ledger.preview.line'
    _description = 'Partner Ledger Preview Line'
    _order = 'ldate'

    partner_id = fields.Many2one('res.partner', string="Partner")
    ldate = fields.Date(string="Date")
    lcode = fields.Char(string="Journal")
    a_code = fields.Char(string="Account")
    reference = fields.Char(string="Reference")
    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")
    balance = fields.Float(string="Balance")
