package com.example.study.board;

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
@RequestMapping("v1")
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

    @PostMapping
    public ResponseEntity<BoardDto> createBoard(@RequestBody BoardDto dto){
        BoardDto boardDto = boardService.saveBoard(dto);
        return ResponseEntity.ok(boardDto);
    }

    @GetMapping("/{boardId}")
    public ResponseEntity<BoardDto> readBoard(@PathVariable("boardId") Long id){
        BoardDto boardDto = boardService.getBoard(id);
        return ResponseEntity.ok(boardDto);
    }

    @PutMapping("/{boardId}")
    public ResponseEntity<BoardDto> updateBoard(@PathVariable("boardId") Long id, @RequestBody BoardDto dto){
        BoardDto boardDto = boardService.updateBoard(id, dto);
        return ResponseEntity.ok(boardDto);
    }


}
