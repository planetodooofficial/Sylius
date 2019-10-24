from odoo import api,fields,models
from odoo import http, tools, _
from odoo.http import request
from odoo.http import controllers_per_module
import requests
import json
import datetime
import time

class StockPickingShippingInherit(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def send_to_shipper(self):
        res = super(StockPickingShippingInherit, self).send_to_shipper()
        sale_order_id = self.env['sale.order'].search([('name','=',self.origin)])
        if sale_order_id.sylius_shipment_id != 0 and sale_order_id.sylius_order_id !=0:
            sylius_shipment_id = sale_order_id.sylius_shipment_id
            sylius_order_id = sale_order_id.sylius_order_id
            controller_instance = None
            for name, instance in controllers_per_module.get('odoo_sylius_connector'):
                if name.endswith('odoo_sylius_connector.controller.main'):
                    controller_instance = instance
                    break
            if controller_instance != None:
                print('No controller found')

            url = 'https://staging.brandsofpuertorico.com/api/v1/orders/'+str(sylius_order_id)+'/shipments/'+str(sylius_shipment_id)+'/ship'
            headers = {
                'authorization': instance.get_auth_token_header(instance),
                'content-type': "application/json",

            }
            type_dict = dict(self.env['delivery.carrier'].fields_get(allfields=['delivery_type'])['delivery_type']['selection'])
            data_body = {'carrierCode':(type_dict[sale_order_id.carrier_id.delivery_type]).lower().replace(" ", ""),
                         'tracking':self.carrier_tracking_ref}

            response = requests.put(url, data=json.dumps(data_body), headers=headers)

        return res

