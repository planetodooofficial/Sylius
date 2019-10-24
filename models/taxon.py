from odoo import models,fields,api,_

class sylius_taxons(models.Model):
    _name = 'sylius.taxons'

    name = fields.Char('Main Taxon')


class sylius_credential(models.Model):
    _name = 'sylius.credential'

    name = fields.Char('Name')
    client_key = fields.Char('Client Key')
    client_secret = fields.Char('Client Secret')
    username = fields.Char('Username')
    password = fields.Char('Password')

class sylius_report(models.Model):
    _name = 'sylius.report'

    name = fields.Char('Name')
    product_id = fields.Many2one('product.template','Product')
    export_date = fields.Datetime("Export Date")
    status_code = fields.Char('Status Code')
    status = fields.Char('Status')
    reason = fields.Char('Failure Reason')