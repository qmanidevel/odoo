# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import base64
import urllib2
import linkedin # TODO add depensy in packaging

import openerp
from openerp.osv import fields, osv

class Binary(openerp.addons.web.http.Controller):
    _cp_path = "/web_linkedin/binary"

    @openerp.addons.web.http.jsonrequest
    def url2binary(self, req,url):
        bfile = urllib2.urlopen(url)
        return base64.b64encode(bfile.read())
    
class web_linkedin_settings(osv.osv_memory):
    _inherit = 'sale.config.settings'
    _columns = {
        'api_key': fields.char(string="API Key", size=50),
        'server_domain': fields.char(size=100),
    }
    
    def get_default_linkedin(self, cr, uid, fields, context=None):
        key = self.pool.get("ir.config_parameter").get_param(cr, uid, "web.linkedin.apikey") or ""
        dom = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
        return {'api_key': key, 'server_domain': dom,}
    
    def set_linkedin(self, cr, uid, ids, context=None):
        key = self.browse(cr, uid, ids[0], context)["api_key"] or ""
        self.pool.get("ir.config_parameter").set_param(cr, uid, "web.linkedin.apikey", key)

class web_linkedin_fields(osv.Model):
    _inherit = 'res.partner'

    def _get_url(self, cr, uid, ids, name, arg, context=None):
        res = dict((id, False) for id in ids)
        for partner in self.browse(cr, uid, ids, context=context):
            res[partner.id] = partner.linkedin_url
        return res

    _columns = {
        'linkedin_id': fields.char(string="LinkedIn ID", size=50),
        'linkedin_url': fields.char(string="LinkedIn url", size=100, store=True),
        'linkedin_public_url': fields.function(_get_url, type='text', string="LinkedIn url", 
            help="This url is set automatically when you join the partner with a LinkedIn account."),
    }