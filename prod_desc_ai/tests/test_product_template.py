import logging
from unittest.mock import patch, Mock
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class TestProductTemplate(TransactionCase):

    def setUp(self):
        super(TestProductTemplate, self).setUp()
        self.product_template = self.env['product.template']
        self.product = self.product_template.create({
            'name': 'Test Product',
            'image_1920': 'some_image_data',  # Use actual image data in a real test
        })

        # Set necessary config parameters
        self.env['ir.config_parameter'].set_param('gpt_opd_api_key', 'fake_api_key')
        self.env['ir.config_parameter'].set_param('gpt_opd_model', 'gpt-4o')
        self.env['ir.config_parameter'].set_param('gpt_opd_max_tokens', 300)

        # Mock OpenAI API response
        self.mock_response = Mock()
        self.mock_response.choices = [Mock(message=Mock(content="Generated description"))]

    @patch('openai.OpenAI')
    def test_update_product_desc_ai(self, mock_openai):
        mock_openai().chat.completions.create.return_value = self.mock_response

        # Call the method
        result = self.product.update_product_desc_ai(self.product.id, 'informal', 'en')

        # Assertions
        self.assertEqual(result, "Generated description")
        self.assertEqual(self.product.description_ecommerce, "Generated description")
        mock_openai().chat.completions.create.assert_called_once()

    @patch('openai.OpenAI')
    def test_button_update_description(self, mock_openai):
        mock_openai().chat.completions.create.return_value = self.mock_response

        # Set context and call the method
        with self.env.do_in_onchange():
            self.product.with_context(desc_tone='informal').button_update_description()

        # Assertions
        self.assertEqual(self.product.description_ecommerce, "Generated description")
        mock_openai().chat.completions.create.assert_called_once()

    @patch('openai.OpenAI')
    def test_update_all_description_ecommerce(self, mock_openai):
        mock_openai().chat.completions.create.return_value = self.mock_response

        # Create additional products
        product2 = self.product_template.create({
            'name': 'Test Product 2',
            'image_1920': 'some_image_data',
        })

        # Call the method
        self.product_template.update_all_description_ecommerce('informal')

        # Assertions
        self.assertEqual(self.product.description_ecommerce, "Generated description")
        self.assertEqual(product2.description_ecommerce, "Generated description")
        self.assertEqual(mock_openai().chat.completions.create.call_count, 2)

    def test_update_product_desc_ai_without_image(self):
        # Create a product without an image
        product = self.product_template.create({
            'name': 'No Image Product',
        })

        with self.assertRaises(UserError):
            product.update_product_desc_ai(product.id, 'informal', 'en')

    def test_update_product_desc_ai_without_api_key(self):
        # Ensure API key is not set
        self.env['ir.config_parameter'].set_param('gpt_opd_api_key', '')

        with self.assertRaises(UserError):
            self.product.update_product_desc_ai(self.product.id, 'informal', 'en')

if __name__ == '__main__':
    import unittest
    unittest.main()
