from odoo import models, fields


class JournalAuditPreviewLine(models.TransientModel):
    _name = 'journal.audit.preview.line'
    _description = 'Journal Audit Preview Line'
    _order = 'date, move_name'

    wizard_id = fields.Many2one('account.print.journal', string="Wizard")
    journal_id = fields.Many2one('account.journal', string="Journal")
    move_name = fields.Char(string="Move")
    date = fields.Date(string="Date")
    account_code = fields.Char(string="Account")
    partner_name = fields.Char(string="Partner")
    label = fields.Char(string="Label")
    debit = fields.Monetary(string="Debit")
    credit = fields.Monetary(string="Credit")
    currency_amount = fields.Monetary(string="Currency Amount")
    currency_id = fields.Many2one('res.currency', string="Currency")
    company_id = fields.Many2one('res.company', related='journal_id.company_id', store=True)
