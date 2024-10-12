package com.example.study.board;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("v1/api/board")
@RequiredArgsConstructor
public class BoardApiController {
    private final BoardService boardService;

    @GetMapping
    public ResponseEntity<Page<BoardDto>> list(
            @PageableDefault(page = 0, size = 10, sort = "id", direction = Sort.Direction.DESC)
            Pageable pageable,
            @RequestParam String searchTitle
    ) {
        Page<BoardDto> boardDtoPage = boardService.boardSearchList(searchTitle, pageable);
        if(boardDtoPage.isEmpty()) {
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.ok(boardDtoPage);
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
