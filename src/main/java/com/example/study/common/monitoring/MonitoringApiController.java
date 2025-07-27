package com.example.study.common.monitoring;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.time.Instant;
import java.util.*;
import java.lang.management.ManagementFactory;
import java.lang.management.OperatingSystemMXBean;
import java.lang.management.ThreadMXBean;

@RestController
@RequestMapping("/api/monitoring")
public class MonitoringApiController {
    
    private static final Logger log = LoggerFactory.getLogger(MonitoringApiController.class);
    private static final int MAX_HISTORY_SIZE = 30;
    private static Instant lastHistoryTime = null;

    @GetMapping("/system-health")
    public Map<String, Object> systemHealth() {
        Map<String, Object> result = new HashMap<>();
        
        try {
            // JVM 정보
            Runtime runtime = Runtime.getRuntime();
            long totalMemory = runtime.totalMemory();
            long freeMemory = runtime.freeMemory();
            long usedMemory = totalMemory - freeMemory;
            double memoryUsagePercent = (double) usedMemory / totalMemory * 100;
            
            // CPU 정보
            OperatingSystemMXBean osBean = ManagementFactory.getOperatingSystemMXBean();
            int cpuCores = osBean.getAvailableProcessors();
            double systemLoad = osBean.getSystemLoadAverage();
            double cpuUsagePercent = systemLoad * 100 / cpuCores;
            if (cpuUsagePercent > 100) cpuUsagePercent = 100;
            
            // 스레드 정보
            ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
            int threadCount = threadBean.getThreadCount();
            int peakThreadCount = threadBean.getPeakThreadCount();
            
            // 업타임
            long uptime = ManagementFactory.getRuntimeMXBean().getUptime();
            String uptimeStr = String.format("%dd %dh %dm %ds", 
                uptime / (24 * 60 * 60 * 1000),
                (uptime % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000),
                (uptime % (60 * 60 * 1000)) / (60 * 1000),
                (uptime % (60 * 1000)) / 1000);
            
            // 최근 에러 로그 (간단한 예시)
            List<String> recentErrorBlocks = getRecentErrorBlocks();
            
            // 히스토리 업데이트
            updateHealthHistory(cpuUsagePercent, memoryUsagePercent);
            
            result.put("service_name", "Spring Boot");
            result.put("cpu_percent", cpuUsagePercent);
            result.put("system_cpu_percent", systemLoad * 100);
            result.put("memory", Map.of(
                "process_heap_total", totalMemory,
                "process_heap_used", usedMemory,
                "process_heap_free", freeMemory,
                "process_heap_percent", memoryUsagePercent,
                "system_total", totalMemory,
                "system_used", usedMemory,
                "system_percent", memoryUsagePercent
            ));
            result.put("uptime", uptimeStr);
            result.put("threads", Map.of(
                "current", threadCount,
                "peak", peakThreadCount
            ));
            result.put("recent_error_blocks", recentErrorBlocks);
            result.put("timestamp", Instant.now().toString());
            result.put("history", getHealthHistory());
            
        } catch (Exception e) {
            result.put("error", "시스템 정보 수집 중 오류 발생: " + e.getMessage());
            result.put("timestamp", Instant.now().toString());
        }
        
        return result;
    }

    @GetMapping("/host-health")
    public Map<String, Object> hostHealth() {
        Map<String, Object> result = new HashMap<>();
        
        try {
            // 호스트 시스템 정보
            OperatingSystemMXBean osBean = ManagementFactory.getOperatingSystemMXBean();
            int cpuCores = osBean.getAvailableProcessors();
            
            // 시스템 전체 CPU 사용률
            double systemCpuPercent = osBean.getSystemLoadAverage() * 100 / cpuCores;
            if (systemCpuPercent > 100) systemCpuPercent = 100;
            
            // 시스템 전체 물리 메모리 정보
            com.sun.management.OperatingSystemMXBean sunOsBean = (com.sun.management.OperatingSystemMXBean) osBean;
            long physicalTotal = sunOsBean.getTotalPhysicalMemorySize();
            long physicalFree = sunOsBean.getFreePhysicalMemorySize();
            long physicalUsed = physicalTotal - physicalFree;
            double physicalPercent = (double) physicalUsed / physicalTotal * 100;
            
            // 업타임
            long uptime = ManagementFactory.getRuntimeMXBean().getUptime();
            String uptimeStr = String.format("%dd %dh %dm %ds", 
                uptime / (24 * 60 * 60 * 1000),
                (uptime % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000),
                (uptime % (60 * 60 * 1000)) / (60 * 1000),
                (uptime % (60 * 1000)) / 1000);
            
            result.put("service_name", "Host System");
            result.put("cpu_percent", systemCpuPercent);
            result.put("cpu_cores", cpuCores);
            result.put("memory", Map.of(
                "physical_total", physicalTotal,
                "physical_used", physicalUsed,
                "physical_free", physicalFree,
                "physical_percent", physicalPercent
            ));
            result.put("uptime", uptimeStr);
            result.put("timestamp", Instant.now().toString());
            
        } catch (Exception e) {
            result.put("error", "호스트 정보 수집 중 오류 발생: " + e.getMessage());
            result.put("timestamp", Instant.now().toString());
        }
        
        return result;
    }

    @GetMapping("/test-500")
    public ResponseEntity<Map<String, Object>> test500() {
        Map<String, Object> result = new HashMap<>();
        result.put("error", "테스트용 500 에러");
        result.put("timestamp", Instant.now().toString());
        return ResponseEntity.status(500).body(result);
    }

    // 기존 AdminHealthController의 헬퍼 메서드들
    private static final Queue<Map<String, Object>> HEALTH_HISTORY = new LinkedList<>();

    private void updateHealthHistory(double cpuPercent, double memoryPercent) {
        Instant now = Instant.now();
        
        if (lastHistoryTime == null || now.minusSeconds(30).isAfter(lastHistoryTime)) {
            Map<String, Object> historyEntry = new HashMap<>();
            historyEntry.put("cpu_percent", cpuPercent);
            historyEntry.put("memory_percent", memoryPercent);
            historyEntry.put("timestamp", now.toString());
            
            HEALTH_HISTORY.offer(historyEntry);
            if (HEALTH_HISTORY.size() > MAX_HISTORY_SIZE) {
                HEALTH_HISTORY.poll();
            }
            
            lastHistoryTime = now;
        }
    }

    private List<Map<String, Object>> getHealthHistory() {
        return new ArrayList<>(HEALTH_HISTORY);
    }

    private List<String> getRecentErrorBlocks() {
        // 실제 구현에서는 로그 파일을 읽어서 에러 블록을 파싱
        return new ArrayList<>();
    }
} 