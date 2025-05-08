import re

from odoo import api, models, fields


class FinancialReport(models.TransientModel):
    _inherit = "financial.report"

    def preview_profit_and_loss(self):
        self.ensure_one()
        data = dict()
        data['form'] = self.read([
            'date_from', 'enable_filter', 'debit_credit', 'date_to',
            'account_report_id', 'target_move', 'view_format', 'company_id'])[0]

        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(
            used_context, lang=self.env.context.get('lang') or 'en_US'
        )

        lines = self.get_account_lines(data['form'])

        # Clean up old preview data if needed
        self.env['profit.and.loss'].search([]).unlink()

        # Store lines in the new model
        for line in lines:
            self.env['profit.and.loss'].create({
                'name': line.get('name'),
                'code': line.get('code'),
                'debit': line.get('debit'),
                'credit': line.get('credit'),
                'balance': line.get('balance'),
                'sequence': line.get('sequence', 0),
            })

        # Return list view
        return {
            'type': 'ir.actions.act_window',
            'name': 'P&L Report Preview',
            'view_mode': 'tree',
            'res_model': 'profit.and.loss',
            'target': 'new',
        }