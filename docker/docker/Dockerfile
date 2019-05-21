FROM alpine:3.7
MAINTAINER hnguyen <nguyenhuong791123@gmail.com>

##############################################################################
# timezone: tokyo
##############################################################################
RUN apk --update add tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*
ENV LANG=C.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

##############################################################################
# glibc
##############################################################################
# Here we install GNU libc (aka glibc) and set C.UTF-8 locale as default.
RUN ALPINE_GLIBC_PACKAGE_VERSION="2.23-r1" && \
    ALPINE_GLIBC_BASE_URL="https://github.com/andyshinn/alpine-pkg-glibc/releases/download" && \
    ALPINE_GLIBC_BASE_PACKAGE_FILENAME="glibc-$ALPINE_GLIBC_PACKAGE_VERSION.apk" && \
    ALPINE_GLIBC_BIN_PACKAGE_FILENAME="glibc-bin-$ALPINE_GLIBC_PACKAGE_VERSION.apk" && \
    ALPINE_GLIBC_I18N_PACKAGE_FILENAME="glibc-i18n-$ALPINE_GLIBC_PACKAGE_VERSION.apk" && \
    # Install wget and ca-certs
    apk add --no-cache --virtual=build-dependencies wget ca-certificates && \
    # Download glibc packages
    wget \
        "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE_VERSION/$ALPINE_GLIBC_BASE_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE_VERSION/$ALPINE_GLIBC_BIN_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE_VERSION/$ALPINE_GLIBC_I18N_PACKAGE_FILENAME" && \
    # Install glibc packages
    apk add --no-cache --allow-untrusted \
        "$ALPINE_GLIBC_BASE_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BIN_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_I18N_PACKAGE_FILENAME" && \
    # Force C.UTF-8 as default locale
    /usr/glibc-compat/bin/localedef --force --inputfile POSIX --charmap UTF-8 C.UTF-8 || true && \
    echo "export LANG=C.UTF-8" > /etc/profile.d/locale.sh && \
    # Cleanup
    apk del glibc-i18n && \
    apk del build-dependencies && \
    # Remove downloaded packages
    rm \
        "$ALPINE_GLIBC_BASE_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BIN_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_I18N_PACKAGE_FILENAME"

##############################################################################
# miniconda
##############################################################################
RUN apk --update add --no-cache --virtual .build-deps mariadb-dev ca-certificates wget && \
    update-ca-certificates 2>/dev/null || true
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    /bin/ash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    echo 'export PATH=/opt/conda/bin:$PATH' >> /etc/profile.d/conda.sh
ENV PATH /opt/conda/bin:$PATH
RUN pip install --upgrade --default-timeout 6000 pip

# install airflow
RUN apk add --virtual .runtime-deps mariadb-client-libs build-base linux-headers bash
ENV AIRFLOW_HOME /airflow
ENV C_FORCE_ROOT true  # run airflow worker by root
RUN pip install --default-timeout 6000 "apache-airflow[celery, mysql, password, slack, s3, redis]"
RUN pip install --default-timeout 6000 boto3
RUN apk del .build-deps mariadb-dev build-base

ADD airflow.cfg /root/airflow.cfg
ADD entrypoint.sh /root/entrypoint.sh
ADD entrypoint_webserver.sh /root/entrypoint_webserver.sh
ADD entrypoint_worker.sh /root/entrypoint_worker.sh
ADD entrypoint_flower.sh /root/entrypoint_flower.sh
RUN chmod +x /root/entrypoint.sh
RUN chmod +x /root/entrypoint_webserver.sh
RUN chmod +x /root/entrypoint_worker.sh
RUN chmod +x /root/entrypoint_flower.sh
RUN mkdir -p /airflow/config && touch /airflow/config/__init__.py
ADD log_config.py /airflow/config/log_config.py
ENV PYTHONPATH /airflow/config/

VOLUME ["/airflow/dags", "/airflow/logs", "/airflow/plugins"]
EXPOSE 8080 5555 8793
WORKDIR ${AIRFLOW_HOME}

ENTRYPOINT ["/root/entrypoint.sh"]
