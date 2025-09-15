{
    'name': 'Product AutoDescriber AI',
    'version': '1.0.1',
    'license': 'LGPL-3',
    'category': 'Sales/Products',
    'summary': 'Automatically generate product descriptions using AI based on product images.',
    'description': """
Product AutoDescriber AI leverages the power of OpenAI's ChatGPT to automatically generate
unique and engaging descriptions for your products based on their images.

**Key Features:**
- Automatically generates product descriptions using AI.
- Supports multiple tones and languages to tailor the content to your brand's voice.
- Integrates seamlessly with your existing product templates in Odoo.

**Requirements:**
To use this module, an **OpenAI API key** is required.

**Configuration:**
Go to Settings → Parameters → System Parameters and add:
- Key: gpt_opd_api_key
- Value: <Your OpenAI API Key>
""",
    'sequence': 10,
    'author': 'Wolfinne IT',
    'maintainer': 'Bojan Nisevic',
    'website': 'https://wolfinne.com',
    'support': 'bojan@wolfinne.com',
    'depends': ['website_sale'],
    'images': ['static/description/thumbnail.png'],
    'external_dependencies': {
        'python': ['openai'],
    },
    'data': [
        'views/product_views.xml',
    ],
    'assets': {
        'web_editor.backend_assets_wysiwyg': [
            'prod_desc_ai/static/src/js/desc_ai_wysiwyg.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
