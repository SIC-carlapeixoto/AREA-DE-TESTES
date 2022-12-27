#-*- coding: utf-8 -*-

from odoo import models, fields, api

class GetPickingSerials(models.TransientModel):
    _name = 'get.picking.serials'

    picking_id = fields.Many2one('stock.picking', string="Picking")
    in_picking_id = fields.Many2one('stock.picking', string="In Picking")
    lot_ids = fields.One2many('picking.serials', 'get_serial_id', string="In Picking")

    def set_lots_in_picking(self):
        for rec in self:
            for this_move in rec.picking_id.move_ids_without_package:
                for lot in rec.lot_ids:
                    if lot.lot_id and this_move.product_id.id == lot.product_id.id:
                        this_move.lot_ids += lot.lot_id   


    @api.onchange('in_picking_id')
    def onchange_in_pick(self):
        for rec in self:
            lots = {}
            lot_ids = []
            rec.lot_ids = False
            for this_move in rec.picking_id.move_ids_without_package:
                #if this_move.product_id.sync_nmvs or verificar se produto sync nmvs
                product_id_str = str(this_move.product_id.id)
                if product_id_str not in lots.keys():
                    lots[product_id_str] = []
                for move in rec.in_picking_id.move_ids_without_package:
                    for lot in move.lot_ids:
                        if not lot.locked and lot.pack_state == 'ACTIVE':
                            lots[product_id_str].append(lot.id)
            for key in lots.keys():
                for lot in lots[key]:
                    lot = self.env['stock.production.lot'].search([('id','=',lot)])
                    if lot and lot.id not in lot_ids:
                        self.env['picking.serials'].create({'get_serial_id':rec.id, 'lot_id':lot.id})
                        lot_ids.append(lot.id)
                            

        
class PickingSerials(models.TransientModel):
    _name = 'picking.serials'

    get_serial_id = fields.Many2one('get.picking.serials', string='Serial Nº')
    lot_id = fields.Many2one('stock.production.lot', string="Serial Nº")
    batch_code = fields.Char(string="Lote", related='lot_id.batch_code')
    expiration_date = fields.Datetime(string="Data de Validade", related='lot_id.expiration_date')
    product_id = fields.Many2one(string="Artigo", related='lot_id.product_id')
    

