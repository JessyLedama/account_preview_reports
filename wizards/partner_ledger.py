from odoo import models, fields
from odoo.exceptions import UserError


class PartnerLedgerPreviewReport(models.TransientModel):
    _inherit = "account.report.partner.ledger"

    def preview_partner_ledger(self):
        self.ensure_one()

        # Clear old preview lines
        self.env['partner.ledger.preview.line'].search([('create_uid', '=', self.env.uid)]).unlink()

        if not self.date_from:
            raise UserError("You must set a start date.")

        # Construct form data like report does
        form_data = {
            'target_move': self.target_move,
            'result_selection': self.result_selection,
            'amount_currency': self.amount_currency,
            'include_initial_balance': self.include_initial_balance,
            'initial_balance': self.include_initial_balance,  # Required by some reports
            'reconciled': self.reconciled,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'partner_ids': self.partner_ids.ids or self.env['res.partner'].search([]).ids,
            'journal_ids': self.journal_ids.ids or self.env['account.journal'].search([]).ids,
        }

        # Set context
        context = self._build_contexts({'form': form_data})
        form_data['used_context'] = dict(context, lang=self.env.context.get('lang') or 'en_US')

        # Use report method that prepares everything
        report_obj = self.env['report.base_accounting_kit.report_partnerledger']
        report_data = report_obj._get_report_values([], {'form': form_data})
        partners = report_data['docs']
        line_method = report_data['lines']

        for partner in partners:
            lines = line_method({'form': form_data, 'computed': report_data['data']['computed']}, partner)
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
