#!/bin/bash
# SHOWCASE.md 파일들을 읽어 슬라이드 HTML을 빌드합니다.
#
# 사용:
#   bash scripts/build_slides.sh          ← 초안 생성 (generate_slides.py + Marp)
#   bash scripts/build_slides.sh --html-only ← HTML만 재빌드 (수정 반영용, Marp만 실행)

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLIDES_DIR="$REPO_ROOT/slides"
MARP_NODE="/opt/homebrew/opt/node@22/bin/node"
MARP_CLI="/opt/homebrew/lib/node_modules/@marp-team/marp-cli/marp-cli.js"

if [ "$1" != "--html-only" ]; then
  echo "① SHOWCASE.md → slides/showcase.md 생성 중..."
  python3 "$REPO_ROOT/scripts/generate_slides.py"
else
  echo "① generate_slides.py 건너뜀 (--html-only 모드)"
fi

echo "② Marp CLI → slides/showcase.html 빌드 중..."
"$MARP_NODE" "$MARP_CLI" \
  "$SLIDES_DIR/showcase.md" \
  --html \
  --allow-local-files \
  -o "$SLIDES_DIR/showcase.html"

echo ""
echo "완료! 빌드된 파일: slides/showcase.html"
echo "GitHub Pages 링크: https://arin-ship-it.github.io/lk-ai-camp2-biz-showcase/slides/showcase.html"
