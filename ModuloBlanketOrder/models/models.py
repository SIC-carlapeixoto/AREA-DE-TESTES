# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class my_module(models.Model):
#     _name = 'my_module.my_module'
#     _description = 'my_module.my_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class search(models.Model):
    _inherit = 'product.template'
   # x_aue_count = fields.Integer()
    

    def get_blanckOrder(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'BlanckOrder',
            'view_mode': 'tree',
            'res_model': 'sale.blanket.order.line',
            'domain': [('product_id', '=', self.name)],
            'context': "{'create': False}"
        }
    x_aue_count = fields.Integer(compute='compute_count')
    
    def compute_count(self):
        for record in self:
            record.x_aue_count = self.env['sale.blanket.order.line'].search_count([('product_id', '=', self.name)])
            if record.x_aue_count > 0:
                record.x_studio_portfolio = 1

#Button - open Blanck Order
    def get_blanckOrderOP(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'BlanckOrder',
            'view_mode': 'tree',
            'res_model': 'sale.blanket.order.line',
            'domain': [('product_id', '=', self.name),('x_studio_state','ilike','Open')],
            'context': "{'create': False}"
        }
    x_aue_count_h = fields.Integer(compute='compute_countOP')
    
    def compute_countOP(self):
        for record in self:
            record.x_aue_count_h = self.env['sale.blanket.order.line'].search_count([('product_id', '=', self.name),('x_studio_state','ilike','Open')])

            