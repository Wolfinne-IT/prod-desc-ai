import logging
from openai import OpenAI, APIError

from odoo import models
from odoo.exceptions import UserError
from odoo.tools import image_data_uri

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def update_product_desc_ai(self, product_id, desc_tone, desc_lang='en'):
        _logger.info(f'Update product (ID: {product_id}) description by AI in {desc_tone} tone.')

        product = self.browse(product_id)
        if not product.image_1920:
            _logger.error('Product image is not available.')
            raise UserError('Product image is not available.')

        api_key = self.env['ir.config_parameter'].get_param('gpt_opd_api_key')
        if not api_key:
            _logger.error('API key is not set.')
            raise UserError('API key is not set.')

        model = self.env['ir.config_parameter'].get_param('gpt_opd_model', default='gpt-4o')
        max_tokens = self.env['ir.config_parameter'].get_param('gpt_opd_max_tokens', default=300)
        image_url = image_data_uri(product.image_1920)
        content = [
            {
                "type": "text",
                "text": f"Describe this product in {desc_tone} tone. Name of the product is {product.name}. "
                        f"The description should be in language with locale code {desc_lang} and should be "
                        f"suitable for e-commerce. Do not use lists and bullet points. Do not style the text, "
                        f"except emoticons when you want them."
            },
            {
              "type": "image_url",
              "image_url": {
                "url": image_url,
              },
            },
        ]
        client = OpenAI(api_key=api_key)

        try:
            response = client.chat.completions.create(
                model = model,
                messages = [{
                    "role": "user",
                    "content": content,
                }],
                max_tokens = max_tokens,
            )
        except APIError as e:
            _logger.error(f"OpenAI API Error: {str(e)}")
            raise UserError(f"Failed to generate description: {str(e)}")
        except Exception as e:
            _logger.error(f"Unexpected Error: {str(e)}")
            raise UserError(f"An unexpected error occurred: {str(e)}")

        product.write({'description_ecommerce': response.choices[0].message.content})

        return response.choices[0].message.content
