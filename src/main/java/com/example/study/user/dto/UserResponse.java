package com.example.study.user.dto;

import com.example.study.user.User;
import lombok.Data;

@Data
public class UserResponse {

    private Long id;
    private String email;
    private String username;
    private String pw;

    public UserResponse(User user){
        this.id = user.getId();
        this.email = user.getEmail();
        this.username = user.getUsername();
        this.pw = user.getPw();
    }
}
