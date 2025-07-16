package com.example.study.board.reply;

import com.example.study.board.Board;
import com.example.study.board.BoardRepository;
import com.example.study.board.BoardService;
import com.example.study.user.User;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import com.example.study.common.ServiceUtil;
import com.example.study.common.exception.DomainException;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ReplyService {

    private final ReplyRepository replyRepository;
    private final BoardRepository boardRepository;
    public List<Reply> cerateReply(ReplyDto replyDto, User user, Long boardId) {
        Board board = ServiceUtil.findByIdOrThrow(boardRepository, boardId, DomainException.notFindRow(boardId));
        Reply reply = Reply.builder()
                .board(board)
                .user(user)
                .content(replyDto.getContent())
                .build();
        Reply savedReply = replyRepository.save(reply);

        List<Reply> replyList = board.getReplyList();

        return replyList;
    }

    public Reply getReply(Long replyId) {
        return ServiceUtil.findByIdOrThrow(replyRepository, replyId, DomainException.notFindRow(replyId));
    }

    public void updateReply(Long replyId, ReplyDto replyDto) {
        Reply reply = ServiceUtil.findByIdOrThrow(replyRepository, replyId, DomainException.notFindRow(replyId));
        reply.updateReply(replyDto.getContent());
    }

    public List<Reply> getReplyList(Long boardId) {
        Board board = ServiceUtil.findByIdOrThrow(boardRepository, boardId, DomainException.notFindRow(boardId));
        return board.getReplyList();
    }

    public void deleteReply(Long replyId) {
        Reply reply = ServiceUtil.findByIdOrThrow(replyRepository, replyId, DomainException.notFindRow(replyId));
        replyRepository.delete(reply);
    }
}
