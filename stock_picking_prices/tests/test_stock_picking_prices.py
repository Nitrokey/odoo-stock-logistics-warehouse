# Copyright 2025 Nitrokey GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestStockPickingPrices(TransactionCase):
    def setUp(self):
        super().setUp()
        # Create a product
        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
                "list_price": 100.0,
            }
        )
        # Create a customer
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Customer",
                "customer_rank": 1,
            }
        )
        # Create a sales order
        self.sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
            }
        )
        # Create a sales order line
        self.sale_order_line = self.env["sale.order.line"].create(
            {
                "order_id": self.sale_order.id,
                "product_id": self.product.id,
                "product_uom_qty": 5.0,
                "price_unit": 100.0,
            }
        )

    def test_price_copied_to_picking(self):
        """Test that prices are copied from sale order to picking."""
        # Confirm the sales order
        self.sale_order.action_confirm()
        # Get the picking created from the sales order
        picking = self.sale_order.picking_ids[0]
        # Check that the picking has the sale_id field set
        self.assertEqual(picking.sale_id, self.sale_order)
        # Check that the move has the price_unit field set
        move = picking.move_ids_without_package[0]
        self.assertEqual(move.price_unit, 100.0)
        # Check that the move has the price_subtotal field set
        self.assertEqual(move.price_subtotal, 500.0)
        # Check that the picking has the amount_total field set
        self.assertEqual(picking.amount_total, 500.0)
