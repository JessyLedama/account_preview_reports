from odoo import models
from datetime import datetime, date
import logging
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class DayBookPreviewReport(models.TransientModel):
    _inherit = "account.day.book.report"

    def preview_day_book(self):
        self.ensure_one()

        # Clear only current user's preview lines to avoid conflicts
        self.env['day.book.preview.line'].search([('create_uid', '=', self.env.uid)]).unlink()

        # Get start and end dates from wizard
        start_date = self.date_from
        end_date = self.date_to

        if not self.account_ids or not self.journal_ids:
            raise UserError("Please select at least one Account and one Journal to generate the report.")

        # Get the move lines data
        accounts = self.account_ids

        form_data = {
            'target_move': self.target_move,          
            'journal_ids': self.journal_ids.ids,     
            'date_from': self.date_from,               
            'date_to': self.date_to,                   
        }


        move_line_groups = self.env['report.base_accounting_kit.day_book_report_template']._get_account_move_entry(
            accounts,
            form_data,
            None
        )

        # Loop through each account group
        for group in move_line_groups.get('lines', []):
            account_id = group.get("account_id") or (accounts.ids[0] if accounts else None)

            for line in group.get("move_lines", []):
                
                ldate_raw = line.get('ldate')
                ldate = None
                if ldate_raw:
                    try:
                        ldate = (
                            ldate_raw if isinstance(ldate_raw, date)
                            else datetime.strptime(ldate_raw, "%Y-%m-%d").date()
                        )
                    except ValueError:
                        _logger.warning("Invalid date format found in line: %s", line)
                        continue  # Skip this line if date is invalid

                # Skip line if ldate is outside selected range
                if (start_date and ldate and ldate < start_date) or (end_date and ldate and ldate > end_date):
                    continue

                self.env['day.book.preview.line'].create({
                    'account_id': account_id,
                    'ldate': ldate,
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
            'domain': [('create_uid', '=', self.env.uid)],
            'target': 'new',
        }
