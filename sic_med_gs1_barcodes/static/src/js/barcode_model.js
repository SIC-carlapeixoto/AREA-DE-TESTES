/** @odoo-module **/

import BarcodeModel from '@stock_barcode/models/barcode_model';
import { patch } from 'web.utils';
import { _t } from 'web.core';


patch(BarcodeModel.prototype, 'barcode_model_sic_medicine', {

  async _parseBarcode(barcode, filters) {
      const result = {
          barcode,
          match: false,
      };
      // First, simply checks if the barcode is an action.
      if (this.commands[barcode]) {
          result.action = this.commands[barcode];
          result.match = true;
          return result; // Simple barcode, no more information to retrieve.
      }
      // Then, parses the barcode through the nomenclature.
      await this.parser.is_loaded();
      try {
          const parsedBarcode = this.parser.parse_barcode(barcode);
          if (parsedBarcode.length) { // With the GS1 nomenclature, the parsed result is a list.
              for (const data of parsedBarcode) {
                  const { rule, value } = data;
                  if (['location', 'location_dest'].includes(rule.type)) {
                      const location = await this.cache.getRecordByBarcode(value, 'stock.location');
                      if (!location) {
                          continue;
                      }
                      // TODO: should be overrided, as location dest make sense only for pickings.
                      if (rule.type === 'location_dest' || this.messageType === 'scan_product_or_dest') {
                          result.destLocation = location;
                      } else {
                          result.location = location;
                      }
                      result.match = true;
                  } else if (rule.type === 'lot') {
                      if (this.useExistingLots) {
                          result.lot = await this.cache.getRecordByBarcode(value, 'stock.production.lot');
                      }
                      if (!result.lot) { // No existing lot found, set a lot name.
                          result.lotName = value;
                      }
                      if (result.lot || result.lotName) {
                          result.match = true;
                      }



                  } else if (rule.type === 'batch_code') { /// Miguel
                      result.batch_code = value;

                  } else if (rule.type === 'exp_date') { /// Miguel
                      result.exp_date = value;

                  }  

                  
                  
                  else if (rule.type === 'package') {
                      const stockPackage = await this.cache.getRecordByBarcode(value, 'stock.quant.package');
                      if (stockPackage) {
                          result.package = stockPackage;
                      } else {
                          // Will be used to force package's name when put in pack.
                          result.packageName = value;
                      }
                      result.match = true;
                  } else if (rule.type === 'package_type') {
                      const packageType = await this.cache.getRecordByBarcode(value, 'stock.package.type');
                      if (packageType) {
                          result.packageType = packageType;
                          result.match = true;
                      } else {
                          const message = _t("An unexisting package type was scanned. This part of the barcode can't be processed.");
                          this.notification.add(message, { type: 'warning' });
                      }
                  } else if (rule.type === 'product') {
                      const product = await this.cache.getRecordByBarcode(value, 'product.product');
                      if (product) {
                          result.product = product;
                          result.match = true;
                      }
                  } else if (rule.type === 'quantity') {
                      result.quantity = value;
                      // The quantity is usually associated to an UoM, but we
                      // ignore this info if the UoM setting is disabled.
                      if (this.groups.group_uom) {
                          result.uom = await this.cache.getRecord('uom.uom', rule.associated_uom_id);
                      }
                      result.match = result.quantity ? true : false;
                  }
              }
              if(result.match) {
                  return result;
              }
          } else if (parsedBarcode.type === 'weight') {
              result.weight = parsedBarcode;
              result.match = true;
              barcode = parsedBarcode.base_code;
          }
      } catch (err) {
          // The barcode can't be parsed but the error is caught to fallback
          // on the classic way to handle barcodes.
          console.log(`%cWarning: error about ${barcode}`, 'text-weight: bold;');
          console.log(err.message);
      }
      const recordByData = await this.cache.getRecordByBarcode(barcode, false, false, filters);
      if (recordByData.size > 1) {
          const message = sprintf(
              _t("Barcode scan is ambiguous with several model: %s. Use the most likely."),
              Array.from(recordByData.keys()));
          this.notification.add(message, { type: 'warning' });
      }

      if (this.groups.group_stock_multi_locations) {
          const location = recordByData.get('stock.location');
          if (location) {
              this._setLocationFromBarcode(result, location);
              result.match = true;
          }
      }

      if (this.groups.group_tracking_lot) {
          const packageType = recordByData.get('stock.package.type');
          const stockPackage = recordByData.get('stock.quant.package');
          if (stockPackage) {
              // TODO: should take packages only in current (sub)location.
              result.package = stockPackage;
              result.match = true;
          }
          if (packageType) {
              result.packageType = packageType;
              result.match = true;
          }
      }

      const product = recordByData.get('product.product');
      if (product) {
          result.product = product;
          result.match = true;
      }
      const packaging = recordByData.get('product.packaging');
      if (packaging) {
          result.match = true;
          result.packaging = packaging;
      }
      if (this.useExistingLots) {
          const lot = recordByData.get('stock.production.lot');
          if (lot) {
              result.lot = lot;
              result.match = true;
          }
      }
      const quantPackage = recordByData.get('stock.quant.package');
      if (this.groups.group_tracking_lot && quantPackage) {
          result.package = quantPackage;
          result.match = true;
      }

      if (!result.match && this.packageTypes.length) {
          // If no match, check if the barcode begins with a package type's barcode.
          for (const [packageTypeBarcode, packageTypeId] of this.packageTypes) {
              if (barcode.indexOf(packageTypeBarcode) === 0) {
                  result.packageType = await this.cache.getRecord('stock.package.type', packageTypeId);
                  result.packageName = barcode;
                  result.match = true;
                  break;
              }
          }
      }
      return result;
  },


  async _processBarcode(barcode) {
      let barcodeData = {};
      let currentLine = false;
      // Creates a filter if needed, which can help to get the right record
      // when multiple records have the same model and barcode.

      const filters = {};
      if (this.selectedLine && this.selectedLine.product_id.tracking !== 'none') {
          filters['stock.production.lot'] = {
              product_id: this.selectedLine.product_id.id,
          };
      }
      try {
          barcodeData = await this._parseBarcode(barcode, filters);
          if (!barcodeData.match && filters['stock.production.lot'] && !this.canCreateNewLot && this.useExistingLots) {
              // Retry to parse the barcode without filters in case it matches an existing
              // record that can't be found because of the filters
              const lot = await this.cache.getRecordByBarcode(barcode, 'stock.production.lot');
              if (lot) {
                  Object.assign(barcodeData, { lot, match: true });
              }
          }
      } catch (parseErrorMessage) {
          barcodeData.error = parseErrorMessage;
      }

      // Process each data in order, starting with non-ambiguous data type.
      if (barcodeData.action) { // As action is always a single data, call it and do nothing else.
          return await barcodeData.action();
      }

      if (barcodeData.packaging) {
          barcodeData.product = this.cache.getRecord('product.product', barcodeData.packaging.product_id);
          barcodeData.quantity = barcodeData.packaging.qty;
          barcodeData.uom = this.cache.getRecord('uom.uom', barcodeData.product.uom_id);
      }

      if (barcodeData.lot && !barcodeData.product) {
          barcodeData.product = this.cache.getRecord('product.product', barcodeData.lot.product_id);
      }

      await this._processLocation(barcodeData);
      await this._processPackage(barcodeData);
      if (barcodeData.stopped) {
          // TODO: Sometime we want to stop here instead of keeping doing thing,
          // but it's a little hacky, it could be better to don't have to do that.
          return;
      }

      if (barcodeData.weight) { // Convert the weight into quantity.
          barcodeData.quantity = barcodeData.weight.value;
      }

      // If no product found, take the one from last scanned line if possible.
      if (!barcodeData.product) {
          if (barcodeData.quantity) {
              currentLine = this.selectedLine || this.lastScannedLine;
          } else if (this.selectedLine && this.selectedLine.product_id.tracking !== 'none') {
              currentLine = this.selectedLine;
          } else if (this.lastScannedLine && this.lastScannedLine.product_id.tracking !== 'none') {
              currentLine = this.lastScannedLine;
          }
          if (currentLine) { // If we can, get the product from the previous line.
              const previousProduct = currentLine.product_id;
              // If the current product is tracked and the barcode doesn't fit
              // anything else, we assume it's a new lot/serial number.
              if (previousProduct.tracking !== 'none' &&
                  !barcodeData.match && this.canCreateNewLot) {
                  barcodeData.lotName = barcode;
                  barcodeData.product = previousProduct;
              }
              if (barcodeData.lot || barcodeData.lotName ||
                  barcodeData.quantity) {
                  barcodeData.product = previousProduct;
              }
          }
      }
      const {product} = barcodeData;
      if (!product) { // Product is mandatory, if no product, raises a warning.
          if (!barcodeData.error) {
              if (this.groups.group_tracking_lot) {
                  barcodeData.error = _t("You are expected to scan one or more products or a package available at the picking location");
              } else {
                  barcodeData.error = _t("You are expected to scan one or more products.");
              }
          }
          return this.notification.add(barcodeData.error, { type: 'danger' });
      }
      if (barcodeData.weight) { // the encoded weight is based on the product's UoM
          barcodeData.uom = this.cache.getRecord('uom.uom', product.uom_id);
      }

      // Default quantity set to 1 by default if the product is untracked or
      // if there is a scanned tracking number.
      if (product.tracking === 'none' || barcodeData.lot || barcodeData.lotName || this._incrementTrackedLine()) {
          barcodeData.quantity = barcodeData.quantity || 1;
          if (product.tracking === 'serial' && barcodeData.quantity > 1 && (barcodeData.lot || barcodeData.lotName)) {
              barcodeData.quantity = 1;
              this.notification.add(
                  _t(`A product tracked by serial numbers can't have multiple quantities for the same serial number.`),
                  { type: 'danger' }
              );
          }
      }

      // Searches and selects a line if needed.
      if (!currentLine || this._shouldSearchForAnotherLine(currentLine, barcodeData)) {
          currentLine = this._findLine(barcodeData);
      }

      if ((barcodeData.lotName || barcodeData.lot) && product) {
          const lotName = barcodeData.lotName || barcodeData.lot.name;
          for (const line of this.currentState.lines) {
              if (line.product_id.tracking === 'serial' && this.getQtyDone(line) !== 0 &&
                  ((line.lot_id && line.lot_id.name) || line.lot_name) === lotName) {
                  return this.notification.add(
                      _t("The scanned serial number is already used."),
                      { type: 'danger' }
                  );
              }
          }
          // Prefills `owner_id` and `package_id` if possible.
          const prefilledOwner = (!currentLine || (currentLine && !currentLine.owner_id)) && this.groups.group_tracking_owner && !barcodeData.owner;
          const prefilledPackage = (!currentLine || (currentLine && !currentLine.package_id)) && this.groups.group_tracking_lot && !barcodeData.package;
          if (this.useExistingLots && (prefilledOwner || prefilledPackage)) {
              const lotId = (barcodeData.lot && barcodeData.lot.id) || (currentLine && currentLine.lot_id && currentLine.lot_id.id) || false;
              const res = await this.orm.call(
                  'product.product',
                  'prefilled_owner_package_stock_barcode',
                  [product.id],
                  {
                      lot_id: lotId,
                      lot_name: (!lotId && barcodeData.lotName) || false,
                  }
              );
              this.cache.setCache(res.records);
              if (prefilledPackage && res.quant && res.quant.package_id) {
                  barcodeData.package = this.cache.getRecord('stock.quant.package', res.quant.package_id);
              }
              if (prefilledOwner && res.quant && res.quant.owner_id) {
                  barcodeData.owner = this.cache.getRecord('res.partner', res.quant.owner_id);
              }
          }
      }

      // Updates or creates a line based on barcode data.
      if (currentLine) { // If line found, can it be incremented ?
          let exceedingQuantity = 0;
          if (product.tracking !== 'serial' && barcodeData.uom && barcodeData.uom.category_id == currentLine.product_uom_id.category_id) {
              // convert to current line's uom
              barcodeData.quantity = (barcodeData.quantity / barcodeData.uom.factor) * currentLine.product_uom_id.factor;
              barcodeData.uom = currentLine.product_uom_id;
          }
          if (this.canCreateNewLine) {
              // Checks the quantity doesn't exceed the line's remaining quantity.
              if (currentLine.product_uom_qty && product.tracking === 'none') {
                  const remainingQty = currentLine.product_uom_qty - currentLine.qty_done;
                  if (barcodeData.quantity > remainingQty) {
                      // In this case, lowers the increment quantity and keeps
                      // the excess quantity to create a new line.
                      exceedingQuantity = barcodeData.quantity - remainingQty;
                      barcodeData.quantity = remainingQty;
                  }
              }
          }
          if (barcodeData.quantity > 0) {
              const fieldsParams = this._convertDataToFieldsParams({
                  qty: barcodeData.quantity,
                  lotName: barcodeData.lotName,
                  lot: barcodeData.lot,
                  package: barcodeData.package,
                  owner: barcodeData.owner,
              });
              if (barcodeData.uom) {
                  fieldsParams.uom = barcodeData.uom;
              }
              await this.updateLine(currentLine, fieldsParams);
          }
          if (exceedingQuantity) { // Creates a new line for the excess quantity.
              const fieldsParams = this._convertDataToFieldsParams({
                  product,
                  qty: exceedingQuantity,
                  lotName: barcodeData.lotName,
                  lot: barcodeData.lot,
                  package: barcodeData.package,
                  owner: barcodeData.owner,
              });
              if (barcodeData.uom) {
                  fieldsParams.uom = barcodeData.uom;
              }
              currentLine = await this._createNewLine({
                  copyOf: currentLine,
                  fieldsParams,
              });
          }
      } else if (this.canCreateNewLine) { // No line found. If it's possible, creates a new line.
          var fieldsParams = this._convertDataToFieldsParams({
              product,
              qty: barcodeData.quantity,
              lotName: barcodeData.lotName,
              lot: barcodeData.lot,
              package: barcodeData.package,
              owner: barcodeData.owner,
          });

          if (barcodeData.batch_code) {/// Miguel
            fieldsParams.batch_code = barcodeData.batch_code;
            }

          if (barcodeData.exp_date) {
                fieldsParams.exp_date = barcodeData.exp_date; /// Miguel
            }

          if (barcodeData.uom) {
              fieldsParams.uom = barcodeData.uom;
          }

          currentLine = await this._createNewLine({fieldsParams});
      }

      // And finally, if the scanned barcode modified a line, selects this line.
      if (currentLine) {
          this.selectLine(currentLine);
      }
      this.trigger('update');
  },


  async _createNewLine(params) {
    if (params.fieldsParams && params.fieldsParams.uom && params.fieldsParams.product_id) {
        let productUOM = this.cache.getRecord('uom.uom', params.fieldsParams.product_id.uom_id);
        let paramsUOM = params.fieldsParams.uom;
        if (paramsUOM.category_id !== productUOM.category_id) {
            // Not the same UoM's category -> Can't be converted.
            const message = sprintf(
                _t("Scanned quantity uses %s as Unit of Measure, but this UoM is not compatible with the product's one (%s)."),
                paramsUOM.name, productUOM.name
            );
            this.notification.add(message, { title: _t("Wrong Unit of Measure"), type: 'danger'});
            return false;
        }
    }
    const newLine = Object.assign(
        {},
        params.copyOf,
        this._getNewLineDefaultValues(params.fieldsParams)
    );
    console.log('inside params create')
    console.log(params.fieldsParams)
    console.log(params)
    console.log(newLine)
    await this.updateLine(newLine, params.fieldsParams);
    this.currentState.lines.push(newLine);
    this.page.lines.push(newLine);
    return newLine;
},


  async updateLine(line, args) {

      let {lot_id, owner_id, package_id} = args;
      if (!line) {
          throw new Error('No line found');
      }
      if (!line.product_id && args.product_id) {
          line.product_id = args.product_id;
          line.product_uom_id = this.cache.getRecord('uom.uom', args.product_id.uom_id);
      }
      if (lot_id) {
          if (typeof lot_id === 'number') {
              lot_id = this.cache.getRecord('stock.production.lot', args.lot_id);
          }
          line.lot_id = lot_id;
      }
      if (owner_id) {
          if (typeof owner_id === 'number') {
              owner_id = this.cache.getRecord('res.partner', args.owner_id);
          }
          line.owner_id = owner_id;
      }
      if (package_id) {
          if (typeof package_id === 'number') {
              package_id = this.cache.getRecord('stock.quant.package', args.package_id);
          }
          line.package_id = package_id;
      }
      if (args.lot_name) {
          await this.updateLotName(line, args.lot_name);
      }
      if (args.batch_code) {
        line.batch_code = args.batch_code;
      }
      if (args.exp_date) {
        line.exp_date = args.exp_date;
      }

      this._updateLineQty(line, args);
      this._markLineAsDirty(line);
  },


  _getSaveLineCommand() {
    const commands = [];
    const fields = this._getFieldToWrite();
    for (const virtualId of this.linesToSave) {
        const line = this.currentState.lines.find(l => l.virtual_id === virtualId);
        if (line.id) { // Update an existing line.
            const initialLine = this.initialState.lines.find(l => l.virtual_id === line.virtual_id);
            const changedValues = {};
            let somethingToSave = false;
            for (const field of fields) {
                const fieldValue = line[field];
                const initialValue = initialLine[field];
                if (fieldValue !== undefined && (
                    (['boolean', 'number', 'string'].includes(typeof fieldValue) && fieldValue !== initialValue) ||
                    (typeof fieldValue === 'object' && fieldValue.id !== initialValue.id)
                )) {
                    changedValues[field] = this._fieldToValue(fieldValue);
                    somethingToSave = true;
                }
            }
            if (somethingToSave) {
                commands.push([1, line.id, changedValues]);
            }
        } else { // Create a new line.
            commands.push([0, 0, this._createCommandVals(line)]);
            console.log('linha create')
            console.log(line)
        }
    }
    return commands;
  },


  async validate() {
    console.log('validate')///  Miguel
    console.log(this.validateMethod)
    await this.save();
    const action = await this.orm.call(
        this.params.model,
        this.validateMethod,
        [this.recordIds]
    );
    
    const options = {
        on_close: ev => this._closeValidate(ev)
    };
    console.log('action')/// 
    console.log(action)
    console.log(options)
    if (action && action.res_model) {
        console.log('action')/// 
        console.log(action)
        console.log(options)
        return this.trigger('do-action', { action, options });
    }
    return options.on_close();
}

});
