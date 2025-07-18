from odoo import models, fields

class AgedPartnerPreviewLine(models.TransientModel):
    _name = 'aged.partner.preview.line'
    _description = 'Aged Partner Preview Line'
    _order = 'name'

    wizard_id = fields.Many2one('account.aged.trial.balance', string="Wizard")
    partner_id = fields.Many2one('res.partner', string="Partner")
    name = fields.Char(string="Partner Name")
    not_due = fields.Float(string="Not Due")
    period_1 = fields.Float(string="Over 120")
    period_2 = fields.Float(string="90 - 120")
    period_3 = fields.Float(string="60 - 90")
    period_4 = fields.Float(string="30 - 60")
    period_5 = fields.Float(string="0 - 30")
    total = fields.Float(string="Total")
