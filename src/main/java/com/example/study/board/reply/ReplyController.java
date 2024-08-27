package com.example.study.board.reply;

import com.example.study.user.User;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/v1/api/board/{boardId}/reply")
@RequiredArgsConstructor
public class ReplyController {

    private final ReplyService replyService;

    @PostMapping
    public ResponseEntity<List<Reply>> createReply(@PathVariable("boardId") Long boardId,
                                                   @RequestBody ReplyDto replyDto,
                                                   @SessionAttribute(name = "user", required = false) User user){
        List<Reply> replyList = replyService.cerateReply(replyDto, user, boardId);
        return ResponseEntity.ok(replyList);
    }
}
