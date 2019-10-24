from odoo import models,fields,api

class SyliusFieldsResPartner(models.Model):

    _inherit = 'res.partner'

    sylius_id = fields.Integer('Sylius Id')