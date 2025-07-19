package com.example.study.board.reply;

import com.example.study.user.User;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/board/{boardId}/reply")
@RequiredArgsConstructor
public class ReplyWebController {
    private final ReplyService replyService;

    // 댓글 목록 조회 (게시글 상세에서 사용)
    @GetMapping
    public String listReplies(@PathVariable Long boardId, Model model) {
        List<Reply> replies = replyService.getReplyList(boardId);
        model.addAttribute("replies", replies);
        model.addAttribute("boardId", boardId);
        return "board/reply-list";
    }

    // 댓글 등록 폼
    @GetMapping("/new")
    public String createReplyForm(@PathVariable Long boardId, Model model) {
        model.addAttribute("replyDto", new ReplyDto());
        model.addAttribute("boardId", boardId);
        return "board/reply-form";
    }

    // 댓글 등록 처리
    @PostMapping
    public String createReply(@PathVariable Long boardId, @ModelAttribute ReplyDto replyDto, @SessionAttribute(name = "user", required = false) User user) {
        replyService.cerateReply(replyDto, user, boardId);
        return "redirect:/board/" + boardId;
    }

    // 댓글 수정 폼
    @GetMapping("/{replyId}/edit")
    public String editReplyForm(@PathVariable Long boardId, @PathVariable Long replyId, Model model) {

        Reply reply = replyService.getReply(replyId);
        model.addAttribute("reply", reply);
        model.addAttribute("replyId", replyId);
        model.addAttribute("boardId", boardId);
        return "board/reply-edit-form";
    }

    // 댓글 수정 처리
    @PostMapping("/{replyId}/edit")
    public String editReply(@PathVariable Long boardId, @PathVariable Long replyId, @ModelAttribute ReplyDto replyDto) {

        replyService.updateReply(replyId, replyDto);
        return "redirect:/board/" + boardId;
    }

    // 댓글 삭제 처리
    @DeleteMapping("/{replyId}")
    @ResponseBody
    public String deleteReply(@PathVariable Long boardId, @PathVariable Long replyId) {
        replyService.deleteReply(replyId);
        return "ok";
    }
} 