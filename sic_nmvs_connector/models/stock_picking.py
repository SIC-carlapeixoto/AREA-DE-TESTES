#-*- coding: utf-8 -*-

from odoo import _, models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'



    #code = fields.Selection([('incoming', 'Receipt'), ('outgoing', 'Delivery'), ('internal', 'Internal Transfer')], 'Type of Operation', required=True)

    nmvs_comms = fields.One2many('nmvs.operation', 'picking_id',string="Comunicações NMVS")
    is_nmvs_checkout_needed = fields.Boolean(string='Needs NMVS Checkout?', compute='_needs_nmvs_checkout')
    so_id = fields.Many2one('sale.order',string='SO', compute='_get_so_id')



    # product
        #batch   #serial
                 #serial

    # product
        #batch   #serial
                 #serial
            
    def set_nmvs_packs_out(self):
        for rec in self:
            if rec.so_id.fiscal_position_id.name == 'Extracomunitário':
                operation = 'G140Export-G145BulkExport'
            else:
                if rec.partner_id.parent_id.desativate_packs:
                    operation = 'G120Dispense-G125BulkDispense'
            data_fill = 'inventory'
            picking_id = rec.id
            manual_op = self.env['nmvs.manual.operation']
            manual_pk = self.env['nmvs.manual.operation.packs']

            for line in rec.move_ids_without_package:
                if line.product_id.product_sync_nmvs == 'sync' or (line.product_id.product_sync_nmvs != 'not_sync' and line.product_id.sync_nmvs):
                    if line.lot_ids:
                        batches = {}
                        product_id = line.product_id.id
                        for serial in line.lot_ids:
                            if serial.batch_code in batches:
                                batches[serial.batch_code].append(serial)
                            else:
                                batches[serial.batch_code] = [serial]
                        
                        for batch_code in batches.keys():
                            manual_op_id = manual_op.create({'operation':operation, 'data_fill':data_fill, 'picking_id':picking_id, 'product_id':product_id, 'batch_code': batch_code})
                            for pack in batches[batch_code]:
                                manual_pk.create({'manual_operation_id':manual_op_id.id, 'pack_id':pack.id})
                            manual_op_id.execute_operation()
            return

    def validate_nmvs_packs(self):
        for rec in self:
            operation = 'G110Verify-G115BulkVerify'
            data_fill = 'inventory'
            picking_id = rec.id
            manual_op = self.env['nmvs.manual.operation']
            manual_pk = self.env['nmvs.manual.operation.packs']

            for line in rec.move_ids_without_package:
                if line.product_id.product_sync_nmvs == 'sync' or (line.product_id.product_sync_nmvs != 'not_sync' and line.product_id.sync_nmvs):
                    if line.lot_ids:
                        batches = {}
                        product_id = line.product_id.id
                        for serial in line.lot_ids:
                            if serial.batch_code in batches:
                                batches[serial.batch_code].append(serial)
                            else:
                                batches[serial.batch_code] = [serial]
                        
                        for batch_code in batches.keys():
                            manual_op_id = manual_op.create({'operation':operation, 'data_fill':data_fill, 'picking_id':picking_id, 'product_id':product_id, 'batch_code': batch_code})
                            for pack in batches[batch_code]:
                                manual_pk.create({'manual_operation_id':manual_op_id.id, 'pack_id':pack.id})
                            manual_op_id.execute_operation()
            return


    def get_picking_serials(self):
        for rec in self:
            return {
                    'context': {'default_picking_id': rec.id},
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'get.picking.serials',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                }

    def _needs_nmvs_checkout(self):
        for rec in self:
            for line in rec.move_ids_without_package:
                if line.product_id.product_sync_nmvs == 'sync' or (line.product_id.product_sync_nmvs != 'not_sync' and line.product_id.sync_nmvs):
                    rec.is_nmvs_checkout_needed = True
                    return True
            rec.is_nmvs_checkout_needed = False
            return False

    def _get_so_id(self):
        for rec in self:
            so_id = self.env['sale.order'].search([('name','=',rec.origin)]).id
            rec.so_id
            return so_id