# -*- coding: utf-8 -*-
"""第3回：分散のイメージ（偏差の矢印と2乗）／分散大・分散小 の図を作る"""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Hiragino Sans'
plt.rcParams['axes.unicode_minus'] = False

TEAL, RED, GRAY = '#00695c', '#e8503a', '#9e9e9e'
OUT = ['slides/data', 'docs/slides/data']

rng = np.random.default_rng(7)

# ── 図1：偏差 → 2乗 ───────────────────────────────
x = np.arange(1, 11)
y = np.array([163, 155, 170, 152, 168, 158, 166, 160, 148, 165], dtype=float)
m = y.mean()
dev = y - m

fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.3))

a = ax[0]
a.axhline(m, color='#1565c0', lw=2, zorder=1)
for xi, yi in zip(x, y):
    a.annotate('', xy=(xi, yi), xytext=(xi, m),
               arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.8))
a.scatter(x, y, s=190, color=RED, edgecolor='white', lw=1.5, zorder=3)
a.text(10.5, m + 0.7, '平均値', ha='right', va='bottom', fontsize=12, color='#1565c0')
a.set_title('① 偏差（矢印）　合計 = 0', fontsize=13, color=TEAL)
a.set_xlim(0.3, 10.7); a.set_ylim(144, 174)
a.set_xticks([]); a.set_ylabel('身長 (cm)', fontsize=11)
a.spines[['top', 'right']].set_visible(False)
a.text(5.5, 146.5, '上向きと下向きが打ち消し合って 0 になる',
       ha='center', fontsize=11.5, color=RED)

b = ax[1]
b.bar(x, dev**2, color=RED, alpha=.75, width=.62)
b.set_title(f'② 偏差を2乗　合計 = {(dev**2).sum():.1f}', fontsize=13, color=TEAL)
b.set_xlim(0.3, 10.7)
b.set_xticks([]); b.set_ylabel('偏差$^2$ (cm$^2$)', fontsize=11)
b.spines[['top', 'right']].set_visible(False)
b.text(5.5, (dev**2).max()*0.88,
       f'全部プラスになる → 平均すると分散\n{(dev**2).sum():.1f} ÷ (10−1) = {dev.var(ddof=1):.1f}',
       ha='center', fontsize=11.5, color=RED)
fig.tight_layout()
for d in OUT:
    fig.savefig(f'{d}/variance_deviation.png', dpi=150, facecolor='white')
plt.close(fig)
print('図1 偏差合計', round(dev.sum(), 10), '2乗和', (dev**2).sum(), '分散(n-1)', round(dev.var(ddof=1), 2))

# ── 図2：分散大・分散小 ─────────────────────────
MU = 158.0
big = MU + rng.normal(0, np.sqrt(60), 200)
sml = MU + rng.normal(0, np.sqrt(20), 200)
big = MU + (big - big.mean()) * np.sqrt(60 / big.var(ddof=1))
sml = MU + (sml - sml.mean()) * np.sqrt(20 / sml.var(ddof=1))
pb, ps = big[:10], sml[:10]

fig, ax = plt.subplots(2, 2, figsize=(11.5, 6.4))
for col, (pts, full, name) in enumerate([(pb, big, '分散大'), (ps, sml, '分散小')]):
    a = ax[0][col]
    a.axhline(MU, color='#1565c0', lw=2, zorder=1)
    for xi, yi in zip(np.arange(1, 11), pts):
        a.annotate('', xy=(xi, yi), xytext=(xi, MU),
                   arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.8))
    a.scatter(np.arange(1, 11), pts, s=170, color=RED, edgecolor='white', lw=1.5, zorder=3)
    a.text(10.5, MU + 0.8, '平均値', ha='right', va='bottom', fontsize=11, color='#1565c0')
    a.set_title(f'{name}（矢印が{"長い" if col == 0 else "短い"}）', fontsize=13, color=TEAL)
    a.set_xlim(0.3, 10.7); a.set_ylim(140, 176)
    a.set_xticks([]); a.set_yticks([145, 155, 165, 175])
    a.spines[['top', 'right']].set_visible(False)

    h = ax[1][col]
    h.hist(full, bins=np.arange(140, 178, 5), color='#cfd8dc', edgecolor='#607d8b')
    h.axvline(MU, color='#1565c0', lw=2)
    h.text(MU + 0.8, h.get_ylim()[1] * 0.88, '平均値', fontsize=11, color='#1565c0')
    h.set_title(f'分散 = {full.var(ddof=1):.0f}　'
                f'SD = {full.std(ddof=1):.1f} cm', fontsize=12.5, color=TEAL)
    h.set_xlim(140, 176); h.set_ylim(0, 95)
    h.set_xlabel('身長 (cm)', fontsize=11)
    h.set_ylabel('度数', fontsize=11)
    h.spines[['top', 'right']].set_visible(False)

fig.tight_layout()
for d in OUT:
    fig.savefig(f'{d}/variance_big_small.png', dpi=150, facecolor='white')
plt.close(fig)
print('図2 平均', round(big.mean(), 3), round(sml.mean(), 3),
      '分散', round(big.var(ddof=1), 2), round(sml.var(ddof=1), 2),
      'SD', round(big.std(ddof=1), 2), round(sml.std(ddof=1), 2))
