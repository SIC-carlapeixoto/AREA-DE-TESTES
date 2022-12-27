#-*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.addons.sic_nmvs_connector.nmvs_data.operations import *
from odoo.addons.sic_nmvs_connector.nmvs_data.nmvs_functions import *

class NmvsMixedBulkOperation(models.TransientModel):
    _name = 'nmvs.mixed.bulk.operation'

    name = fields.Char(string="Nome")

    operation_ids = fields.One2many('nmvs.manual.operation', 'mixed_bulk_operation', string="Operações")

    operation_date = fields.Datetime(string="Data")

    operation_done = fields.Boolean()
    operation_status = fields.Selection(string="Estado da Operação", selection=[('done','Concluída'), ('failed','Falhada'), ('waiting','A aguardar Confirmação')])
    result = fields.Char(string="Resultado")

    def get_packs_and_operations_data(self):
        # temp_data['ProductScheme'] = pack[0]
        # temp_data['ProductCode'] = pack[1]
        # temp_data['ProductBatchId'] = pack[2]
        # temp_data['ProdutctExpDate'] = pack[3]
        # temp_data['Pack'] = pack[4]
        for rec in self:
            operations_list = []
            transaction_id = 0
            for operation in rec.operation_ids:
                operation_code = operation.operation
                packs = []
                if operation.data_fill == 'inventory':
                    if len(operation.inventory_pack_ids.ids) == 1:
                        operation_code = operation.operation.split('-')[0]
                        #  for pack in operation.inventory_pack_ids:acabar de preencher com os campos a ser criados
                        #packs.append()
                        #packs.append()
                        #packs.append()
                        #packs.append()
                        packs = [packs]
                        # else:
                        #  operation_code = operation.operation.split('-')[1]
                        #  for pack in operation.inventory_pack_ids:
                        #temp_pack = []
                        #temp_pack.append()
                        #temp_pack.append()
                        #temp_pack.append()
                        #temp_pack.append()
                        #temp_pack.append()
                        #packs.append(temp_pack)

                else:
                    operation_code = operation.operation.split('-')[0]
                    for pack in operation.manual_pack_ids:
                        temp_pack = []
                        temp_pack.append('GTIN')
                        temp_pack.append(operation.product_code)
                        temp_pack.append(operation.batch_code)
                        temp_pack.append(operation.expiration_date)
                        temp_pack.append(pack.serial_code)
                        client_transaction_id = rec.env['ir.sequence'].next_by_code('nmvs.operation')
                        language = 'eng'
                        operations_list.append({'packs':temp_pack,'operation_code':operation_code,'transaction_id':client_transaction_id,'language':language,'operation_date': fields.datetime.now(), 'data_fill':operation.data_fill})
            return operations_list

    def create_mixed_operations(self,operations_list,mixed_bulk_operation):
        for operation in operations_list:
            vals ={
                'operation': operation['operation_code'],
                'operation_date': operation['operation_date'],
                'operation_status': 'waiting',
                'product_code': operation['packs'][1],
                'batch_code': operation['packs'][2],
                'expiration_date': operation['packs'][3],
                'serial_code': operation['packs'][4],
                'data_fill':operation['data_fill'],
                'name': operation['transaction_id'],
                'operation_id': mixed_bulk_operation.id
            }
            self.env['nmvs.operation.mixed.bulk.lines'].sudo().create(vals)

    def execute_operation(self):
        for rec in self:
            operations_list = rec.get_packs_and_operations_data()
            client_transaction_id = rec.env['ir.sequence'].next_by_code('nmvs.operation')

            ClientLoginId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_login")
            UserId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_user")
            Password = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_key")
            USName = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_name")
            USSupplier = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_supplier")
            USVersion = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_version")
            TransactionLanguage = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_transaction_language")
            TransactionId = self.env['ir.sequence'].next_by_code('nmvs.operation')

            result_code, transaction_id, op_obj = call_nmvs(OPERATIONS['G195SubmitBulkTransaction'], operations_list, client_transaction_id, ClientLoginId, UserId, Password, USName, USSupplier, USVersion, TransactionId, TransactionLanguage)
            operation_status = 'waiting'
            vals = {
                'operation': 'G195SubmitBulkTransaction',
                'result_code': result_code[0],
                'result_code_desc': result_code[1],
                'transaction_id': transaction_id,
                'operation_date': fields.datetime.now(),
                'operation_status': operation_status,
                'result': 'waiting',
                'type': 'system',
                'name': client_transaction_id
                }
            mixed_bulk_operation = rec.env['nmvs.operation'].sudo().create(vals)
            rec.create_mixed_operations(operations_list,mixed_bulk_operation)


            ClientLoginId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_login")
            UserId = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_user")
            Password = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_key")
            USName = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_name")
            USSupplier = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_supplier")
            USVersion = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_us_version")
            TransactionLanguage = self.env['ir.config_parameter'].sudo().get_param("sic_nmvs_connector.nmvs_transaction_language")
            TransactionId = self.env['ir.sequence'].next_by_code('nmvs.operation')

            result_code, transaction_id, op_obj = call_nmvs(OPERATIONS['G196RequestBulkTransactionResult'], [], transaction_id, ClientLoginId, UserId, Password, USName, USSupplier, USVersion, TransactionId, TransactionLanguage)

            operation_status = 'waiting'
            client_transaction_id = rec.env['ir.sequence'].next_by_code('nmvs.operation')
            vals = {
                'operation': 'G196RequestBulkTransactionResult',
                'operation_date': fields.datetime.now(),
                'parent_id': mixed_bulk_operation.id,
                'operation_status': operation_status,
                'result': 'waiting',
                'type': 'system',
                'name': TransactionId
                }
            mixed_bulk_result_operation = rec.env['nmvs.operation'].sudo().create(vals)
            mixed_bulk_result_operation.execute_operation()




        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'nmvs.mixed.bulk.operation',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
