package com.example.study.user;

import com.example.study.common.ServiceUtil;
import com.example.study.common.exception.DomainException;
import com.example.study.user.dto.UserRequest;
import com.example.study.user.dto.UserResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    @Transactional
    public UserResponse createUser(UserRequest.CreateUserRequest request) {
        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .pw(request.getPw())
                .build();
        userRepository.save(user);
        return new UserResponse(user);
    }

    @Transactional
    public List<UserResponse> readUserList() {
        return userRepository.findAll().stream().map(UserResponse::new).collect(Collectors.toList());
    }

    @Transactional
    public UserResponse readUser(Long id) {
        User user = ServiceUtil.findByIdOrThrow(userRepository, id, DomainException.notFindRow(id));
        return new UserResponse(user);
    }

    @Transactional
    public void deleteUser(Long id) {
        User user = ServiceUtil.findByIdOrThrow(userRepository, id, DomainException.notFindRow(id));
        user.delete();
    }

    @Transactional
    public void updateUser(Long id, UserRequest.UpdateUserRequest request) {
        User user = ServiceUtil.findByIdOrThrow(userRepository, id, DomainException.notFindRow(id));
        user.updateUser(request);
    }
}
