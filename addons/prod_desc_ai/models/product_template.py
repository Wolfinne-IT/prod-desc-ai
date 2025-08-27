import logging
from openai import OpenAI, APIError

from odoo import _, models, api
from odoo.exceptions import UserError
from odoo.tools import image_data_uri

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def update_product_desc_ai(self, product_id, desc_tone, desc_lang="en_US", server_action=False):
        _logger.info("Update product (ID: %s) description by AI in %s tone.", product_id, desc_tone)

        product = self.browse(product_id)
        if not product.exists():
            _logger.error("Product not found.")
            if server_action:
                return False
            raise UserError(_("Product not found."))

        if not product.image_1920:
            _logger.error("Product image is not available.")
            if server_action:
                return False
            raise UserError(_("Product image is not available."))

        icp = self.env["ir.config_parameter"].sudo()
        api_key = icp.get_param("gpt_opd_api_key")
        if not api_key:
            _logger.error("API key is not set.")
            raise UserError(_("API key is not set."))

        model = icp.get_param("gpt_opd_model", default="gpt-4o")
        try:
            max_tokens = int(icp.get_param("gpt_opd_max_tokens", default="300"))
        except Exception:
            max_tokens = 300

        image_url = image_data_uri(product.image_1920)
        content = [
            {
                "type": "text",
                "text": (
                    f"Describe this product in {desc_tone} tone. "
                    f"Name of the product is {product.name}. "
                    f"The description should be in language with locale code {desc_lang} and should be "
                    f"suitable for e-commerce. Do not use lists and bullet points. Do not style the text, "
                    f"except emoticons when those are suitable and convenient for the use."
                ),
            },
            {"type": "image_url", "image_url": {"url": image_url}},
        ]

        client = OpenAI(api_key=api_key)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content}],
                max_tokens=max_tokens,
            )
        except APIError as e:
            _logger.error("OpenAI API Error: %s", str(e))
            raise UserError(_("Failed to generate description: %s") % str(e))
        except Exception as e:
            _logger.error("Unexpected Error: %s", str(e))
            raise UserError(_("An unexpected error occurred: %s") % str(e))

        text = (response.choices[0].message.content or "").strip()
        if not text:
            if server_action:
                return False
            raise UserError(_("Empty response from the model."))

        # v16: koristi website_description; fallback na core polja
        fields_map = product._fields
        values = {}
        if "website_description" in fields_map:
            values["website_description"] = text
        else:
            if "description" in fields_map:
                values["description"] = text
            if "description_sale" in fields_map:
                values["description_sale"] = text

        if not values:
            _logger.warning("No suitable description field on product.template.")
            if server_action:
                return False
            raise UserError(_("No suitable description field found on product."))

        product.with_context(lang=self.env.user.lang).write(values)
        return text

    def button_update_description(self):
        desc_tone = self.env.context.get("desc_tone")
        if not desc_tone:
            raise UserError(_("Description tone is not set."))
        lang = self.env.context.get("lang") or "en_US"
        for record in self:
            record.update_product_desc_ai(record.id, desc_tone, lang)

    def update_all_description_ecommerce(self, tone):
        lang = self.env.context.get("lang") or "en_US"
        for record in self.env["product.template"].search([]):
            record.update_product_desc_ai(record.id, tone, lang, server_action=True)
