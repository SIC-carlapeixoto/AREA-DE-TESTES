#-*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.addons.sic_nmvs_connector.nmvs_data.operations import *
from odoo.addons.sic_nmvs_connector.nmvs_data.nmvs_functions import *

class NmvsManualOperation(models.TransientModel):
    _name = 'nmvs.manual.operation'

    name = fields.Char(string="Nome")

    operation = fields.Selection(string="Operação", selection= [
         ('G110Verify-G115BulkVerify', 'Verificar Serial Nº'),
         ('G120Dispense-G125BulkDispense', 'Dispensar Serial Nº'),
         ('G121UndoDispense-G127BulkUndoDispense', 'Undo Dispensar Serial Nº'),
         ('G130Destroy-G135BulkDestroy', 'Destruir Serial Nº'),
         ('G140Export-G145BulkExport', 'Exportar Serial Nº'),
         ('G141UndoExport-G147BulkUndoExport', 'Undo Exportar Serial Nº'),
         ('G150Sample-G155BulkSample', 'Para Amostra'),
         ('G151UndoSample-G157BulkUndoSample', 'Undo Para Amostra'),
         ('G160FreeSample-G165BulkFreeSample', 'Para Amostra Gratuita'),
         ('G161UndoFreeSample-G167BulkUndoFreeSample', 'Undo Para Amostra Gratuita'),
         ('G170Lock-G175BulkLocks', 'Bloquear Serial Nº'),
         ('G171UndoLock-G177BulkUndoLock', 'Undo Bloquear Serial Nº'),
         ('G180Stolen-G185BulkStolen', 'Packs Roubados'),
          ])

    operation_date = fields.Datetime(string="Data")
    data_fill = fields.Selection(string="Inserir Serial Nº", selection=[('manual','Manualmente'),('inventory','A partir do Inventário')], default="inventory")
    mixed_bulk_operation = fields.Many2one('nmvs.mixed.bulk.operation', string="Mixed Bulk")
    
    picking_id = fields.Many2one('stock.picking', string='Saída')

    product_id = fields.Many2one('product.product', string="Artigo",)

    inventory_pack_ids = fields.One2many('nmvs.manual.operation.packs', 'manual_operation_id', string="Packs")
    manual_pack_ids = fields.One2many('nmvs.manual.operation.manual.packs', 'manual_operation_id', string="Packs")

    product_code = fields.Char(string="Código do Artigo")
    batch_code = fields.Char(string='Lote')
    batch_select = fields.Many2one('nmvs.temp.batch.code', string='Lote')
    expiration_date = fields.Char(string='Data de Validade (YYMMDD)')

    operation_done = fields.Boolean()
    operation_status = fields.Selection(string="Estado da Operação", selection=[('done','Concluída'), ('failed','Falhada'), ('waiting','A aguardar Confirmação')])
    result = fields.Char(string="Resultado")

    @api.onchange('product_id')
    def get_temp_batches(self):
        for rec in self:
            batches = self.env['nmvs.temp.batch.code']
            lots = self.env['stock.production.lot']
            rec.batch_select = False
            rec.batch_code = False
            if rec.product_id:
                lot_names = []
                for lot in lots.search([('product_id','=',rec.product_id.id)]):
                    if lot.batch_code and lot.batch_code not in lot_names:
                        lot_names.append(lot.batch_code)
                for lot in lot_names:
                    if not batches.search([('name','=',lot),('product_id','=',rec.product_id.id)]):
                        batches.create({'name':lot,'product_id':rec.product_id.id})


    def select_all_batch_packs(self):
        for rec in self:
            if rec.batch_code and rec.product_id and rec.data_fill == 'inventory':
                rec.inventory_pack_ids = False
                rec.manual_pack_ids = False
                packs = self.env['stock.production.lot'].search([('batch_code','=',rec.batch_code),('product_id','=',rec.product_id.id)])
                for pack in packs:
                    vals = {
                        'manual_operation_id': rec.id,
                        'product_id': rec.product_id,
                        'pack_id': pack.id,
                    }
                    rec.env['nmvs.manual.operation.packs'].sudo().create(vals)
            return {
                'context': self.env.context,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'nmvs.manual.operation',
                'res_id': self.id,
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'new',
        }





    @api.onchange('batch_select')
    def set_temp_batches(self):
        for rec in self:
            rec.batch_code = rec.batch_select.name
                    

    @api.onchange('operation','data_fill','product_id','product_code','batch_code','expiration_date')
    def clear_packs(self):
        for rec in self:
            rec.inventory_pack_ids = False
            rec.manual_pack_ids = False

    def execute_operation(self):
    # chamar operação
        def set_pack_result(self,pack_obj):
            if self.data_fill == 'manual':
                for man_pack in self.manual_pack_ids:
                    for po in pack_obj:
                        if po[0] == man_pack.serial_code:
                            man_pack.pack_state = po[1]
                            man_pack.operation_status = 'done'
                            if len(po) > 2:
                                man_pack.pack_state_reason = po[2]
                            if len(po) > 3:
                                man_pack.result_code = po[3]
            else:
                for p in self.inventory_pack_ids:
                    for po in pack_obj:
                        if po[0] == p.pack_id.name:
                            p.pack_state = po[1]
                            p.pack_id.pack_state = po[1]
                            p.operation_status = 'done'
                            if len(p) > 2:
                                p.pack_id.pack_state_reason = po[2]
                                p.pack_state_reason = po[2]
                                if len(p) > 3:
                                    p.result_code = po[3]

        def set_bulk_pack_result(self,pack_obj):
            #[{'pack': 'PK001E09DE7E25FD94F', 'state': 'ACTIVE', 'return_code': 'NMVS_SUCCESS'}
            if self.data_fill == 'manual':
                for man_pack in self.manual_pack_ids:
                    for po in pack_obj:
                        if po['pack'] == man_pack.serial_code:
                            if po['return_code'][0] == 'NMVS_SUCCESS':
                                man_pack.operation_status = 'done'
                            if 'state' in po.keys():
                                man_pack.pack_state = po['state']
                                if 'reason' in po.keys():
                                    man_pack.pack_state_reason = po['reason']
                            if 'return_code' in po.keys():
                                man_pack.return_code = po['return_code']
            else:
                for inv_pack in rec.inventory_pack_ids:
                    for po in pack_obj:
                        if po['pack'] == inv_pack.pack_id.name:
                            if po['return_code'][0] == 'NMVS_SUCCESS':
                                inv_pack.operation_status = 'done'
                            if 'state' in po.keys():
                                inv_pack.pack_state = po['state']
                                inv_pack.pack_id.pack_state = po['state']
                                if 'reason' in po.keys():
                                    inv_pack.pack_state_reason = po['reason']
                                    inv_pack.pack_id.pack_state_reason = po['reason']
                            if 'return_code' in po.keys():
                                inv_pack.return_code = po['return_code']

        def send_packs_to_operation(self, operation_id):
            if self.data_fill == 'manual':
                for pack in self.manual_pack_ids:
                    vals = {
                        'operation_id': operation_id.id,
                        'product_code': self.product_code,
                        'serial_code': pack.serial_code,
                        'pack_state': pack.pack_state,
                        'pack_state_reason': pack.pack_state_reason,
                        'operation_status': pack.operation_status,
                    }
                    rec.env['nmvs.operation.manual.packs'].sudo().create(vals)
            else:
                for pack in self.inventory_pack_ids:
                    vals = {
                        'operation_id': operation_id.id,
                        'product_id': self.product_id,
                        'pack_id': pack.pack_id.id,
                        'pack_state': pack.pack_state,
                        'pack_state_reason': pack.pack_state_reason,
                        'operation_status': pack.operation_status,
                    }
                    rec.env['nmvs.operation.packs'].sudo().create(vals)



        for rec in self:
            transaction_id = ''
            operation = rec.operation
            packs,operation = self.get_packs_and_operation_data()

            ClientLoginId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_login")
            UserId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_user")
            Password = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_key")
            USName = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_name")
            USSupplier = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_supplier")
            USVersion = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_version")
            TransactionLanguage = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_transaction_language")
            TransactionId = self.env['ir.sequence'].next_by_code('nmvs.operation')

            result_code, transaction_id, pack_obj = call_nmvs(OPERATIONS[operation], packs, transaction_id, ClientLoginId, UserId, Password, USName, USSupplier, USVersion, TransactionId, TransactionLanguage)
            operation_status = False
            if result_code:
                if result_code[0]  == 'NMVS_SUCCESS':
                    operation_status = 'done'
                else:
                    operation_status = 'failed'
            else:
                result_code = ['Failed', 'Failed']
                operation_status = 'failed'

            if OPERATIONS[operation]['type'] == 'SinglePack':
                set_pack_result(rec,pack_obj)


            if rec.product_id:
                p_id = rec.product_id.id
            else:
                p_id = False

            vals = {
                'operation': operation,
                'result_code': result_code[0],
                'result_code_desc': result_code[1],
                'transaction_id': transaction_id,
                'operation_date': fields.datetime.now(),
                'operation_status': operation_status,
                'product_code': rec.product_code,
                'product_id': p_id,
                'result': rec.result,
                'data_fill': rec.data_fill,
                'type': 'manual',
                'name': TransactionId,
                'batch_code': rec.batch_code,
                'expiration_date': rec.expiration_date
                }
            if rec.picking_id:
                vals['picking_id'] = rec.picking_id.id

            operation_line = rec.env['nmvs.operation'].sudo().create(vals)
            rec.name = operation_line.name
            rec.operation_date = operation_line.operation_date
            rec.operation_done = True

            if OPERATIONS[operation]['type'] == 'Bulk' and operation_status != 'failed':
                operation = OPERATIONS['G188RequestBulkPackResult']
                TransactionId = self.env['ir.sequence'].next_by_code('nmvs.operation')

                result_code, transaction_id, packs_obj = call_nmvs(operation, [], transaction_id, ClientLoginId, UserId, Password, USName, USSupplier, USVersion, TransactionId, TransactionLanguage)
                vals = {
                    'operation': 'G188RequestBulkPackResult',
                    'operation_date': fields.datetime.now(),
                    'parent_id': operation_line.id,
                    'result': 'waiting',
                    'transaction_id': transaction_id,
                    'type': 'system',
                    'name': TransactionId
                    }
                if result_code[0] == 'NMVS_FE_TX_02': #Result not ready create history with pending status   # verificar possiveis codigos de falha !
                    G188operation_status = 'waiting'
                    operation_line.operation_status = 'waiting'

                elif result_code[0] == 'NMVS_SUCCESS':
                        G188operation_status = 'done'
                        operation_line.operation_status = 'done'
                        set_bulk_pack_result(rec,packs_obj)

                else:
                    G188operation_status = 'failed'
                    operation_line.operation_status = 'failed'

                    #NMVS_SUCCESS
                    # [{'pack': 'PK001E09DE7E25FD94F', 'state': 'ACTIVE', 'return_code': 'NMVS_SUCCESS'}, {'pack': 'PK0028E21615B83AA4C', 'state': 'ACTIVE', 'return_code': 'NMVS_SUCCESS'}]

                vals['operation_status'] = G188operation_status
                vals['result_code'] = result_code[0]
                vals['result_code_desc'] = result_code[1]
                G188_operation_line = rec.env['nmvs.operation'].sudo().create(vals)

            send_packs_to_operation(rec,operation_line)
            return {
                'context': self.env.context,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'nmvs.manual.operation',
                'res_id': self.id,
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }

    def get_packs_and_operation_data(self):
        # temp_data['ProductScheme'] = pack[0]
        # temp_data['ProductCode'] = pack[1]
        # temp_data['ProductBatchId'] = pack[2]
        # temp_data['ProdutctExpDate'] = pack[3]
        # temp_data['Pack'] = pack[4]
        for rec in self:
            operation = rec.operation
            packs = []
            if rec.data_fill == 'inventory':
                if len(rec.inventory_pack_ids.ids) == 1:
                    operation = rec.operation.split('-')[0]
                    for pack in rec.inventory_pack_ids:
                        year = str(pack.pack_id.expiration_date.year)[-2:]
                        month = str(pack.pack_id.expiration_date.month)
                        day = str(pack.pack_id.expiration_date.day)
                        if len(day) == 1:
                            day = '0' + day
                        if len(month) == 1:
                            month = '0' + month
                        expiration_date = year + month + day

                        packs.append('GTIN')
                        packs.append(rec.product_id.barcode)
                        packs.append(rec.batch_code)
                        packs.append(expiration_date) ### trocar data
                        packs.append(pack.pack_id.name)
                        packs = [packs]
                else:
                    operation = rec.operation.split('-')[1]
                    for pack in rec.inventory_pack_ids:
                        year = str(pack.pack_id.expiration_date.year)[-2:]
                        month = str(pack.pack_id.expiration_date.month)
                        day = str(pack.pack_id.expiration_date.day)
                        if len(day) == 1:
                            day = '0' + day
                        if len(month) == 1:
                            month = '0' + month
                        expiration_date = year + month + day

                        temp_pack = []
                        temp_pack.append('GTIN')
                        temp_pack.append(rec.product_id.barcode)
                        temp_pack.append(rec.batch_code)
                        temp_pack.append(expiration_date)
                        temp_pack.append(pack.pack_id.name)
                        packs.append(temp_pack)

            else:
                if len(rec.manual_pack_ids.ids) == 1:
                    operation = rec.operation.split('-')[0]
                    for pack in rec.manual_pack_ids:
                        packs.append('GTIN')
                        packs.append(rec.product_code)
                        packs.append(rec.batch_code)
                        packs.append(rec.expiration_date)
                        packs.append(pack.serial_code)
                        packs = [packs]
                else:
                    operation = rec.operation.split('-')[1]
                    for pack in rec.manual_pack_ids:
                        temp_pack = []
                        temp_pack.append('GTIN')
                        temp_pack.append(rec.product_code)
                        temp_pack.append(rec.batch_code)
                        temp_pack.append(rec.expiration_date)
                        temp_pack.append(pack.serial_code)
                        packs.append(temp_pack)
        return packs,operation



class NmvsManualOperationPacks(models.TransientModel):
    _name = 'nmvs.manual.operation.packs'

    manual_operation_id = fields.Many2one('nmvs.manual.operation', string="Comunicação")
    product_id = fields.Many2one(related='pack_id.product_id', string="Artigo")
    pack_state = fields.Selection(string="Estado", selection=[('ACTIVE','Ativo'),('INACTIVE','Inativo'),('UNKNOWN','Desconhecido')])
    pack_state_reason = fields.Char(string="Motivo")
    pack_id = fields.Many2one('stock.production.lot', string="Pack", domain="[('product_id', '=', product_id)]")
    operation_status = fields.Selection(string="Estado da Operação", selection=[('done','Concluída'), ('failed','Falhada'), ('waiting','A aguardar Confirmação')])
    return_code = fields.Char(string="Return Code")
    #pack_status = fields.Selection()
    #pack_status_reason = fields.Selection()

class NmvsManualOperationManualPacks(models.TransientModel):
    _name = 'nmvs.manual.operation.manual.packs'

    manual_operation_id = fields.Many2one('nmvs.manual.operation', string="Comunicação")

    product_code = fields.Char(string="Código do Artigo", related='manual_operation_id.product_code')
    serial_code = fields.Char(string='Nº de Série')
    pack_state = fields.Selection(string="Estado", selection=[('ACTIVE','Ativo'),('INACTIVE','Inativo'),('UNKNOWN','Desconhecido')])
    pack_state_reason = fields.Char(string="Motivo")
    return_code = fields.Char(string="Return Code")


    operation_status = fields.Selection(string="Estado da Operação", selection=[('done','Concluída'), ('failed','Falhada'), ('waiting','A aguardar Confirmação')])
    #pack_status = fields.Selection()
    #pack_status_reason = fields.Selection()



class NmvsTempBatchCode(models.TransientModel):
    _name = 'nmvs.temp.batch.code'

    name = fields.Char(string='lote')
    product_id = fields.Many2one(string="Artigo")

