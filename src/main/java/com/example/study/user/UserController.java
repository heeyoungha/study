package com.example.study.user;

import com.example.study.user.dto.UserRequest;
import com.example.study.user.dto.UserResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/v1/api/user")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @PostMapping
    public ResponseEntity<UserResponse> createUser(@RequestBody UserRequest.CreateUserRequest request){
        UserResponse response = userService.createUser(request);
        return ResponseEntity.ok(response);
    }

    @GetMapping
    public ResponseEntity<List<UserResponse>> readUserList() {
        List<UserResponse> users = userService.readUserList();
        return ResponseEntity.ok(users);
    }

    @PatchMapping("/{id}")
    public ResponseEntity<Void> updateUser(Long id, @RequestBody UserRequest.UpdateUserRequest request){
        userService.updateUser(id, request);
        return ResponseEntity.status(HttpStatus.OK).build();
    }
}
