# -*- coding: utf-8 -*-
#SmartImproveConsulting
from odoo.addons.sic_nmvs_connector.nmvs_data.soaps import *


NMVS_OPERATIONS = [
                   ('PingSinglePack','PingSinglePack'),
                   ('G110Verify', 'G110Verify'),
                   ('G120Dispense', 'G120Dispense'),
                   ('G121UndoDispense', 'G121UndoDispense'),
                   ('G130Destroy', 'G130Destroy'),
                   ('G140Export', 'G140Export'),
                   ('G141UndoExport', 'G141UndoExport'),
                   ('G150Sample', 'G150Sample'),
                   ('G151UndoSample', 'G151UndoSample'),
                   ('G160FreeSample', 'G160FreeSample'),
                   ('G161UndoFreeSample', 'G161UndoFreeSample'),
                   ('G170Lock', 'G170Lock'),
                   ('G171UndoLock', 'G171UndoLock'),
                   ('G180Stolen', 'G180Stolen'),

                   ('PingBulk', 'PingBulk'),
                   ('G115BulkVerify', 'G115BulkVerify'),
                   ('G125BulkDispense', 'G125BulkDispense'),
                   ('G127BulkUndoDispense', 'G127BulkUndoDispense'),
                   ('G135BulkDestroy', 'G135BulkDestroy'),
                   ('G145BulkExport', 'G145BulkExport'),
                   ('G147BulkUndoExport', 'G147BulkUndoExport'),
                   ('G155BulkSample', 'G155BulkSample'),
                   ('G157BulkUndoSample', 'G157BulkUndoSample'),
                   ('G165BulkFreeSample', 'G165BulkFreeSample'),
                   ('G167BulkUndoFreeSample', 'G167BulkUndoFreeSample'),
                   ('G175BulkLocks', 'G175BulkLocks'),
                   ('G177BulkUndoLock', 'G177BulkUndoLock'),
                   ('G185BulkStolen', 'G185BulkStolen'),
                   ('G188RequestBulkPackResult', 'G188RequestBulkPackResult'),

                   ('PingMixedBulk', 'PingMixedBulk'),
                   ('G195SubmitBulkTransaction', 'G195SubmitBulkTransaction'),
                  ]



OPERATIONS = {
    'PingSinglePack': {'name': 'PingSinglePack', 'type': 'Ping', 'response_unpacker':'SinglePackPing_response_unpacker'},
    'G110Verify': {'name': 'G110Verify', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G120Dispense': {'name': 'G120Dispense', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G121UndoDispense': {'name': 'G121UndoDispense', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G130Destroy': {'name': 'G130Destroy', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G140Export': {'name': 'G140Export', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G141UndoExport': {'name': 'G141UndoExport', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G150Sample': {'name': 'G150Sample', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G151UndoSample': {'name': 'G151UndoSample', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G160FreeSample': {'name': 'G160FreeSample', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G161UndoFreeSample': {'name': 'G161UndoFreeSample', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G170Lock': {'name': 'G170Lock', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G171UndoLock': {'name': 'G171UndoLock', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},
    'G180Stolen': {'name': 'G180Stolen', 'type': 'SinglePack', 'header': standard_header, 'body': standard_single_pack_body, 'response_unpacker': 'standard_single_pack_response_unpacker'},


    'PingBulk': {'name': 'PingBulk', 'type': 'Ping', 'response_unpacker':'BulkPing_response_unpacker'},
    'G115BulkVerify': {'name': 'G115BulkVerify', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G125BulkDispense': {'name': 'G125BulkDispense', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G127BulkUndoDispense': {'name': 'G127BulkUndoDispense', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G135BulkDestroy': {'name': 'G135BulkDestroy', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G145BulkExport': {'name': 'G145BulkExport', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G147BulkUndoExport': {'name': 'G147BulkUndoExport', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G155BulkSample': {'name': 'G155BulkSample', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G157BulkUndoSample': {'name': 'G157BulkUndoSample', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G165BulkFreeSample': {'name': 'G165BulkFreeSample', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G167BulkUndoFreeSample': {'name': 'G167BulkUndoFreeSample', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G175BulkLocks': {'name': 'G175BulkLocks', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G177BulkUndoLock': {'name': 'G177BulkUndoLock', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G185BulkStolen': {'name': 'G185BulkStolen', 'type': 'Bulk', 'header': standard_header, 'body': standard_bulk_body, 'response_unpacker': 'standard_bulk_response_unpacker'},
    'G188RequestBulkPackResult': {'name': 'G188RequestBulkPackResult', 'type': 'BulkResult', 'header': standard_header, 'body': request_bulk_pack_result_body, 'response_unpacker': 'G188_response_unpacker'},

    'G195SubmitBulkTransaction': {'name': 'G195SubmitBulkTransaction', 'type': 'MixedBulk', 'header': standard_header, 'body': standard_mixed_bulk_body, 'response_unpacker': 'standard_mixed_bulk_response_unpacker'},
    'G196RequestBulkTransactionResult': {'name': 'G196RequestBulkTransactionResult', 'type': 'MixedBulkResult', 'header': standard_header, 'body': request_mixed_bulk_result_body, 'response_unpacker': 'G196_response_unpacker'},
}
