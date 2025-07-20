package com.example.study.common;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.lang.management.ManagementFactory;
import java.lang.management.OperatingSystemMXBean;
import java.nio.file.*;
import java.time.*;
import java.util.*;
import java.util.stream.*;

@RestController
public class AdminHealthController {

    @GetMapping("/admin/sys-health")
    public Map<String, Object> systemHealth() {
        Map<String, Object> result = new HashMap<>();
        OperatingSystemMXBean osBean = ManagementFactory.getOperatingSystemMXBean();
        Runtime runtime = Runtime.getRuntime();

        // CPU, 메모리
        result.put("cpu_load", osBean.getSystemLoadAverage());
        result.put("memory", Map.of(
                "total", runtime.totalMemory(),
                "free", runtime.freeMemory(),
                "used", runtime.totalMemory() - runtime.freeMemory()
        ));

        // Uptime
        long uptimeMillis = ManagementFactory.getRuntimeMXBean().getUptime();
        result.put("uptime", uptimeMillis / 1000 + "s");

        // 최근 30분 에러로그 (예: logs/app.log)
        List<String> errorLogs = new ArrayList<>();
        try {
            Path logPath = Paths.get("logs/app.log"); // 로그 경로에 맞게 수정
            if (Files.exists(logPath)) {
                Instant cutoff = Instant.now().minus(Duration.ofMinutes(30));
                errorLogs = Files.lines(logPath)
                        .filter(line -> line.contains("ERROR"))
                        .filter(line -> {
                            try {
                                String ts = line.substring(0, 19);
                                LocalDateTime logTime = LocalDateTime.parse(ts, java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
                                return logTime.atZone(ZoneId.systemDefault()).toInstant().isAfter(cutoff);
                            } catch (Exception e) { return false; }
                        })
                        .collect(Collectors.toList());
            }
        } catch (Exception e) {
            errorLogs.add("로그 파싱 오류: " + e.getMessage());
        }
        result.put("recent_errors", errorLogs);

        result.put("timestamp", Instant.now().toString());
        return result;
    }
} 