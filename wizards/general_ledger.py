from odoo import models
from odoo.exceptions import UserError


class GeneralLedgerPreviewReport(models.TransientModel):
    _inherit = "account.report.general.ledger"

    def preview_general_ledger(self):
        self.ensure_one()

        self.env['general.ledger.preview.line'].search([('create_uid', '=', self.env.uid)]).unlink()

        if self.initial_balance and not self.date_from:
            raise UserError("You must define a Start Date.")

        form_data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'initial_balance': self.initial_balance,
            'sortby': self.sortby,
            'target_move': self.target_move,
            'display_account': self.display_account,
            'journal_ids': self.journal_ids.ids,
            'company_id': [self.company_id.id],
        }

        used_context = self._build_contexts({'form': form_data})
        used_context.update({
            'date_from': self.date_from,
            'date_to': self.date_to,
        })

        form_data['used_context'] = used_context

        # Get account set based on context
        accounts = self.env['account.account'].search([])

        # Call report logic
        report_lines = self.env['report.base_accounting_kit.report_general_ledger'].with_context(**used_context)._get_account_move_entry(
            accounts,
            self.initial_balance,
            self.sortby,
            self.display_account
        )

        for account in report_lines:
            for line in account['move_lines']:
                ldate = line.get('ldate')
                if not ldate:
                    continue

                # Filter strictly by date range
                if self.date_from and ldate < self.date_from:
                    continue
                if self.date_to and ldate > self.date_to:
                    continue

                self.env['general.ledger.preview.line'].create({
                    'account_code': account.get('code'),
                    'account_name': account.get('name'),
                    'ldate': ldate,
                    'lcode': line.get('l    code'),
                    'partner_name': line.get('partner_name'),
                    'lref': line.get('lref'),
                    'move_name': line.get('move_name'),
                    'lname': line.get('lname'),
                    'debit': line.get('debit'),
                    'credit': line.get('credit'),
                    'balance': line.get('balance'),
                    'currency_code': line.get('currency_code'),
                })

        return {
            'name': 'General Ledger Preview',
            'type': 'ir.actions.act_window',
            'res_model': 'general.ledger.preview.line',
            'view_mode': 'tree',
            'domain': [('create_uid', '=', self.env.uid)],
            'target': 'new',
        }
