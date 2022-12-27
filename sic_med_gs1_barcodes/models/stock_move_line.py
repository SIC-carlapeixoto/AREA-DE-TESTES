# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from calendar import monthrange


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    exp_date = fields.Char()
    batch_code = fields.Char('Batch Code')

    def _get_value_production_lot(self):
        self.ensure_one()
        res = super(StockMoveLine, self)._get_value_production_lot()
        if self.batch_code:
            res['batch_code'] = self.batch_code
        if self.exp_date:
            date_6 = self.exp_date
            day = str(date_6[4:6])
            month = str(date_6[2:4])
            year =str(date_6[0:2])
            if day == '00':
                day = str(monthrange(int(year), int(month))[1])
            
            odoo_date = day + '/' + month + '/20' + year 

            res['expiration_date'] = datetime.strptime(odoo_date, '%d/%m/%Y')
            
        return res