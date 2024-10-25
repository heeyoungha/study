package com.example.study.db;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.sql.DataSource;
import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class DatabaseMetadataService {

    private final JdbcTemplate jdbcTemplate;

    public DatabaseMetadataService(DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
    }

    public List<Map<String, Object>> getTableDetails() {
        List<Map<String, Object>> tables = new ArrayList<>();

        try (Connection connection = jdbcTemplate.getDataSource().getConnection()) {
            DatabaseMetaData metaData = connection.getMetaData();

            // Specify the database name (schema) you want to filter
            String databaseName = "study-version";

            // Use the specified database
            connection.setCatalog(databaseName);

            // Fetch table details
            try (Statement statement = connection.createStatement();
                 ResultSet tablesResultSet = statement.executeQuery("SHOW TABLES")) {

                while (tablesResultSet.next()) {
                    String tableName = tablesResultSet.getString(1);

                    Map<String, Object> tableDetails = new HashMap<>();
                    tableDetails.put("tableName", tableName);

                    // Fetch column details
                    List<Map<String, String>> columns = new ArrayList<>();
                    try (ResultSet columnsResultSet = metaData.getColumns(null, databaseName, tableName, null)) {
                        while (columnsResultSet.next()) {
                            Map<String, String> columnDetails = new HashMap<>();
                            columnDetails.put("name", columnsResultSet.getString("COLUMN_NAME"));
                            columnDetails.put("type", columnsResultSet.getString("TYPE_NAME"));
                            columnDetails.put("size", columnsResultSet.getString("COLUMN_SIZE"));
                            columnDetails.put("nullable", columnsResultSet.getString("IS_NULLABLE"));
                            columns.add(columnDetails);
                        }
                    }
                    tableDetails.put("columns", columns);

                    // Fetch foreign key details
                    List<Map<String, String>> foreignKeys = new ArrayList<>();
                    try (ResultSet foreignKeysResultSet = metaData.getImportedKeys(null, databaseName, tableName)) {
                        while (foreignKeysResultSet.next()) {
                            Map<String, String> fkDetails = new HashMap<>();
                            fkDetails.put("columnName", foreignKeysResultSet.getString("FKCOLUMN_NAME"));
                            fkDetails.put("referencedTable", foreignKeysResultSet.getString("PKTABLE_NAME"));
                            fkDetails.put("referencedColumn", foreignKeysResultSet.getString("PKCOLUMN_NAME"));
                            foreignKeys.add(fkDetails);
                        }
                    }
                    tableDetails.put("foreignKeys", foreignKeys);

                    tables.add(tableDetails);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return tables;
    }
}