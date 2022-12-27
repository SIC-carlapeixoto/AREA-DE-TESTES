# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nmvs_transaction_language = fields.Char(string="Transaction Language", default="eng", config_parameter='sic_nmvs_connector.nmvs_transaction_language')
    nmvs_us_supplier = fields.Char(string="US Supplier", config_parameter='sic_nmvs_connector.nmvs_us_supplier')
    nmvs_us_version = fields.Char(string="US Version", config_parameter='sic_nmvs_connector.nmvs_us_version')
    nmvs_us_name = fields.Char(string="US Name", config_parameter='sic_nmvs_connector.nmvs_us_name')
    nmvs_login = fields.Char(string="Login", config_parameter='sic_nmvs_connector.nmvs_login')
    nmvs_user = fields.Char(string="User", config_parameter='sic_nmvs_connector.nmvs_user')
    nmvs_key = fields.Char(string="Key", config_parameter='sic_nmvs_connector.nmvs_key')

   # def set_values(self):
   #     """employee setting field values"""
   #     res = super(ResConfigSettings, self).set_values()
   #     self.env['ir.config_parameter'].set_param('sic_nmvs_connector.base_salary', self.base_salary)
   #     return res
   # def get_values(self):
   #     """employee limit getting field values"""
   #     res = super(ResConfigSettings, self).get_values()
   #     value = self.env['ir.config_parameter'].sudo().get_param('sic_nmvs_connector.base_salary')
   #     res.update(
   #         base_salary=float(value)
   #     )
   #     return res


    # ClientLoginId = 'SWS'
    # UserId = 'TEIX1006'
    # Password = 'by2-fnNUXaes!20SIC22'
    #
    # #  User Software and Transaction Data
    # USName = '1-Teste-0'
    # USSupplier = 'SIC'
    # USVersion = '0.1'
    # TransactionLanguage = 'eng'

    # TransactionId = 'Test-0001'
