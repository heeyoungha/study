package com.example.study.board.reply;

import com.example.study.user.User;
import com.example.study.user.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

import java.util.List;

@RestController
@RequestMapping("/api/board/{boardId}/reply")
@RequiredArgsConstructor
public class ReplyApiController {

    private final ReplyService replyService;
    private final UserRepository userRepository;

    @PostMapping
    public ResponseEntity<List<Reply>> createReply(@PathVariable("boardId") Long boardId,
                                                   @RequestBody ReplyDto replyDto){
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        String username = authentication.getName();
        
        User user = userRepository.findByUsername(username);
        if (user == null) {
            return ResponseEntity.status(401).build();
        }
        
        List<Reply> replyList = replyService.cerateReply(replyDto, user, boardId);
        return ResponseEntity.ok(replyList);
    }
}
