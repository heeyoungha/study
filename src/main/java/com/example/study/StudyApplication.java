package com.example.study;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.SQLException;

@SpringBootApplication
@EnableJpaAuditing
@EnableTransactionManagement
public class StudyApplication {

    private static final Logger logger = LoggerFactory.getLogger(StudyApplication.class);

    public static void main(String[] args) {

        ConfigurableApplicationContext context = SpringApplication.run(StudyApplication.class, args);
        DataSource dataSource = context.getBean(DataSource.class);
        try (Connection conn = dataSource.getConnection()) {
            logger.info("Connected to database: " + conn.getMetaData().getURL());
        } catch (SQLException e) {
            logger.error("Database connection failed", e);
        }
    }

}
