package com.example.study;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.SQLException;

@SpringBootApplication
@EntityScan(basePackages = "com.example")
public class StudyApplication {

    private static final Logger logger = LoggerFactory.getLogger(StudyApplication.class);

    public static void main(String[] args) {

        // 환경변수 디버깅
        String debug = System.getenv("DEBUG");
        if ("true".equals(debug)) {
            logger.info("=== Environment Variables Debug ===");
            logger.info("GOOGLE_CLIENT_ID: " + System.getenv("GOOGLE_CLIENT_ID"));
            logger.info("GOOGLE_CLIENT_SECRET: " + (System.getenv("GOOGLE_CLIENT_SECRET") != null ? "SET" : "NOT SET"));
            logger.info("SPRING_PROFILES_ACTIVE: " + System.getenv("SPRING_PROFILES_ACTIVE"));
            logger.info("KAKAO_REST_API_KEY: " + System.getenv("KAKAO_REST_API_KEY"));
            logger.info("=== End Debug ===");
        }

        ConfigurableApplicationContext context = SpringApplication.run(StudyApplication.class, args);
        DataSource dataSource = context.getBean(DataSource.class);
        try (Connection conn = dataSource.getConnection()) {
            logger.info("Connected to database: " + conn.getMetaData().getURL());
        } catch (SQLException e) {
            logger.error("Database connection failed", e);
        }
    }

}
