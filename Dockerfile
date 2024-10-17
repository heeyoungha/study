FROM openjdk:17-jdk-slim
COPY build/libs/app.jar app.jar
ENV TZ=Asia/Seoul
ENTRYPOINT ["java", "-jar", "./app.jar"]