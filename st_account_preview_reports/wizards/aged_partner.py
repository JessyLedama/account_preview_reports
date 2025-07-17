from odoo import models
from odoo.exceptions import UserError


class AgedPartnerPreviewReport(models.TransientModel):
    _inherit = "account.aged.trial.balance"

    def preview_aged_partner(self):
        self.ensure_one()

        self.env['aged.partner.preview.line'].search([('create_uid', '=', self.env.uid)]).unlink()

        if self.period_length <= 0:
            raise UserError("Period length must be greater than 0.")
        if not self.date_from:
            raise UserError("You must set a start date.")

        form_data = {
            'date_from': self.date_from.strftime('%Y-%m-%d'),
            'period_length': self.period_length,
            'result_selection': self.result_selection,
            'target_move': self.target_move,
        }

        # Determine account type
        if self.result_selection == 'customer':
            account_type = ['asset_receivable']
        elif self.result_selection == 'supplier':
            account_type = ['liability_payable']
        else:
            account_type = ['liability_payable', 'asset_receivable']

        # Call the same method used in the report
        move_lines, _, _ = self.env['report.base_accounting_kit.report_agedpartnerbalance']._get_partner_move_lines(
            account_type,
            form_data['date_from'],
            form_data['target_move'],
            form_data['period_length']
        )

        for line in move_lines:
            self.env['aged.partner.preview.line'].create({
                'wizard_id': self.id,
                'partner_id': line.get('partner_id'),
                'name': line.get('name'),
                'not_due': line.get('direction'),
                'period_5': line.get('4'),
                'period_4': line.get('3'),
                'period_3': line.get('2'),
                'period_2': line.get('1'),
                'period_1': line.get('0'),
                'total': line.get('total'),
            })

        return {
            'name': 'Aged Partner Preview',
            'type': 'ir.actions.act_window',
            'res_model': 'aged.partner.preview.line',
            'view_mode': 'tree',
            'domain': [('create_uid', '=', self.env.uid)],
            'target': 'new',
        }
