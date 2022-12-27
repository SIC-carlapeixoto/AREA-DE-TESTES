#-*- coding: utf-8 -*-

from odoo import _, models, fields, api


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'


    batch_code = fields.Char(string='Lote')
    pack_serial = fields.Char(string='Nº de Série')
    pack_state = fields.Selection(string="Estado", selection=[('ACTIVE','Ativo'),('INACTIVE','Inativo'),('UNKNOWN','Desconhecido')])
    pack_state_reason = fields.Char(string="Motivo")

    @api.model
    def create(self, vals):
        """Force the locking/unlocking, ignoring the value of 'locked'."""
        product = self.env["product.product"].browse(
            vals.get(
                "product_id",
                # Web quick-create provide in context
                self.env.context.get(
                    "product_id", self.env.context.get("default_product_id", False)
                ),
            )
        )

        locked = vals["locked"]
        vals["locked"] = self._get_product_locked(product)

        lot = super(StockProductionLot, self.with_context(bypass_lock_permission_check=True) ).create(vals)

        #override por causa da call NMVS
        if lot.pack_state:
            lot.locked = locked

        return self.browse(lot.id)  # for cleaning context
