from odoo import models
from odoo.exceptions import UserError


class JournalAuditPreviewReport(models.TransientModel):
    _inherit = "account.print.journal"

    def preview_journal_audit(self):
        self.ensure_one()

        self.env['journal.audit.preview.line'].search([('create_uid', '=', self.env.uid)]).unlink()

        if not self.journal_ids:
            raise UserError("Please select at least one journal.")

        form_data = {
            'journal_ids': self.journal_ids.ids,
            'target_move': self.target_move,
            'sort_selection': self.sort_selection,
            'amount_currency': self.amount_currency,
            'used_context': self._build_contexts({'form': self.read()[0]}),
        }

        journal_model = self.env['report.base_accounting_kit.report_journal_audit']
        for journal in self.journal_ids:
            lines = journal_model.with_context(form_data['used_context']).lines(
                target_move=form_data['target_move'],
                journal_ids=journal.id,
                sort_selection=form_data['sort_selection'],
                data={'form': form_data}
            )
            for line in lines:
                self.env['journal.audit.preview.line'].create({
                    'wizard_id': self.id,
                    'journal_id': journal.id,
                    'move_name': line.move_id.name,
                    'date': line.date,
                    'account_code': line.account_id.code,
                    'partner_name': line.partner_id.name if line.partner_id else '',
                    'label': line.name,
                    'debit': line.debit,
                    'credit': line.credit,
                    'currency_amount': line.amount_currency if self.amount_currency else 0.0,
                    'currency_id': line.currency_id.id if line.currency_id else False,
                })

        return {
            'name': 'Journal Audit Preview',
            'type': 'ir.actions.act_window',
            'res_model': 'journal.audit.preview.line',
            'view_mode': 'tree',
            'domain': [('create_uid', '=', self.env.uid)],
            'target': 'new',
        }
