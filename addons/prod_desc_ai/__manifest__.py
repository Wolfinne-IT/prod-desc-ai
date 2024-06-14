{
    'name': 'Product AutoDescriber AI',
    'version': '1.0.1',
    'license': 'LGPL-3',
    'category': 'Sales/Products',
    'summary': 'Automatically generate product descriptions using AI based on product images.',
    "description": """
        Product AutoDescriber AI leverages the power of OpenAI's ChatGPT to automatically generate unique and engaging descriptions for your products based on their images. This module is perfect for e-commerce businesses looking to enhance their product listings with high-quality AI-generated content.
        
        **Key Features:**
        - Automatically generates product descriptions using AI.
        - Supports multiple tones and languages to tailor the content to your brand's voice.
        - Integrates seamlessly with your existing product templates in Odoo.
        
        **Requirements:**
        To use this module, an **OpenAI API key** is required. This key allows the module to interact with OpenAI's services to generate descriptions based on the images of your products.
        
        **Getting an OpenAI API Key:**
        1. Visit OpenAI’s official website and sign up for an account if you do not have one.
        2. Navigate to the API section and apply for access to the API. Depending on your usage, you may need to provide details about your use case.
        3. Once approved, you will receive an API key. This key is essential for the module to function and should be entered in the Odoo configuration panel under the settings specified by this module.
        
        **Configuring the API Key in Odoo:**
        After obtaining the API key, go to Odoo’s Settings → Parameters → System Parameters and add a new parameter:
        - Key: `gpt_opd_api_key`
        - Value: `<Your OpenAI API Key>`
        
        Ensure you replace `<Your OpenAI API Key>` with the actual key provided by OpenAI. This key will be securely stored and used to authenticate requests from your Odoo instance to OpenAI.
        
        **Security Note:**
        Keep your API key confidential to prevent unauthorized usage, which could lead to unexpected charges or data breaches.
        
        With Product AutoDescriber AI, enrich your product presentations and engage your customers like never before. Enhance your online shop's appeal and functionality with cutting-edge AI technology.
        
        This module currently supports Odoo 17. For earlier versions, please contact us for compatibility information.
    """,
    'sequence': 10,
    'author': 'Bojan Nisevic',
    'maintainer': 'Bojan Nisevic',
    'website': 'https://boyan.pro',
    'support': 'bojan@wolfinne.com',
    'depends': ['website_sale'],
    'images': [
        'static/description/thumbnail.png',
    ],
    'external_dependencies': {
        'python': [
            'openai',
        ],
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
