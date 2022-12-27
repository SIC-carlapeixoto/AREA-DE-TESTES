# -*- coding: utf-8 -*-
#SmartImproveConsulting

import requests
import os
import xmltodict

from odoo.addons.sic_nmvs_connector.nmvs_data import soaps as s


def soap_request(payload, url, **kwargs):

    # headers
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    # POST request
    base_path = str(os.path.dirname(os.path.realpath(__file__)))
    response = requests.request("POST", url, headers=headers, data=payload, cert=(base_path + '/cert/certificate.pem', base_path + '/cert/plainkey.pem'), verify=True)
    return response


def format_payload(soap, filled_header, filled_body):
    merged_formats = {**{'header': filled_header}, **{'body': filled_body}}
    return soap.format_map(merged_formats)  # Return Formatted payload


def get_soap_and_url(operation):
    try:
        return eval('s.' + operation['name'] + '[\'soap\']'), eval('s.' + operation['name'] + '[\'url\']')
    except:
        print("Erro na Procura do Soap/Url: " + operation['name'])


def get_single_pack_data(pack):
    temp_data = dict(s.single_pack_data)
    temp_data['ProductScheme'] = pack[0]
    temp_data['ProductCode'] = pack[1]
    temp_data['ProductBatchId'] = pack[2]
    temp_data['ProdutctExpDate'] = pack[3]
    temp_data['Pack'] = pack[4]
    return temp_data


def get_bulk_data(packs):
    temp_data = dict(s.bulk_data)
    temp_data['ProductScheme'] = packs[0][0]
    temp_data['ProductCode'] = packs[0][1]
    temp_data['ProductBatchId'] = packs[0][2]
    temp_data['ProdutctExpDate'] = packs[0][3]
    for pack in packs:
        temp_data['Packs'] += '<urn1:Pack urn1:sn=\"' + pack[4] + '\"/>'
    return temp_data


def get_mixed_bulk_data(operations):
    operations_list_data = []
    for op in operations:
        temp_data = dict(s.mixed_bulk_data)
        temp_data['reqType'] = op['operation_code'][:4]
        temp_data['TransactionId'] = op['transaction_id']
        temp_data['TransactionLanguage'] = op['language']
        temp_data['ProductScheme'] = op['packs'][0]
        temp_data['ProductCode'] = op['packs'][1]
        temp_data['ProductBatchId'] = op['packs'][2]
        temp_data['ProdutctExpDate'] = op['packs'][3]
        temp_data['Packs'] += '<urn1:Pack urn1:sn=\"' + op['packs'][4] + '\"/>'
        operations_list_data.append(temp_data)
    return operations_list_data


def prepare_header_and_body(operation, pack_data, basic_auth_format, software_supplier_and_transaction_format):
    filled_header = operation['header'].format_map({**basic_auth_format, **software_supplier_and_transaction_format})
    filled_body = operation['body'].format_map(pack_data)
    return filled_header, filled_body

def mixed_bulk_operation_prepare_header_and_body(operation, operations_list_data, basic_auth_format, software_supplier_and_transaction_format):
    filled_header = operation['header'].format_map(
        {**basic_auth_format, **software_supplier_and_transaction_format})
    mixed_body = ''
    for op in operations_list_data:
        item = ''
        if op['reqType'][3] in ['1','7']:
            item = s.G195_item_undo
        else:
            item = s.G195_item
        mixed_body += item.format_map(op)


    filled_body = operation['body'].format_map({'Items':mixed_body})
    return filled_header, filled_body




def call_nmvs(operation, packs, transaction_id, ClientLoginId, UserId, Password, USName, USSupplier, USVersion, TransactionId, TransactionLanguage):

    basic_auth_format = {
        "ClientLoginId": ClientLoginId,
        "UserId": UserId,
        "Password": Password,
    }
    software_supplier_and_transaction_format = {
        "USName": USName,
        "USSupplier": USSupplier,
        "USVersion": USVersion,
        "TransactionId": TransactionId,
        "TransactionLanguage": TransactionLanguage,
    }

    if operation['type'] == 'Ping':
        soap, soap_url = get_soap_and_url(operation)  # Buscar Soap e Url
        payload = soap   # only in pings
        response = soap_request(payload, soap_url)

    elif operation['type'] == 'SinglePack':
        if len(packs) > 0:
            for pack in packs:
                soap, soap_url = get_soap_and_url(operation)  # Buscar Soap e Url
                pack_data = get_single_pack_data(pack)
                filled_header, filled_body = prepare_header_and_body(operation, pack_data, basic_auth_format, software_supplier_and_transaction_format)
                payload = format_payload(soap, filled_header, filled_body)
                response = soap_request(payload, soap_url)

    elif operation['type'] == 'Bulk':
        soap, soap_url = get_soap_and_url(operation)  # Buscar Soap e Url
        bulk_data = get_bulk_data(packs)
        filled_header, filled_body = prepare_header_and_body(operation, bulk_data, basic_auth_format, software_supplier_and_transaction_format)
        payload = format_payload(soap, filled_header, filled_body)
        response = soap_request(payload, soap_url)

    elif operation['type'] == 'MixedBulk':
        soap, soap_url = get_soap_and_url(operation)  # Buscar Soap e Url
        mixed_bulk_data = get_mixed_bulk_data(packs)
        filled_header, filled_body = mixed_bulk_operation_prepare_header_and_body(operation, mixed_bulk_data, basic_auth_format, software_supplier_and_transaction_format)
        payload = format_payload(soap, filled_header, filled_body)
        response = soap_request(payload, soap_url)

    elif operation['type'] == 'MixedBulkResult':
        soap, soap_url = get_soap_and_url(operation)  # Buscar Soap e Url
        transaction_data = {'RefNMVSTrxId': transaction_id}
        filled_header, filled_body = prepare_header_and_body(operation, transaction_data, basic_auth_format, software_supplier_and_transaction_format)
        payload = format_payload(soap, filled_header, filled_body)
        response = soap_request(payload, soap_url)

    elif operation['type'] == 'BulkResult':
        soap, soap_url = get_soap_and_url(operation)  # Buscar Soap e Url
        transaction_data = {'RefNMVSTrxId': transaction_id}
        filled_header, filled_body = prepare_header_and_body(operation, transaction_data, basic_auth_format, software_supplier_and_transaction_format)
        payload = format_payload(soap, filled_header, filled_body)
        response = soap_request(payload, soap_url)

    else:
        print("Operação não suportada.")

    result_code = False
    output = False
    result_str = False
    if response:
        result_code, output, result_str = eval(operation['response_unpacker'] + '(response)')
    return result_code, output, result_str


def BulkPing_response_unpacker(response):
    obj = xmltodict.parse(response.text)
    new_obj = obj['soap:Envelope']['soap:Body']['ns2:BulkPingResponse']['ns1:Output']
    if new_obj == "Bulk Ping OK":
        return True, new_obj, True


def SinglePackPing_response_unpacker(response):
    obj = xmltodict.parse(response.text)
    new_obj = obj['soap:Envelope']['soap:Body']['ns2:SinglePackPingResponse']['ns1:Output']
    if new_obj == "SinglePack Ping OK":
        return True, new_obj, True


def G188_response_unpacker(response):
    obj = xmltodict.parse(response.text)
    new_obj = obj['soap:Envelope']['soap:Body']['ns2:G188Response']
    transaction_id = new_obj['ns1:Header']['ns1:Transaction']['ns1:NMVSTrxId']
    new_obj = new_obj['ns1:Body']
    return_code = new_obj['ns1:ReturnCode']['@ns1:code'],new_obj['ns1:ReturnCode']['@ns1:desc']
    if return_code == 'NMVS_FE_TX_02': #Result not ready
        return return_code,False,False
    if  'ns1:Packs' in new_obj.keys():
        packs_obj = new_obj['ns1:Packs']['ns1:Pack']
    else:
        packs_obj = []
    packs = []
    for pack in packs_obj:
        p = {}
        if '@ns1:sn' in pack.keys():
            p['pack'] = pack['@ns1:sn']
        if '@ns1:state' in pack.keys():
            p['state'] = pack['@ns1:state']
        if 'ns1:Reason' in pack.keys():
            p['reason'] = pack['ns1:Reason']
        p['return_code'] = pack['ns1:ReturnCode']['@ns1:code'],pack['ns1:ReturnCode']['@ns1:desc']
        packs.append(p)
    return return_code, transaction_id, packs

def G196_response_unpacker(response):

    obj = xmltodict.parse(response.text)
    new_obj = obj['soap:Envelope']['soap:Body']['ns2:G196Response']
    transaction_id = new_obj['ns1:Header']['ns1:Transaction']['ns1:NMVSTrxId']
    new_obj = new_obj['ns1:Body']
    return_code = new_obj['ns1:ReturnCode']['@ns1:code'],new_obj['ns1:ReturnCode']['@ns1:desc']
    if return_code == 'NMVS_FE_TX_02': #Result not ready
        return return_code,False,False

    if  'ns1:TrxList' in new_obj.keys():
        op_list = new_obj['ns1:TrxList']['ns1:TrxItem']
    else:
        op_list = []
    ops = []

    for op in op_list:
        p = {}
        if 'ns1:Transaction' in op.keys():
            if 'ns1:ClientTrxId' in op['ns1:Transaction'].keys():
                p['client_transaction_id'] = op['ns1:Transaction']['ns1:ClientTrxId']
                print(p)
                print('ppppppp')
        if '@ns1:state' in op['ns1:Pack'].keys():
            p['state'] = op['ns1:Pack']['@ns1:state']
        if 'ns1:Reason' in op['ns1:Pack'].keys():
            p['reason'] = op['ns1:Pack']['ns1:Reason']
        p['return_code'] = op['ns1:Pack']['ns1:ReturnCode']['@ns1:code'],op['ns1:Pack']['ns1:ReturnCode']['@ns1:desc']
        ops.append(p)
    return return_code, transaction_id, ops


def standard_mixed_bulk_response_unpacker(response):
    obj = xmltodict.parse(response.text)
    new_obj = obj['soap:Envelope']['soap:Body']
    key = ''
    for x in new_obj.keys():
        key += x
        break
    new_obj = new_obj[x]
    transaction_id = new_obj['ns1:Header']['ns1:Transaction']['ns1:NMVSTrxId']

    return_code = new_obj['ns1:Body']['ns1:ReturnCode']['@ns1:code'],new_obj['ns1:Body']['ns1:ReturnCode']['@ns1:desc']
    return return_code, transaction_id, []

def standard_bulk_response_unpacker(response):
    obj = xmltodict.parse(response.text)
    new_obj = obj['soap:Envelope']['soap:Body']
    key = ''
    for x in new_obj.keys():
        key += x
        break
    new_obj = new_obj[x]
    transaction_id = new_obj['ns1:Header']['ns1:Transaction']['ns1:NMVSTrxId']
    return_code = new_obj['ns1:Body']['ns1:ReturnCode']['@ns1:code'],new_obj['ns1:Body']['ns1:ReturnCode']['@ns1:desc']
    return return_code, transaction_id, []


def standard_single_pack_response_unpacker(response):
    obj = xmltodict.parse(response.text)
    new_obj = obj['soap:Envelope']['soap:Body']
    key = ''
    for x in new_obj.keys():
        key += x
        break
    new_obj = new_obj[x]
    transaction_id = new_obj['ns1:Header']['ns1:Transaction']['ns1:NMVSTrxId']
    return_code = new_obj['ns1:Body']['ns1:ReturnCode']['@ns1:code'],new_obj['ns1:Body']['ns1:ReturnCode']['@ns1:desc']
    pack = new_obj['ns1:Body']['ns1:Pack']
    pack_obj = [pack['@ns1:sn'],pack['@ns1:state']]

    if 'ns1:Reason' in pack.keys():
        pack_obj.append(pack['ns1:Reason'])
    if 'ns1:ReturnCode' in pack.keys():
        pack_obj.append(pack['ns1:ReturnCode']['@ns1:code'])
    return return_code, transaction_id, [pack_obj]
