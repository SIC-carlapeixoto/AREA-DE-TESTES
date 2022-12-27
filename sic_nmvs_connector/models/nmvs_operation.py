#-*- coding: utf-8 -*-
from odoo import models, fields, api

from odoo.addons.sic_nmvs_connector.nmvs_data.operations import *
from odoo.addons.sic_nmvs_connector.nmvs_data.nmvs_functions import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
import playsound
from pathlib import Path

UNDO_OPS = {
            'G120Dispense':'G121UndoDispense',
            'G125BulkDispense':'G127BulkUndoDispense',
            'G140Export':'G141UndoExport',
            'G145BulkExport':'G147BulkUndoExport',
            'G150Sample':'G151UndoSample',
            'G155BulkSample':'G157BulkUndoSample',
            'G160FreeSample':'G161UndoFreeSamplee',
            'G165BulkFreeSample':'G167BulkUndoFreeSample',
            'G170Lock':'G171UndoLock',
            'G175BulkLocks':'G177BulkUndoLock',
            } 





class NMVSOperation(models.Model):
    _name = 'nmvs.operation'
    _description = 'NMVS Operations'

    name = fields.Char(string="Nome")
    parent_id = fields.Many2one('nmvs.operation', string="Documento de Origem")
    data_fill = fields.Selection(string="Inserir Serial Nº", selection=[('manual','Manualmente'),('inventory','A partir do Inventário')], default="inventory")
    type = fields.Selection(string="Tipo", selection=[('system','Sistema'),('manual','Manual')], default='system')
    operation = fields.Selection(string="Operação", selection= [
         ('G110Verify', 'Verificar Serial Nº'),
         ('G115BulkVerify', 'Verificar Serial Nº'),
         ('G120Dispense', 'Dispensar Serial Nº'),
         ('G125BulkDispense', 'Dispensar Serial Nº'),
         ('G121UndoDispense', 'Undo Dispensar Serial Nº'),
         ('G127BulkUndoDispense', 'Undo Dispensar Serial Nº'),
         ('G130Destroy', 'Destruir Serial Nº'),
         ('G135BulkDestroy', 'Destruir Serial Nº'),
         ('G140Export', 'Exportar Serial Nº'),
         ('G145BulkExport', 'Exportar Serial Nº'),
         ('G141UndoExport', 'Undo Exportar Serial Nº'),
         ('G147BulkUndoExport', 'Undo Exportar Serial Nº'),
         ('G150Sample', 'Para Amostra'),
         ('G155BulkSample', 'Para Amostra'),
         ('G151UndoSample', 'Undo Para Amostra'),
         ('G157BulkUndoSample', 'Undo Para Amostra'),
         ('G160FreeSample', 'Para Amostra Gratuita'),
         ('G165BulkFreeSample', 'Para Amostra Gratuita'),
         ('G161UndoFreeSample', 'Undo Para Amostra Gratuita'),
         ('G167BulkUndoFreeSample', 'Undo Para Amostra Gratuita'),
         ('G170Lock', 'Bloquear Serial Nº'),
         ('G175BulkLocks', 'Bloquear Serial Nº'),
         ('G171UndoLock', 'Undo Bloquear Serial Nº'),
         ('G177BulkUndoLock', 'Undo Bloquear Serial Nº'),
         ('G180Stolen', 'Serial Nº Roubado'),
         ('G185BulkStolen', 'Serial Nº Roubados'),
         ('G188RequestBulkPackResult', 'Resultado Bulk'),
         ('G195SubmitBulkTransaction', 'Enviar Lista de Comunicações'),
         ('G196RequestBulkTransactionResult', 'Resultado Lista de Comunicações'),
          ])

    operation_date = fields.Datetime(string="Data")
    transaction_id = fields.Char(string="ID Trans. NMVS")
    product_id = fields.Many2one('product.product', string="Artigo",)

    product_code = fields.Char(string="Código do Artigo")
    batch_code = fields.Char(string='Lote')
    expiration_date = fields.Char(string='Data de Validade (YYMMDD)')

    inventory_pack_ids = fields.One2many('nmvs.operation.packs', 'operation_id', string="Packs")
    manual_pack_ids = fields.One2many('nmvs.operation.manual.packs', 'operation_id', string="Packs")
    mixed_bulk_lines = fields.One2many('nmvs.operation.mixed.bulk.lines', 'operation_id', string="Packs")

    result = fields.Char(string="Resultado")
    result_code = fields.Char(string="Código de Reultado")
    result_code_desc = fields.Char(string="Desc. Código de Reultado")
    operation_status = fields.Selection(string="Estado da Operação", selection=[('done','Concluída'), ('failed','Falhada'), ('waiting','A aguardar Confirmação')])

    undone = fields.Boolean(string='Comunicação Revertida', default=False)
    can_be_undone = fields.Boolean(string='Pode ser Revertida', compute='_check_undo_option')

    picking_id = fields.Many2one('stock.picking', string='Saída')

    def _check_undo_option(self):
        for rec in self:
            rec.can_be_undone = (datetime.now() <= rec.operation_date + relativedelta(days=10)) and rec.operation in UNDO_OPS.keys() and not rec.undone


    def undo_operation(self):
        for rec in self:
            transaction_id = ''
            ClientLoginId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_login")
            UserId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_user")
            Password = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_key")
            USName = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_name")
            USSupplier = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_supplier")
            USVersion = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_version")
            TransactionLanguage = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_transaction_language")
            TransactionId = self.env['ir.sequence'].next_by_code('nmvs.operation')
            packs,operation = self.get_packs_and_operation_data()
            operation = UNDO_OPS[rec.operation]


            values = {}
            values['name'] = TransactionId
            values['operation'] = operation
            values['operation_date'] = fields.datetime.now()
            values['type'] = 'system'
            values['batch_code'] = rec.batch_code
            values['expiration_date'] = rec.expiration_date
            values['data_fill'] = rec.data_fill

            if rec.data_fill == 'manual':
                values['product_code'] = rec.product_code
            else:
                values['product_id'] = rec.product_id.id
            
            operation_line = self.create(values)

            result_code, transaction_id, pack_obj = call_nmvs(OPERATIONS[operation], packs, transaction_id, ClientLoginId, UserId, Password, USName, USSupplier, USVersion, TransactionId, TransactionLanguage)
            
            operation_status = False

            if result_code:
                if result_code[0]  == 'NMVS_SUCCESS':
                    operation_status = 'done'
                else:
                    operation_status = 'failed'

            if OPERATIONS[operation]['type'] == 'SinglePack':
                self.set_pack_result(pack_obj)
            if OPERATIONS[operation]['type'] == 'BulkResult':
                self.set_bulk_pack_result(pack_obj)

            vals = {
                'result_code': result_code[0],
                'result_code_desc': result_code[1],
                'transaction_id': transaction_id,
                'operation_status': operation_status,
                'result': rec.result,
                }
            operation_line.write(vals)

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
                        self.set_bulk_pack_result(packs_obj)

                else:
                    G188operation_status = 'failed'
                    operation_line = 'failed'

                    #NMVS_SUCCESS
                    # [{'pack': 'PK001E09DE7E25FD94F', 'state': 'ACTIVE', 'return_code': 'NMVS_SUCCESS'}, {'pack': 'PK0028E21615B83AA4C', 'state': 'ACTIVE', 'return_code': 'NMVS_SUCCESS'}]

                vals['operation_status'] = G188operation_status
                vals['result_code'] = result_code[0]
                vals['result_code_desc'] = result_code[1]
                G188_operation_line = rec.env['nmvs.operation'].sudo().create(vals)

            self.send_packs_to_operation(operation_line)
            rec.undone = True

            return {
                'context': self.env.context,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'nmvs.operation',
                'res_id': operation_line.id,
                'view_id': False,
                'type': 'ir.actions.act_window',
            }



    @api.model
    def create_single_pack_verification(self, values):
        data_fill = ''
        pack_id = False
        pack_serial = ''

        if 'pack_serial' in values.keys():
            if values['pack_serial'] not in [False, None, '']:
                pack_serial = values['pack_serial']
                data_fill = 'manual'
            values.pop('pack_serial')

        if 'pack_id' in values.keys():
            if  values['pack_id'] not in [False, None, '']:
                pack_serial = values['pack_id']['name']
                pack_id = values['pack_id']['id']
                data_fill = 'inventory'
            values.pop('pack_id')




        values['data_fill'] = data_fill
        ClientLoginId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_login")
        UserId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_user")
        Password = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_key")
        USName = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_name")
        USSupplier = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_supplier")
        USVersion = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_version")
        TransactionLanguage = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_transaction_language")
        TransactionId = self.env['ir.sequence'].next_by_code('nmvs.operation')
        values['name'] = TransactionId
        operation_id = self.create(values)

        if data_fill == 'manual':
            pack_id = self.env['nmvs.operation.manual.packs'].create({'operation_id':operation_id.id, 'serial_code':pack_serial})
            packs = [['GTIN', values['product_code'], values['batch_code'], values['expiration_date'], pack_serial]]
        else:
            p = self.env['stock.production.lot'].search([('id','=',pack_id)])
            pack_id = self.env['nmvs.operation.packs'].create({'operation_id':operation_id.id, 'pack_id':p.id})
            packs = [['GTIN', values['product_code'], values['batch_code'], values['expiration_date'], pack_serial]]   


        result_code, transaction_id, pack_obj = call_nmvs(OPERATIONS['G110Verify'], packs, False, ClientLoginId, UserId, Password, USName, USSupplier, USVersion, TransactionId, TransactionLanguage)
        
        # Set Serial Nº Result
        po = pack_obj[0]
        pack_id.pack_state = po[1]
        if data_fill == 'inventory':
            pack_id.pack_id.pack_state = po[1]

        pack_id.operation_status = 'done'
        if len(po) > 2:
            pack_id.pack_state_reason = po[2]
            if data_fill == 'inventory':
                pack_id.pack_id.pack_state_reason = po[1]
        if len(po) > 3:
            pack_id.result_code = po[3]
        
        #Set Operation Result
        operation_status = False
        if result_code:
            if result_code[0]  == 'NMVS_SUCCESS':
                operation_status = 'done'
            else:
                operation_status = 'failed'

        operation_id.result_code = result_code[0]
        operation_id.result_code_desc = result_code[1]
        operation_id.transaction_id = transaction_id
        operation_id.operation_date = fields.datetime.now()
        operation_id.operation_status = operation_status

        if pack_id.pack_state == 'ACTIVE':
            print(str(Path(__file__).parent.resolve())+'/success_beep.mp3')
            #playsound
        else:
            #playsound
            print(str(Path(__file__).parent.resolve())+'/error_beep.mp3')
        
        locked = False
        if data_fill == 'inventory':
            if pack_id.pack_id.locked:
                locked = True
            pack_serial = pack_id.pack_id.name
        else:
            pack_serial = pack_id.serial_code


        return [pack_serial, pack_id.pack_state, locked]


    def set_bulk_pack_result(self,pack_obj):
        #[{'pack': 'PK001E09DE7E25FD94F', 'state': 'ACTIVE', 'return_code': 'NMVS_SUCCESS'}

        if self.parent_id.data_fill == 'manual':
            for man_pack in self.parent_id.manual_pack_ids:
                for po in pack_obj:
                    if po['pack'] == man_pack.serial_code:

                        if po['return_code'] == 'NMVS_SUCCESS':
                            man_pack.operation_status = 'done'
                        if 'state' in po.keys():
                            man_pack.pack_state = po['state']
                            if 'reason' in po.keys():
                                man_pack.pack_state_reason = po['reason']
                        if 'return_code' in po.keys():
                            man_pack.return_code = po['return_code']

        else:
            for inv_pack in self.parent_id.inventory_pack_ids:
                for po in pack_obj:
                    if po['pack'] == inv_pack.serial_code:
                        if po['return_code'] == 'NMVS_SUCCESS':
                            inv_pack.operation_status = 'done'
                        if 'state' in po.keys():
                            inv_pack.pack_state = po['state']
                            if 'reason' in po.keys():
                                inv_pack.pack_state_reason = po['reason']
                        if 'return_code' in po.keys():
                            inv_pack.return_code = po['return_code']


    def set_mixed_bulk_result(self,op_obj):
        #[{'client_transaction_id': 'RB-00000376', 'return_code': ('NMVS_SUCCESS', 'Successfully processed.')},
        for op in op_obj:
            for parent_op_line in self.parent_id.mixed_bulk_lines:
                if parent_op_line.name == op['client_transaction_id']:
                    if 'state' in op.keys():
                        parent_op_line.pack_state = op['state']
                    if 'reason' in op.keys():
                        parent_op_line.pack_state_reason = op['reason']
                    if 'return_code' in op.keys():
                        parent_op_line.return_code = op['return_code'][0] + ' - ' + op['return_code'][1]
                        if op['return_code'][0] == 'NMVS_SUCCESS':
                            parent_op_line.operation_status = 'done'


    def execute_operation(self):
        for rec in self:

            ClientLoginId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_login")
            UserId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_user")
            Password = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_key")
            USName = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_name")
            USSupplier = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_supplier")
            USVersion = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_version")
            TransactionLanguage = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_transaction_language")


            if rec.operation == 'G188RequestBulkPackResult':
                operation = OPERATIONS['G188RequestBulkPackResult']
                result_code, transaction_id, packs_obj = call_nmvs(operation, [], rec.parent_id.transaction_id, ClientLoginId, UserId, Password, USName, USSupplier, USVersion, rec.name, TransactionLanguage) ## rec.name no lugar do transactionID
                rec.operation_date = fields.datetime.now()
                rec.result_code = result_code[0]
                rec.result_code_desc = result_code[1]
                if result_code[0] == 'NMVS_FE_TX_02': #Result not ready create history with pending status   # verificar possiveis codigos de falha !
                    rec.operation_status = 'waiting'
                    rec.parent_id.operation_status = 'waiting'

                elif result_code[0] == 'NMVS_SUCCESS':
                    rec.operation_status = 'done'
                    rec.parent_id.operation_status = 'done'
                    rec.set_bulk_pack_result(packs_obj)
                else:
                    rec.operation_status = 'failed'
                    rec.parent_id.operation_status = 'failed'

            if rec.operation == 'G196RequestBulkTransactionResult':
                operation = OPERATIONS['G196RequestBulkTransactionResult']
                result_code, transaction_id, packs_obj = call_nmvs(operation, [], rec.parent_id.transaction_id, ClientLoginId, UserId, Password, USName, USSupplier, USVersion, TransactionId, TransactionLanguage)## rec.name no lugar do transactionID
                rec.operation_date = fields.datetime.now()
                rec.result_code = result_code[0]
                rec.result_code_desc = result_code[1]
                if result_code[0] == 'NMVS_FE_TX_02': #Result not ready create history with pending status   # verificar possiveis codigos de falha !
                    rec.operation_status = 'waiting'
                    rec.parent_id.operation_status = 'waiting'

                elif result_code[0] == 'NMVS_SUCCESS':
                    rec.operation_status = 'done'
                    rec.parent_id.operation_status = 'done'
                    rec.set_mixed_bulk_result(packs_obj)
                else:
                    rec.operation_status = 'failed'
                    rec.parent_id.operation_status = 'failed'


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
                    operation = rec.operation
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
                    operation = rec.operation
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
                    operation = rec.operation
                    for pack in rec.manual_pack_ids:
                        packs.append('GTIN')
                        packs.append(rec.product_code)
                        packs.append(rec.batch_code)
                        packs.append(rec.expiration_date)
                        packs.append(pack.serial_code)
                        packs = [packs]
                else:
                    operation = rec.operation
                    for pack in rec.manual_pack_ids:
                        temp_pack = []
                        temp_pack.append('GTIN')
                        temp_pack.append(rec.product_code)
                        temp_pack.append(rec.batch_code)
                        temp_pack.append(rec.expiration_date)
                        temp_pack.append(pack.serial_code)
                        packs.append(temp_pack)
        return packs,operation


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
                self.env['nmvs.operation.manual.packs'].sudo().create(vals)
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
                self.env['nmvs.operation.packs'].sudo().create(vals)


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





class NmvsOperationPacks(models.Model):
    _name = 'nmvs.operation.packs'

    operation_id = fields.Many2one('nmvs.operation', string="Comunicação")
    product_id = fields.Many2one(related='pack_id.product_id', string="Artigo")
    pack_id = fields.Many2one('stock.production.lot', string="Serial Nº")
    pack_state = fields.Selection(string="Estado", selection=[('ACTIVE','Ativo'),('INACTIVE','Inativo'),('UNKNOWN','Desconhecido')])
    pack_state_reason = fields.Char(string="Motivo")
    return_code = fields.Char(string="Return Code")

    operation_status = fields.Selection(string="Estado da Operação", selection=[('done','Concluída'), ('failed','Falhada'), ('waiting','A aguardar Confirmação')])


class NmvsOperationManualPacks(models.Model):
    _name = 'nmvs.operation.manual.packs'

    operation_id = fields.Many2one('nmvs.operation', string="Comunicação")

    product_code = fields.Char(string="Código do Artigo", related='operation_id.product_code')
    serial_code = fields.Char(string='Serial Nº')
    pack_state = fields.Selection(string="Estado", selection=[('ACTIVE','Ativo'),('INACTIVE','Inativo'),('UNKNOWN','Desconhecido')])
    pack_state_reason = fields.Char(string="Motivo")
    return_code = fields.Char(string="Return Code")

    operation_status = fields.Selection(string="Estado da Operação", selection=[('done','Concluída'), ('failed','Falhada'), ('waiting','A aguardar Confirmação')])
    #pack_status = fields.Selection()
    #pack_status_reason = fields.Selection()

class NmvsOperationMixedBulkLines(models.Model):
    _name = 'nmvs.operation.mixed.bulk.lines'

    name = fields.Char(string="Nome")
    operation_id = fields.Many2one('nmvs.operation', string="Comunicação")
    operation = fields.Selection(string="Operação", selection= [
         ('G110Verify', 'Verificar Serial Nº'),
         ('G115BulkVerify', 'Verificar Serial Nº'),
         ('G120Dispense', 'Dispensar Serial Nº'),
         ('G125BulkDispense', 'Dispensar Serial Nº'),
         ('G121UndoDispense', 'Undo Dispensar Serial Nº'),
         ('G127BulkUndoDispense', 'Undo Dispensar Serial Nº'),
         ('G130Destroy', 'Destruir Serial Nº'),
         ('G135BulkDestroy', 'Destruir Serial Nº'),
         ('G140Export', 'Exportar Serial Nº'),
         ('G145BulkExport', 'Exportar Serial Nºcks'),
         ('G141UndoExport', 'Undo Exportar Serial Nº'),
         ('G147BulkUndoExport', 'Undo Exportar Serial Nº'),
         ('G150Sample', 'Para Amostra'),
         ('G155BulkSample', 'Para Amostra'),
         ('G151UndoSample', 'Undo Para Amostra'),
         ('G157BulkUndoSample', 'Undo Para Amostra'),
         ('G160FreeSample', 'Para Amostra Gratuita'),
         ('G165BulkFreeSample', 'Para Amostra Gratuita'),
         ('G161UndoFreeSamplee', 'Undo Para Amostra Gratuita'),
         ('G167BulkUndoFreeSample', 'Undo Para Amostra Gratuita'),
         ('G170Lock', 'Bloquear Serial Nº'),
         ('G175BulkLocks', 'Bloquear Serial Nº'),
         ('G171UndoLock', 'Undo Bloquear Serial Nº'),
         ('G177BulkUndoLock', 'Undo Bloquear Serial Nº'),
         ('G180Stolen', 'Serial Nº Roubado'),
         ('G185BulkStolen', 'Serial Nº Roubados'),
         ('G188RequestBulkPackResult', 'Resultado Bulk'),
         ('G195SubmitBulkTransaction', 'Enviar Lista de Comunicações'),
         ('G196RequestBulkTransactionResult', 'Resultado Lista de Comunicações'),
          ])

    data_fill = fields.Selection(string="Inserir Serial Nº", selection=[('manual','Manualmente'),('inventory','A partir do Inventário')], default="inventory")
    operation_date = fields.Datetime(string="Data")
    product_code = fields.Char(string="Código do Artigo")
    serial_code = fields.Char(string='Nº de Série')
    batch_code = fields.Char(string='Lote')
    expiration_date = fields.Char(string='Data de Validade (YYMMDD)')
    pack_state = fields.Selection(string="Estado", selection=[('ACTIVE','Ativo'),('INACTIVE','Inativo'),('UNKNOWN','Desconhecido')])
    pack_state_reason = fields.Char(string="Motivo")
    return_code = fields.Char(string="Return Code")

    operation_status = fields.Selection(string="Estado da Operação", selection=[('done','Concluída'), ('failed','Falhada'), ('waiting','A aguardar Confirmação')])
    #pack_status = fields.Selection()
    #pack_status_reason = fields.Selection()
