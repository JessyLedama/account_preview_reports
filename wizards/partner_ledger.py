from odoo import models, fields
from odoo.exceptions import UserError
from datetime import date


class PartnerLedgerPreviewReport(models.TransientModel):
    _inherit = "account.report.partner.ledger"

    def preview_partner_ledger(self):
        self.ensure_one()

        # Clear old lines
        self.env['partner.ledger.preview.line'].search([('create_uid', '=', self.env.uid)]).unlink()

        if not self.date_from:
            raise UserError("You must set a start date.")

        form_data = {
            'target_move': self.target_move,
            'result_selection': self.result_selection,
            'amount_currency': self.amount_currency,
            'include_initial_balance': self.include_initial_balance,
            'reconciled': self.reconciled,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'partner_ids': self.partner_ids.ids,
            'journal_ids': self.journal_ids.ids,
        }

        # Use the same context building method
        context = self._build_contexts({'form': form_data})
        form_data['used_context'] = dict(context, lang=self.env.context.get('lang') or 'en_US')

        # Set computed data same as in the report
        result_selection = form_data.get('result_selection', 'customer')
        if result_selection == 'supplier':
            account_type = ['liability_payable']
        elif result_selection == 'customer':
            account_type = ['asset_receivable']
        else:
            account_type = ['liability_payable', 'asset_receivable']

        move_state = ['posted'] if form_data.get('target_move') == 'posted' else ['draft', 'posted']

        account_ids = self.env['account.account'].search([
            ('account_type', 'in', account_type),
            ('deprecated', '=', False)
        ]).ids

        form_data['computed'] = {
            'ACCOUNT_TYPE': account_type,
            'move_state': move_state,
            'account_ids': account_ids,
        }

        # Find partners involved in move lines
        computed = {}
        aml = self.env['account.move.line'].with_context(form_data['used_context'])
        query_get_data = aml._query_get()
        domain_sql = query_get_data[1]
        params = [tuple(move_state), tuple(account_ids)] + query_get_data[2]
        reconcile_clause = "" if form_data['reconciled'] else ' AND "account_move_line".full_reconcile_id IS NULL '

        self.env.cr.execute(f"""
            SELECT DISTINCT "account_move_line".partner_id
            FROM {query_get_data[0]}, account_account AS account, account_move AS am
            WHERE "account_move_line".partner_id IS NOT NULL
                AND "account_move_line".account_id = account.id
                AND am.id = "account_move_line".move_id
                AND am.state IN %s
                AND "account_move_line".account_id IN %s
                AND NOT account.deprecated
                AND {domain_sql}
                {reconcile_clause}
        """, tuple(params))

        partner_ids = [res['partner_id'] for res in self.env.cr.dictfetchall()]
        partners = self.env['res.partner'].browse(partner_ids)

        for partner in partners:
            # lines = self.env['report.base_accounting_kit.report_partnerledger']._lines(form_data, partner)

            lines = self.env['report.base_accounting_kit.report_partnerledger']._lines({'form': form_data}, partner)
            for line in lines:
                self.env['partner.ledger.preview.line'].create({
                    'partner_id': partner.id,
                    'ldate': line.get('date'),
                    'lcode': line.get('code'),
                    'a_code': line.get('a_code'),
                    'reference': line.get('displayed_name'),
                    'debit': line.get('debit'),
                    'credit': line.get('credit'),
                    'balance': line.get('progress'),
                })

        return {
            'name': 'Partner Ledger Preview',
            'type': 'ir.actions.act_window',
            'res_model': 'partner.ledger.preview.line',
            'view_mode': 'tree',
            'domain': [('create_uid', '=', self.env.uid)],
            'target': 'new',
        }
