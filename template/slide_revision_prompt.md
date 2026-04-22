# 슬라이드 수정 요청 프롬프트

## 진행 절차

### 1. 영문 이름 확인
발표자의 영문 이름이 무엇인지 먼저 물어본다.
(예: Arin, Evan 등 submissions/ 폴더명과 동일한 이름 — 대소문자 구분 없음)

### 2. 섹션 존재 확인
`slides/showcase.md` 파일에서
`<!-- === 발표자: [영문이름] === -->` 마커를 대소문자 구분 없이 검색한다.
- 없으면 "해당 발표자 섹션을 찾을 수 없습니다. 이름을 다시 확인해주세요."라고 알리고 중단한다.

### 3. 수정 내용 확인
어떤 내용을 수정하고 싶은지 물어본다.

### 4. 수정 실행
`<!-- === 발표자: [영문이름] === -->` ~
`<!-- === /발표자: [영문이름] === -->` 구간 **안의 내용만** 수정한다.
이 구간 밖은 절대 수정하지 않는다.
- 슬라이드 추가·삭제도 이 구간 안에서 가능하다.
- 필요하면 `submissions/[영문이름]/` 하위 파일을 읽어서 내용을 참조해도 된다.
  그 외 다른 파일은 읽지 않는다.

### 5. 커밋 전 최신화 (동시 수정 충돌 방지)
수정 완료 후 커밋 전에 origin/main을 rebase로 반영한다.
```
git fetch origin
git rebase origin/main
```
- rebase 충돌 발생 시: 본인 섹션 마커 안의 내용을 기준으로 해결한다.
- push 후 거절(rejected)되면: git fetch → git rebase origin/main → push 재시도한다.

### 6. 확인 후 커밋
a. 변경된 내용(diff)을 보여주고 최종 확인을 받는다.
b. 확인되면 `bash scripts/build_slides.sh --html-only` 실행해서 HTML 재빌드한다.
c. `[영문이름]: 슬라이드 수정` 메시지로 커밋하고 main에 push한다.
d. push 완료 후 슬라이드 링크를 알려준다.
   https://arin-ship-it.github.io/lk-ai-camp2-biz-showcase/slides/showcase.html
