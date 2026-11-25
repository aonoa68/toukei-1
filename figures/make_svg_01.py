# -*- coding: utf-8 -*-
"""第01回ガイダンスの図を作る。出力は figures/out/*.svg（本文に貼るインラインSVG）。

図に書く数値はすべてこのスクリプトで計算する。計算結果は標準出力にも出すので、
本文の数値と図の数値が食い違っていないかを目で確かめられる。
"""
import math
import os
import numpy as np
from svgkit import Svg, RED, INDIGO, TEAL, AMBER

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def save(name, svg):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(svg.render())
    print(f"  -> {p}  ({len(svg.render())} 字)")


# ===== 図1：モンティ・ホール ============================================
def fig_monty():
    s = Svg(720, 352, "mh",
            "モンティ・ホール ―― 最初の1枚で結果は決まっている",
            "縦の幅が確率を表す。最初に当たりを引く確率は3分の1で、このときだけ"
            "「変えない」が当たり、「変える」はハズレになる。最初にハズレを引く確率は"
            "3分の2で、このときは「変えない」がハズレ、「変える」が必ず当たる。"
            "したがって変えないときに当たる確率は3分の1、変えるときは3分の2である。")
    x0, y0, H = 176, 74, 198
    cw, gap = 248, 16
    cols = [("変えない", x0), ("変える", x0 + cw + gap)]
    h1, h2 = H / 3, H * 2 / 3

    s.text(0, 30, "最初の1枚を選んだ時点で、結果は決まっている", 13.5, bold=True)
    for name, x in cols:
        s.text(x + cw / 2, 62, name, 13, anchor="middle", bold=True)
    # 行ラベル
    s.text(166, y0 + h1 / 2 - 6, "最初が当たり", 12, anchor="end", bold=True)
    s.text(166, y0 + h1 / 2 + 11, "確率 1/3", 12, anchor="end", op=0.75)
    s.text(166, y0 + h1 + h2 / 2 - 6, "最初がハズレ", 12, anchor="end", bold=True)
    s.text(166, y0 + h1 + h2 / 2 + 11, "確率 2/3", 12, anchor="end", op=0.75)
    # セル（当たり=緑、ハズレ=赤）
    cells = [(0, 0, True), (1, 0, False), (0, 1, False), (1, 1, True)]
    for ci, ri, win in cells:
        x = cols[ci][1]
        y = y0 if ri == 0 else y0 + h1
        h = h1 if ri == 0 else h2
        col = TEAL if win else RED
        s.rect(x, y, cw, h, fill=col, fop=0.14, stroke=col, sop=0.65, r=4)
        s.text(x + cw / 2, y + h / 2 + 6, "○ 当たり" if win else "× ハズレ",
               15 if h > 80 else 13.5, anchor="middle", bold=True, color=col)
    # 合計
    s.line(0, y0 + H + 16, 720, y0 + H + 16, op=0.25)
    for (name, x), p in zip(cols, ["1/3 ＝ 約33%", "2/3 ＝ 約67%"]):
        col = RED if "33" in p else TEAL
        s.text(x + cw / 2, y0 + H + 40, f"当たる確率 {p}", 13.5,
               anchor="middle", bold=True, color=col)
    s.text(0, 344,
           "縦の幅が確率。「変える」が勝つのは、最初にハズレを引いていた場合"
           "（確率2/3）であり、そのときは必ず当たる。", 11.5, op=0.85)
    save("01_monty.svg", s)


# ===== 図2：誕生日のパラドックス ========================================
def fig_birthday():
    ns = np.arange(1, 61)
    any_pair = np.array([1 - np.prod([(365 - k) / 365 for k in range(n)]) for n in ns])
    with_me = 1 - (364 / 365) ** (ns - 1)
    i23 = 22
    print(f"  23人：誰かと誰かが同じ = {any_pair[i23]:.4f} / "
          f"自分と同じ人がいる = {with_me[i23]:.4f} / ペア数 = {23*22//2}")
    print(f"  41人：{any_pair[40]:.4f}  /  60人：{any_pair[-1]:.4f}")

    s = Svg(720, 348, "bd",
            "誕生日のパラドックス ―― 「誰かと誰か」と「自分と」はまるで違う",
            f"横軸は人数、縦軸は確率。誰かと誰かの誕生日が一致する確率は23人で"
            f"{any_pair[i23]:.3f}、41人で{any_pair[40]:.3f}に達する。一方、自分と同じ"
            f"誕生日の人がいる確率は23人でも{with_me[i23]:.3f}しかない。"
            f"直感がこちらの低い曲線を思い浮かべるため、確率を小さく見積もる。")
    L, R, T, B = 58, 574, 56, 262
    px = lambda n: L + (n - 0) / 60 * (R - L)
    py = lambda p: B - p * (B - T)
    # 枠と目盛り
    for p in (0, 0.25, 0.5, 0.75, 1.0):
        s.line(L, py(p), R, py(p), op=0.14 if p else 0.5)
        s.text(L - 8, py(p) + 4, f"{int(p*100)}%", 11, anchor="end", op=0.75)
    for n in (0, 10, 20, 30, 40, 50, 60):
        s.line(px(n), T, px(n), B, op=0.1)
        s.text(px(n), B + 18, f"{n}", 11, anchor="middle", op=0.75)
    s.line(L, T, L, B, op=0.5)
    s.text(R + 12, B + 18, "人数", 11.5, op=0.85)
    # 2本の曲線
    s.path([(px(n), py(p)) for n, p in zip(ns, any_pair)], INDIGO, 2.4)
    s.path([(px(n), py(p)) for n, p in zip(ns, with_me)], AMBER, 2.0, dash="5 3")
    # 23人のしるし
    s.line(px(23), py(0), px(23), py(any_pair[i23]), RED, 1, 0.7, dash="3 3")
    s.line(L, py(any_pair[i23]), px(23), py(any_pair[i23]), RED, 1, 0.7, dash="3 3")
    s.circle(px(23), py(any_pair[i23]), 4.2, RED)
    s.circle(px(23), py(with_me[i23]), 4.2, AMBER)
    s.text(px(23) + 8, py(any_pair[i23]) - 10,
           f"23人で {any_pair[i23]*100:.1f}%", 12, bold=True, color=RED)
    s.text(px(23) + 8, py(with_me[i23]) - 8,
           f"こちらは {with_me[i23]*100:.1f}% だけ", 11.5, color=AMBER)
    # 凡例
    s.line(590, 92, 620, 92, INDIGO, 2.4)
    s.text(626, 96, "誰かと誰かが", 11.5)
    s.text(626, 111, "同じ（本当の問い）", 11.5)
    s.line(590, 136, 620, 136, AMBER, 2.0, dash="5 3")
    s.text(626, 140, "自分と同じ人が", 11.5)
    s.text(626, 155, "いる（直感の問い）", 11.5)
    s.text(0, 300, f"23人のペアは {23*22//2} 通りある。"
           f"比べる組の数が人数のほぼ2乗で増えるので、"
           f"「誰かと誰か」は一気に上がる。", 11.5, op=0.9)
    s.text(0, 326, "（うるう日を除く365日が等確率・各人独立という仮定のもとでの"
           "理論値。実データの集計ではない。）", 11, op=0.7)
    save("01_birthday.svg", s)


# ===== 図3：少数は偶然に振り回される ====================================
def fig_coin():
    rng = np.random.default_rng(2026)
    N = 10000
    paths = []
    for _ in range(6):
        x = rng.integers(0, 2, N)
        paths.append(np.cumsum(x) / np.arange(1, N + 1))
    paths = np.array(paths)
    # ばらつきの実測（1000回ずつ）
    many = rng.integers(0, 2, (1000, N))
    r10 = many[:, :10].mean(axis=1)
    r10000 = many.mean(axis=1)
    far10 = int(((r10 < 0.3) | (r10 > 0.7)).sum())   # 1000回のうち何回が外れたか
    far10000 = int(((r10000 < 0.3) | (r10000 > 0.7)).sum())
    print(f"  表の割合（1000回ずつ）： n=10 → 範囲 {r10.min():.2f}〜{r10.max():.2f}, "
          f"0.3〜0.7の外 {far10}回 / n=10000 → 範囲 "
          f"{r10000.min():.4f}〜{r10000.max():.4f}, 0.3〜0.7の外 {far10000}回")

    s = Svg(720, 360, "cn",
            "少数は偶然に振り回される ―― 6回ぶんの「表の割合」の動き",
            f"横軸は投げた回数（対数目盛り）、縦軸は表の割合。6本の線は独立な6回ぶんの"
            f"シミュレーション。回数が少ないうちは線が大きく上下し、"
            f"回数が増えると0.5の近くに収まっていく。1000回ずつ試すと、"
            f"10回投げたときは、表の割合が0.3未満または0.7より大きくなったのが"
            f"{far10}回あった。10000回投げたときは割合がすべて"
            f"{r10000.min():.3f}から{r10000.max():.3f}の中に収まった。"
            f"ただし1回投げ足すごとに必ず0.5へ近づくわけではない。")
    L, R, T, B = 58, 688, 56, 250
    lo, hi = 0.0, 1.0
    px = lambda n: L + (math.log10(n) / 4.0) * (R - L)
    py = lambda p: B - (p - lo) / (hi - lo) * (B - T)
    for p in (0.0, 0.25, 0.5, 0.75, 1.0):
        s.line(L, py(p), R, py(p), op=0.5 if p == 0.5 else 0.14)
        s.text(L - 8, py(p) + 4, f"{p:.2f}", 11, anchor="end", op=0.75)
    for e in range(5):
        n = 10 ** e
        s.line(px(n), T, px(n), B, op=0.1)
        s.text(px(n), B + 18, f"{n:,}", 11, anchor="middle", op=0.75)
    s.line(L, T, L, B, op=0.5)
    s.text(R - 6, B - 10, "横軸：投げた回数（対数目盛り）", 11.5,
           anchor="end", op=0.7)
    cols = [INDIGO, TEAL, AMBER, RED, "#6d4c41", "#546e7a"]
    idx = np.unique(np.round(np.logspace(0, 4, 320)).astype(int)) - 1
    for k in range(6):
        pts = [(px(i + 1), py(paths[k][i])) for i in idx]
        s.path(pts, cols[k], 1.4, 0.8)
    # 実測のばらつき
    s.text(0, 296, f"1000回ずつ試すと、10回では表の割合が 0.3未満か0.7超 になった回が "
           f"{far10}回（{far10/10:.1f}%）。10000回では "
           f"全部が {r10000.min():.3f}〜{r10000.max():.3f} に収まった。", 11.5, op=0.9)
    s.text(0, 318, "少ない回数で見えた「偏り」は、たいてい偶然の幅の中にある。"
           "ただし回数を増やす途中で0.5から離れることもある。", 11.5, op=0.9)
    s.text(0, 340, "（乱数の種を 2026 に固定して実際に計算した結果。）", 11, op=0.7)
    save("01_coin.svg", s)


# ===== 図4：このコースの地図 ============================================
def fig_map():
    s = Svg(720, 372, "mp",
            "統計学Ⅰの地図 ―― 記述統計から推測統計へ",
            "左の箱が記述統計（第2回 代表値、第3回 ばらつき、第5回 相関と因果）で、"
            "手元のデータを要約する。右の箱が推測統計（第6回 標本と中心極限定理、"
            "第7回 推定と信頼区間、第8・9回 仮説検定、第10〜13回 モデル）で、"
            "一部から全体を推し量る。この左右の境を越えるのが第6回である。"
            "下の帯が Python（Colab）で、第4回から最後まで全体を通して使う。"
            "第14回で両方を使って自分で判断する。"
            "おおまかな地図であり厳密な分類ではない。")
    s.text(0, 28, "いま自分がどこにいるかを、毎回ここで確かめる", 13.5, bold=True)

    def box(x, y, w, h, title, sub, items, col):
        s.rect(x, y, w, h, fill=col, fop=0.08, stroke=col, sop=0.6, r=6)
        s.text(x + 14, y + 26, title, 14, bold=True, color=col)
        s.text(x + 14, y + 45, sub, 11.5, op=0.8)
        for i, it in enumerate(items):
            yy = y + 72 + i * 25
            s.circle(x + 20, yy - 4, 2.6, col, 0.8)
            s.text(x + 32, yy, it, 12.5)

    LX, LW, RX, RW = 0, 310, 410, 310
    box(LX, 50, LW, 152, "記述統計", "手元のデータを「要約」する",
        ["第02回　代表値（平均・中央値・最頻値）",
         "第03回　ばらつき（分散・標準偏差）",
         "第05回　相関（と、因果ではないこと）"], INDIGO)
    box(RX, 50, RW, 178, "推測統計", "一部から「全体」を推し量る",
        ["第06回　標本と母集団／中心極限定理",
         "第07回　推定（信頼区間）",
         "第08・09回　仮説検定（t検定・分散分析）",
         "第10〜13回　モデル（回帰・AIC・ベイズ・PCA）"], TEAL)
    # 境を越える矢印（文字は矢印の上にまとめる）
    s.text(360, 118, "ここを越えるのが", 11.5, anchor="middle", bold=True, color=RED)
    s.text(360, 134, "第06回", 11.5, anchor="middle", bold=True, color=RED)
    s.arrow(318, 152, 402, 152, RED, 2, 0.85)
    # 下の帯へつなぐ線
    s.line(LX + 80, 202, LX + 80, 252, op=0.3)
    s.line(RX + 80, 228, RX + 80, 252, op=0.3)
    s.rect(0, 252, 720, 46, fill=AMBER, fop=0.1, stroke=AMBER, sop=0.6, r=6)
    s.text(16, 280, "Python（Colab）―― 第04回で始動し、ここから最後まで全部これで動かす",
           12.5, bold=True, color=AMBER)
    s.line(360, 298, 360, 316, op=0.3)
    s.rect(180, 316, 360, 38, fill="currentColor", fop=0.05, sop=0.35, r=6)
    s.text(360, 341, "第14回　総括 ―― 両方を使って、自分で決める",
           12.5, anchor="middle", bold=True)
    s.text(0, 368, "（この授業を進めるためのおおまかな地図。回帰や多変量解析のように、"
           "記述・探索・推測のどの目的にも使われる方法がある。）", 11, op=0.7)
    save("01_map.svg", s)


if __name__ == "__main__":
    print("図1 モンティ・ホール"); fig_monty()
    print("図2 誕生日のパラドックス"); fig_birthday()
    print("図3 大数の法則"); fig_coin()
    print("図4 コースの地図"); fig_map()
