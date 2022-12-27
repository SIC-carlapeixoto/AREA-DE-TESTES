#-*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    deactivate_packs = fields.Boolean(string="Art 23")