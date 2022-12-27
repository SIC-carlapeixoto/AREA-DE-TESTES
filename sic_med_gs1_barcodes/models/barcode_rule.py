import re

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'


    type = fields.Selection(
        selection_add=[
            ('batch_code', 'Medicine Batch Code'),
            ('exp_date', 'Medicine Expiration Date'),
        ], ondelete={
            'batch_code': 'set default',
            'exp_date': 'set default',
        })
