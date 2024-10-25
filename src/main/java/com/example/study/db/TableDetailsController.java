package com.example.study.db;

import com.example.study.db.DatabaseMetadataService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class TableDetailsController {

    private final DatabaseMetadataService metadataService;

    public TableDetailsController(DatabaseMetadataService metadataService) {
        this.metadataService = metadataService;
    }

    @GetMapping("/tables")
    public List<Map<String, Object>> getTableDetails() {
        return metadataService.getTableDetails();
    }
}