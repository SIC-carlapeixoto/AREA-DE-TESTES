from odoo import api, models, fields, _

class SaleOrder(models.Model):
    _inherit = "sale.order"


    def write(self, values):
        if 'name' in values.keys():
            purchase_ids = self.env['purchase.order'].search([('origin', '=', self.name)])
            for po in purchase_ids:
                po.origin = values['name']
        super(SaleOrder, self).write()
        
