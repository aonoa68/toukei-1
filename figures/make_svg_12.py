# -*- coding: utf-8 -*-
"""第12回（ベイズ統計の入り口）の図。数値はすべてここで計算する。"""
import os
import numpy as np
from scipy import stats
from svgkit import Svg, RED, INDIGO, TEAL, AMBER

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg.render())
    print(f"  -> out/{name}")


def ci(a, b):
    lo, hi = stats.beta.ppf([0.025, 0.975], a, b)
    return lo, hi, hi - lo


# ===== 図A：データが増えると信念は締まる ===============================
def fig_posterior():
    rows = [(0, 0), (5, 5), (20, 14), (100, 75)]
    info = []
    for n, k in rows:
        a, b = 1 + k, 1 + n - k
        lo, hi, w = ci(a, b)
        info.append((n, k, a, b, (k+1)/(n+2), lo, hi, w))
        print(f"  n={n:3d} k={k:3d} Beta({a}, {b}) 平均 {(k+1)/(n+2):.2f} "
              f"95%区間 {lo:.3f}〜{hi:.3f}（幅 {w:.2f}）")

    s = Svg(720, 400, "po",
            "投げるほど、信念は締まっていく",
            "横軸は未知の表確率 θ の候補、縦軸はその候補の確からしさ。"
            "0回は真っ平らで区間の幅は0.95、5回で0.46、20回で0.38、"
            "100回で0.17まで狭くなる。山は真の値0.7のあたりに寄っていくが、"
            "5回の時点では表が5回続いたため平均0.86と行きすぎている。"
            "データが増えるほど、事前の置き方より観測が効いてくる。")
    L, R, T, B = 58, 690, 76, 252
    px = lambda v: L + v * (R - L)
    ymax = 9.5
    py = lambda v: B - min(v, ymax) / ymax * (B - T)
    s.text(0, 30, "ベイズ更新 ―― 見るたびに信念を上書きする", 13.5, bold=True)
    xs = np.linspace(0.001, 0.999, 420)
    cols = ["currentColor", AMBER, TEAL, INDIGO]
    for (n, k, a, b, m, lo, hi, w), col in zip(info, cols):
        ys = stats.beta.pdf(xs, a, b)
        s.path([(px(x), py(y)) for x, y in zip(xs, ys)], col, 2.4,
               0.55 if n == 0 else 1.0)
    s.line(L, B, R, B, op=0.5)
    for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        s.line(px(v), T, px(v), B, op=0.08)
        s.text(px(v), B + 19, f"{v:g}", 11, anchor="middle", op=0.75)
    s.text((L + R) / 2, B + 40, "未知の表確率 θ の候補", 11.5, anchor="middle", op=0.8)
    s.line(px(0.7), T - 14, px(0.7), B, RED, 1.6, 0.8, dash="4 3")
    s.text(px(0.7), T - 20, "真の値 0.7", 11.5, anchor="middle", bold=True, color=RED)
    for i, ((n, k, a, b, m, lo, hi, w), col) in enumerate(zip(info, cols)):
        y = 96 + i * 24
        s.line(76, y - 4, 106, y - 4, col, 2.4, 0.6 if n == 0 else 1.0)
        s.text(114, y, f"{n}回中 表{k}回　Beta({a}, {b})　"
               f"平均 {m:.2f}　区間の幅 {w:.2f}", 11.5, op=0.95)
    s.text(0, 316, "0回では幅0.95 ―― ほとんど何も言えていない。"
           "100回で幅0.17まで狭まる。これが「信念が締まる」ということ。",
           11.5, op=0.95)
    s.text(0, 340, "5回の時点で平均0.86と行きすぎているのは、"
           "表が5回続いたから。増やせば必ず近づくわけではない。", 11.5, op=0.95)
    s.text(0, 364, "それでも 100回では 0.75、真の値 0.7 を区間がきちんと含んでいる。",
           11.5, op=0.95)
    s.text(0, 394, "（一様な事前 Beta(1,1) から出発し、表 k 回・裏 n−k 回で "
           "Beta(1+k, 1+n−k) に更新。区間は95%信用区間。）", 11, op=0.7)
    save("12_posterior.svg", s)


# ===== 図B：正反対の事前も、データに押し流される =======================
def fig_prior():
    k, n = 75, 100
    pri = [("懐疑的 Beta(2, 8)", 2, 8, TEAL), ("楽観的 Beta(8, 2)", 8, 2, AMBER)]
    post = [(lab, a0 + k, b0 + n - k, col) for lab, a0, b0, col in pri]
    for (lab, a0, b0, _), (_, a, b, _) in zip(pri, post):
        print(f"  {lab}: 事前平均 {a0/(a0+b0):.2f} → 事後 Beta({a}, {b}) "
              f"平均 {a/(a+b):.3f}")
    gap0 = abs(pri[0][1]/(pri[0][1]+pri[0][2]) - pri[1][1]/(pri[1][1]+pri[1][2]))
    gap1 = abs(post[0][1]/(post[0][1]+post[0][2]) - post[1][1]/(post[1][1]+post[1][2]))
    print(f"  平均の差： 事前 {gap0:.2f} → 事後 {gap1:.3f}")

    s = Svg(720, 392, "pr",
            "正反対の出発点でも、100回のデータを見たあとはほぼ同じ",
            "左は2人の事前。懐疑的な人はBeta(2,8)で平均0.20、楽観的な人は"
            "Beta(8,2)で平均0.80と、正反対から出発する。"
            "右は同じ100回の結果（表75回）を見たあとの事後で、"
            "Beta(77,33)の平均0.700とBeta(83,27)の平均0.755。"
            "出発点の差0.60が、0.055まで縮んでいる。")
    s.text(0, 30, "出発点の差 0.60 が、100回のデータで 0.055 まで縮む", 13.5,
           bold=True)
    xs = np.linspace(0.001, 0.999, 420)

    def panel(x0, w, dists, title, ymax, labels):
        T, B = 92, 258
        px = lambda v: x0 + v * w
        py = lambda v: B - min(v, ymax) / ymax * (B - T)
        s.text(x0, 74, title, 12.5, bold=True)
        s.line(x0, B, x0 + w, B, op=0.5)
        for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
            s.line(px(v), T, px(v), B, op=0.07)
            s.text(px(v), B + 18, f"{v:g}", 10.5, anchor="middle", op=0.7)
        s.line(px(0.7), T, px(0.7), B, RED, 1.4, 0.7, dash="4 3")
        for (lab, a, b, col), ytext in zip(dists, labels):
            ys = stats.beta.pdf(xs, a, b)
            s.path([(px(x), py(y)) for x, y in zip(xs, ys)], col, 2.4)
            m = a / (a + b)
            s.circle(px(m), B, 4.4, col)
            s.text(x0, ytext, f"{lab}　平均 {m:.3f}", 11.5, bold=True, color=col)
        s.text(x0 + w, B + 36, "θ の候補", 11, anchor="end", op=0.75)

    panel(10, 320, [(l, a, b, c) for l, a, b, c in pri], "① 投げる前（事前）", 3.6,
          [292, 312])
    panel(390, 320, [(l.split()[0] + "の人", a, b, c) for l, a, b, c in post],
          "② 100回のうち表75回を見たあと（事後）", 9.5, [292, 312])
    s.text(0, 348, "事前の違いは $a_0$ の 2 と 8、つまり「6回ぶん」の差しかない。"
           .replace("$a_0$", "a₀"), 11.5, op=0.95)
    s.text(0, 370, "データ100回に対して6回ぶんなので薄まる。"
           "事前は結論を決めるものではなく、出発点である。", 11.5, op=0.95)
    save("12_prior.svg", s)


if __name__ == "__main__":
    print("図A 事後分布"); fig_posterior()
    print("図B 事前の違い"); fig_prior()
