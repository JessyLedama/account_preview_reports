from odoo import models
from odoo.exceptions import UserError

class TrialBalancePreviewReport(models.TransientModel):
    _inherit = "account.balance.report"

    def preview_trial_balance(self):
        self.ensure_one()

        # Clear previous previews for this user
        self.env['trial.balance.preview.line'].search([('create_uid', '=', self.env.uid)]).unlink()

        if not self.date_from or not self.date_to:
            raise UserError("You must select both a Start Date and an End Date.")

        # Read form data as used in _get_report_values
        # form_data = self.read()[0]
        # form_data['used_context'] = self._build_contexts({'form': form_data})

        form_data = self.read()[0]
        used_context = self._build_contexts({'form': form_data})
        form_data['used_context'] = used_context

        accounts = self.env['account.account'].search([])

        # Call the same method used in print
        trial_data = self.env['report.base_accounting_kit.report_trial_balance'].with_context(used_context)._get_accounts(
            accounts,
            form_data['display_account']
        )

        for line in trial_data:
            self.env['trial.balance.preview.line'].create({
                'wizard_id': self.id,
                'code': line.get('code'),
                'name': line.get('name'),
                'debit': line.get('debit'),
                'credit': line.get('credit'),
                'balance': line.get('balance'),
            })

        return {
            'name': 'Trial Balance Preview',
            'type': 'ir.actions.act_window',
            'res_model': 'trial.balance.preview.line',
            'view_mode': 'tree',
            'domain': [('create_uid', '=', self.env.uid)],
            'target': 'new',
        }
