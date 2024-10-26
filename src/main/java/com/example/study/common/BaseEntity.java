package com.example.study.common;


import jakarta.persistence.Column;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.MappedSuperclass;
import lombok.Getter;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity {

    @CreatedDate
    @Column(nullable = true, updatable = false)
    private LocalDateTime createdDate;

    @LastModifiedDate
    @Column(nullable = true)
    private LocalDateTime modifiedDate;

    private Boolean isDeleted = false;

    public void delete(){
        this.isDeleted = true;
    }
}
