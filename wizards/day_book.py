from odoo import models
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError


class DayBookPreviewReport(models.TransientModel):
    _inherit = "account.day.book.report"

    def preview_day_book(self):
        self.ensure_one()

        # Clear old preview lines created by this user
        self.env['day.book.preview.line'].search([('create_uid', '=', self.env.uid)]).unlink()

        if not self.journal_ids:
            raise UserError("Please select at least one Journal to preview the Day Book.")

        accounts = self.account_ids or self.env['account.account'].search([])
        form_data = {
            'target_move': self.target_move,
            'journal_ids': self.journal_ids.ids,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }

        # Loop through each day between date_from and date_to
        start_date = self.date_from
        end_date = self.date_to
        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        for pass_date in date_range:
            result = self.env['report.base_accounting_kit.day_book_report_template']._get_account_move_entry(
                accounts, form_data, str(pass_date)
            )

            for line in result.get('lines', []):
                self.env['day.book.preview.line'].create({
                    'wizard_id': self.id,
                    'account_id': line.get('account_id'),
                    'ldate': line.get('ldate'),
                    'lcode': line.get('lcode'),
                    'lname': line.get('lname'),
                    'lref': line.get('lref'),
                    'partner_name': line.get('partner_name'),
                    'debit': line.get('debit'),
                    'credit': line.get('credit'),
                    'balance': line.get('balance'),
                })

        return {
            'name': 'Day Book Preview',
            'type': 'ir.actions.act_window',
            'res_model': 'day.book.preview.line',
            'view_mode': 'tree',
            'domain': [('wizard_id', '=', self.id)],
            'target': 'new',
        }
