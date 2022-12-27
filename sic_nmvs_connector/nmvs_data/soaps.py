# -*- coding: utf-8 -*-
#SmartImproveConsulting

# Auth Data
ClientLoginId = 'SWS'
UserId = 'TEIX1006'
Password = 'by2-fnNUXaes!20SIC22'

#  User Software and Transaction Data
USName = 'BTeste-0'
USSupplier = 'SIC'
USVersion = '0.2'
TransactionId = 'Test-0001'
TransactionLanguage = 'eng'


standard_header = '''
<urn1:Header>
    <urn1:Auth>
       <urn1:ClientLoginId>{ClientLoginId}</urn1:ClientLoginId>
       <urn1:UserId>{UserId}</urn1:UserId>
       <urn1:Password>{Password}</urn1:Password>
        <!--Optional: <urn1:SubUserId>?</urn1:SubUserId>-->
    </urn1:Auth>
    <urn1:UserSoftware urn1:name="{USName}" urn1:supplier="{USSupplier}" urn1:version="{USVersion}"/>
    <urn1:Transaction>
       <urn1:ClientTrxId>{TransactionId}</urn1:ClientTrxId>
       <urn1:Language>{TransactionLanguage}</urn1:Language>
    </urn1:Transaction>
</urn1:Header>
'''

standard_single_pack_body = '''
 <urn1:Body>
    <urn1:Product>
       <urn1:ProductCode urn1:scheme="{ProductScheme}">{ProductCode}</urn1:ProductCode>
       <!--Optional <urn1:NHRN>?</urn1:NHRN>-->
       <urn1:Batch>
          <urn1:Id>{ProductBatchId}</urn1:Id>
          <urn1:ExpDate>{ProdutctExpDate}</urn1:ExpDate>
       </urn1:Batch>
    </urn1:Product>
    <urn1:Pack urn1:sn="{Pack}"/>
 </urn1:Body>
'''

standard_bulk_body = '''
     <urn1:Body>
        <urn1:Product>
           <urn1:ProductCode urn1:scheme="{ProductScheme}">{ProductCode}</urn1:ProductCode>
           <!--Optional:  <urn1:NHRN>?</urn1:NHRN>-->
           <urn1:Batch>
              <urn1:Id>{ProductBatchId}</urn1:Id>
              <urn1:ExpDate>{ProdutctExpDate}</urn1:ExpDate>
           </urn1:Batch>
        </urn1:Product>
        <urn1:Packs>
           <!--1 to 100000 repetitions:-->
           {Packs}
        </urn1:Packs>
     </urn1:Body>

'''

request_bulk_pack_result_body = '''
     <urn1:Body>
        <urn1:RefNMVSTrxId>{RefNMVSTrxId}</urn1:RefNMVSTrxId>
     </urn1:Body>
'''

#  Auth Dict
basic_auth_format = {
    "ClientLoginId": ClientLoginId,
    "UserId": UserId,
    "Password": Password,
}

#  User Software and Transaction Data Dict
software_supplier_and_transaction_format = {
    "USName": USName,
    "USSupplier": USSupplier,
    "USVersion": USVersion,
    "TransactionId": TransactionId,
    "TransactionLanguage": TransactionLanguage,
}


G445ChangePassword_format = {
    "NewPassword": '123'
}

single_pack_data = {
    "ProductScheme": '',
    "ProductCode": '',
    "ProductBatchId": '',
    "ProdutctExpDate": '',  # YYMMDD
    "Pack": ''
}

bulk_data = {
    "ProductScheme": '',
    "ProductCode": '',
    "ProductBatchId": '',
    "ProdutctExpDate": '',  # YYMMDD
    "Packs": ''  # <urn1:Pack urn1:sn=""/> <urn1:Pack urn1:sn=""/>
}

request_bulk_pack_result_data = {
    "RefNMVSTrxId": '',
}

#################################################################################################################
#################################################################################################################
#                                                SOAPs
#################################################################################################################
#################################################################################################################

#################################################################################################################
#                                             SUPPORT SOAPs
#################################################################################################################

support_soap_url = 'https://ws-support-int-bp.nmvs.eu:8448/WS_SUPPORT_V1/SupportServiceV50'

ping_support = '''
                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                   <soap:Header/>
                   <soap:Body>
                      <urn:SupportPingRequest>
                         <urn1:Input>{ping}</urn1:Input>
                      </urn:SupportPingRequest>
                   </soap:Body>
                </soap:Envelope>
            '''



G445ChangePassword = {"soap": '''
                        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                           <soap:Header/>
                           <soap:Body>
                              <urn:G445Request>
                                {header}
                                 <urn1:Body>
                                    <urn1:Password>{Password}</urn1:Password>
                                    <urn1:NewPassword>{NewPassword}</urn1:NewPassword>
                                 </urn1:Body>
                              </urn:G445Request>
                           </soap:Body>
                        </soap:Envelope>
                        ''',
                      "url": support_soap_url
                      }

#################################################################################################################
#                                           Single Serial Nº SOAPs
#################################################################################################################

single_pack_url = 'https://ws-single-transactions-int-bp.nmvs.eu:8443/WS_SINGLE_TRANSACTIONS_V1/SinglePackServiceV50'

PingSinglePack = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:SinglePackPingRequest>
                             <urn1:Input>SinglePack Ping OK</urn1:Input>
                          </urn:SinglePackPingRequest>
                       </soap:Body>
                    </soap:Envelope>
                    ''',
                  "url": single_pack_url
                  }

G110Verify = {"soap": '''
                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                   <soap:Header/>
                   <soap:Body>
                      <urn:G110Request>
                         {header}
                         {body}
                      </urn:G110Request>
                   </soap:Body>
                </soap:Envelope>
                ''',
              "url": single_pack_url
              }

G120Dispense = {"soap": '''
                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                   <soap:Header/>
                   <soap:Body>
                      <urn:G120Request>
                         {header}
                         {body}
                      </urn:G120Request>
                   </soap:Body>
                </soap:Envelope>
                ''',
                "url": single_pack_url
                }

G121UndoDispense = {"soap": '''
                       <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G121Request>
                            {header}
                            {body}
                          </urn:G121Request>
                       </soap:Body>
                    </soap:Envelope>
                    ''',
                    "url": single_pack_url
                    }


G130Destroy = {"soap": '''
                        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                           <soap:Header/>
                           <soap:Body>
                              <urn:G130Request>
                                {header}
                                {body}
                              </urn:G130Request>
                           </soap:Body>
                        </soap:Envelope>
                       ''',
               "url": single_pack_url
               }


G140Export = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G140Request>
                            {header}
                            {body}
                          </urn:G140Request>
                       </soap:Body>
                    </soap:Envelope>
                       ''',
              "url": single_pack_url
              }

G141UndoExport = {"soap": '''
                     <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G141Request>
                            {header}
                            {body}
                          </urn:G141Request>
                       </soap:Body>
                    </soap:Envelope>
                       ''',
                  "url": single_pack_url
                  }


G150Sample = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G150Request>
                            {header}
                            {body}
                          </urn:G150Request>
                       </soap:Body>
                    </soap:Envelope>
                       ''',
              "url": single_pack_url
              }


G151UndoSample = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G151Request>
                            {header}
                            {body}
                          </urn:G151Request>
                       </soap:Body>
                    </soap:Envelope>
                       ''',
                  "url": single_pack_url
                  }

G160FreeSample = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G160Request>
                            {header}
                            {body}
                          </urn:G160Request>
                       </soap:Body>
                    </soap:Envelope>
                       ''',
                  "url": single_pack_url
                  }


G161UndoFreeSample = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G161Request>
                            {header}
                            {body}
                          </urn:G161Request>
                       </soap:Body>
                    </soap:Envelope>
                       ''',
                      "url": single_pack_url
                      }


G170Lock = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G170Request>
                            {header}
                            {body}
                          </urn:G170Request>
                       </soap:Body>
                    </soap:Envelope>
                       ''',
            "url": single_pack_url
            }


G171UndoLock = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G171Request>
                            {header}
                            {body}
                          </urn:G171Request>
                       </soap:Body>
                    </soap:Envelope>
                       ''',
                "url": single_pack_url
                }


G180Stolen = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G180Request>
                            {header}
                            {body}
                          </urn:G180Request>
                       </soap:Body>
                    </soap:Envelope>
                       ''',
                      "url": single_pack_url
              }








#################################################################################################################
#                                          Bulk (Product and Batches) SOAPs
#################################################################################################################

bulk_url = 'https://ws-bulk-transactions-int-bp.nmvs.eu:8445/WS_BULK_TRANSACTIONS_V1/BulkServiceV50'

PingBulk = {"soap": '''
                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                   <soap:Header/>
                   <soap:Body>
                      <urn:BulkPingRequest>
                         <urn1:Input>Bulk Ping OK</urn1:Input>
                      </urn:BulkPingRequest>
                   </soap:Body>
                </soap:Envelope>
                ''',
             "url": bulk_url
             }

G115BulkVerify = {"soap": '''
                   <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G115Request>
                            {header}
                            {body}
                          </urn:G115Request>
                       </soap:Body>
                    </soap:Envelope>
                    ''',
                  "url": bulk_url
                  }


G125BulkDispense = {"soap": '''
                                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                                   <soap:Header/>
                                   <soap:Body>
                                      <urn:G125Request>
                                        {header}
                                        {body}
                                      </urn:G125Request>
                                   </soap:Body>
                                </soap:Envelope>
                                ''',
                    "url": bulk_url
                    }

G127BulkUndoDispense = {"soap": '''
                        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                           <soap:Header/>
                           <soap:Body>
                              <urn:G127Request>
                                {header}
                                {body}
                              </urn:G127Request>
                           </soap:Body>
                        </soap:Envelope>
                                ''',
                        "url": bulk_url
                        }

G135BulkDestroy = {"soap": '''
                            <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                               <soap:Header/>
                               <soap:Body>
                                  <urn:G135Request>
                                    {header}
                            {body}
                                  </urn:G135Request>
                               </soap:Body>
                            </soap:Envelope>
                                ''',
                   "url": bulk_url
                   }


G145BulkExport = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G145Request>
                            {header}
                            {body}
                          </urn:G145Request>
                       </soap:Body>
                    </soap:Envelope>
                        ''',
                  "url": bulk_url
                  }

G147BulkUndoExport = {"soap": '''
                        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                           <soap:Header/>
                           <soap:Body>
                              <urn:G147Request>
                                {header}
                                {body}
                              </urn:G147Request>
                           </soap:Body>
                        </soap:Envelope>
                        ''',
                      "url": bulk_url
                      }


G155BulkSample = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G155Request>
                            {header}
                            {body}
                          </urn:G155Request>
                       </soap:Body>
                    </soap:Envelope>
                        ''',
                  "url": bulk_url
                  }

G157BulkUndoSample = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G157Request>
                            {header}
                            {body}
                          </urn:G157Request>
                       </soap:Body>
                    </soap:Envelope>
                        ''',
                      "url": bulk_url
                      }


G165BulkFreeSample = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G165Request>
                            {header}
                            {body}
                          </urn:G165Request>
                       </soap:Body>
                    </soap:Envelope>
                        ''',
                      "url": bulk_url
                      }


G167BulkUndoFreeSample = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G167Request>
                            {header}
                            {body}
                          </urn:G167Request>
                       </soap:Body>
                    </soap:Envelope>
                        ''',
                          "url": bulk_url
                          }

G175BulkLocks = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G175Request>
                            {header}
                            {body}
                          </urn:G175Request>
                       </soap:Body>
                    </soap:Envelope>
                        ''',
                 "url": bulk_url
                 }


G177BulkUndoLock = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G177Request>
                            {header}
                            {body}
                          </urn:G177Request>
                       </soap:Body>
                    </soap:Envelope>
                        ''',
                    "url": bulk_url
                    }


G185BulkStolen = {"soap": '''
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                       <soap:Header/>
                       <soap:Body>
                          <urn:G185Request>
                            {header}
                            {body}
                          </urn:G185Request>
                       </soap:Body>
                    </soap:Envelope>
                        ''',
                  "url": bulk_url
                  }

G188RequestBulkPackResult = {"soap": '''
                                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                                   <soap:Header/>
                                   <soap:Body>
                                      <urn:G188Request>
                                        {header}
                                        {body}
                                      </urn:G188Request>
                                   </soap:Body>
                                </soap:Envelope>
                                ''',
                             "url": bulk_url
                             }

#################################################################################################################
#                                      Mixed Bulk SOAPs
#################################################################################################################
mixed_bulk_url = 'https://ws-mixed-bulk-transactions-int-bp.nmvs.eu:8446/WS_MIXED_BULK_TRANSACTIONS_V1/MixedBulkServiceV50'


mixed_bulk_data = {
    "reqType": '',
    "TransactionId": '',
    "TransactionLanguage": '',
    "ProductScheme": '',
    "ProductCode": '',
    "ProductBatchId": '',
    "ProdutctExpDate": '',  # YYMMDD
    "Packs": ''  # <urn1:Pack urn1:sn=""/> <urn1:Pack urn1:sn=""/>
}

request_mixed_bulk_result_body = '''
     <urn1:Body>
        <urn1:RefNMVSTrxId>{RefNMVSTrxId}</urn1:RefNMVSTrxId>
     </urn1:Body>
'''

request_mixed_bulk_result_data = {
    "RefNMVSTrxId": '',
}

standard_mixed_bulk_body = '''
         <urn1:Body>
            <urn1:TrxList>
               <!--1 to 100000 repetitions:-->
              {Items}
            </urn1:TrxList>
         </urn1:Body>
'''

G195_item = '''
                <urn1:TrxItem>
                  <urn1:Item urn1:reqType="{reqType}">
                     <urn1:Product>
                         <urn1:ProductCode urn1:scheme="{ProductScheme}">{ProductCode}</urn1:ProductCode>
                         <urn1:Batch>
                              <urn1:Id>{ProductBatchId}</urn1:Id>
                              <urn1:ExpDate>{ProdutctExpDate}</urn1:ExpDate>
                         </urn1:Batch>
                     </urn1:Product>

                     {Packs} <!--  <urn1:Pack urn1:sn="?"/> -->

                     <urn1:Transaction>
                       <urn1:ClientTrxId>{TransactionId}</urn1:ClientTrxId>
                       <urn1:Language>{TransactionLanguage}</urn1:Language>
                     </urn1:Transaction>
                  </urn1:Item>
                </urn1:TrxItem>
            '''

G195_item_undo = '''
                <urn1:TrxItem>
                  <urn1:ItemUndo urn1:reqType="{reqType}">
                     <urn1:Product>
                         <urn1:ProductCode urn1:scheme="{ProductScheme}">{ProductCode}</urn1:ProductCode>
                         <urn1:Batch>
                              <urn1:Id>{ProductBatchId}</urn1:Id>
                              <urn1:ExpDate>{ProdutctExpDate}</urn1:ExpDate>
                         </urn1:Batch>
                     </urn1:Product>
                     {Packs} <!--  <urn1:Pack urn1:sn="?"/> -->
                     <urn1:Transaction>
                       <urn1:ClientTrxId>{TransactionId}</urn1:ClientTrxId>
                       <urn1:Language>{TransactionLanguage}</urn1:Language>
                     </urn1:Transaction>
                  </urn1:ItemUndo>
                </urn1:TrxItem>
                '''


G195SubmitBulkTransaction = {"soap": '''
                                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                                   <soap:Header/>
                                   <soap:Body>
                                      <urn:G195Request>
                                            {header}
                                            {body}

                                      </urn:G195Request>
                                   </soap:Body>
                                </soap:Envelope>
                                ''',
                                "url": mixed_bulk_url
                                }
G196RequestBulkTransactionResult = {"soap": '''
                                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:wsdltypes.nmvs.eu:v5.0" xmlns:urn1="urn:types.nmvs.eu:v5.0">
                                   <soap:Header/>
                                   <soap:Body>
                                      <urn:G196Request>
                                        {header}
                                        {body}
                                      </urn:G196Request>
                                   </soap:Body>
                                </soap:Envelope>
                                ''',
                                "url": mixed_bulk_url
                                }
