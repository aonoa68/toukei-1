# -*- coding: utf-8 -*-
"""第08回（仮説検定・t検定）の図。数値はすべてここで計算する。"""
import math, os
import numpy as np, pandas as pd
from scipy import stats
from svgkit import Svg, RED, INDIGO, TEAL, AMBER

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
DATA = os.path.join(HERE, "..", "docs", "data", "primates.csv")


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg.render())
    print(f"  -> out/{name}")


def load():
    w = pd.read_csv(DATA).dropna(subset=["体重g"])
    return {n: np.log10(w.loc[w["科"] == n, "体重g"].values)
            for n in ("オナガザル科", "オマキザル科", "クモザル科")}


def welch(a, b):
    t, p = stats.ttest_ind(a, b, equal_var=False)
    va, vb, na, nb = a.var(ddof=1), b.var(ddof=1), len(a), len(b)
    dfree = (va/na + vb/nb)**2 / ((va/na)**2/(na-1) + (vb/nb)**2/(nb-1))
    return t, p, dfree


# ===== 図A：帰無分布・棄却域・p値 =======================================
def fig_null():
    G = load()
    t1, p1, df1 = welch(G["オナガザル科"], G["オマキザル科"])
    t2, p2, df2 = welch(G["オナガザル科"], G["クモザル科"])
    tc = stats.t.ppf(0.975, df2)
    print(f"  オマキザル科: t={t1:.2f} p={p1:.2e} df={df1:.1f}")
    print(f"  クモザル科  : t={t2:.2f} p={p2:.3f} df={df2:.1f}  棄却域 |t|>{tc:.2f}")

    s = Svg(720, 346, "nl",
            "帰無仮説が正しいとき、t はこの形で散らばる",
            f"横軸は t の値。曲線は「差はない」と仮定したときに t が取る分布"
            f"（自由度約{df2:.0f}）。両端の塗った部分が棄却域で、面積は左右あわせて5%、"
            f"境目は±{tc:.2f}である。クモザル科との比較の t = {t2:.2f} は"
            f"中央にあり棄却域に入らない。オマキザル科との比較の t = {t1:.2f} は"
            f"この図の右端のはるか外にあり、p は {p1:.0e} である。")
    L, R, T, B = 48, 600, 70, 250
    xr = 4.6
    px = lambda t: L + (t + xr) / (2 * xr) * (R - L)
    ts = np.linspace(-xr, xr, 400)
    ys = stats.t.pdf(ts, df2)
    py = lambda y: B - y / 0.42 * (B - T)

    # 棄却域の塗り
    for lo, hi in [(-xr, -tc), (tc, xr)]:
        g = np.linspace(lo, hi, 60)
        pts = [f"{px(g[0]):.1f},{B:.1f}"] + \
              [f"{px(v):.1f},{py(stats.t.pdf(v, df2)):.1f}" for v in g] + \
              [f"{px(g[-1]):.1f},{B:.1f}"]
        s.parts.append(f'<polygon points="{" ".join(pts)}" fill="{RED}"'
                       f' fill-opacity="0.3" stroke="none"/>')
    s.path([(px(t), py(y)) for t, y in zip(ts, ys)], INDIGO, 2.2)
    s.line(L, B, R, B, op=0.5)
    for v in (-4, -2, 0, 2, 4):
        s.line(px(v), B, px(v), B + 5, op=0.5)
        s.text(px(v), B + 20, f"{v}", 11, anchor="middle", op=0.75)
    s.text(L - 6, B + 20, "t の値", 11.5, anchor="end", op=0.8)
    for v, lab in [(-tc, f"−{tc:.2f}"), (tc, f"+{tc:.2f}")]:
        s.line(px(v), py(stats.t.pdf(v, df2)), px(v), B, RED, 1, 0.8, dash="3 3")
        s.text(px(v), 60, lab, 11.5, anchor="middle", bold=True, color=RED)
    s.text(px(-3.6), 100, "棄却域", 12, anchor="middle", bold=True, color=RED)
    s.text(px(-3.6), 116, "2.5%", 11, anchor="middle", color=RED)
    s.text(px(3.6), 100, "棄却域", 12, anchor="middle", bold=True, color=RED)
    s.text(px(3.6), 116, "2.5%", 11, anchor="middle", color=RED)
    s.text(0, 34, "「差はない」と仮定したとき、t はこう散らばる", 13.5, bold=True)
    # 観測された2つの t
    s.line(px(t2), B, px(t2), py(stats.t.pdf(t2, df2)) - 6, TEAL, 2)
    s.circle(px(t2), py(stats.t.pdf(t2, df2)) - 6, 4, TEAL)
    XE = px(-1.35)
    s.text(XE, 152, "クモザル科との比較", 12, anchor="end", bold=True, color=TEAL)
    s.text(XE, 170, f"t = {t2:.2f}　ど真ん中", 12, anchor="end", color=TEAL)
    s.text(XE, 188, f"p = {p2:.2f} ―― 偶然で説明がつく", 11.5, anchor="end",
           color=TEAL, op=0.9)
    s.text(620, 168, "オマキザル科との比較", 12, anchor="middle", bold=True, color=AMBER)
    s.arrow(px(4.2), 188, 702, 188, AMBER, 2, 0.9)
    s.text(620, 212, f"t = {t1:.2f}", 12.5, anchor="middle", bold=True, color=AMBER)
    s.text(620, 228, "この図の外、ずっと右", 11.5, anchor="middle", color=AMBER)
    s.text(0, 296, f"p値は「塗った裾と同じ側にどれだけ入るか」の面積。"
           f"t = {t1:.2f} では面積が 8×10⁻²⁷ しか残らない。", 11.5, op=0.9)
    s.text(0, 318, "同じデータ・同じ手法でも、比べる相手を変えるだけで"
           "t はこれだけ動く。", 11.5, op=0.9)
    s.text(0, 340, f"（Welch の t検定。自由度は約 {df2:.0f}。体重は第3回のとおり"
           f"常用対数で扱っている。）", 11, op=0.7)
    save("08_null.svg", s)


# ===== 図B：3つの科を同じ軸に並べる ====================================
def fig_groups():
    G = load()
    rng = np.random.default_rng(8)
    s = Svg(720, 352, "gp",
            "比べる相手を変えると、結論は正反対になる",
            "横軸は体重の常用対数。点は1種ずつ。オナガザル科（92種）の平均と"
            "クモザル科（16種）の平均はほとんど同じ位置に重なるが、"
            "オマキザル科（39種）はまるごと左にずれている。"
            "どちらもオナガザル科との比較なのに、結論が逆になる理由がこれである。")
    L, R = 92, 690
    lo, hi = 2.0, 4.8
    px = lambda v: L + (v - lo) / (hi - lo) * (R - L)
    rows = [("オナガザル科", G["オナガザル科"], INDIGO, 92),
            ("クモザル科", G["クモザル科"], TEAL, 160),
            ("オマキザル科", G["オマキザル科"], AMBER, 228)]
    s.text(0, 32, "同じ「オナガザル科との比較」でも、相手でこれだけ違う", 13.5, bold=True)
    # 目盛り
    for v in (2, 3, 4):
        s.line(px(v), 62, px(v), 262, op=0.12)
        s.text(px(v), 282, f"{v}", 11, anchor="middle", op=0.75)
        s.text(px(v), 297, f"({10**v:,}g)", 10, anchor="middle", op=0.6)
    s.line(L, 262, R, 262, op=0.4)
    s.text(R, 282, "体重の常用対数 log10(g)", 11.5, anchor="end", op=0.8)
    for name, x, col, y in rows:
        s.text(L - 10, y + 4, f"{name}", 12, anchor="end", bold=True, color=col)
        s.text(L - 10, y + 20, f"n = {len(x)}", 11, anchor="end", op=0.7)
        for v in x:
            s.circle(px(v), y + rng.uniform(-13, 13), 2.8, col, 0.55)
        m = x.mean()
        s.line(px(m), y - 22, px(m), y + 22, col, 2.2)
        s.text(px(m), y - 28, f"平均 {m:.2f}", 11, anchor="middle", bold=True, color=col)
    # 比較の結果
    for a, b, lab, col, yy in [
            ("オナガザル科", "クモザル科", "差があるとは言えない（t = −0.02, p = 0.98）", TEAL, 318),
            ("オナガザル科", "オマキザル科", "はっきり差がある（t = 20.03, p ≒ 8×10⁻²⁷）", AMBER, 340)]:
        t, p, _ = welch(G[a], G[b])
        print(f"  {a} vs {b}: t={t:.2f} p={p:.2e}  平均差={G[a].mean()-G[b].mean():.3f}")
        s.circle(8, yy - 4, 3.4, col, 0.9)
        s.text(20, yy, f"{a} と {b} → {lab}", 11.5, op=0.95)
    save("08_groups.svg", s)


# ===== 図C：n を増やすと「有意」になる ==================================
def fig_power():
    d = 0.18
    ns = np.arange(5, 1001)
    crit = stats.t.ppf(0.975, 2 * ns - 2)
    power = stats.nct.sf(crit, 2 * ns - 2, d * np.sqrt(ns / 2)) + \
            stats.nct.cdf(-crit, 2 * ns - 2, d * np.sqrt(ns / 2))
    marks = {n: float(power[list(ns).index(n)]) for n in (20, 100, 500)}
    for n, v in marks.items():
        print(f"  n={n}: 有意になる割合 {v*100:.1f}%  （t = d√(n/2) = {d*math.sqrt(n/2):.2f}）")

    s = Svg(720, 374, "pw",
            "差の大きさは同じ。増やしたのは人数だけ",
            f"横軸は各群の頭数（対数目盛り）、縦軸は「有意（p<0.05）になる割合」。"
            f"真の差は常に0.2kg（効果量 d = 0.18）で固定されている。"
            f"それでも各群20頭なら{marks[20]*100:.1f}%、100頭で{marks[100]*100:.1f}%、"
            f"500頭で{marks[500]*100:.1f}%が有意になる。"
            f"人数を増やすだけで「有意差あり」は作れてしまう。")
    L, R, T, B = 58, 600, 66, 258
    px = lambda n: L + (math.log10(n) - 1) / 2 * (R - L)
    py = lambda v: B - v * (B - T)
    s.text(0, 32, "真の差は 0.2kg のまま。増やしたのは人数だけ", 13.5, bold=True)
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        s.line(L, py(v), R, py(v), op=0.5 if v == 0 else 0.13)
        s.text(L - 8, py(v) + 4, f"{int(v*100)}%", 11, anchor="end", op=0.75)
    for n in (10, 100, 1000):
        s.line(px(n), T, px(n), B, op=0.1)
        s.text(px(n), B + 19, f"{n}", 11, anchor="middle", op=0.75)
    s.line(L, T, L, B, op=0.5)
    s.text((L + R) / 2, B + 40, "各群の頭数（対数目盛り）", 11.5,
           anchor="middle", op=0.8)
    s.text(L - 8, py(0.05) + 4, "5%", 11, anchor="end", color=RED, op=0.9)
    s.line(L, py(0.05), R, py(0.05), RED, 1, 0.6, dash="4 3")
    s.text(px(900), py(0.05) - 10, "差が無いときでも有意になる割合（＝5%）", 11,
           anchor="end", color=RED, op=0.9)
    m = (ns >= 10) & (ns <= 1000)
    s.path([(px(n), py(v)) for n, v in zip(ns[m], power[m])], INDIGO, 2.4)
    for n, v in marks.items():
        s.circle(px(n), py(v), 4.6, RED)
        s.line(px(n), py(v), px(n), B, RED, 1, 0.4, dash="3 3")
        s.text(px(n), py(v) - 12, f"{v*100:.1f}%", 12, anchor="middle",
               bold=True, color=RED)
    s.text(612, 110, "効果量 d = 0.18", 12, bold=True, color=TEAL)
    s.text(612, 128, "（小さい効果）", 11.5, color=TEAL, op=0.9)
    s.text(612, 152, "は、どの人数でも", 11.5, op=0.85)
    s.text(612, 170, "まったく動かない", 11.5, op=0.85)
    s.text(0, 322, "「有意差あり」と書いてあったら、まず n を見る。"
           "n が大きければ、小さな差でも有意になる。", 11.5, op=0.9)
    s.text(0, 344, "逆に n が小さいと、本当にある差も見逃す（各群20頭では"
           f"{(1-marks[20])*100:.0f}%を見逃している）。", 11.5, op=0.9)
    s.text(0, 366, f"（両側5%・等分散のt検定の理論値。20万回のシミュレーションでも "
           f"{marks[20]*100:.1f}%・{marks[100]*100:.1f}%・{marks[500]*100:.1f}% "
           f"と一致した。）", 11, op=0.7)
    save("08_power.svg", s)


# ===== 図D：2種類の誤り =================================================
def fig_errors():
    n, d = 100, 0.18
    dfree = 2 * n - 2
    ncp = d * math.sqrt(n / 2)
    tc = stats.t.ppf(0.975, dfree)
    alpha_r = stats.t.sf(tc, dfree)
    beta = stats.nct.cdf(tc, dfree, ncp) - stats.nct.cdf(-tc, dfree, ncp)
    print(f"  n={n}: 境目 t={tc:.2f}, ずれ ncp={ncp:.2f}, "
          f"α右側={alpha_r*100:.1f}%, β={beta*100:.1f}%, 検出力={(1-beta)*100:.1f}%")

    s = Svg(720, 356, "er",
            "2種類の誤り ―― 偽陽性と見逃し",
            f"左の青い曲線が「本当は差がない」ときの t の分布、"
            f"右の緑の曲線が「本当は0.2kgの差がある」ときの t の分布"
            f"（各群{n}頭）。縦の赤い線が有意かどうかの境目 t = {tc:.2f} である。"
            f"青い曲線のうち境目より右（赤）が第一種の誤り＝偽陽性で{alpha_r*100:.1f}%、"
            f"緑の曲線のうち境目より左（灰）が第二種の誤り＝見逃しで{beta*100:.0f}%を占める。"
            f"見逃しのほうがずっと大きい。")
    L, R, T, B = 48, 690, 86, 250
    xr0, xr1 = -4.2, 5.4
    px = lambda t: L + (t - xr0) / (xr1 - xr0) * (R - L)
    py = lambda y: B - y / 0.42 * (B - T)
    ts = np.linspace(xr0, xr1, 420)
    y0 = stats.t.pdf(ts, dfree)
    y1 = stats.nct.pdf(ts, dfree, ncp)

    def fill(xs, ys, col, op):
        pts = [f"{px(xs[0]):.1f},{B:.1f}"] + \
              [f"{px(a):.1f},{py(b):.1f}" for a, b in zip(xs, ys)] + \
              [f"{px(xs[-1]):.1f},{B:.1f}"]
        s.parts.append(f'<polygon points="{" ".join(pts)}" fill="{col}"'
                       f' fill-opacity="{op}" stroke="none"/>')
    m = ts >= tc
    fill(ts[m], y0[m], RED, 0.45)
    m = ts <= tc
    fill(ts[m], y1[m], "currentColor", 0.22)
    s.path([(px(a), py(b)) for a, b in zip(ts, y0)], INDIGO, 2.2)
    s.path([(px(a), py(b)) for a, b in zip(ts, y1)], TEAL, 2.2)
    s.line(L, B, R, B, op=0.5)
    for v in (-4, -2, 0, 2, 4):
        s.text(px(v), B + 19, f"{v}", 11, anchor="middle", op=0.75)
    s.text(R - 4, B + 19, "t の値", 11.5, anchor="end", op=0.8)
    s.line(px(tc), T - 16, px(tc), B, RED, 1.6, 0.85, dash="4 3")
    s.text(px(tc), T - 22, f"有意かどうかの境目  t = {tc:.2f}", 11.5,
           anchor="middle", bold=True, color=RED)
    s.text(0, 32, "間違え方は2つある ―― 偽陽性と、見逃し", 13.5, bold=True)
    s.text(px(-1.4), 112, "本当は差がない", 12, anchor="middle", bold=True, color=INDIGO)
    s.text(px(3.6), 100, f"本当は0.2kgの差がある", 12, anchor="middle",
           bold=True, color=TEAL)
    s.text(px(3.6), 116, f"（各群{n}頭のとき）", 11, anchor="middle", color=TEAL, op=0.9)
    s.circle(10, 288, 5, RED, 0.45)
    s.text(24, 292, f"第一種の誤り（偽陽性）＝ 差がないのに「あり」と言う。"
           f"片側 {alpha_r*100:.1f}%、両側あわせて 5%。", 11.5)
    s.circle(10, 312, 5, "currentColor", 0.22)
    s.text(24, 316, f"第二種の誤り（見逃し）＝ 差があるのに「なし」と言う。"
           f"ここでは {beta*100:.0f}%。有意になるのは残りの {(1-beta)*100:.0f}% だけ。", 11.5)
    s.text(0, 348, "αは5%と決め打ちできるが、見逃しの大きさは効果量と人数で決まる。"
           "小さい差を小さい標本で追うと、ほとんど見逃す。", 11, op=0.7)
    save("08_errors.svg", s)


if __name__ == "__main__":
    print("図A 帰無分布と棄却域"); fig_null()
    print("図B 3つの科"); fig_groups()
    print("図C 人数と有意"); fig_power()
    print("図D 2種類の誤り"); fig_errors()
