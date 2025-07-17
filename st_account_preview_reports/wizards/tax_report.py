from odoo import models
from odoo.exceptions import UserError


class TaxReportPreviewReport(models.TransientModel):
    _inherit = "kit.account.tax.report"

    def preview_tax_report(self):
        self.ensure_one()

        self.env['tax.report.preview.line'].search([('create_uid', '=', self.env.uid)]).unlink()

        if not self.date_from or not self.date_to:
            raise UserError("Please select both a Start Date and an End Date.")

        options = {
            'date_from': self.date_from.isoformat(),
            'date_to': self.date_to.isoformat(),
            'target_move': self.target_move,
        }

        tax_lines = self.env['report.base_accounting_kit.report_tax'].get_lines(options)

        for line in tax_lines.get('sale', []):
            self.env['tax.report.preview.line'].create({
                'type': 'sale',
                'name': line.get('name'),
                'net': line.get('net'),
                'tax': line.get('tax'),
                'wizard_id': self.id,
            })

        for line in tax_lines.get('purchase', []):
            self.env['tax.report.preview.line'].create({
                'type': 'purchase',
                'name': line.get('name'),
                'net': line.get('net'),
                'tax': line.get('tax'),
                'wizard_id': self.id,
            })

        return {
            'name': 'Tax Report Preview',
            'type': 'ir.actions.act_window',
            'res_model': 'tax.report.preview.line',
            'view_mode': 'tree',
            'domain': [('create_uid', '=', self.env.uid)],
            'target': 'new',
        }
