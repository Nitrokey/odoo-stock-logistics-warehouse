# Copyright 2025 Nitrokey GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # Add a computed field to show the total amount of the picking
    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_amount_total",
        store=True,
        help="Total amount of the picking based on the prices of the products",
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        related="sale_id.currency_id",
        readonly=True,
    )
    sale_id = fields.Many2one(
        "sale.order",
        string="Sales Order",
        compute="_compute_sale_id",
        store=True,
    )

    @api.depends("move_ids_without_package.sale_line_id")
    def _compute_sale_id(self):
        """Compute the sale order from the move lines"""
        for picking in self:
            sale_lines = picking.move_ids_without_package.mapped("sale_line_id")
            if sale_lines:
                picking.sale_id = sale_lines[0].order_id
            else:
                picking.sale_id = False

    @api.depends("move_ids_without_package.price_subtotal")
    def _compute_amount_total(self):
        """Compute the total amount of the picking"""
        for picking in self:
            picking.amount_total = sum(
                picking.move_ids_without_package.mapped("price_subtotal")
            )
