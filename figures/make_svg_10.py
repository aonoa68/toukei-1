# -*- coding: utf-8 -*-
"""第10回（回帰分析）の図。数値はすべてここで計算する。"""
import math, os
import numpy as np, pandas as pd
from svgkit import Svg, RED, INDIGO, TEAL, AMBER

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
D = pd.read_csv(os.path.join(HERE, "..", "docs", "data", "primates.csv"))
M = D.dropna(subset=["体重g", "行動圏km2"])
X = np.log10(M["体重g"].values)
Y = np.log10(M["行動圏km2"].values)
N = len(X)
B = np.cov(X, Y, ddof=1)[0, 1] / np.var(X, ddof=1)
A = Y.mean() - B * X.mean()
R2 = np.corrcoef(X, Y)[0, 1] ** 2
NAMES = M["学名"].values


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg.render())
    print(f"  -> out/{name}")


# ===== 図A：回帰直線と残差 =============================================
def fig_fit():
    res = Y - (A + B * X)
    i = int(np.argmax(res))
    print(f"  n={N} 傾き={B:.4f} 切片={A:.4f} R2={R2:.4f}")
    print(f"  最大の残差 {NAMES[i]} 実測{10**Y[i]:.1f}km2 "
          f"予測{10**(A+B*X[i]):.3f}km2 = {10**res[i]:.1f}倍")

    s = Svg(720, 392, "fit",
            "体重で行動圏を予測する ―― 直線と、そこからの縦のズレ",
            f"横軸は体重の常用対数、縦軸は行動圏の常用対数で、点は{N}種。"
            f"赤い直線が回帰直線で、傾き{B:.3f}・切片{A:.3f}、決定係数は{R2:.3f}である。"
            f"細い縦線が残差（実測と予測の差）で、最小二乗法はこの縦線の二乗和を"
            f"いちばん小さくする直線を選んでいる。"
            f"最も大きく外れているのはパタスモンキーで、予測の{10**res[i]:.0f}倍の"
            f"行動圏を使っている。")
    L, R, T, Bt = 62, 560, 64, 268
    xlo, xhi = X.min() - 0.15, X.max() + 0.15
    ylo, yhi = Y.min() - 0.2, Y.max() + 0.35
    px = lambda v: L + (v - xlo) / (xhi - xlo) * (R - L)
    py = lambda v: Bt - (v - ylo) / (yhi - ylo) * (Bt - T)
    s.text(0, 30, "最小二乗法は「縦のズレの二乗和」を最小にする直線を選ぶ", 13.5,
           bold=True)
    for v in range(2, 6):
        s.line(px(v), T, px(v), Bt, op=0.09)
        s.text(px(v), Bt + 19, f"{v}", 11, anchor="middle", op=0.7)
    for v in range(-4, 3):
        if ylo <= v <= yhi:
            s.line(L, py(v), R, py(v), op=0.09)
            s.text(L - 8, py(v) + 4, f"{v}", 11, anchor="end", op=0.7)
    s.line(L, Bt, R, Bt, op=0.4); s.line(L, T, L, Bt, op=0.4)
    s.text((L + R) / 2, Bt + 40, "体重 log10(g)", 11.5, anchor="middle", op=0.8)
    s.text(L - 8, T - 12, "行動圏 log10(km²)", 11, op=0.8)
    # 残差の縦線（間引いて描く）
    for j in range(0, N, 3):
        s.line(px(X[j]), py(Y[j]), px(X[j]), py(A + B * X[j]), RED, 0.8, 0.3)
    for j in range(N):
        s.circle(px(X[j]), py(Y[j]), 2.6, INDIGO, 0.5)
    s.path([(px(xlo), py(A + B * xlo)), (px(xhi), py(A + B * xhi))], RED, 2.4)
    # パタスモンキー
    s.circle(px(X[i]), py(Y[i]), 5.4, AMBER)
    s.line(px(X[i]), py(Y[i]), px(X[i]), py(A + B * X[i]), AMBER, 2, 0.9)
    s.text(px(X[i]) + 10, py(Y[i]) - 6, "パタスモンキー", 11.5, bold=True, color=AMBER)
    s.text(px(X[i]) + 10, py(Y[i]) + 10, f"予測の {10**res[i]:.0f}倍", 11.5, color=AMBER)
    s.text(576, 110, f"傾き {B:.3f}", 12.5, bold=True, color=RED)
    s.text(576, 130, f"切片 {A:.3f}".replace("-", "−"), 12.5, color=RED)
    s.text(576, 154, f"R² = {R2:.3f}", 12.5, bold=True)
    s.text(576, 174, f"n = {N}種", 11.5, op=0.8)
    s.text(576, 204, "細い縦線が", 11, op=0.8)
    s.text(576, 220, "残差（3つに", 11, op=0.8)
    s.text(576, 236, "1つを表示）", 11, op=0.8)
    s.text(0, 330, f"両方とも対数なので、傾き {B:.3f} は「体重が10倍になると"
           f"行動圏は約 {10**B:.1f}倍」という意味になる。", 11.5, op=0.95)
    s.text(0, 354, "残差の大きい点は「外れ」ではなく、モデルが捉えていない何かの"
           "合図である。パタスモンキーはサバンナで地上生活する。", 11.5, op=0.95)
    s.text(0, 386, "（体重・行動圏がそろう153種。どちらも常用対数で扱っている。）",
           11, op=0.7)
    save("10_fit.svg", s)


# ===== 図B：R²の罠 ======================================================
def fig_r2trap():
    ks = list(range(0, 51))

    def run(k, seed):
        rg = np.random.default_rng(seed)
        Xm = np.column_stack([np.ones(N), X] + [rg.normal(0, 1, N) for _ in range(k)])
        c, *_ = np.linalg.lstsq(Xm, Y, rcond=None)
        p = Xm @ c
        return 1 - ((Y - p) ** 2).sum() / ((Y - Y.mean()) ** 2).sum()

    runs = np.array([[run(k, 1000 + i) for k in ks] for i in range(60)])
    med = np.median(runs, axis=0)
    lo = np.percentile(runs, 10, axis=0)
    hi = np.percentile(runs, 90, axis=0)
    for k in (0, 1, 5, 20, 50):
        j = ks.index(k)
        print(f"  でたらめ{k}本: 中央値 {med[j]:.3f}（10〜90%点 "
              f"{lo[j]:.3f}〜{hi[j]:.3f}）")

    s = Svg(720, 400, "r2",
            "中身が乱数でも、変数を足せば R² は必ず上がる",
            f"横軸は行動圏と何の関係もない「でたらめな乱数の列」を足した本数、"
            f"縦軸は決定係数 R²。帯は60回くりかえしたときの10〜90%の幅、"
            f"太い線はその中央値。1本も足さないときの{med[0]:.3f}から、"
            f"50本足すと中央値で{med[50]:.3f}まで上がる。"
            f"R²は決して下がらない。当てはまりの良さは、良いモデルの証拠にならない。")
    L, R, T, Bt = 62, 560, 66, 262
    px = lambda k: L + k / 50 * (R - L)
    py = lambda v: Bt - (v - 0.4) / 0.45 * (Bt - T)
    s.text(0, 30, "足したのは、行動圏と何の関係もない乱数の列だけ", 13.5, bold=True)
    for v in (0.4, 0.5, 0.6, 0.7, 0.8):
        s.line(L, py(v), R, py(v), op=0.13)
        s.text(L - 8, py(v) + 4, f"{v:.1f}", 11, anchor="end", op=0.75)
    for k in (0, 10, 20, 30, 40, 50):
        s.text(px(k), Bt + 19, f"{k}", 11, anchor="middle", op=0.75)
    s.line(L, Bt, R, Bt, op=0.45); s.line(L, T, L, Bt, op=0.45)
    s.text((L + R) / 2, Bt + 40, "足した「でたらめな列」の本数", 11.5,
           anchor="middle", op=0.8)
    s.text(L - 8, T - 12, "R²", 11.5, op=0.8)
    pts = [f"{px(k):.1f},{py(v):.1f}" for k, v in zip(ks, hi)] + \
          [f"{px(k):.1f},{py(v):.1f}" for k, v in zip(reversed(ks), reversed(lo))]
    s.parts.append(f'<polygon points="{" ".join(pts)}" fill="{INDIGO}"'
                   f' fill-opacity="0.16" stroke="none"/>')
    s.path([(px(k), py(v)) for k, v in zip(ks, med)], INDIGO, 2.6)
    for k in (0, 50):
        j = ks.index(k)
        s.circle(px(k), py(med[j]), 4.6, RED)
        s.text(px(k) + (10 if k == 0 else -10), py(med[j]) + (16 if k == 0 else -12),
               f"{med[j]:.3f}", 12, anchor="start" if k == 0 else "end",
               bold=True, color=RED)
    s.text(576, 110, "帯は60回ぶんの", 11.5)
    s.text(576, 126, "10〜90%の幅", 11.5)
    s.text(576, 150, "太線は中央値", 11.5, bold=True, color=INDIGO)
    s.text(576, 182, f"n = {N}種に対して", 11.5, color=AMBER)
    s.text(576, 198, "変数50本", 11.5, bold=True, color=AMBER)
    s.text(0, 322, "当てはまりを上げたいだけなら、変数をたくさん入れればよい。"
           "だがそれは手元のデータに合わせただけで、未来の予測は良くならない。",
           11.5, op=0.95)
    s.text(0, 346, "だから「R²が高いから良いモデル」とは言えない。"
           "複雑さの代金をどう払うかが、次回（第11回 AIC）のテーマになる。",
           11.5, op=0.95)
    s.text(0, 380, "（本文の表は1回ぶんの実行例。ここでは乱数の種を変えて60回"
           "くりかえし、散らばりの幅と中央値を描いている。）", 11, op=0.7)
    save("10_r2trap.svg", s)


# ===== 図C：外挿の危険 =================================================
def fig_extrap():
    tests = [(1, "1gの霊長類"), (1_000_000, "1トンの霊長類"),
             (3_000_000, "アフリカゾウ（霊長類ですらない）")]
    for w, lab in tests:
        print(f"  体重{w:,}g → 予測 {10**(A+B*math.log10(w)):.4f} km² ({lab})")

    s = Svg(720, 398, "ex",
            "式はどんな数字を入れても答えを返す",
            f"横軸を1gから300万gまで広げて描いた図。"
            f"データが実際にある範囲は{10**X.min():.0f}gから{10**X.max():,.0f}gまでで、"
            f"図の中央の帯の部分しかない。"
            f"その外側に直線を伸ばせば、1gの霊長類にも3トンのゾウにも予測値が出るが、"
            f"確かめる相手が存在しない。外挿は外れ値とは別の問題である。")
    L, R, T, Bt = 62, 600, 70, 254
    xlo, xhi = -0.2, 6.7
    ylo, yhi = -4.6, 2.6
    px = lambda v: L + (v - xlo) / (xhi - xlo) * (R - L)
    py = lambda v: Bt - (v - ylo) / (yhi - ylo) * (Bt - T)
    s.text(0, 30, "データがあるのは、この帯の中だけ", 13.5, bold=True)
    # データのある範囲の帯
    s.rect(px(X.min()), T, px(X.max()) - px(X.min()), Bt - T,
           fill=TEAL, fop=0.10, stroke=TEAL, sop=0.45, r=3)
    s.text((px(X.min()) + px(X.max())) / 2, T - 10,
           f"データのある範囲　{10**X.min():.0f}g 〜 {10**X.max():,.0f}g", 11.5,
           anchor="middle", bold=True, color=TEAL)
    for v in range(0, 7):
        s.text(px(v), Bt + 19, f"{v}", 11, anchor="middle", op=0.7)
    for v in range(-4, 3, 2):
        s.line(L, py(v), R, py(v), op=0.09)
        s.text(L - 8, py(v) + 4, f"{v}", 11, anchor="end", op=0.7)
    s.line(L, Bt, R, Bt, op=0.4); s.line(L, T, L, Bt, op=0.4)
    s.text((L + R) / 2, Bt + 40, "体重 log10(g)", 11.5, anchor="middle", op=0.8)
    s.text(L - 8, T - 12, "行動圏 log10(km²)", 11, op=0.8)
    for j in range(N):
        s.circle(px(X[j]), py(Y[j]), 2.4, INDIGO, 0.45)
    s.path([(px(X.min()), py(A + B * X.min())),
            (px(X.max()), py(A + B * X.max()))], RED, 2.6)
    s.path([(px(xlo), py(A + B * xlo)), (px(X.min()), py(A + B * X.min()))],
           RED, 2, 0.75, dash="6 4")
    s.path([(px(X.max()), py(A + B * X.max())), (px(xhi), py(A + B * xhi))],
           RED, 2, 0.75, dash="6 4")
    for w, lab in tests:
        lx = math.log10(w); ly = A + B * lx
        s.circle(px(lx), py(ly), 4.6, AMBER)
        v = 10 ** ly
        txt = f"{v:,.1f} km²" if v >= 0.01 else f"{v:.4f} km²"
        if w == 1:
            s.text(px(lx) + 8, py(ly) + 4, f"{txt}（{lab}）", 11.5, color=AMBER)
        elif w == 1_000_000:
            s.text(px(lx), py(ly) - 12, txt, 11.5, anchor="middle",
                   bold=True, color=AMBER)
            s.text(px(lx), py(ly) - 28, lab, 11, anchor="middle", color=AMBER)
        else:   # ゾウは重なるので線の下に置く
            s.text(px(lx) + 10, py(ly) + 20, txt, 11.5, anchor="end",
                   bold=True, color=AMBER)
            s.text(px(lx) + 10, py(ly) + 36, lab, 11, anchor="end", color=AMBER)
    s.text(0, 316, "外れ値は「ありえない値か」を人間が判断できた。"
           "外挿は、出てきた数字を確かめる相手がそもそも存在しない。", 11.5, op=0.95)
    s.text(0, 340, "エラーは出ない。だから自分で範囲を見張るしかない。",
           11.5, op=0.95)
    s.text(0, 374, f"（回帰式は log(行動圏) = {A:.3f} + {B:.3f} × log(体重)。"
           f"破線はデータの外へ伸ばした部分。）".replace("-", "−"), 11, op=0.7)
    save("10_extrap.svg", s)


if __name__ == "__main__":
    print("図A 回帰直線と残差"); fig_fit()
    print("図B R²の罠"); fig_r2trap()
    print("図C 外挿"); fig_extrap()
