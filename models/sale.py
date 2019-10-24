from odoo import models,fields,api

class SaleSyliusInherit(models.Model):

    _inherit = 'sale.order'
    sale_adjustment_lines_ids = fields.One2many('sale.adjustment.lines','sale_adjustment_order_id', string="Adjustment Lines")
    sylius_order_id = fields.Integer('Sylius Order Id')
    sylius_shipment_id = fields.Integer('Sylius Shipment Id')

    @api.depends('sale_adjustment_lines_ids.adjustment_amount')
    def _amount_adjustment(self):
        for order in self:
            adjustment_amount_total = 0.0
            for line in order.sale_adjustment_lines_ids:
                adjustment_amount_total += line.adjustment_amount

            order.update({'adjustment_amount_total':adjustment_amount_total})
    adjustment_amount_total = fields.Monetary('Total Adjustment Cost',store=True,compute=_amount_adjustment)

    @api.one
    @api.depends('order_line.price_total','adjustment_amount_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = amount_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_discount += (line.product_uom_qty * line.price_unit * line.discount) / 100
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax + self.adjustment_amount_total
            })







class SaleAdjustmentLines(models.Model):
    _name = 'sale.adjustment.lines'

    sale_adjustment_order_id = fields.Many2one('sale.order',)
    sylius_adjustment_id = fields.Integer('Sylius Adjustment Id')
    adjustment_type = fields.Char('Type')
    adjustment_label = fields.Char('Label')
    adjustment_amount = fields.Float('Amount')

