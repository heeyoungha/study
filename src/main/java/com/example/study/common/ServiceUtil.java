package com.example.study.common;

import org.springframework.data.jpa.repository.JpaRepository;

public class ServiceUtil {
    public static <T, ID> T findByIdOrThrow(JpaRepository<T, ID> repository, ID id, RuntimeException exception) {
        return repository.findById(id).orElseThrow(() -> exception);
    }
} 