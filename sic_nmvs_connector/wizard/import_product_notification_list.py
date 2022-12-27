#-*- coding: utf-8 -*-

from xlrd import open_workbook
import base64

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ImportProductNotificationList(models.TransientModel):
    _name = 'import.product.notification.list'

    file_content = fields.Binary(string="Listagem Infarmed")
    file_name = fields.Char(string='Ficheiro')

    def read_file(self):
        for rec in self:
            file_data = base64.b64decode(rec.file_content)
            wb = open_workbook(file_contents=file_data)
            sheet = wb.sheet_by_index(0)
            values = sheet._cell_values
            internal_refs_not_prev = []
            for line in values[1:]:
                #['Timogel', 'Timolol', 'Gel oftálmico', '0.4 mg/0.4 g', 'Laboratoires Théa', '5932082', 'Recipiente unidose - 30 unidades(s) - ,4 g']
                name = line[0]
                internal_ref = line[5]
                internal_refs_not_prev.append(internal_ref)
                product_id = self.env['product.template'].search([('default_code','=',internal_ref)])
                if not product_id:
                    product_id = self.env['product.template'].create({'name':name, 'default_code':internal_ref, 'prior_notification': True})
                product_id.prior_notification = True

            products_without_prev_notif = self.env['product.template'].search([('default_code','not in', internal_refs_not_prev),('prior_notification','=',True)]) ## Desativar os Outros
            for p in products_without_prev_notif:
                p.prior_notification = False
