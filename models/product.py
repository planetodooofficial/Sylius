import datetime
import itertools

from odoo.addons import decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo.osv import expression
from odoo.tools import pycompat

class product_product(models.Model):
    _inherit = 'product.product'

    sylius_variant_id = fields.Integer('Sylius Variant Id')
    sylius_variant_code = fields.Char('Sylius Variant Code')
    sylius_id = fields.Integer('Sylius Id',related='product_tmpl_id.sylius_id')
    sylius_code = fields.Char('Sylius Code',related='product_tmpl_id.sylius_code',readonly=False)
    sylius_slug = fields.Char('Sylius Slug',related='product_tmpl_id.sylius_slug',readonly=False)
    website = fields.Selection([
        ('0', 'Online for everyone'),
        ('1', 'Only for Wholesale customer'),],default='0',related='product_tmpl_id.website')
    main_taxon_id = fields.Many2one('sylius.taxons',related='product_tmpl_id.main_taxon_id',readonly=False)
    updated_at = fields.Datetime('Updated At',related='product_tmpl_id.updated_at',readonly=False)
    last_sylius_update = fields.Datetime('Last Sylius Update',related='product_tmpl_id.last_sylius_update')
    translation_name=fields.Char('Name',related='product_tmpl_id.translation_name',readonly=False)
    description = fields.Char('Description',related='product_tmpl_id.description',readonly=False)
    ean = fields.Char('EAN',related='product_tmpl_id.ean',readonly=False)
    stock_remark=fields.Char('Stock Level Notes',related='product_tmpl_id.stock_remark',readonly=False)
    # bom = fields.Boolean('Has BOM',related='product_tmpl_id.bom',readonly=False)

    country_of_origin =  country_id = fields.Many2one(
        'res.country', 'Country of Origin',related='product_tmpl_id.country_of_origin',readonly=False)
    hs_code = fields.Char('HS Code',related='product_tmpl_id.hs_code',readonly=False)
    ce_code = fields.Char('CE Code',related='product_tmpl_id.ce_code',readonly=False)
    dg_batt = fields.Selection([
        ('0', 'No Battery'),
        ('1', 'Batt < 2.7Wh'),
        ('2', '2.7Wh< Batt < 20Wh'),
        ('3', ' Batt < 100Wh'),
        ('4', 'Packed with equipment'),
        ('5', 'Installed')
        ,],default='0',related='product_tmpl_id.dg_batt')
    map = fields.Monetary('Minimum Advertise Price',related='product_tmpl_id.map',readonly=False)
    map_eur = fields.Monetary('Minimum Advertise Price',related='product_tmpl_id.map_eur',readonly=False)
    map_gbp = fields.Monetary('MAP GBP',related='product_tmpl_id.map_gbp',readonly=False)
    failure_reason = fields.Char('Export Failure Reason',readonly=True)
    product_status =  fields.Selection([
        ('0', 'Disabled'),
        ('1', 'Enabled'),
        ('2', 'Pending to launch'),
        ('3', 'Discontinue'),
        ],default='0',
        related='product_tmpl_id.product_status')

    current_stock = fields.Integer('Current Stock',related='product_tmpl_id.current_stock',readonly=False)
    tracked = fields.Boolean('Tracked',related='product_tmpl_id.tracked',readonly=False)
    bom = fields.Selection([
        ('0', 'Yes'),
        ('1', 'No')],default='1',
        related='product_tmpl_id.bom')

    cost = fields.Float('Cost',related='product_tmpl_id.cost',readonly=False)
    date_launched = fields.Date('Date Launched',related='product_tmpl_id.date_launched',readonly=False)



class product_template(models.Model):
    _inherit = 'product.template'

    sylius_id = fields.Integer('Sylius Id',readonly=True)
    sylius_code = fields.Char('Sylius Code')
    sylius_slug = fields.Char('Sylius Slug')
    website = fields.Selection([
        ('0', 'Online for everyone'),
        ('1', 'Only for Wholesale customer'), ],default='0')
    main_taxon_id = fields.Many2one('sylius.taxons')
    updated_at = fields.Datetime('Updated At')
    last_sylius_update = fields.Datetime('Last Sylius Update',readonly=True)
    translation_name = fields.Char('Name')
    description = fields.Char('Description')
    ean = fields.Char('EAN')
    stock_remark = fields.Char('Stock Remark')
    # bom = fields.Boolean('Has BOM')
    country_of_origin = country_id = fields.Many2one(
        'res.country', 'Country of Origin')
    hs_code = fields.Char('HS Code')
    ce_code = fields.Char('CE Code')
    dg_batt = fields.Selection([
        ('0', 'No Battery'),
        ('1', 'Batt < 2.7Wh'),
        ('2', '2.7Wh< Batt < 20Wh'),
        ('3', ' Batt < 100Wh'),
        ('4', 'Packed with equipment'),
        ('5', 'Installed')
        , ],default='0')
    map = fields.Monetary('Minimum Advertise Price')
    map_eur = fields.Monetary('MAP EUR')
    map_gbp = fields.Monetary('MAP GBP')
    failure_reason = fields.Char('Export Failure Reason',readonly=True)
    product_status = fields.Selection([
        ('0', 'Disabled'),
        ('1', 'Enabled'),
        ('2', 'Pending to launch'),
        ('3', 'Discontinue'),
    ],default='0')

    current_stock = fields.Integer('Current Stock')
    tracked = fields.Boolean('Tracked')
    bom = fields.Selection([
        ('0', 'Yes'),
        ('1', 'No')],default='0')
    cost = fields.Float('Cost')
    date_launched = fields.Date('Date Launched')


    @api.multi
    def write(self, vals):
        vals.update({'updated_at': datetime.datetime.now()})
        res = super(product_template,self).write(vals)

        return res

