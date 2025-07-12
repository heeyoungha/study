FROM openjdk:17-jdk-slim
COPY build/libs/app.jar app.jar
COPY start.sh /start.sh
ENV TZ=Asia/Seoul
RUN chmod +x /start.sh
ENTRYPOINT ["sh", "/start.sh"]