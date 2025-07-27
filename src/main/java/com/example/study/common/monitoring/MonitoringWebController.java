package com.example.study.common.monitoring;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MonitoringWebController {

    @GetMapping("/unified-monitoring")
    public String getUnifiedMonitoring() {
        return "monitoring/unified-monitoring";
    }
} 