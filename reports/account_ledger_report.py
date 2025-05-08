from odoo import models

class ReportAccountLedger(models.AbstractModel):
    _name = 'report.account_ledger_report.report_account_ledger'
    _description = 'Account Ledger Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['account.ledger.report'].browse(docids)

        # Prepare a dictionary mapping each doc to its ledger entries
        doc_ledger_entries = {}
        for doc in docs:
            ledger_entries = doc.get_ledger_data(doc.account_id.id, doc.start_date, doc.end_date)
            doc_ledger_entries[doc.id] = ledger_entries

        return {
            'doc_ids': docids,
            'doc_model': 'account.ledger.report',
            'docs': docs,
            'doc_ledger_entries': doc_ledger_entries,  # Pass it separately!
        }
