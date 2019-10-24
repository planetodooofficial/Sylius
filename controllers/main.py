##############################################################################
#
#    TeckZilla Software Solutions and Services
#    Copyright (C) 2012-2013 TeckZilla-OpenERP Experts(<http://www.teckzilla.net>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import http, tools, _
from odoo.http import request
from odoo.http import controllers_per_module
import requests
import json
import datetime
import time
import base64
from xml.dom.minidom import parse, parseString
import pytz
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.parser import parse
class customer_sign_up(http.Controller):

    def get_auth_token_header(self):
        client_key = '5qdr7kpiuwgs4wg8w08ckkwckssskk8cogkoc840488okss8ss'
        client_secret = '1ol2reik0c68os00wcgw8cc80gog0k808wwc88csw0s48gsgos'
        url = "https://staging.brandsofpuertorico.com/api/oauth/v2/token"
        options_list = []
        data = {
            'client_id': client_key,
            'client_secret': client_secret,
            'grant_type': 'password',
            'username': 'wms',
            'password': '12345678'
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, data=data, headers=headers)

        print("response================>", response.content)
        content = json.loads(response.content.decode('utf-8'))
        auth_header = "Bearer {0}".format(content['access_token'])
        return auth_header

    @http.route('/page/import_country_codes', auth='public', type='http', website=True)
    def import_country_codes(self, **post):
        auth_header = self.get_auth_token_header()
        headers_country = {
            'Authorization': auth_header,
            'Accept': 'application/json',

        }
        print("header===========>", headers_country)
        country_url = 'https://staging.brandsofpuertorico.com/api/v1/countries/'
        country_response = requests.get(country_url, headers=headers_country)
        print("customer_response================>", json.loads((country_response.content).decode("utf-8")))
        res = json.loads((country_response.content).decode("utf-8"))
        pages = res['pages']
        print('pages=====>', pages)
        # items = json.loads(product_response(['_embedded']['items']))
        i = 1
        countries = []
        while i <= 5:
            page_vise_url = 'https://staging.brandsofpuertorico.com/api/v1/countries/?page=' + str(i)
            time.sleep(0.01)
            r = requests.get(page_vise_url, headers=headers_country)
            # val =json.loads(r.content)
            val = json.loads(r.text)
            items = val['_embedded']['items']
            for item in items:
                detailed_country_url = 'https://staging.brandsofpuertorico.com/api/v1/countries/' + item['code']
                r_detailed = requests.get(detailed_country_url, headers=headers_country)
                val_detailed = json.loads(r_detailed.text)
                countries.append(val_detailed)
            i = i + 1
        self.create_country(countries)
        return request.render("odoo_sylius_connector.sylius_page")

    def create_country(self, countries):
        for country in countries:
            print("countires===>",country)


    @http.route('/page/import_customer_sylius', auth='public', type='http', website=True)
    def import_customer_sylius(self, **post):
        auth_header = self.get_auth_token_header()
        headers_customer = {
            'Authorization': auth_header,
            'Accept': 'application/json',

        }
        print("header===========>", headers_customer)
        customer_url = 'https://staging.brandsofpuertorico.com/api/v1/customers/'
        customer_response = requests.get(customer_url, headers=headers_customer)
        print("customer_response================>", json.loads((customer_response.content).decode("utf-8")))
        res = json.loads((customer_response.content).decode("utf-8"))
        pages = res['pages']
        print('pages=====>', pages)
        # items = json.loads(product_response(['_embedded']['items']))
        i = 1
        customers = []
        while i <= 5:
            page_vise_url = 'https://staging.brandsofpuertorico.com/api/v1/customers/?page=' + str(i)
            time.sleep(0.01)
            r = requests.get(page_vise_url, headers=headers_customer)
            # val =json.loads(r.content)
            val = json.loads(r.text)
            items = val['_embedded']['items']
            for item in items:
                customers.append(item)
            i = i + 1
        self.create_customer(customers)
        return request.render("odoo_sylius_connector.sylius_page")

    def create_customer(self, customers):
        for customer in customers:
            print("Customer====>", customer)
            values = {
                'name': customer['email'],
                'customer': True,
                'email': customer['email'],
                'sylius_id': customer['id']

            }
            #checking if customer has firstName and updating the dictonary accordingly
            if 'firstName' in customer:
                if customer['firstName']:
                    values.update({'name':customer['firstName']})

            if 'firstName' in customer and 'lastName' in customer:
                if customer['firstName'] and customer['lastName']:
                    values.update({'name':customer['firstName']+' '+customer['lastName']})


            partner_id = request.env['res.partner'].sudo().search([('email','=',customer['email'])])

            if partner_id:
                partner_id.write(values)

            else:
                customer_id = request.env['res.partner'].sudo().create(values)
                print(customer_id)


    @http.route('/page/import_order_sylius', auth='public', type='http', website=True)
    def import_order_sylius(self, **post):
        auth_header = self.get_auth_token_header()
        headers_order = {
            'Authorization': auth_header,
            'Accept': 'application/json',

        }
        print("header===========>", headers_order)
        order_url = 'https://staging.brandsofpuertorico.com/api/v1/orders/'
        order_response = requests.get(order_url, headers=headers_order)
        print("order_response================>", json.loads((order_response.content).decode("utf-8")))
        res = json.loads((order_response.content).decode("utf-8"))
        pages = res['pages']
        print('pages=====>', pages)
        # items = json.loads(product_response(['_embedded']['items']))
        i = 1
        orders = []
        # while i <= 1:
        #     page_vise_url = 'https://staging.brandsofpuertorico.com/api/v1/orders/?page=' + str(i)
        #     time.sleep(0.01)
        #     r = requests.get(page_vise_url, headers=headers_order)
        #     # val =json.loads(r.content)
        #     val = json.loads(r.text)
        #     items = val['_embedded']['items']
        #     for item in items:
        detailed_page_url = 'https://staging.brandsofpuertorico.com/api/v1/orders/51887'
        r_detailed = requests.get(detailed_page_url, headers=headers_order)
        val_detailed = json.loads(r_detailed.text)
        orders.append(val_detailed)
            # i = i + 1
        self.create_order(orders)
        return request.render("odoo_sylius_connector.sylius_page")


    def create_order(self, orders):
        for order in orders:
            print("Order====>", order)
            sale_order_id = request.env['sale.order'].sudo().search([('sylius_order_id', '=', order['id'])])
            self.create_customer([order['customer']])
            customer_id = request.env['res.partner'].sudo().search([('email', '=', order['customer']['email'])])
            # del_add = customer_id.address_get(['delivery'])
            # if not del_add:
            #     del_add =  request.env['res.partner'].sudo().create({'parent_id':customer_id.id,
            #                                                   'type':'delivery',
            #                                                   'street': order['istreet'],
            #                                                   'street2': order['istreet2'],
            #                                                   'city':order['icity'],
            #                                                   'state_id':order['iselection_state'],
            #                                                   'zip':order['izip'],
            #                                                   'country_id':order['iselection_country']})


            values = {'sylius_order_id': order['id'],
                      'partner_id': customer_id.id}
            if not sale_order_id:
                sale_order_id = request.env['sale.order'].create(values)
                print(sale_order_id)

            if 'shipments' in order:
                sale_order_id.write({'sylius_shipment_id':order['shipments'][0]['id']})

            # here we get the sale order lines and check if the product in present or we create the product and its variants
            for line in order['items']:
                prod_id = request.env['product.product'].search([('sylius_variant_id','=',line['variant']['id'])])
                if not prod_id:
                    # prod_id = request.env['product.product'].search([('sylius_id','=',line['variant']['id']),])
                    # if not prod_id:
                    product_url_detailed = 'https://staging.brandsofpuertorico.com'+ line['variant']['_links']['product']['href']
                    product_detailed_res = requests.get(product_url_detailed, headers={'Authorization': self.get_auth_token_header(),'Accept': 'application/json',})
                    val_detailed = json.loads(product_detailed_res.text)
                    self.create_product([val_detailed])
                    prod_created_id = request.env['product.template'].search([('sylius_id','=',val_detailed['id'])])
                    var_vise_url = 'https://staging.brandsofpuertorico.com/index.php/api/v1/products/' + prod_created_id.sylius_code + '/variants'
                    r = requests.get(var_vise_url, headers={'Authorization': self.get_auth_token_header(),'Accept': 'application/json',})
                    val = json.loads(r.text)
                    prod_var = []
                    items = val['_embedded']['items']
                    for item in items:
                        variant_vise_url = 'https://staging.brandsofpuertorico.com/index.php/api/v1/products/' + prod_created_id.sylius_code + '/variants/' + item['code']
                        r_var = requests.get(variant_vise_url, headers={'Authorization': self.get_auth_token_header(),'Accept': 'application/json',})
                        val_var = json.loads(r_var.text)
                        prod_var.append(val_var)

                    if val['total'] > 1:
                        attribute_id = request.env['product.attribute'].sudo().search(
                            [('name', '=', prod_created_id.name)])
                        if not attribute_id:
                            attribute_id = request.env['product.attribute'].sudo().create(
                                {'name': prod_created_id.name})
                        vals_ids = []
                        for product in prod_var:
                            value_id = request.env['product.attribute.value'].sudo().search(
                                [('attribute_id', '=', attribute_id.id),
                                 ('name', '=', product['translations']['en']['name'])])
                            if not value_id:
                                value_id = request.env['product.attribute.value'].sudo().create(
                                    {'attribute_id': attribute_id.id,
                                     'name': product['translations']['en']['name']})

                            vals_ids.append(value_id.id)
                        vals_prod_var = {'attribute_id': attribute_id.id,
                                         'value_ids': [(6, 0, vals_ids)]}
                        prod_created_id.sudo().write({'attribute_line_ids': [(0, 0, vals_prod_var)]})

                        for att_val in prod_var:
                            var_value_id = request.env['product.attribute.value'].sudo().search(
                                [('attribute_id', '=', attribute_id.id),
                                 ('name', '=', att_val['translations']['en']['name'])])
                            # product_var_id = request.env['product.product'].search([('attribute_value_ids','child_of',[var_value_id.id])])
                            request.cr.execute(
                                "select product_product_id from product_attribute_value_product_product_rel where product_attribute_value_id = %s",
                                (var_value_id.id,))
                            product_var_id = request.cr.fetchall()

                            if product_var_id:
                                product_id_variant = request.env['product.product'].browse(product_var_id[0])
                                product_id_variant.write({'sylius_variant_id': att_val['id'],
                                                          'sylius_variant_code': att_val['code'],
                                                          'weight': att_val['weight']})

                        prod_id = request.env['product.product'].search([('sylius_variant_id','=',line['variant']['id'])])

                    else:
                        for prod_var_new in prod_var:
                            prod_created_id.valid_existing_variant_ids.write({'sylius_variant_id': prod_var_new['id'],
                                                                              'sylius_variant_code':prod_var_new['code'],
                                                                              'weight': prod_var_new['weight'], })

                            prod_id = prod_created_id.valid_existing_variant_ids

                vals_order_line = {'order_id':sale_order_id.id,
                                   'product_id':prod_id.id,
                                   'name':prod_id.name,
                                   'product_uom_qty':line['quantity'],
                                   'price_unit':line['unitPrice']/100}

                request.env['sale.order.line'].create(vals_order_line)

            #check if the order has adjustments and add it
            if order['adjustments']:
                for adjustmentlines in order['adjustments']:
                    values_adjustment_lines = {'sylius_adjustment_id':adjustmentlines['id'],
                                               'sale_adjustment_order_id':sale_order_id.id,
                                               'adjustment_type':adjustmentlines['type'],
                                               'adjustment_label':adjustmentlines['label'],
                                               'adjustment_amount':adjustmentlines['amount']/100}

                    request.env['sale.adjustment.lines'].create(values_adjustment_lines)







    @http.route('/page/update_products_sylius', auth='public', type='http', website=True)
    def update_products_sylius(self, **post):

        options_list = []
        auth_header = self.get_auth_token_header()
        produtcs = request.env['product.template'].search(
            [('sylius_id', '!=', False),('supplier_ids', 'child_of', request.env.user.id)])
        if produtcs:
            for product in produtcs:
                #taking products which is updated after exported to sylius, those products will get updated this time
                if product.last_sylius_update and product.updated_at and product.last_sylius_update < product.updated_at:
                    print('product present!')
                    url = "https://staging.brandsofpuertorico.com/index.php/api/v1/products/"+product.sylius_code
                    headers = {
                        'authorization': auth_header,
                        'content-type': "application/json",

                    }

                    if product.attribute_line_ids:

                        options_url = "https://staging.brandsofpuertorico.com/api/v1/product-options/"
                        variants_url = "https://staging.brandsofpuertorico.com/api/v1/products/" + product.sylius_code + "/variants/"
                        #if variants present in product first creating product options.
                        for attribute in product.attribute_line_ids:
                            options_data = {}
                            values = []
                            for val in attribute.value_ids:
                                selection = {
                                    "code": val.name.lower().replace(" ", ""),
                                    "translations": {
                                        "en_US": {
                                            "value": val.name
                                        }
                                    }
                                }
                                values.append(selection)

                            options_data.update({
                                "code": (attribute.attribute_id.name).lower(),
                                "translations": {
                                    "en_US": {
                                        "name": attribute.attribute_id.name,
                                    }},
                                "values": values
                            })
                            print(json.dumps(options_data))
                            options_response = requests.post(options_url, data=json.dumps(options_data),
                                                             headers=headers)
                            #if status is 400 that means option already exist. Updating option since it may contain new values for the option
                            if options_response.status_code == 400:
                                options_update_url = "https://staging.brandsofpuertorico.com/api/v1/product-options/" + (
                                    attribute.attribute_id.name).lower()
                                options_update_response = requests.patch(options_update_url,
                                                                         data=json.dumps(options_data),
                                                                         headers=headers)
                                print('update respone===========>', options_update_response)
                            options_list.append((attribute.attribute_id.name).lower())

                    if product.attribute_line_ids:
                        data = {
                            "code": product.sylius_code,
                            "translations": {
                                "en_US": {
                                    "name": product.name,
                                    "slug": product.sylius_slug
                                }
                            },
                            "options": options_list,
                            "website": product.website

                        }


                    else:
                        data = {
                            "code": product.sylius_code,
                            "translations": {
                                "en_US": {
                                    "name": product.name,
                                    "slug": product.sylius_slug
                                }
                            },
                            "website": product.website

                        }

                    print('data====>', json.dumps(data))

                    response = requests.put(url,data=json.dumps(data),headers=headers)

                    if response.status_code == 204:
                        product.write({'last_sylius_update':datetime.datetime.now()})

                    #After updating products. checking if new variants are added
                    variants_get_url = "https://staging.brandsofpuertorico.com/api/v1/products/"+product.sylius_code+"/variants"
                    var_response = requests.get(variants_get_url,headers=headers)
                    vars = json.loads(var_response.content.decode('utf-8'))
                    #if initially product dont have any variant and need to update with variant
                    # if vars['total'] == 0:
                    i = 0
                    if product.product_variant_ids:
                        for product_var in product.product_variant_ids:

                            option_vals = {}

                            variants_url = "https://staging.brandsofpuertorico.com/index.php/api/v1/products/" + product.sylius_code + "/variants/"

                            for var in product_var.attribute_value_ids:
                                attr_id = request.env['product.attribute'].search([('id', '=', var.attribute_id.id)])
                                if attr_id:
                                    option_vals.update({attr_id.name.lower(): var.name.lower().replace(" ", "")})

                                    print("options vals==========>", option_vals)
                            variants_data = {
                                "code": product_var.name + '_variant_' + str(i),
                                "translations": {
                                    "en_US": {
                                        "name": product_var.name + '-variant-' + str(i),
                                    }
                                },
                                "optionValues": option_vals,
                                "cost": product_var.cost,
                                "map_eur": product_var.map_eur,
                                "map_gbp": product_var.map_gbp,
                                "bom": product_var.bom,
                                "dg_batt": product_var.dg_batt,
                                "enabled": product_var.product_status

                            }
                            if product_var.current_stock:
                                variants_data.update({'onHand': product_var.current_stock})
                            if product_var.ean:
                                variants_data.update({'ean': product_var.ean})
                            if product_var.tracked:
                                variants_data.update({'tracked': product_var.tracked})
                            if product_var.hs_code:
                                variants_data.update({'hs_code': product_var.hs_code})
                            if product_var.ce_code:
                                variants_data.update({'ce_code': product_var.ce_code})
                            if product_var.stock_remark:
                                variants_data.update({'stock': product_var.stock_remark})
                            if product_var.date_launched:
                                variants_data.update({'date_launched': product_var.date_launched.__str__()})
                            if product_var.country_of_origin:
                                variants_data.update({'country_of_origin': product_var.country_of_origin.code})

                            print("variants====>", variants_data)
                            i = i + 1
                            varinats_response = requests.post(variants_url, data=json.dumps(variants_data),
                                                              headers=headers)
                            content = json.loads(varinats_response.content.decode('utf-8'))
                            print("variant_response=====>", varinats_response)
                            print("content=====>", content)

                            # if varinats_response.status_code == 500:
                            # #that means variant already exist so just update the variant
                            #   update_url = "http://139.59.76.203/index.php/api/v1/products/" + product.sylius_code + "/variants/"+product_var.name + '_variant_' + str(i)
                            #   var_update_response = requests.patch(update_url, data=json.dumps(variants_data),
                            #                                          headers=headers)
                            product_var.write({'last_sylius_update':datetime.datetime.now()})
            else:
                print('No products!')
        return request.render("odoo_sylius_connector.sylius_page")

    @http.route('/page/add_export_products_data', auth='public', type='http', website=True)
    def add_export_products_data(self, **post):
        #TDE: if there is a large number of products to upload the access token will get expired.so need to regenerate it.
        auth_header = self.get_auth_token_header()

        headers = {
            'authorization': auth_header,
            'content-type': "application/json",

        }
        url = "https://staging.brandsofpuertorico.com/index.php/api/v1/products/"
        # produtcs = request.env['product.product'].search([('create_date', '>', sup_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT))])
        produtcs = request.env['product.template'].search([('sylius_id','=',False),('supplier_ids', 'child_of', request.env.user.id)])
        print(produtcs)
        options_list = []

        html_vals = []
        # html = 0
        if produtcs:

            print('product===>',produtcs)
            for product in produtcs:
                print(product.image_medium)
                if product.attribute_line_ids:

                    options_url = "https://staging.brandsofpuertorico.com/index.php/api/v1/product-options/"
                    variants_url = "https://staging.brandsofpuertorico.com/index.php/api/v1/products/" + product.sylius_code + "/variants/"
                    for attribute in product.attribute_line_ids:
                        html =0
                        options_data = {}
                        sel = {}
                        selection = {}
                        values = []
                        html_vals =[]
                        for val in attribute.value_ids:
                            # if val.html_color:
                            #     html = 1
                            #     sel = {
                            #         "code": 'html'+val.html_color.replace('#','_'),
                            #         "translations": {
                            #             "en_US": {
                            #                 "value": val.html_color
                            #             }
                            #         }
                            #     }
                            #     html_vals.append(sel)




                            selection =  {
                                "code": val.name.lower().replace(" ",""),
                                "translations": {
                                    "en_US": {
                                        "value": val.name
                                    }
                                }
                            }
                            values.append(selection)

                        options_data.update( {
                            "code": (attribute.attribute_id.name).lower(),
                            "translations": {
                                "en_US": {
                                    "name": attribute.attribute_id.name,
                                }},
                            "values": values
                        })
                        print(json.dumps(options_data))
                        options_response = requests.post(options_url, data=json.dumps(options_data),
                                                         headers=headers)
                        if options_response.status_code == 400:
                            options_update_url ="https://staging.brandsofpuertorico.com/index.php/api/v1/product-options/"+(attribute.attribute_id.name).lower()
                            options_update_response = requests.patch(options_update_url, data=json.dumps(options_data),
                                                                     headers=headers)
                            print('update respone===========>',options_update_response)
                        options_list.append((attribute.attribute_id.name).lower())
                        # if html ==1:
                        #     html_options = {
                        #         "code": 'html_color',
                        #         "translations": {
                        #             "en_US": {
                        #                 "name": 'Html Color',
                        #             }},
                        #         "values": html_vals
                        #     }
                        #     options_html_response = requests.post(options_url, data=json.dumps(html_options),
                        #                                      headers=headers)
                        #     options_list.append('html_color')


                if product.attribute_line_ids:
                    data = {
                        "code": product.sylius_code,
                        "translations": {
                            "en_US": {
                                "name": product.name,
                                "slug": product.sylius_slug
                            }
                        },
                        "options": options_list,
                        "website":product.website,
                        "images": [
                            {
                                "type":"type1"
                            }
                        ]

                    }


                else:
                    data = {
                        "code": product.sylius_code,
                        "translations": {
                            "en_US": {
                                "name": product.name,
                                "slug": product.sylius_slug
                            }
                        },
                        "website":product.website,
                        "images": [
                            {
                                "type":"type1"
                            }
                        ]

                    }



                print('data====>',json.dumps(data))
                response = requests.post(url,data=json.dumps(data),headers=headers)

                # response = requests.post(url,data=json.dumps(data),json=json.dumps({'images':[{"file":str(base64.b64encode(product.image_medium).decode("utf-8")),}]}),headers=headers)
                # response = requests.post(url,data=json.dumps(data),files={'images': [{'/opt/odoo12/odoo/custom_addons/odoo_sylius_connector/static/src/img/back-enable.jpg'}]},headers=headers)
                print('response===>',response)
                if response.status_code == 201:
                    report = request.env['sylius.report'].create(
                        {'product_id': product.id, 'export_date': datetime.datetime.now(),'status':'Success',
                         'status_code': response.status_code})
                    res = json.loads(response.content.decode('utf-8'))
                    print('sylius_id=======>',res['id'])
                    product.write({'sylius_id':res['id'],'last_sylius_update':datetime.datetime.now()})
                    i = 0
                    for product_var in product.product_variant_ids:
                        print("attributes==================>")
                        print(product_var.attribute_value_ids)
                        product_var.write({'sylius_id':res['id'],
                                           'last_sylius_update': datetime.datetime.now()})

                        option_vals = { }

                        variants_url = "https://staging.brandsofpuertorico.com/index.php/api/v1/products/" + product.sylius_code + "/variants/"

                        for var in product_var.attribute_value_ids:
                            attr_id = request.env['product.attribute'].search([('id','=',var.attribute_id.id)])
                            if attr_id:
                                option_vals.update({attr_id.name.lower():var.name.lower().replace(" ","")})

                                print("options vals==========>",option_vals)
                        variants_data = {
                            "code": product_var.name+'_variant_'+str(i),
                            "translations": {
                                "en_US": {
                                    "name": product_var.name+'-variant-'+str(i),
                                }
                            },
                            "optionValues": option_vals,
                            "cost":product_var.cost,
                            "map_eur":product_var.map_eur,
                            "map_gbp":product_var.map_gbp,
                            "bom":product_var.bom,
                            "dg_batt":product_var.dg_batt,
                            "enabled":product_var.product_status


                        }
                        if product_var.current_stock:
                            variants_data.update({'onHand':product_var.current_stock})
                        if product_var.ean:
                            variants_data.update({'ean':product_var.ean})
                        if product_var.tracked:
                            variants_data.update({'tracked': product_var.tracked})
                        if product_var.hs_code:
                            variants_data.update({'hs_code': product_var.hs_code})
                        if product_var.ce_code:
                            variants_data.update({'ce_code': product_var.ce_code})
                        if product_var.stock_remark:
                            variants_data.update({'stock': product_var.stock_remark})
                        if product_var.date_launched:
                            variants_data.update({'date_launched': product_var.date_launched.__str__()})
                        if product_var.country_of_origin:
                            variants_data.update({'country_of_origin': product_var.country_of_origin.code})

                        print("variants====>",variants_data)
                        i=i+1
                        varinats_response = requests.post(variants_url, data=json.dumps(variants_data),
                                                          headers=headers)
                        print("variant_response=====>",varinats_response)
                        # res = json.loads(varinats_response.content.decode('utf-8'))
                        # print("errror=====>", res)


                        product_var.write({'sylius_id':res['id'],'last_sylius_update':datetime.datetime.now()})



                else:

                    report = request.env['sylius.report'].create({'product_id':product.id,'export_date':datetime.datetime.now(),'status':'Fail','status_code':response.status_code,'reason':json.loads(response.content.decode('utf-8'))})
                    res = json.loads(response.content.decode('utf-8'))


        else:
            print("no products")

        return request.render("odoo_sylius_connector.sylius_page")



    @http.route('/page/sylius', auth='public', type='http', website=True)
    def sylius_page(self, **kwargs):

        return request.render("odoo_sylius_connector.sylius_page")

    @http.route('/page/add_import_products_data', auth='public', type='http', website=True, csrf=False)
    def add_import_products_data(self, **post):
        auth_header = self.get_auth_token_header()
        headers_product = {
            'Authorization': auth_header,
            'Accept': 'application/json',


        }
        print("header===========>",headers_product)
        product_url = 'https://staging.brandsofpuertorico.com/api/v1/products/'
        product_response = requests.get(product_url,headers=headers_product)
        print("product_response================>", json.loads((product_response.content).decode("utf-8")))
        res = json.loads((product_response.content).decode("utf-8"))
        pages = res['pages']
        print('pages=====>',pages)
        # items = json.loads(product_response(['_embedded']['items']))
        i = 1
        products = []
        while  i <= pages:
            print(i)
            page_vise_url = 'https://staging.brandsofpuertorico.com/api/v1/products/?page=' + str(i)
            time.sleep(0.01)
            r = requests.get(page_vise_url, headers=headers_product)
            # val =json.loads(r.content)
            val =json.loads(r.text)
            items = val['_embedded']['items']
            for item in items:
                # prod_detail_url = 'https://staging.brandsofpuertorico.com/index.php/api/v1/products/'+ item['code']
                # r_detailed = requests.get(prod_detail_url, headers=headers_product)
                # val_detailed = json.loads(r_detailed.text)
                products.append(item)
            i = i+1
        self.create_product(products)
        return request.render("odoo_sylius_connector.sylius_page")


    def create_product(self,products):
        for product in products:
            print("product====>",product)

            values ={
                'type':'product',
                'name':product['name'],
                'sylius_id':product['id'],
                'sylius_code':product['code']

            }
            product_id = request.env['product.template'].sudo().search([('sylius_id','=',product['id'])])
            if not product_id:
                product_id = request.env['product.template'].sudo().create(values)

            else:
                product_id.write(values)

            print(product_id)

    @http.route('/page/import_product_variants', auth='public', type='http', website=True, csrf=False)
    def add_product_variants(self, **post):
        auth_header = self.get_auth_token_header()
        headers_product_variant = {
            'Authorization': auth_header,
            'Accept': 'application/json',

        }
        # options_url_product = 'https://staging.brandsofpuertorico.com/api/v1/product-options/'
        # options_url_product_response = requests.get(options_url_product, headers=headers_product_variant)
        # x = (options_url_product_response.content).decode("utf-8")
        # res_options = json.loads((options_url_product_response.content).decode("utf-8"))
        # pages_option = res_options['pages']
        # i = 1
        # products_options = []
        # while i <= pages_option:
        #     page_vise_url = 'https://staging.brandsofpuertorico.com/index.php/api/v1/product-options/?page=' + str(i)
        #     time.sleep(0.01)
        #     r = requests.get(page_vise_url, headers=headers_product_variant)
        #     val = json.loads(r.text)
        #     items = val['_embedded']['items']
        #     for item in items:
        #         products_options.append(item)
        #     i = i + 1


        prods = request.env['product.template'].search([('sylius_id','!=',False)],)
        print(prods)
        if prods:
            for prod in prods:
                print(prod.name)
                product_variant_url = "https://staging.brandsofpuertorico.com/index.php/api/v1/products/" + prod.sylius_code + "/variants/"
                product_variant_response = requests.get(product_variant_url, headers=headers_product_variant)

                res = json.loads((product_variant_response.content).decode("utf-8"))
                pages = res['pages']
                print('pages=====>', pages)
                # items = json.loads(product_response(['_embedded']['items']))
                i = 1
                products_var = []
                while i <= pages:
                    page_vise_url = 'https://staging.brandsofpuertorico.com/index.php/api/v1/products/' + prod.sylius_code + '/variants/?page=' + str(i)
                    time.sleep(0.01)
                    r = requests.get(page_vise_url, headers=headers_product_variant)
                    val = json.loads(r.text)
                    items = val['_embedded']['items']
                    for item in items:
                        variant_vise_url ='https://staging.brandsofpuertorico.com/index.php/api/v1/products/'+ prod.sylius_code+'/variants/'+ item['code']
                        r_var = requests.get(variant_vise_url, headers=headers_product_variant)
                        val_var = json.loads(r_var.text)
                        products_var.append(val_var)

                    i = i + 1
                    # self.create_product_variants(products_var,prod.id,val['total'])
                    attribute_id = request.env['product.attribute'].sudo().search([('name', '=', prod.name)])
                    if not attribute_id:
                        attribute_id = request.env['product.attribute'].sudo().create({'name': prod.name})

                    if val['total'] > 1:
                        vals_ids = []
                        for product in products_var:
                            value_id = request.env['product.attribute.value'].sudo().search([('attribute_id','=',attribute_id.id),('name','=',product['translations']['en']['name'])])
                            if not value_id:
                                value_id = request.env['product.attribute.value'].sudo().create({'attribute_id' : attribute_id.id,
                                                                                                 'name':product['translations']['en']['name']})

                            vals_ids.append(value_id.id)
                        attribute_template_line_id  = request.env['product.template.attribute.line'].sudo().create({'product_tmpl_id':prod.id,
                                                                                          'attribute_id': attribute_id.id,
                                                                                          'value_ids': [(6,0,vals_ids)]
                                                                                          })

                        # vals_prod_var = {'attribute_id': attribute_id.id,
                        #                  'value_ids':[(6,0,vals_ids)]}
                        prod.sudo().write({'attribute_line_ids':[(6,0,[attribute_template_line_id.id])]})

                        for att_val in products_var:
                            var_value_id = request.env['product.attribute.value'].sudo().search([('attribute_id','=',attribute_id.id),('name','=',att_val['translations']['en']['name'])])
                            # product_var_id = request.env['product.product'].search([('attribute_value_ids','child_of',[var_value_id.id])])
                            request.cr.execute("select product_product_id from product_attribute_value_product_product_rel where product_attribute_value_id = %s",(var_value_id.id,))
                            product_var_id = request.cr.fetchall()

                            if product_var_id:
                                product_id_variant = request.env['product.product'].browse(product_var_id[0])
                                product_id_variant.write({'sylius_variant_id': att_val['id'],
                                                          'sylius_variant_code':att_val['code'],
                                                          'weight':att_val['weight'],})
                                                          # 'qty_available':att_val['onHand']})


                    else:
                        for prod_var_prod in products_var:
                            prod.valid_existing_variant_ids.write({'sylius_variant_id': prod_var_prod['id'],
                                                                   'sylius_variant_code':prod_var_prod['code'],
                                                                   'weight':prod_var_prod['weight'],})
                                                                   # 'qty_available':prod_var_prod['onHand']})

                            # wizard = request.env['stock.change.product.qty'].create({
                            #     'product_id': prod.valid_existing_variant_ids.id,
                            #     'new_quantity': prod_var_prod['onHand'],
                            #     'location_id': 12,
                            # })
                            # wizard.change_product_qty()





        return request.render("odoo_sylius_connector.sylius_page")