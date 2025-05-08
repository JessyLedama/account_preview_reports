from odoo import api, fields, models
from odoo.tools.misc import get_lang


class CashFlowReportWizard(models.TransientModel):
    _inherit = 'cash.flow.report'

    preview_line_ids = fields.One2many('cash.flow.preview.line', 'report_id', string="Preview Lines")

    def action_preview(self):
        # Clear previous lines
        self.preview_line_ids.unlink()

        data = {'form': self.read([
            'account_report_id', 'date_from_cmp', 'date_to_cmp',
            'journal_ids', 'filter_cmp', 'target_move',
            'date_from', 'date_to', 'company_id',
            'enable_filter', 'debit_credit', 'label_filter'
        ])[0]}

        comparison_context = self._build_comparison_context(data)
        data['form']['comparison_context'] = comparison_context

        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context)

        # Use the logic from your report method (get_account_lines or similar)
        report_lines = self.env['account.financial.report'].browse(data['form']['account_report_id']).get_account_lines(data['form'])

        for line in report_lines:
            self.env['cash.flow.preview.line'].create({
                'report_id': self.id,
                'name': line.get('name'),
                'amount': line.get('balance'),
                'sequence': line.get('sequence', 0),
            })

        return {
            'name': 'Cash Flow Preview',
            'view_mode': 'tree',
            'res_model': 'cash.flow.preview.line',
            'type': 'ir.actions.act_window',
            'domain': [('report_id', '=', self.id)],
            'target': 'new',
        }
