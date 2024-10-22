package com.example.study.project;

import com.example.study.common.BaseEntity;
import com.example.study.projectUser.ProjectUser;
import jakarta.persistence.*;
import lombok.Getter;
import org.hibernate.annotations.SQLRestriction;

@Entity
@Getter
@Table(name = "project")
@SQLRestriction("status <> 'DELETED'")
public class Project extends BaseEntity {

    @Id @GeneratedValue
    private Long id;

    private String title;

    private String startDate;

    @ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "project_user_id")
    private ProjectUser projectUser;

    public static Project of(String title, String startDate){
        Project project = new Project();
        project.title = title;
        project.startDate = startDate;
        return project;
    }

    public void updateProject(String title, String startDate){
        this.title = title;
        this.startDate = startDate;
    }

}
