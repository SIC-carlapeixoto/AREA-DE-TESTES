#-*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sync_nmvs = fields.Boolean(string="Comunicar NMVS", related="categ_id.sync_nmvs")
    product_sync_nmvs = fields.Selection(string='Comunicar NMVS', selection=[('sync','Sim'),('not_sync','Não')])
    prior_notification = fields.Boolean(string="Prior Notification")


