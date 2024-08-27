package com.example.study.board.reply;

import com.example.study.board.Board;
import com.example.study.board.BoardRepository;
import com.example.study.board.BoardService;
import com.example.study.user.User;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ReplyService {

    private final ReplyRepository replyRepository;
    private final BoardRepository boardRepository;
    public List<Reply> cerateReply(ReplyDto replyDto, User user, Long boardId) {
        Board board = boardRepository.findById(boardId).orElseThrow();
        Reply reply = Reply.builder()
                .board(board)
                .user(user)
                .content(replyDto.getContent())
                .build();
        Reply savedReply = replyRepository.save(reply);

        List<Reply> replyList = board.getReplyList();

        return replyList;
    }
}
