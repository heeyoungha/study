package com.example.study.projectUser;

import com.example.study.BaseEntity;
import com.example.study.project.Project;
import com.example.study.user.User;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.DialectOverride;
import org.hibernate.annotations.SQLRestriction;
import org.hibernate.annotations.Where;

import java.util.ArrayList;
import java.util.List;

@Getter
@NoArgsConstructor
@Entity
@Table(name = "project_user")
@SQLRestriction("status <> 'DELETED'")
public class ProjectUser extends BaseEntity {

    @Id @GeneratedValue
    private Long id;

    private String role;
    private String status;
    private String startDate;
    private String endDate;
    private String memo;
    private String permission;

    @OneToMany(mappedBy = "projectUser", cascade = CascadeType.ALL)
    private List<Project> projects = new ArrayList<>();

    @OneToMany(mappedBy = "projectUser", cascade = CascadeType.ALL)
    private List<User> users = new ArrayList<>();



}
