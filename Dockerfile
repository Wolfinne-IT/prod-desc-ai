FROM odoo:17
USER root
COPY ./requirements.txt .
RUN pip3 install --timeout=100 -r requirements.txt
COPY ./addons /mnt/custom_addons
USER odoo
CMD ["odoo", "-c", "/etc/odoo/odoo.conf", "--dev", "all"]
