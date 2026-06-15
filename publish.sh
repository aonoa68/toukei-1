#!/usr/bin/env bash
# ソースをmainにpush → mkdocs gh-deploy で公開するラッパー。
#
# 使い方:
#   ./publish.sh            # git push → gh-deploy
#   ./publish.sh --no-push  # git push をスキップして gh-deploy のみ

set -euo pipefail
cd "$(dirname "$0")"

echo "▶ 1/2 ソースを GitHub(main) にバックアップ push"
if [[ "${1:-}" == "--no-push" ]]; then
  echo "   （--no-push 指定のためスキップ）"
elif [[ -n "$(git status --porcelain)" ]]; then
  echo "   未コミットの変更があります。コミットしてから実行してください："
  git status --short
  exit 1
else
  git push origin main
fi

echo ""
echo "▶ 2/2 公開（mkdocs gh-deploy → gh-pages へ反映）"
mkdocs gh-deploy --message "publish.sh による公開"

echo ""
echo "✅ 公開完了：https://aonoa68.github.io/toukei-1/"
echo "   （CDN反映に1〜2分かかる場合があります。⌘+Shift+R で再読み込み）"
