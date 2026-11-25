"""授業ページ用のインラインSVGを書くための最小の道具。

方針（既存の 05/06/07 の図と合わせる）：
- 色は currentColor を基本にし、ライト／ダークどちらのテーマでも読めるようにする。
- 強調だけ固定色（赤・藍・緑）を使う。
- <title> と <desc> を必ず書く（読み上げと、図が出ないときの代替）。
"""
FONT = "system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif"
RED, INDIGO, TEAL, AMBER = "#c62828", "#5c6bc0", "#00897b", "#ef6c00"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Svg:
    def __init__(self, w, h, uid, title, desc, maxw=None):
        self.w, self.h, self.uid = w, h, uid
        self.title, self.desc = title, desc
        self.maxw = maxw or w
        self.parts = []

    # --- 図形 ---
    def line(self, x1, y1, x2, y2, color="currentColor", width=1, op=1.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"'
            f' stroke="{color}" stroke-width="{width}" stroke-opacity="{op}"{d}/>')

    def rect(self, x, y, w, h, fill="none", stroke="currentColor", width=1,
             fop=1.0, sop=0.5, r=0):
        rr = f' rx="{r}" ry="{r}"' if r else ""
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{rr}'
            f' fill="{fill}" fill-opacity="{fop}" stroke="{stroke}"'
            f' stroke-width="{width}" stroke-opacity="{sop}"/>')

    def circle(self, cx, cy, r, fill="currentColor", op=1.0):
        self.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"'
                          f' fill="{fill}" fill-opacity="{op}"/>')

    def path(self, pts, color="currentColor", width=2, op=1.0, dash=None):
        d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color}"'
                          f' stroke-width="{width}" stroke-opacity="{op}"{da}/>')

    def text(self, x, y, s, size=12, anchor="start", bold=False, color="currentColor",
             op=1.0):
        w = ' font-weight="bold"' if bold else ""
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}"'
            f'{w} fill="{color}" fill-opacity="{op}">{esc(s)}</text>')

    def arrow(self, x1, y1, x2, y2, color="currentColor", width=1.5, op=0.8):
        """矢印（終点に三角をひとつ）。"""
        import math
        self.line(x1, y1, x2, y2, color, width, op)
        a = math.atan2(y2 - y1, x2 - x1)
        L, S = 9, 0.42
        p = [(x2, y2),
             (x2 - L * math.cos(a - S), y2 - L * math.sin(a - S)),
             (x2 - L * math.cos(a + S), y2 - L * math.sin(a + S))]
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in p)
        self.parts.append(f'<polygon points="{d}" fill="{color}" fill-opacity="{op}"/>')

    # --- 出力 ---
    def render(self):
        t, d = f"{self.uid}t", f"{self.uid}d"
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}"'
                f' role="img" aria-labelledby="{t} {d}"'
                f' style="width:100%;height:auto;max-width:{self.maxw}px;display:block;'
                f'margin:0.8em auto" font-family="{FONT}" font-size="13">')
        return (head + f'<title id="{t}">{esc(self.title)}</title>'
                + f'<desc id="{d}">{esc(self.desc)}</desc>'
                + "".join(self.parts) + "</svg>")
