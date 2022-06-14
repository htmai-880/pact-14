FROM nginx

LABEL name="s2r-nginx" \
      version="0.1"

EXPOSE 80

RUN rm /etc/nginx/conf.d/default.conf

COPY templates /etc/nginx/templates
