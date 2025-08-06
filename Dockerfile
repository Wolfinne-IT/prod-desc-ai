FROM odoo:18

USER root

RUN apt-get update && \
    apt-get install -y python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/odoo-venv \
 && /opt/odoo-venv/bin/pip install --upgrade pip

ENV PATH="/opt/odoo-venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/odoo-venv"

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./addons /mnt/custom_addons
USER odoo
CMD ["odoo", "-c", "/etc/odoo/odoo.conf", "--dev", "all"]
