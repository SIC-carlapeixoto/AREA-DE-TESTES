#-*- coding: utf-8 -*-

from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = "product.category"

    sync_nmvs = fields.Boolean(string="Comunicar NMVS")
