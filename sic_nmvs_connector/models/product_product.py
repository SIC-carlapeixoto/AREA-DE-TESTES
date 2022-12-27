# -*- coding: utf-8 -*-

from odoo import models, api


class Product(models.Model):
    _inherit = 'product.product'
    _barcode_field = 'barcode'

    @api.model
    def _get_fields_stock_barcode(self):
        res = super(Product, self)._get_fields_stock_barcode()
        return res + ['sync_nmvs','product_sync_nmvs']


