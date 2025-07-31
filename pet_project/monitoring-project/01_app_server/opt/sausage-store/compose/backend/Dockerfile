FROM openjdk:16-jdk-alpine

ENV REPORT_PATH=/var/sausage-store/reports
ENV LOG_PATH=/var/sausage-store/logs

WORKDIR /app

COPY ./sausage-store-0.0.1-SNAPSHOT.jar /app/sausage-store.jar
COPY jmx-exporter/jmx_prometheus_javaagent-0.20.0.jar /app/
COPY jmx-exporter/config.yml /app/config.yml

VOLUME ["/var/sausage-store/reports", "/var/sausage-store/logs"]

EXPOSE 8080

CMD ["java", "-javaagent:/app/jmx_prometheus_javaagent-0.20.0.jar=9404:/app/config.yml", "-jar", "/app/sausage-store.jar"]
