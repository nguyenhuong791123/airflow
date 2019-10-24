FROM mysql

# RUN mkdir /etc/certs
# ADD ./db/ca-key.pem /etc/certs
# ADD ./db/ca.pem /etc/certs
# ADD ./db/client-cert.pem /etc/certs
# ADD ./db/client-key.pem /etc/certs
# ADD ./db/server-cert.pem /etc/certs
# ADD ./db/server-key.pem /etc/certs

ADD ./my.cnf /etc/mysql/conf.d/my.cnf
RUN chmod 644 /etc/mysql/conf.d/my.cnf

RUN mkdir /var/log/mysql
RUN chmod 0750 /var/log/mysql
# RUN chmod 0640 /var/log/mysql/mysql-error.log
# RUN chmod 0640 /var/log/mysql/mysql-slow.log
# RUN chmod 0640 /var/log/mysql/mysql-query.log