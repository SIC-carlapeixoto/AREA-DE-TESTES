#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import base64

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    director_signature = fields.Binary(string="Signature")
    
    psico = fields.Boolean(string='Psico', compute='_is_psico')
    anexo_7 = fields.Boolean(string='Anexo VII', compute='_is_anexo_7')
    export = fields.Boolean(string='Exportar', compute='_is_export')


    def _is_psico(self):
        for rec in self:
            for x in rec.order_line:
                if x.product_id.categ_id.name == 'PSICOS - Psicotrópicos e Estupefacientes':
                    rec.psico = True
                    return True
                rec.psico = False
                return False


    def _is_anexo_7(self):
        for rec in self:
            if rec.psico and rec.fiscal_position_id.name in ['Continente','Madeira','Açores']:
                rec.anexo_7 = True
                return True
            rec.anexo_7 = False
            return False

    def _is_export(self):
        for rec in self:
            if rec.psico and rec.fiscal_position_id.name not in ['Continente','Madeira','Açores']:
                rec.export = True
                return True
            rec.export = False
            return False


    def action_rfq_send(self):
        '''
        This function opens a window to compose an email, with the edi purchase template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            if self.env.context.get('send_rfq', False):
                template_id = ir_model_data._xmlid_lookup('purchase.email_template_edi_purchase')[2]
            else:
                template_id = ir_model_data._xmlid_lookup('purchase.email_template_edi_purchase_done')[2]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[2]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'purchase.order',
            'active_model': 'purchase.order',
            'active_id': self.ids[0],
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': "mail.mail_notification_layout_with_responsible_signature",
            'force_email': True,
            'mark_rfq_as_sent': True,
        })

        # In the case of a RFQ or a PO, we want the "View..." button in line with the state of the
        # object. Therefore, we pass the model description in the context, in the language in which
        # the template is rendered.
        lang = self.env.context.get('lang')
        if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
            template = self.env['mail.template'].browse(ctx['default_template_id'])
            template.attachment_ids = False
            if template and template.lang:
                lang = template._render_lang([ctx['default_res_id']])[ctx['default_res_id']]

        self = self.with_context(lang=lang)
        if self.state in ['draft', 'sent']:
            ctx['model_description'] = _('Request for Quotation')
        else:
            ctx['model_description'] = _('Purchase Order')

########################
########################

        if self.anexo_7:
            pdf = self.env.ref('sic_nmvs_connector.report_anexo_7_rec')._render_qweb_pdf(self.ids)
            b64_pdf = base64.b64encode(pdf[0])
            name = "Anexo VII - " + self.name + ".pdf"
            anexo_7 = self.env['ir.attachment'].create({
                'name': name,
                'type': 'binary',
                'datas': b64_pdf,
                # 'datas_fname': name + '.pdf',
                'store_fname': name,
                'res_model': self._name,
                'res_id': self.id,
                'mimetype': 'application/x-pdf'
            })

            template.attachment_ids = False
            template.attachment_ids = [(4, anexo_7.id)]




########################
########################





        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


