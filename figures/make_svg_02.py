# -*- coding: utf-8 -*-
"""第02回（代表値）の図。数値はすべてここで計算する。"""
import math, os
import numpy as np, pandas as pd
from scipy import stats
from svgkit import Svg, RED, INDIGO, TEAL, AMBER

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
D = pd.read_csv(os.path.join(HERE, "..", "docs", "data", "primates.csv"))


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg.render())
    print(f"  -> out/{name}")


W = D.dropna(subset=["体重g"])["体重g"].values
HITO = D[(D["科"] == "ヒト科") & D["体重g"].notna()]["体重g"].values
NOHITO = D[(D["科"] != "ヒト科") & D["体重g"].notna()]["体重g"].values


def bars(s, counts, edges, px, py0, hmax, col, cmax):
    """ヒストグラムの棒。edges は px に渡す値の境界。"""
    for c, lo, hi in zip(counts, edges[:-1], edges[1:]):
        x0, x1 = px(lo), px(hi)
        h = c / cmax * hmax
        if h > 0:
            s.rect(x0 + 0.5, py0 - h, max(x1 - x0 - 1, 1), h,
                   fill=col, fop=0.35, stroke=col, sop=0.6)


# ===== 図A：体重の分布（線形 と 対数20区分） ============================
def fig_hist():
    mean, med = W.mean(), np.median(W)
    print(f"  265種: n={len(W)} 平均={mean:.0f} 中央値={med:.0f} "
          f"最大={W.max():.0f} 最小={W.min():.0f}")
    # 対数20区分（本文の表と同じ切り方）
    e = np.logspace(np.log10(W.min()), np.log10(W.max()), 21)
    cnt, _ = np.histogram(W, bins=e)
    for i in (9, 10, 11, 12):
        print(f"    {e[i]:,.0f}〜{e[i+1]:,.0f}g : {cnt[i]}種")

    s = Svg(720, 404, "hs",
            "体重265種の分布 ―― 平均と中央値がずれる理由",
            f"上は体重をそのままの目盛りで20区分したヒストグラム。"
            f"ほとんどの種が左端の最初の区分に入り、右へ長い裾を引く。"
            f"平均{mean:,.0f}gは中央値{med:,.0f}gの約2倍で、"
            f"少数の大型種に引き上げられている。"
            f"下は同じデータを対数の目盛りで20区分したもので、"
            f"小型のまとまりと5,039〜7,696gの55種のまとまりが見える。"
            f"中央値は谷ではなく、平均は最多の区分に入っている。")
    L, R = 58, 690
    s.text(0, 28, "同じ265種を、目盛りを変えて2回描く", 13.5, bold=True)

    # --- 上：線形 ---
    T1, B1 = 64, 160
    e1 = np.linspace(W.min(), W.max(), 21)
    c1, _ = np.histogram(W, bins=e1)
    px1 = lambda v: L + (v - W.min()) / (W.max() - W.min()) * (R - L)
    bars(s, c1, e1, px1, B1, B1 - T1, INDIGO, c1.max())
    s.line(L, B1, R, B1, op=0.45)
    for v in (0, 50000, 100000, 150000):
        vv = min(max(v, W.min()), W.max())
        s.text(px1(vv), B1 + 17, f"{v:,}", 10.5, anchor="middle", op=0.7)
    s.text(R, B1 + 34, "体重 (g)　そのままの目盛り", 11, anchor="end", op=0.75)
    s.text(L, T1 - 8, f"最も多い区分に {c1.max()}種（265種中）が入る", 11.5, op=0.85)
    for v, lab, col in [(med, f"中央値 {med:,.0f}g", TEAL),
                        (mean, f"平均 {mean:,.0f}g", RED)]:
        s.line(px1(v), T1 - 2, px1(v), B1, col, 1.6, 0.9, dash="4 3")
    s.arrow(px1(mean) + 86, 96, px1(mean) + 6, 112, RED, 1.4, 0.9)
    s.text(px1(mean) + 92, 92, f"平均 {mean:,.0f}g と", 11.5, color=RED)
    s.text(px1(mean) + 92, 107, f"中央値 {med:,.0f}g は", 11.5, color=TEAL)
    s.text(px1(mean) + 92, 122, "ここに重なって見える", 11.5, op=0.85)
    s.text(px1(W.max()) - 6, 140, f"← ヒガシゴリラ {W.max():,.0f}g", 11,
           anchor="end", color=AMBER)

    # --- 下：対数20区分 ---
    T2, B2 = 232, 320
    px2 = lambda v: L + (math.log10(v) - math.log10(W.min())) / \
        (math.log10(W.max()) - math.log10(W.min())) * (R - L)
    bars(s, cnt, e, px2, B2, B2 - T2, INDIGO, cnt.max())
    s.line(L, B2, R, B2, op=0.45)
    for v in (100, 1000, 10000, 100000):
        s.text(px2(v), B2 + 17, f"{v:,}", 10.5, anchor="middle", op=0.7)
    s.text(R, B2 + 34, "体重 (g)　対数の目盛り（20区分）", 11, anchor="end", op=0.75)
    k = int(np.argmax(cnt))
    s.text(px2(e[k]), T2 - 26, f"{e[k]:,.0f}〜{e[k+1]:,.0f}g に {cnt[k]}種",
           11.5, anchor="middle", bold=True, color=AMBER)
    s.line(px2(med), T2 - 10, px2(med), B2, TEAL, 1.8, 0.9, dash="4 3")
    s.line(px2(mean), T2 - 10, px2(mean), B2, RED, 1.8, 0.9, dash="4 3")
    s.text(px2(med) - 6, T2 - 14, f"中央値 {med:,.0f}g", 11.5, anchor="end",
           bold=True, color=TEAL)
    s.text(px2(mean) + 6, T2 - 14, f"平均 {mean:,.0f}g", 11.5, bold=True, color=RED)
    s.text(0, 374, "そのままの目盛りでは、265種のほとんどが左端の1本に潰れて"
           "分布の形が見えない。対数にすると、まとまりが2つあることが分かる。",
           11.5, op=0.9)
    s.text(0, 396, f"（区分の切り方は本文の表と同じ。最小 {W.min():,.0f}g から"
           f"最大 {W.max():,.0f}g までを対数で20等分している。）", 11, op=0.7)
    save("02_hist.svg", s)


# ===== 図B：外れ値を動かすと、平均と中央値はどうなるか ==================
def fig_robust():
    x = np.array([1, 2, 3, 4, 100.0])
    y = np.array([1, 2, 3, 4, 1000.0])
    z = np.array([1, 2, 3, 4.0])
    rows = [("1, 2, 3, 4, 100", x), ("100 を 1000 に変える", y),
            ("100 を 削除する", z)]
    for lab, v in rows:
        print(f"  {lab}: 平均={v.mean():.1f} 中央値={np.median(v):.1f}")
    m1, md1 = NOHITO.mean(), np.median(NOHITO)
    print(f"  全265種: 平均={W.mean():.0f} 中央値={np.median(W):.0f}")
    print(f"  ヒト科7種を除く258種: 平均={m1:.0f} 中央値={md1:.0f} "
          f"→ 平均は{W.mean()-m1:.0f}g、中央値は{np.median(W)-md1:.0f}g動く "
          f"（比 {(W.mean()-m1)/(np.median(W)-md1):.1f}倍）")

    s = Svg(720, 348, "rb",
            "極端な値を動かすと、平均だけが大きく動く",
            f"5個の数字 1, 2, 3, 4, 100 で、平均は22、中央値は3。"
            f"100を1000に変えると平均は202に跳ね上がるが、中央値は3のまま動かない。"
            f"100を削除すると個数が4個になり、中央値は2.5に変わる。"
            f"実データでも同じで、ヒト科7種を除くと平均は"
            f"{W.mean()-m1:,.0f}g動くのに中央値は{np.median(W)-md1:,.0f}gしか動かない。")
    s.text(0, 28, "中央値は「動かない」のではなく「動きにくい」", 13.5, bold=True)
    L, R = 150, 560
    px = lambda v: L + (math.log10(v) - 0) / (math.log10(1000)) * (R - L)
    for i, (lab, v) in enumerate(rows):
        y0 = 78 + i * 62
        s.text(L - 14, y0 + 4, lab, 11.5, anchor="end", op=0.95)
        s.line(L, y0, R, y0, op=0.3)
        for u in v:
            s.circle(px(u), y0, 4.2, INDIGO, 0.6)
        s.circle(px(np.median(v)), y0, 5.4, TEAL)
        s.circle(px(v.mean()), y0, 5.4, RED)
        s.text(px(np.median(v)), y0 + 22, f"中央値 {np.median(v):g}", 11,
               anchor="middle", color=TEAL, bold=True)
        s.text(px(v.mean()), y0 - 14, f"平均 {v.mean():g}", 11,
               anchor="middle", color=RED, bold=True)
    for v in (1, 10, 100, 1000):
        s.text(px(v), 262, f"{v}", 10.5, anchor="middle", op=0.6)
    s.text(R, 280, "値（対数の目盛り）", 11, anchor="end", op=0.7)
    s.text(0, 308, f"実データでも同じ。ヒト科7種（全体の2.6%）を除くと、"
           f"平均は {W.mean()-m1:,.0f}g 動くのに、中央値は {np.median(W)-md1:,.0f}g "
           f"しか動かない（比 {(W.mean()-m1)/(np.median(W)-md1):.1f}倍）。", 11.5, op=0.9)
    s.text(0, 330, "順位だけを見る中央値は、端の値の大きさに引っ張られない。"
           "ただし観測を足し引きすると真ん中の位置がずれるので、変わることはある。",
           11.5, op=0.9)
    s.text(0, 346, "", 11, op=0.7)
    save("02_robust.svg", s)


# ===== 図C：「下手さ」の形が、答えを決める ==============================
def fig_loss():
    data = np.array([1.0, 2.0, 6.0])
    cs = np.linspace(0.6, 6.6, 400)
    sq = np.array([((data - c) ** 2).sum() for c in cs])
    ab = np.array([np.abs(data - c).sum() for c in cs])
    print(f"  データ 1,2,6: 平均={data.mean():.0f} 中央値={np.median(data):.0f}")
    print(f"  二乗の最小 c={cs[sq.argmin()]:.2f} 値={sq.min():.0f} / "
          f"絶対値の最小 c={cs[ab.argmin()]:.2f} 値={ab.min():.0f}")

    s = Svg(720, 366, "ls",
            "「下手さ」の測り方を変えると、答えが平均か中央値に変わる",
            "データ 1, 2, 6 について、代表の候補 c をいろいろ動かしたときの"
            "「ズレの合計」を描いた。二乗で測った赤い曲線はなめらかな放物線で、"
            "最小になるのは c = 3、すなわち平均である。"
            "絶対値で測った青い折れ線は角のある形で、最小になるのは c = 2、"
            "すなわち中央値（データの点）である。"
            "同じデータでも、下手さの測り方を変えると答えが変わる。")
    L, R, T, B = 58, 560, 72, 262
    px = lambda c: L + (c - 0) / 7 * (R - L)
    sy = lambda v: B - v / 56 * (B - T)
    ay = lambda v: B - v / 13 * (B - T)
    s.text(0, 30, "同じデータなのに、最小になる場所が違う", 13.5, bold=True)
    s.line(L, B, R, B, op=0.45)
    for c in range(0, 8):
        s.line(px(c), T, px(c), B, op=0.08)
        s.text(px(c), B + 18, f"{c}", 11, anchor="middle", op=0.75)
    s.text((L + R) / 2, B + 40, "代表の候補 c", 11.5, anchor="middle", op=0.8)
    for u in data:
        s.circle(px(u), B, 4.4, INDIGO, 0.75)
    s.path([(px(c), sy(v)) for c, v in zip(cs, sq)], RED, 2.4)
    s.path([(px(c), ay(v)) for c, v in zip(cs, ab)], TEAL, 2.4)
    s.circle(px(3), sy(14), 5, RED)
    s.circle(px(2), ay(5), 5, TEAL)
    s.line(px(3), sy(14), px(3), B, RED, 1, 0.45, dash="3 3")
    s.line(px(2), ay(5), px(2), B, TEAL, 1, 0.45, dash="3 3")
    s.text(px(3) + 16, sy(14) + 5, "最小は c = 3 ＝ 平均", 12, bold=True, color=RED)
    s.text(px(2) - 12, ay(5) - 10, "最小は c = 2 ＝ 中央値", 12, anchor="end",
           bold=True, color=TEAL)
    s.line(574, 96, 604, 96, RED, 2.4)
    s.text(610, 100, "ズレを二乗して", 11.5)
    s.text(610, 115, "合計（放物線）", 11.5)
    s.line(574, 148, 604, 148, TEAL, 2.4)
    s.text(610, 152, "ズレの絶対値を", 11.5)
    s.text(610, 167, "合計（折れ線）", 11.5)
    s.text(0, 320, "二乗はなめらかなので、最小の場所はデータの点でなくてよい。"
           "絶対値は角があるので、最小の場所はデータの点そのものになる。",
           11.5, op=0.9)
    s.text(0, 342, "これが導出①・②で証明することの正体である。"
           "平均と中央値は、同じ問いに対する2つの答えだった。", 11.5, op=0.9)
    s.text(0, 362, "（横軸上の●がデータの位置 1, 2, 6。縦軸は2本で目盛りが別で、形の違いを見るための図。）", 11, op=0.7)
    save("02_loss.svg", s)


# ===== 図D：妊娠期間は、ほとんどずれない ================================
def fig_gest():
    g = D.dropna(subset=["妊娠期間日"])["妊娠期間日"].values
    mean, med, sk = g.mean(), np.median(g), stats.skew(g)
    skw = stats.skew(W)
    print(f"  妊娠期間: n={len(g)} 平均={mean:.1f} 中央値={med:.1f} 歪度={sk:.2f}")
    print(f"  体重の歪度={skw:.2f}")

    s = Svg(720, 336, "gs",
            "列が変われば分布も変わる ―― 妊娠期間はほとんどずれない",
            f"同じデータセットの妊娠期間{len(g)}種のヒストグラム。"
            f"平均{mean:.1f}日と中央値{med:.1f}日はほとんど重なり、"
            f"歪度は{sk:.2f}".replace("-", "−") + "である。"
            f"体重の歪度{skw:.1f}とはまるで違う。"
            f"平均を使ってよいかは、データセットごとではなく列ごとに決まる。")
    L, R, T, B = 58, 600, 76, 252
    e = np.linspace(g.min(), g.max(), 24)
    c, _ = np.histogram(g, bins=e)
    px = lambda v: L + (v - g.min()) / (g.max() - g.min()) * (R - L)
    s.text(0, 30, f"妊娠期間{len(g)}種 ―― 平均と中央値がほぼ重なる", 13.5, bold=True)
    bars(s, c, e, px, B, B - T, TEAL, c.max())
    s.line(L, B, R, B, op=0.45)
    for v in (50, 100, 150, 200, 250):
        if g.min() <= v <= g.max():
            s.text(px(v), B + 18, f"{v}", 11, anchor="middle", op=0.7)
    s.text(R + 8, B + 18, "妊娠期間 (日)", 11, op=0.75)
    s.line(px(med), T - 30, px(med), B, TEAL, 1.8, 0.9, dash="4 3")
    s.line(px(mean), T - 30, px(mean), B, RED, 1.8, 0.9, dash="4 3")
    s.text(px(mean) - 8, T - 34, f"平均 {mean:.1f}日", 11.5, anchor="end",
           bold=True, color=RED)
    s.text(px(med) + 8, T - 34, f"中央値 {med:.1f}日", 11.5, bold=True, color=TEAL)
    s.text(612, 120, f"歪度 {sk:.2f}".replace("-", "−"), 12.5, bold=True)
    s.text(612, 140, "ほぼ左右対称", 11.5, op=0.85)
    s.text(612, 170, f"体重は {skw:.1f}", 12, color=AMBER)
    s.text(612, 188, "（右に長い裾）", 11.5, color=AMBER, op=0.9)
    s.text(0, 296, f"平均と中央値の差は {abs(mean-med):.1f}日。"
           f"体重では平均が中央値の約2倍だったのに、同じデータセットの別の列では"
           f"ほとんど一致する。", 11.5, op=0.9)
    s.text(0, 318, "「このデータは平均を使ってよいか」は、列ごとに判断することになる。"
           "だからまずヒストグラムを見る。", 11.5, op=0.9)
    s.text(0, 334, "", 11, op=0.7)
    save("02_gest.svg", s)


if __name__ == "__main__":
    print("図A 体重のヒストグラム"); fig_hist()
    print("図B 外れ値と頑健性"); fig_robust()
    print("図C 下手さの形"); fig_loss()
    print("図D 妊娠期間"); fig_gest()
