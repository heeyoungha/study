package com.example.study.user;

인import com.example.study.common.BaseEntity;
import com.example.study.projectUser.ProjectUser;
import com.example.study.user.dto.UserRequest;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.SQLRestriction;

@Entity
@Table(name = "user")
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@SQLRestriction("status <> 'DELETED'")
public class User extends BaseEntity {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String username;
    private String email;
    private String pw;

    @ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "project_user_id")
    private ProjectUser projectUser;

    public void updateUser(UserRequest.UpdateUserRequest request) {
        this.pw = request.getPw();
        this.email = request.getEmail();
        this.username = request.getUsername();
    }
}
