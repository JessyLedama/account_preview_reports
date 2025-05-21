from odoo import api, fields, models
from odoo.tools.misc import get_lang
from odoo.exceptions import UserError


class CashFlowReportWizard(models.TransientModel):
    _inherit = 'cash.flow.report'

    # preview_line_ids = fields.One2many('cash.flow.preview.line', 'report_id', string="Preview Lines")

    def action_preview(self):
        self.ensure_one()

        # self.preview_line_ids.unlink()
        self.env['cash.flow.preview.line'].search([('create_uid', '=', self.env.uid)]).unlink()

        if self.date_from:
            raise UserError("You must define a Start Date.")

        options = self._get_options(previous_options=None)
        options['comparison'] = self.enable_filter and {
            'filter': self.filter_cmp,
            'date_from': self.date_from_cmp,
            'date_to': self.date_to_cmp,
            'label': self.label_filter
        } or {}

        # Ensure proper context (if needed)
        report_lines = self._get_lines(options)

        for line in report_lines:
            if line.get('level') == 0:  # Skip headers/groups if needed
                continue

            self.env['cash.flow.preview.line'].create({
                'report_id': self.id,
                'name': line.get('name'),
                'amount': line.get('columns')[0].get('no_format_name') if line.get('columns') else 0.0,
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
