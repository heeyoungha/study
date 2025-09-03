package com.example.study.board.reply;

import com.example.study.board.Board;
import com.example.study.user.User;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
public class ReplyDto {

    private Long replyId;

    private Long boardId;

    private String content;
    private String username;
    private LocalDateTime createdDate;
    private LocalDateTime modifiedDate;

    public Reply toEntity(Board board, User user){
        Reply build = Reply.builder()
                .content(this.content)
                .user(user)
                .board(board)
                .build();
        return build;
    }

    @Builder
    public ReplyDto(Reply reply){
        this.replyId = reply.getId();
        this.content = reply.getContent();
        this.createdDate = reply.getCreatedDate();
        this.modifiedDate = reply.getModifiedDate();
    }

}