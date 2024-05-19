/** @odoo-module **/

// import { loadBundle } from "@web/core/assets";
import { Wysiwyg } from "@web_editor/js/wysiwyg/wysiwyg";
// import { closestElement } from "@web_editor/js/editor/odoo-editor/src/OdooEditor";
import "@web_editor/js/wysiwyg/wysiwyg_iframe";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

// export class DescAIWysiwyg extends Wysiwyg {
patch(Wysiwyg.prototype, {

    _getPowerboxOptions() {
        const options = super._getPowerboxOptions();

        if (this.websiteService !== undefined) {

            const mainObject = this.websiteService.currentWebsite.metadata.mainObject;
            const lang = this.options.context.lang;

            if (mainObject.model === 'product.template') {
                options.categories.push({
                    name: _t('Description AI'),
                    priority: 300,
                });
                options.commands.push({
                    name: _t('Cute'),
                    category: _t('Description AI'),
                    description: _t("Generates a cute description for the product."),
                    fontawesome: 'fa-magic',
                    priority: 3,
                    callback: () => {
                        this._updateProductDescription(mainObject, 'cute', lang);
                    },
                });
                options.commands.push({
                    name: _t('Funny'),
                    category: _t('Description AI'),
                    description: _t("Generates a funny description for the product."),
                    fontawesome: 'fa-magic',
                    priority: 2,
                    callback: () => {
                        this._updateProductDescription(mainObject, 'funny', lang);
                    },
                });
                options.commands.push({
                    name: _t('Feminine'),
                    category: _t('Description AI'),
                    description: _t("Generates an feminine description for the product."),
                    fontawesome: 'fa-magic',
                    priority: 1,
                    callback: () => {
                        this._updateProductDescription(mainObject, 'official', lang);
                    },
                });
                options.commands.push({
                    name: _t('Official'),
                    category: _t('Description AI'),
                    description: _t("Generates an official description for the product."),
                    fontawesome: 'fa-magic',
                    priority: 1,
                    callback: () => {
                        this._updateProductDescription(mainObject, 'official', lang);
                    },
                });
            }
        }
        return options;
    },

    async _updateProductDescription(product, type, lang) {

        console.log(`Updating product description: ${product.id} - ${type} - ${lang}`);
        console.log(this);

        await this.orm.call('product.template', 'update_product_desc_ai', [[], product.id, type, lang]).then((result) => {
            console.log(result);
            this.props.reloadCallback();
        });
    },
});
