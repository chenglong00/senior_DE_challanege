FROM postgres:alpine

ENV POSTGRES_USER user
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB ecommerce

COPY sql_scripts/init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
