/** @odoo-module **/

import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { patch } from 'web.utils';
import { _t } from 'web.core';


patch(BarcodePickingModel.prototype, 'barcode_picking_model_sic_medicine', {

    _createCommandVals(line) {
        const values = {
            dummy_id: line.virtual_id,
            location_id: line.location_id,
            location_dest_id: line.location_dest_id,
            lot_name: line.lot_name,
            lot_id: line.lot_id,
            package_id: line.package_id,
            picking_id: line.picking_id,
            product_id: line.product_id,
            product_uom_id: line.product_uom_id,
            owner_id: line.owner_id,
            qty_done: line.qty_done,
            result_package_id: line.result_package_id,
            state: 'assigned',
            batch_code: line.batch_code, // miguel IMPORTANTE 
            exp_date: line.exp_date, // miguel IMPORTANTE 
        };

        for (const [key, value] of Object.entries(values)) {
            values[key] = this._fieldToValue(value);
        }
        return values;
    }

});
