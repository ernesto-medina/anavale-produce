# -*- coding: utf-8 -*-
from odoo import api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    sale_order_quantity = fields.Float(
        'Quantity in Sale Order', compute='_compute_sale_order_qty',
        help='Quantity of products in this quant in Sale Orders but not yet Reserved in a Stock Picking , in the default unit of measure of the product',
        store=True, readonly=True)
        
    available_quantity = fields.Float(
        'Quantity available for Sell', compute='_compute_sale_order_qty',
        help='Quantity of products in this quant avaiable for Sell including in-transit stock, in the default unit of measure of the product',
        store=True, readonly=True)
        
    def _compute_sale_order_qty(self):
        for quant in self.sudo():        
            domain = [('product_id', '=', quant.product_id.id),
                # ('qty_to_deliver', '>', 0),
                ('order_id.state', '=', 'sale'),
                ('lot_id', '=', quant.lot_id.id)]
                
            sale_order_quantity = 0    
            for sol in self.env['sale.order.line'].search(domain):
                # sale_order_quantity += sol._compute_real_qty_to_deliver() 
                # sol._compute_qty_delivered()
                sale_order_quantity += sol.product_uom_qty - sol.qty_delivered
            available_quantity = quant.quantity - sale_order_quantity
            quant.write({'sale_order_quantity': sale_order_quantity, 'available_quantity': available_quantity})

    @api.model
    def _quant_tasks(self):
        res = super(StockQuant, self)._quant_tasks()
        self.sudo().search([])._compute_sale_order_qty()
        return res
