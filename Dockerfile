FROM odoo:18.0-20250807
USER root
RUN apt-get update && \
    apt-get install -y python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/odoo-venv --system-site-packages \
 && /opt/odoo-venv/bin/pip install --upgrade pip
ENV PATH="/opt/odoo-venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/odoo-venv"
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN chown -R odoo:odoo /var/lib/odoo
COPY ./addons /mnt/custom_addons
USER odoo
CMD ["/opt/odoo-venv/bin/python", "/usr/bin/odoo", "-c", "/etc/odoo/odoo.conf", "--dev", "all"]

