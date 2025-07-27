package com.example.study.project;

import com.example.study.common.BaseEntity;
import com.example.study.projectUser.ProjectUser;
import jakarta.persistence.*;
import lombok.Getter;
import org.hibernate.annotations.SQLRestriction;

@Entity
@Getter
@Table(name = "project")
@SQLRestriction("is_deleted = false")
public class Project extends BaseEntity {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    private String timeZone;
    private String targetMonths;
    private String quarters;
    private String place;
    private String status;

    @ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "project_user_id")
    private ProjectUser projectUser;

    public static Project of(String title, String timeZone, String targetMonths, String quarters, String place, String status){
        Project project = new Project();
        project.title = title;
        project.timeZone = timeZone;
        project.targetMonths = targetMonths;
        project.quarters = quarters;
        project.place = place;
        project.status = status;
        return project;
    }

    public void updateProject(String title, String timeZone, String targetMonths, String quarters){
        this.title = title;
        this.timeZone = timeZone;
        this.targetMonths = targetMonths;
        this.quarters = quarters;
    }

}
