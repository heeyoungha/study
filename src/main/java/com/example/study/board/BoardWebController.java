package com.example.study.board;

import com.example.study.board.reply.Reply;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/v1")
@RequiredArgsConstructor
public class BoardWebController {
    private final BoardService boardService;

    @GetMapping(value = {"/boardList", "/"})
    public String list(Model model,
                       @PageableDefault(page = 0, size = 10, sort = "id", direction = Sort.Direction.DESC)
            Pageable pageable,
                       @RequestParam(required = false) String searchTitle
    ) {
        Page<BoardDto> boardDtoPage = boardService.boardSearchList(searchTitle, pageable);

        int nowPage = boardDtoPage.getPageable().getPageNumber() + 1; //pageable에서 넘어온 현재페이지를 가지고올수있다 * 0부터시작하니까 +1
        int startPage = Math.max(nowPage - 4, 1); //매개변수로 들어온 두 값을 비교해서 큰값을 반환
        int endPage = Math.min(nowPage + 5, boardDtoPage.getTotalPages());

        model.addAttribute("boardList" , boardDtoPage);
        model.addAttribute("nowPage", nowPage);
        model.addAttribute("startPage", startPage);
        model.addAttribute("endPage", endPage);

        return "board/getBoardList";
    }

    @GetMapping("/board")
    public String getCreateBoard(){
        return "board/create-board.html";
    }

    @PostMapping("/board")
    public BoardDto createBoard(@RequestBody BoardDto dto){
        return boardService.saveBoard(dto);
    }

    @GetMapping("/board/{boardId}")
    public String readBoard(@PathVariable("boardId") Long id, Model model){
        BoardDto boardDto = boardService.getBoard(id);
        List<Reply> replyList = boardService.getReplyList(id);
        model.addAttribute("boardDto", boardDto);
        model.addAttribute("replyList", replyList);

        return "board/board-detail";
    }

    @GetMapping("/board/edit/{boardId}")
    public String editBoard(@PathVariable("boardId") Long id, Model model){
        BoardDto boardDto = boardService.getBoard(id);
        model.addAttribute("boardDto", boardDto);
        return "board/edit";
    }

    @PutMapping("/board/edit/{boardId}")
    @ResponseBody
    public ResponseEntity<?> updateBoard(@PathVariable("boardId") Long id, @RequestBody BoardDto dto){
        boardService.updateBoard(id, dto);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/board/{id}")
    @ResponseBody
    public ResponseEntity<?> deleteBoard(@PathVariable Long id) {
        boardService.deleteBoard(id);
        return ResponseEntity.ok().build();
    }

}
