# -*- coding: utf-8 -*-
"""第09回（分散分析）の図。数値はすべてここで計算する。"""
import math, os
from itertools import combinations
import numpy as np, pandas as pd
from scipy import stats
from svgkit import Svg, RED, INDIGO, TEAL, AMBER

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
DATA = os.path.join(HERE, "..", "docs", "data", "primates.csv")
D = pd.read_csv(DATA)


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg.render())
    print(f"  -> out/{name}")


# ===== 図A：検定を繰り返すと偽陽性が増える ==============================
def simulate(ks, n=20, R=20000, seed=2026):
    rng = np.random.default_rng(seed)
    res = {}
    for k in ks:
        x = rng.normal(0, 1, (R, k, n))
        mean, var = x.mean(axis=2), x.var(axis=2, ddof=1)
        sig = np.zeros(R, bool)
        for i, j in combinations(range(k), 2):
            sp = np.sqrt(((n-1)*var[:, i] + (n-1)*var[:, j]) / (2*n-2))
            t = (mean[:, i] - mean[:, j]) / (sp * np.sqrt(2/n))
            sig |= 2*stats.t.sf(np.abs(t), 2*n-2) < 0.05
        res[k] = float(sig.mean())
    return res


def fig_multi():
    ks = list(range(2, 13))
    obs = simulate(ks)
    ind = {k: 1 - 0.95 ** (k*(k-1)//2) for k in ks}
    for k in (2, 3, 5, 10):
        print(f"  k={k} ペア{k*(k-1)//2}: 実測 {obs[k]*100:.1f}%  "
              f"独立仮定の式 {ind[k]*100:.1f}%")

    s = Svg(720, 372, "mc",
            "検定を繰り返すほど、まぐれの「発見」が増える",
            f"横軸は群の数、縦軸は「差がまったく無いのに、全ペアのt検定で最低1つが"
            f"有意になる割合」。実測（各群20個体・2万回）は3群で{obs[3]*100:.0f}%、"
            f"5群で{obs[5]*100:.0f}%、10群で{obs[10]*100:.0f}%まで上がる。"
            f"検定を独立と仮定した式 1−0.95^m はさらに上を行くが、"
            f"全ペア検定は同じ群のデータを使い回すので独立ではなく、"
            f"実測はこの式より低く出る。")
    L, R, T, B = 58, 560, 66, 258
    px = lambda k: L + (k - 2) / 10 * (R - L)
    py = lambda v: B - v * (B - T)
    s.text(0, 32, "差がまったく無いのに「どれかは有意」になる割合", 13.5, bold=True)
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        s.line(L, py(v), R, py(v), op=0.5 if v == 0 else 0.13)
        s.text(L - 8, py(v) + 4, f"{int(v*100)}%", 11, anchor="end", op=0.75)
    for k in range(2, 13, 2):
        s.text(px(k), B + 19, f"{k}", 11, anchor="middle", op=0.75)
    s.line(L, T, L, B, op=0.5)
    s.text(R + 14, B + 19, "群の数 k", 11.5, op=0.8)
    s.line(L, py(0.05), R, py(0.05), RED, 1, 0.6, dash="4 3")
    s.text(R - 4, py(0.05) - 8, "検定1回ぶんの 5%", 11, anchor="end", color=RED, op=0.9)
    s.path([(px(k), py(ind[k])) for k in ks], AMBER, 2.2, dash="6 4")
    s.path([(px(k), py(obs[k])) for k in ks], INDIGO, 2.6)
    for k in (3, 5, 10):
        s.circle(px(k), py(obs[k]), 4.4, INDIGO)
        if k == 3:   # 独立仮定の線とぶつかるので左に置く
            s.text(px(k) - 10, py(obs[k]) + 4, f"{obs[k]*100:.0f}%", 12,
                   anchor="end", bold=True, color=INDIGO)
        else:
            s.text(px(k), py(obs[k]) - 12, f"{obs[k]*100:.0f}%", 12,
                   anchor="middle", bold=True, color=INDIGO)
    s.line(574, 96, 604, 96, AMBER, 2.2, dash="6 4")
    s.text(610, 100, "検定が独立だと", 11.5)
    s.text(610, 115, "仮定した式", 11.5)
    s.text(610, 130, "1−0.95ᵐ", 11.5, op=0.8)
    s.line(574, 160, 604, 160, INDIGO, 2.6)
    s.text(610, 164, "実測（各群20個体・", 11.5)
    s.text(610, 179, "2万回）", 11.5)
    s.text(0, 302, f"3群で全ペアを検定すると、差が無くても {obs[3]*100:.0f}% は"
           f"「どれか有意」になる。10群なら {obs[10]*100:.0f}%。", 11.5, op=0.9)
    s.text(0, 324, "実測が式より低いのは、同じ群のデータを使い回していて"
           "検定どうしが独立でないため。式は増え方の勢いを示す目安である。",
           11.5, op=0.9)
    s.text(0, 346, f"（各群20個体・正規分布・2万回。等分散のt検定を両側5%で。"
           f"k=2 では理論どおり {obs[2]*100:.1f}% になる。）", 11, op=0.7)
    save("09_multi.svg", s)


# ===== 図B：F が大きいとき、1前後のとき ================================
def dotpanel(s, x0, w, groups, title, sub, col, top, bot, rng, fmt="{:.2f}"):
    """縦方向のドットプロット。groups は [(名前, 値の配列)]。"""
    vals = np.concatenate([v for _, v in groups])
    lo, hi = vals.min(), vals.max()
    pad = (hi - lo) * 0.12
    lo, hi = lo - pad, hi + pad
    py = lambda v: bot - (v - lo) / (hi - lo) * (bot - top)
    gm = vals.mean()
    s.text(x0, top - 34, title, 13, bold=True, color=col)
    s.text(x0, top - 17, sub, 11.5, op=0.8)
    s.line(x0, py(gm), x0 + w, py(gm), op=0.45, dash="5 3")
    s.text(x0 + w, py(gm) - 6, "全体平均", 10.5, anchor="end", op=0.7)
    step = w / len(groups)
    for i, (name, v) in enumerate(groups):
        cx = x0 + step * (i + 0.5)
        for u in v:
            s.circle(cx + rng.uniform(-step*0.3, step*0.3), py(u), 2.6, col, 0.5)
        m = v.mean()
        s.line(cx - step*0.36, py(m), cx + step*0.36, py(m), col, 2.6)
        s.text(cx, bot + 18, name, 10.5, anchor="middle", op=0.85)
        s.text(cx, bot + 32, f"n={len(v)}", 10, anchor="middle", op=0.6)
    s.line(x0, bot, x0 + w, bot, op=0.35)


def fig_fvalue():
    w = D.dropna(subset=["体重g"])
    g1 = [(n.replace("科", ""), np.log10(w.loc[w["科"] == n, "体重g"].values))
          for n in ("オマキザル科", "クモザル科", "コビトキツネザル科")]
    r = D.dropna(subset=["月降水量mm"])
    g2 = [(n.replace("科", ""), r.loc[r["科"] == n, "月降水量mm"].values)
          for n in ("オナガザル科", "クモザル科", "サキ科")]
    F1, p1 = stats.f_oneway(*[v for _, v in g1])
    F2, p2 = stats.f_oneway(*[v for _, v in g2])
    print(f"  体重（対数）  F={F1:.2f} p={p1:.1e}")
    print(f"  月降水量      F={F2:.2f} p={p2:.2f}")

    s = Svg(720, 378, "fv",
            "F が151のときと、0.08のときの見え方",
            f"左は3科の体重（常用対数）で F = {F1:.2f}。群の平均（太い横線）が"
            f"互いに大きく離れていて、群の中の散らばりではとても埋められない。"
            f"右は同じ枠組みで月降水量を見たもので F = {F2:.2f}。"
            f"平均はほとんど同じ高さに並び、群内の散らばりに完全に埋もれている。"
            f"F は「群の平均どうしの離れ方」を「群の中の散らばり」で割った比である。")
    rng = np.random.default_rng(9)
    s.text(0, 30, "F は「平均どうしの離れ方」を「群の中の散らばり」で割った比", 13.5,
           bold=True)
    dotpanel(s, 10, 320, g1, f"体重（常用対数）　F = {F1:.2f}",
             f"p = 3×10⁻²⁵　平均が大きく離れている", INDIGO, 108, 282, rng)
    dotpanel(s, 390, 320, g2, f"月降水量（mm）　F = {F2:.2f}",
             f"p = {p2:.2f}　平均は散らばりに埋もれている", TEAL, 108, 282, rng)
    s.text(0, 346, "同じ3群という形でも、平均の離れ方が群内の散らばりに対して"
           "大きいか小さいかで、F はこれだけ違う。", 11.5, op=0.9)
    s.text(0, 368, "（左右で縦軸の単位も目盛りも別。点は1種、太い横線が群の平均、"
           "破線が全体平均。）", 11, op=0.7)
    save("09_fvalue.svg", s)


# ===== 図C：ばらつきの分解 ==============================================
def fig_ss():
    w = D.dropna(subset=["体重g"])
    names = ("オマキザル科", "クモザル科", "コビトキツネザル科")
    g = [np.log10(w.loc[w["科"] == n, "体重g"].values) for n in names]
    allx = np.concatenate(g); m = allx.mean()
    sst = float(((allx - m) ** 2).sum())
    ssb = float(sum(len(x) * (x.mean() - m) ** 2 for x in g))
    ssw = float(sum(((x - x.mean()) ** 2).sum() for x in g))
    print(f"  SS全体={sst:.4f} = SS群間 {ssb:.4f} + SS群内 {ssw:.4f} "
          f"（和 {ssb+ssw:.4f}）  群間の割合 {ssb/sst*100:.1f}%")

    s = Svg(720, 388, "ss",
            "ばらつきを、群の中と群どうしに分ける",
            f"左は3科の体重（常用対数）。1つの点について、全体平均からのズレが"
            f"「その群の平均までのズレ（群間）」と「群の平均から点までのズレ（群内）」"
            f"の和にちょうど分かれる。右の帯はそれを全データで合計したもので、"
            f"総平方和 {sst:.4f} が群間 {ssb:.4f} と群内 {ssw:.4f} に"
            f"余りなく分かれている（群間が {ssb/sst*100:.1f}%）。")
    s.text(0, 30, "全体のばらつきは、群間と群内にちょうど分かれる", 13.5, bold=True)
    # 左：点と2本のズレ
    L, W, T, B = 10, 330, 72, 268
    vals = allx; lo, hi = vals.min() - 0.2, vals.max() + 0.2
    py = lambda v: B - (v - lo) / (hi - lo) * (B - T)
    rng = np.random.default_rng(11)
    step = W / 3
    s.line(L, py(m), L + W, py(m), RED, 1.6, 0.8, dash="5 3")
    s.text(L + W, py(m) - 7, f"全体平均 {m:.2f}", 11, anchor="end",
           bold=True, color=RED)
    pick = None
    for i, (nm, v) in enumerate(zip(names, g)):
        cx = L + step * (i + 0.5)
        skip = int(np.argmax(v)) if i == 1 else -1   # 強調する1種は別に描く
        for j, u in enumerate(v):
            if j == skip:
                continue
            s.circle(cx + rng.uniform(-step*0.28, step*0.28), py(u), 2.6,
                     INDIGO, 0.45)
        gmean = v.mean()
        s.line(cx - step*0.34, py(gmean), cx + step*0.34, py(gmean), TEAL, 2.6)
        s.text(cx, B + 18, nm.replace("科", ""), 10.5, anchor="middle", op=0.85)
        if i == 1:
            pick = (cx, gmean, float(v.max()))
    cx, gmean, top = pick
    xx = cx + step * 0.40
    s.circle(xx, py(top), 4.6, AMBER)
    s.line(xx, py(top), xx, py(gmean), AMBER, 2.2)
    s.line(xx, py(gmean), xx, py(m), RED, 2.2)
    s.text(xx + 8, (py(top) + py(gmean)) / 2 + 4, "群内のズレ", 11,
           bold=True, color=AMBER)
    s.text(xx + 8, (py(gmean) + py(m)) / 2 + 4, "群間のズレ", 11,
           bold=True, color=RED)
    s.line(L, B, L + W, B, op=0.35)
    s.text(L, B + 38, "ある1種のズレ ＝ 群内のズレ ＋ 群間のズレ", 11.5, op=0.9)
    # 右：合計の帯
    X, BW = 400, 300
    yb, hb = 110, 54
    wb = BW * ssb / sst
    s.rect(X, yb, wb, hb, fill=RED, fop=0.25, stroke=RED, sop=0.7, r=4)
    s.rect(X + wb, yb, BW - wb, hb, fill=AMBER, fop=0.25, stroke=AMBER,
           sop=0.7, r=4)
    s.text(X, yb - 14, f"総平方和 SS全体 ＝ {sst:.4f}", 12, bold=True)
    s.text(X + wb / 2, yb + 32, "群間", 12.5, anchor="middle", bold=True, color=RED)
    s.text(X + wb + (BW - wb) / 2, yb + 32, "群内", 12, anchor="middle",
           bold=True, color=AMBER)
    s.text(X, yb + 82, f"群間 {ssb:.4f}（{ssb/sst*100:.1f}%）", 12, color=RED)
    s.text(X, yb + 104, f"群内 {ssw:.4f}（{100-ssb/sst*100:.1f}%）", 12, color=AMBER)
    s.line(X, yb + 118, X + BW, yb + 118, op=0.4)
    s.text(X, yb + 140, f"合計 {ssb+ssw:.4f}", 12, bold=True)
    s.text(X, yb + 160, "総平方和と小数点以下14桁まで一致する", 11, op=0.75)
    s.text(0, 362, "交差項が消えるので、この分解には余りが出ない。"
           "「分散分析」という名前はこの等式に由来する。", 11.5, op=0.9)
    s.text(0, 382, "（3科の体重を常用対数で。点は1種、太い横線が群の平均。）",
           11, op=0.7)
    save("09_ss.svg", s)


if __name__ == "__main__":
    print("図A 多重比較"); fig_multi()
    print("図B Fの大小"); fig_fvalue()
    print("図C ばらつきの分解"); fig_ss()
