# -*- coding: utf-8 -*-

from odoo import api, fields, models

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    pack_state = fields.Char('Pack State')
    locked = fields.Boolean('Locked')

    def _get_value_production_lot(self):
        self.ensure_one()
        res = super(StockMoveLine, self)._get_value_production_lot()
        if self.pack_state:
            res['pack_state'] = self.pack_state
        res['locked'] = self.locked

        return res

    def _get_fields_stock_barcode(self):
        res = super(StockMoveLine, self)._get_fields_stock_barcode()
        return res + ['batch_code','exp_date','pack_state','locked']
