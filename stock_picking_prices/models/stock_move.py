# Copyright 2025 Nitrokey GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    price_unit = fields.Float(
        string="Unit Price",
        digits="Product Price",
        compute="_compute_price_unit",
        store=True,
        help="Unit price from the sale order line",
    )
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute="_compute_price_subtotal",
        store=True,
        help="Subtotal amount for the move line",
    )
    currency_id = fields.Many2one(
        related="picking_id.currency_id",
        string="Currency",
        readonly=True,
    )

    @api.depends("sale_line_id.price_unit")
    def _compute_price_unit(self):
        """Copy the price from the sale order line"""
        for move in self:
            if move.sale_line_id:
                move.price_unit = move.sale_line_id.price_unit
            else:
                move.price_unit = move.product_id.lst_price

    @api.depends("price_unit", "product_uom_qty")
    def _compute_price_subtotal(self):
        """Compute the subtotal amount"""
        for move in self:
            move.price_subtotal = move.price_unit * move.product_uom_qty
