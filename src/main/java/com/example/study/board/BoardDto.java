package com.example.study.board;

import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
public class BoardDto {

    private Long id;
    private String writer;
    private String title;
    private String content;
    private LocalDateTime createdDate;
    private LocalDateTime modifiedDate;

    @Builder
    public BoardDto(Board board){
        this.id = board.getId();
        this.writer = board.getWriter();
        this.content = board.getContent();
        this.createdDate = board.getCreatedDate();
    }
}
