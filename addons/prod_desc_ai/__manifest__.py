{
    'name': 'Product Descriptor AI',
    'version': '0.0.1',
    'category': 'Website/Website',
    'summary': 'This module provides AI generated product descriptions',
    'sequence': 10,
    'author': 'Bojan Nisevic',
    'maintainer': 'Bojan Nisevic',
    'website': 'https://boyan.pro',
    'depends': ['website_sale'],
    'data': [
        # 'views/product_template_views.xml',
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
