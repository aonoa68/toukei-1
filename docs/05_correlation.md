# 第05回　相関と因果

**10/27（火）Ⅱ講 10:35〜12:15・B402教室**

> 「相関がある」と「原因である」は、まったく違う

---


<!-- LINKS:START -->
!!! info "今日のリンク"
    - [📊 スライドを開く](slides/05.html)
    - [📓 Colabノートを開く（05_correlation.ipynb）](https://colab.research.google.com/github/aonoa68/toukei-1/blob/main/colab/05_correlation.ipynb)
    - [📝 課題を提出する（Moodle・第5回）](https://moodle.hokusei.ac.jp/mod/assign/view.php?id=990625)
    - 課題の本文は**このページの末尾**にあります
    - [🤖 NotebookLMで復習する](https://notebook.google.com/notebook/1866d439-994f-4265-894f-112d31f39e30)（この回の内容をAIに質問できます）
<!-- LINKS:END -->

!!! tip "考え方をガイドで確かめる"
    この回の考え方は、統計の考え方ガイドの[「相関と因果」](https://aonoa68.github.io/teaching/guide/correlation/)、[「グラフで見る」](https://aonoa68.github.io/teaching/guide/visualize/)でも解説しています。霊長類のデータを動かしながら確かめられます。

## この回のゴール

- 散布図と相関係数 r で2変数の関係を読める
- **相関 ≠ 因果**であることを、交絡・逆因果・偶然の観点から説明できる
- 相関を見たときに「対抗仮説（第三の変数）」を立てて批判的に検証できる
- **発展**：\( r \) が標準化した値の積の平均であることと、\( -1 \le r \le 1 \) を、自分で導ける
- **発展**：「体重を統制する（偏相関）」が何を引き算しているのかを、標準化だけで導ける

到達目標との対応：**G1（記述）・G2（批判的検証の入口）**。

---

## 前回の答案から

第4回の記述（パートB・60点）は、10/25時点の69名で**満点36名（52%）／平均55.7点**だった。
パートAの小テストは77名中70名が満点。初めてコードを書いた回としては上出来である。

!!! success "まず、配布ノートの不具合をお詫びする"
    `print("妊娠期間日 標準偏差", df["妊娠期間日"].____().round(1), "日")` という形が残っていた。
    `.std()` が返すのは**1個の数値（float）**で、列まるごと（Series）ではない。
    floatには `.round()` が無いので `'float' object has no attribute 'round'` が出る。
    **10名がここで詰まった。ノート側の間違いで、皆さんのミスではない**（10/20に修正済み）。

    そのうえで、**4名が型の違いまで自力で突き止めた**。
    「Seriesには `.round()` があるが、計算後の単一の数値には無い」――正しい診断である。
    直し方は、組み込み関数で囲む `round(df["妊娠期間日"].std(), 1)`。

    **板書**：`df["列"]` → Series（列まるごと）／`df["列"].std()` → float（1個の数値）

!!! warning "① 直したあとに出た数値を書かなかった（69名中30名）"
    引用が無くて点が止まった人が**43%**。第3回の25%から増えた。内容が悪いのではない。
    B2が「エラーの原因と解決」を聞く問題だったので、**原因を特定したところで話が終わって**しまった。

    > 列名を間違えるとエラーが起きるため計算ができなかった。もう一度列名を確認し、修正した

    直ったのは分かる。**だが何が出たのかが書かれていない。**
    「直したら平均5880.9gが出た」の一言があれば満点だった。

    **「直った」で終わらせず、出力を見るところまでを1セットにする。**
    これはエラー処理の作法でもある。直ったつもりで値がおかしい、はよくある。

!!! warning "② `.mode()` が返す値を「典型値」と読んでしまう"
    今回いちばん良かった答案を挙げる。

    > 最頻値（一腹産子数）**1.01** は、一回の出産で1.01頭生まれる種が多い、という意味に見える。
    > しかし実際には、**一腹産子数として1.01という値が記録されている種が最も多かった**ことを表している

    `.mode()` は**記録値の重複を数えて最多のもの**を返すだけで、分布の山とは別物である。
    体重の最頻値 **992.4g** も、**6種で最多**というだけのこと。
    同じ留保を書けた人は10名ほどいた。

    **「数字が出た」と「その数字が何を表している」は別。**これが今日の入口になる。

!!! warning "③ 手計算のほうが正確だ、と書いた"
    > 手計算は、値を求める正確さにおいて役立ち、コードは値を求める速さで役に立つ

    **逆である。**376種の体重を電卓で足せば、どこかで打ち間違える。
    コードの強みは速さだけでなく、**同じ処理を何度でも間違いなく繰り返せること**にある。
    手計算の利点は正確さではなく、**仕組みが見えること**である。

!!! danger "④ B2が感想で終わった（2名）"
    > 頻繁にエラーが発生していたので、目的意識をしっかり持っていくようにしたい

    どのコードで、どの文字が、どう間違っていたのかが分からない。
    次の4点を書く。**場所・原因・直し方・出た数値。**

    > 穴埋め①で `df["体重ｇ"]` とgを全角で打って KeyError が出た。半角に直したら先頭の 4749.96 が表示された

### 今日につながること

前回は「機械が出した数字に、**何の数字で、単位は何で、それは信じてよいのか**というラベルを貼るのが人間の仕事」という話だった。

今日は、そのラベルの中でもいちばん間違えやすいものを扱う。**「この2つには関係がある」というラベル**である。

`r = 0.657` という数字は、コードが一瞬で出してくれる。だが**それが「原因と結果」なのかどうかは、画面には出ない。**
今日は、同じ `r` を出したあとで**体重をそろえて計算し直す**と 0.051 まで落ちる例を見る。
数字は何も嘘をついていない。読み方のほうが間違っていたのである。

---

## 1. フック：この相関を信じる？

- 「**アイスの売上**が増えると**水難事故**も増える」――アイスを禁止すれば事故は減る？
- 「**チョコ消費量**が多い国ほど**ノーベル賞**が多い」――チョコで頭が良くなる？

相関は本物。でも結論はばかげている。**なぜそうなるのか**を、霊長類データで解き明かす。

そして今日は、**ばかげているとすぐには分からない例**を扱う。そちらが本番である。

---

## 2. 散布図と相関係数 r

2つの量の関係は、点を打った**散布図**で見るのが基本。その「直線的な関係の強さ」を1つの数にしたのが **相関係数 r**（−1〜+1）。

| r | 意味 |
|---|---|
| +1 に近い | 片方が増えると他方も増える（右上がり） |
| −1 に近い | 片方が増えると他方は減る（右下がり） |
| 0 に近い | 直線的な関係がない |

!!! note "何桁にもまたがる量は対数で見る"
    体重・行動圏などは種によって数千倍違う。第3回でやったとおり、こういう量は**対数の目盛り**で扱う（そうしないとゴリラ1種が図を支配し、アンスコムのIV型になる）。以下の r はすべて対数変換後の値。

**体重 と 行動圏**：r ≈ **0.68**（n=153種）。体の大きい種ほど広い範囲を使う ―― 大きい動物はたくさん食べる必要があるから、というのは**納得のいく**関係だ。

???+ note "導出①：相関係数 r は「標準化した値の積の平均」である"

    2つの変数を、それぞれ**標準化**する。\( z_{x_i} = (x_i-\bar{x})/s_x \)、\( z_{y_i} = (y_i-\bar{y})/s_y \)。標準化すると平均0・標準偏差1になり、**単位が消える**（第3回の偏差値と同じ操作）。

    r の定義は、共分散を両者の標準偏差で割ったものである。

    $$ r \;=\; \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{s_x s_y} $$

    分母の \( s_x s_y \) を、分子の2つの因子に1つずつ配ると、

    $$ r \;=\; \frac{1}{n}\sum_{i=1}^{n} \frac{x_i-\bar{x}}{s_x}\cdot\frac{y_i-\bar{y}}{s_y} \;=\; \frac{1}{n}\sum_{i=1}^{n} z_{x_i} z_{y_i} $$

    つまり r は「**標準化した2つの値の積の平均**」である。両方とも平均より上（または両方とも下）の個体は積が正、片方だけ上の個体は積が負。r はその符号つきの積をならしたものだ。

    ここから「**r は単位に依存しない**」が出る。体重を g から kg に直しても、標準化の段階で倍率が消えるので r は変わらない。上の注記で対数に直すと r が変わるのは、対数変換が単なる倍率変更ではなく、値の**並び方**そのものを変えるからである。

    **数値で確かめる**：体重 × 行動圏（ともに対数、n=153）では、共分散を割る定義でも、標準化した積の平均でも、どちらも r = 0.6799 になる。

    **使った数学**：平均・標準偏差の定義（微I）、総和の記号操作と定数の括り出し（線I）。

???+ note "導出②：なぜ r は −1 と +1 の間に収まるのか"

    **二乗は負にならない。**必要なのはこれだけである。

    標準偏差1に揃えた定義から \( \sum z_{x_i}^2 = n \)、\( \sum z_{y_i}^2 = n \)。また導出①より \( \sum z_{x_i} z_{y_i} = nr \)。

    差の二乗和を展開すると、

    $$ \sum_{i=1}^{n}(z_{x_i}-z_{y_i})^2 \;=\; \sum z_{x_i}^2 - 2\sum z_{x_i}z_{y_i} + \sum z_{y_i}^2 \;=\; n - 2nr + n \;=\; 2n-2nr $$

    左辺は二乗の和だから0以上。よって \( 2n-2nr \ge 0 \)、すなわち **\( r \le 1 \)**。

    同じように和の二乗和を展開すると \( \sum (z_{x_i}+z_{y_i})^2 = 2n+2nr \ge 0 \) で、**\( r \ge -1 \)**。合わせて \( -1 \le r \le 1 \) が出る。

    **等号はいつ成り立つか。**\( r=1 \) は \( \sum(z_{x_i}-z_{y_i})^2 = 0 \)、つまりすべての個体で \( z_{x_i}=z_{y_i} \) のときだけ。標準化した値が完全に一致する、すなわち y が x の**正の一次式**で書けるときである。\( r=-1 \) は \( z_{x_i}=-z_{y_i} \) で、負の傾きの直線。**「r = ±1 は完全な直線関係」という言い方は、この等号条件から来ている。**

    **数値で確かめる**：体重 × 行動圏（対数、n=153、r=0.6799）では \( \sum(z_x-z_y)^2 = 97.95 \) で、\( 2n-2nr = 97.95 \)。一致する。そしてこれが0より大きいぶんだけ、r は1に届いていない。

    !!! note "r が測っているのは直線関係の強さだけ"
        この導出が保証するのは「r が −1 から 1 に収まること」と「両端が直線に対応すること」であって、**r の大小がどちらを原因と見なすべきかは一切語らない**。交絡があれば r は大きく出るし（§4）、直線でない関係なら r は小さく出る（§5）。導出は「r が何を測っているか」を正確にするためのものであり、因果の判断は式の外側の問題である。

    **使った数学**：二乗の非負性、展開と総和の整理（微I・線I）。

---

## 3. 「乳離れが遅い種ほど、広く動きまわる」？

`離乳日齢`（子が乳離れするまでの日数）と `行動圏km2` の相関：r ≈ **0.66**（n=97種）。

さきほどの体重と行動圏（0.68）とほとんど変わらない強さである。

「**子育て期間が長い種ほど、広い行動圏を必要とする**」――もっともらしい。生態学の論文の見出しになりそうだし、理屈も後付けできる（長く子を連れて歩くから広い範囲を使うのだろう、など）。

だが――**本当に離乳の遅さが原因か？**　ここで立ち止まるのが統計の思考。

---

## 4. 交絡を疑え ―― 第三の変数

「乳離れが遅い種」とは、どんな種か。**大きい種**である。そして大きい種は行動圏も広い。確かめると：

- 離乳日齢 と 体重 の相関：r ≈ **0.85**（ほとんど同じことを測っていると言えるほど強い）

```
        （体の大きさ）
          ／       ＼
     離乳が遅い    行動圏が広い
```

チンパンジー（45kg）は離乳まで1,261日＝3年半かかり、行動圏は10.85km²。ネズミキツネザル（48g）は離乳40日、行動圏0.01km²。**どちらの列も、体の大きさが動かしている。**これが **交絡（confounding）** だ。

### 確かめ方：体重を統制する（偏相関）

| 離乳日齢と行動圏 | r |
|---|---|
| 単純な相関 | 0.657 |
| **体重を統制後** | **0.051（ほぼ0）** |

!!! success "離乳の効果は消えた"
    アイスと水難事故（犯人は「気温」）、チョコとノーベル賞（犯人は「経済的豊かさ」）と同じ構造。
    **相関を見たら、因果を結論する前に『隠れた第三の変数（交絡）』を疑う。**

???+ note "導出③：「体重を統制する」とは、何を引き算しているのか（偏相関）"

    ノートブックのこのセルは `np.linalg.lstsq` ―― **最小二乗法** ―― を呼んでいる。これは**第10回の回帰の先取り**なので、いまはコードの中身を書けなくてよい。出てきた2つの数字（0.657 と 0.051）を読み比べられれば十分である。

    !!! info "先に定義"
        **偏相関（partial correlation）** \( r_{xy \mid w} \)：第三の変数 \( w \) で説明できる分を \( x \) と \( y \) の**両方から引き**、その**残り同士でとった相関**のこと。「\( w \) を統制したときの \( x \) と \( y \) の相関」と言うときの、その相関である。

        以下は、この「説明できる分」とは何で、引き算の結果どういう式になるのかを導くものである。

    ノートブックが内部で何をしているのかは、**第3回の標準化と、導出①②で出した事実だけ**で追える。回帰の公式は要らない。記号も導出①②と同じ ―― 総和 \( \sum \) のまま進める。

    **ステップ0：道具をそろえる。**

    3つの量 ―― 離乳日齢 \( x \)・行動圏 \( y \)・体重 \( w \)（すべて対数）―― を**標準化**して \( z_{x_i}, z_{y_i}, z_{w_i} \) とする。導出①②で確かめたことを、そのまま持ってくる。

    | 事実 | 式 | 出どころ |
    |---|---|---|
    | 標準化した値の平均は0 | \( \sum z_{x_i} = 0 \)（他も同様） | 第3回・導出① |
    | 標準化した値の二乗和は n | \( \sum z_{x_i}^2 = n \)（他も同様） | 導出② |
    | 積の和は n×相関 | \( \sum z_{x_i} z_{y_i} = n\,r_{xy} \) | 導出① |

    3つめは、任意の組について成り立つ。つまり \( \sum z_{x_i} z_{w_i} = n\,r_{xw} \)、\( \sum z_{y_i} z_{w_i} = n\,r_{yw} \) も使える。**これだけが材料である。**

    **ステップ1：体重で説明できる分を引いた「残り」を作る。**

    各個体 \( i \) について、\( z_{x_i} \) から \( a\,z_{w_i} \) を引いた残りを

    $$ e_{x_i} \;=\; z_{x_i} - a\,z_{w_i} $$

    と書く。体重が大きいほど離乳も遅いのだから、体重ぶんを \( a \) 倍して差し引いてやる、という操作である。係数 \( a \) はまだ決まっていない。

    まず、残りの平均は0のままである（あとで使う）。

    $$ \sum e_{x_i} \;=\; \sum z_{x_i} - a\sum z_{w_i} \;=\; 0 - a\cdot 0 \;=\; 0 $$

    **ステップ2：残りのばらつきを、a の式として書く。**

    \( a \) は「**引いたあとに残るばらつきが最小**」になるように決めたい。そこで残りの二乗和を展開する。導出②と同じ、二乗を展開して項ごとに和をとるだけである。

    $$ \sum e_{x_i}^2 \;=\; \sum \left(z_{x_i} - a\,z_{w_i}\right)^2 \;=\; \sum z_{x_i}^2 \;-\; 2a\sum z_{x_i} z_{w_i} \;+\; a^2 \sum z_{w_i}^2 $$

    ステップ0の表を、3つの和に1つずつ代入する。

    $$ \sum e_{x_i}^2 \;=\; n \;-\; 2a\cdot n\,r_{xw} \;+\; a^2\cdot n \;=\; n\left(1 - 2a\,r_{xw} + a^2\right) $$

    **ステップ3：平方完成して、最小になる a を見つける。**

    かっこの中は \( a \) についての二次式である。\( a \) を含む項をまとめて平方完成する。

    $$ a^2 - 2a\,r_{xw} + 1 \;=\; \underbrace{\left(a^2 - 2a\,r_{xw} + r_{xw}^2\right)}_{(a-r_{xw})^2} - r_{xw}^2 + 1 \;=\; (a - r_{xw})^2 + \left(1 - r_{xw}^2\right) $$

    第1項は二乗だから負にならず、**\( a = r_{xw} \) のときだけ0**になる。第2項は \( a \) を含まない定数である。したがって

    - 最小になるのは \( a = r_{xw} \) のとき
    - そのときの残りのばらつきは \( \sum e_{x_i}^2 = n\left(1 - r_{xw}^2\right) \)

    **最適な係数が、相関係数そのものになった。** これが標準化の効きどころである。単位をそろえておいたから、「どれだけ引けばよいか」が r で書けてしまう。

    行動圏のほうも、文字を入れ替えるだけでまったく同じ計算になる。

    $$ e_{y_i} = z_{y_i} - r_{yw}\,z_{w_i}, \qquad \sum e_{y_i}^2 = n\left(1 - r_{yw}^2\right) $$

    **ステップ4：残り同士の積の和を計算する（ここが山場）。**

    \( e_x \) と \( e_y \) の積の和を、**かっこを展開して4つの項に分ける**。

    $$ \sum e_{x_i} e_{y_i} \;=\; \sum \left(z_{x_i} - r_{xw} z_{w_i}\right)\left(z_{y_i} - r_{yw} z_{w_i}\right) $$

    $$ =\; \sum z_{x_i} z_{y_i} \;-\; r_{yw}\sum z_{x_i} z_{w_i} \;-\; r_{xw}\sum z_{w_i} z_{y_i} \;+\; r_{xw} r_{yw}\sum z_{w_i}^2 $$

    4つの和に、ステップ0の表を1つずつ代入する。

    | 項 | 代入する和 | 結果 |
    |---|---|---|
    | 第1項 | \( \sum z_{x_i} z_{y_i} = n\,r_{xy} \) | \( +n\,r_{xy} \) |
    | 第2項 | \( \sum z_{x_i} z_{w_i} = n\,r_{xw} \) | \( -n\,r_{xw} r_{yw} \) |
    | 第3項 | \( \sum z_{w_i} z_{y_i} = n\,r_{yw} \) | \( -n\,r_{xw} r_{yw} \) |
    | 第4項 | \( \sum z_{w_i}^2 = n \) | \( +n\,r_{xw} r_{yw} \) |

    第2項と第3項で**同じものを2回引き**、第4項で**1回足している**。差し引き、1回ぶんだけ引いたことになる。

    $$ \sum e_{x_i} e_{y_i} \;=\; n\,r_{xy} - n\,r_{xw}r_{yw} - n\,r_{xw}r_{yw} + n\,r_{xw}r_{yw} \;=\; n\left(r_{xy} - r_{xw} r_{yw}\right) $$

    **ステップ5：残り同士の相関を作る。**

    「体重を統制した相関」とは、**残り \( e_x \) と残り \( e_y \) の相関**のことである。相関係数の定義（導出①）を、平均0の量どうしに当てはめると

    $$ r_{xy \mid w} \;=\; \frac{\sum e_{x_i} e_{y_i}}{\sqrt{\sum e_{x_i}^2}\,\sqrt{\sum e_{y_i}^2}} $$

    （分母が標準偏差の役をしている。**ステップ1で平均が0のままだと確かめておいたので、偏差を取り直す必要がない。**）ステップ2〜4の結果を入れる。

    $$ r_{xy \mid w} \;=\; \frac{n\left(r_{xy} - r_{xw} r_{yw}\right)}{\sqrt{n\left(1-r_{xw}^2\right)}\,\sqrt{n\left(1-r_{yw}^2\right)}} $$

    分母の2つの平方根をかけると \( \sqrt{n}\times\sqrt{n}=n \) が出るので、**n が約分されて消える**。

    $$ r_{xy \mid w} \;=\; \frac{r_{xy} - r_{xw} r_{yw}}{\sqrt{(1-r_{xw}^2)(1-r_{yw}^2)}} $$

    これが **偏相関** である。**標本の大きさ n がきれいに消えた**ことに注意したい。偏相関は、3つの相関係数だけから計算できる。

    **ここまでを図で見る。**

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 344" role="img" aria-labelledby="t t2" style="width:100%;height:auto;max-width:720px;display:block;margin:0.6em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="t">体重で説明できる分を引くと何が残るか</title><desc id="t2">左：離乳日齢を体重に対して描くと強い関係があり、直線からの縦のずれが「残り」である。右：離乳と行動圏それぞれの残り同士を描くと、関係はほとんど残らない。</desc><text x="60.0" y="32.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">① 体重で説明できる分（傾き r = 0.854）</text><line x1="60.0" y1="62.0" x2="60.0" y2="252.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><line x1="60.0" y1="252.0" x2="250.0" y2="252.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><line x1="60.0" y1="157.0" x2="250.0" y2="157.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.2"/><line x1="155.0" y1="62.0" x2="155.0" y2="252.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.2"/><line x1="60.0" y1="238.2" x2="250.0" y2="75.8" stroke="#c62828" stroke-width="2"/><line x1="138.4" y1="187.0" x2="138.4" y2="171.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="144.7" y1="171.5" x2="144.7" y2="165.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="168.4" y1="143.8" x2="168.4" y2="145.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="118.7" y1="178.5" x2="118.7" y2="188.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="150.1" y1="149.8" x2="150.1" y2="161.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="127.4" y1="162.4" x2="127.4" y2="180.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="149.9" y1="175.4" x2="149.9" y2="161.4" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="120.9" y1="212.7" x2="120.9" y2="186.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="176.3" y1="143.2" x2="176.3" y2="138.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="177.3" y1="126.9" x2="177.3" y2="138.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="114.1" y1="188.7" x2="114.1" y2="192.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="92.3" y1="213.1" x2="92.3" y2="210.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="150.3" y1="165.8" x2="150.3" y2="161.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="183.2" y1="136.1" x2="183.2" y2="132.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="228.5" y1="119.3" x2="228.5" y2="94.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="140.2" y1="166.9" x2="140.2" y2="169.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="150.8" y1="151.2" x2="150.8" y2="160.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="172.2" y1="134.9" x2="172.2" y2="142.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="196.7" y1="116.5" x2="196.7" y2="121.4" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="153.5" y1="177.3" x2="153.5" y2="158.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="169.7" y1="142.2" x2="169.7" y2="144.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="140.4" y1="196.4" x2="140.4" y2="169.4" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="145.2" y1="160.6" x2="145.2" y2="165.4" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="128.9" y1="177.5" x2="128.9" y2="179.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="131.4" y1="209.1" x2="131.4" y2="177.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="152.3" y1="177.1" x2="152.3" y2="159.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="157.2" y1="168.4" x2="157.2" y2="155.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="154.4" y1="157.1" x2="154.4" y2="157.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="118.0" y1="161.3" x2="118.0" y2="188.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="170.4" y1="150.1" x2="170.4" y2="143.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="168.5" y1="129.1" x2="168.5" y2="145.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="146.5" y1="165.4" x2="146.5" y2="164.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="87.1" y1="222.0" x2="87.1" y2="215.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="169.9" y1="152.1" x2="169.9" y2="144.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="189.9" y1="125.7" x2="189.9" y2="127.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="121.3" y1="188.4" x2="121.3" y2="185.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="133.0" y1="186.5" x2="133.0" y2="175.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="211.1" y1="126.3" x2="211.1" y2="109.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="115.0" y1="182.7" x2="115.0" y2="191.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="150.1" y1="145.3" x2="150.1" y2="161.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="166.3" y1="147.3" x2="166.3" y2="147.4" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="140.7" y1="154.8" x2="140.7" y2="169.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="185.7" y1="161.4" x2="185.7" y2="130.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="160.2" y1="163.3" x2="160.2" y2="152.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="117.2" y1="179.8" x2="117.2" y2="189.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="166.4" y1="149.3" x2="166.4" y2="147.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="120.6" y1="196.4" x2="120.6" y2="186.4" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="165.7" y1="152.2" x2="165.7" y2="147.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="135.5" y1="183.4" x2="135.5" y2="173.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="130.7" y1="171.1" x2="130.7" y2="177.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="188.7" y1="131.0" x2="188.7" y2="128.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="152.1" y1="156.5" x2="152.1" y2="159.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="221.1" y1="95.9" x2="221.1" y2="100.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="140.5" y1="163.4" x2="140.5" y2="169.4" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="128.3" y1="187.4" x2="128.3" y2="179.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="113.4" y1="158.1" x2="113.4" y2="192.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="197.8" y1="130.7" x2="197.8" y2="120.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="108.6" y1="222.6" x2="108.6" y2="196.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="147.6" y1="150.2" x2="147.6" y2="163.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="148.6" y1="194.5" x2="148.6" y2="162.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="137.9" y1="154.0" x2="137.9" y2="171.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="143.8" y1="206.8" x2="143.8" y2="166.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="176.9" y1="139.8" x2="176.9" y2="138.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="252.5" y1="51.9" x2="252.5" y2="73.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="131.6" y1="179.9" x2="131.6" y2="177.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="180.6" y1="132.9" x2="180.6" y2="135.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="140.9" y1="157.3" x2="140.9" y2="169.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="142.4" y1="146.2" x2="142.4" y2="167.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="134.7" y1="167.4" x2="134.7" y2="174.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="150.2" y1="145.2" x2="150.2" y2="161.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="188.4" y1="121.7" x2="188.4" y2="128.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="171.6" y1="131.8" x2="171.6" y2="142.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="180.7" y1="144.1" x2="180.7" y2="135.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="204.4" y1="112.2" x2="204.4" y2="114.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="194.7" y1="112.7" x2="194.7" y2="123.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="168.7" y1="129.0" x2="168.7" y2="145.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="154.5" y1="103.9" x2="154.5" y2="157.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="158.1" y1="152.0" x2="158.1" y2="154.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="158.6" y1="143.8" x2="158.6" y2="153.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="147.1" y1="153.7" x2="147.1" y2="163.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="131.9" y1="194.4" x2="131.9" y2="176.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="128.3" y1="181.6" x2="128.3" y2="179.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="151.8" y1="168.4" x2="151.8" y2="159.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="113.1" y1="184.7" x2="113.1" y2="192.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="146.5" y1="188.6" x2="146.5" y2="164.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="199.6" y1="109.7" x2="199.6" y2="118.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="167.0" y1="131.6" x2="167.0" y2="146.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="162.4" y1="157.8" x2="162.4" y2="150.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="119.7" y1="171.5" x2="119.7" y2="187.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="123.7" y1="171.6" x2="123.7" y2="183.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="188.8" y1="153.4" x2="188.8" y2="128.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="159.4" y1="177.2" x2="159.4" y2="153.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="146.8" y1="156.8" x2="146.8" y2="164.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="195.2" y1="98.6" x2="195.2" y2="122.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="138.7" y1="168.0" x2="138.7" y2="170.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="186.2" y1="137.0" x2="186.2" y2="130.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><line x1="207.8" y1="98.2" x2="207.8" y2="111.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.45"/><circle cx="138.4" cy="187.0" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="144.7" cy="171.5" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="168.4" cy="143.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="118.7" cy="178.5" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="150.1" cy="149.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="127.4" cy="162.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="149.9" cy="175.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="120.9" cy="212.7" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="176.3" cy="143.2" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="177.3" cy="126.9" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="114.1" cy="188.7" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="92.3" cy="213.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="150.3" cy="165.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="183.2" cy="136.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="228.5" cy="119.3" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="140.2" cy="166.9" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="150.8" cy="151.2" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="172.2" cy="134.9" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="196.7" cy="116.5" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="153.5" cy="177.3" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="169.7" cy="142.2" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="140.4" cy="196.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="145.2" cy="160.6" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="128.9" cy="177.5" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="131.4" cy="209.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="152.3" cy="177.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="157.2" cy="168.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="154.4" cy="157.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="118.0" cy="161.3" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="170.4" cy="150.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="168.5" cy="129.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="146.5" cy="165.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="87.1" cy="222.0" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="169.9" cy="152.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="189.9" cy="125.7" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="121.3" cy="188.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="133.0" cy="186.5" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="211.1" cy="126.3" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="115.0" cy="182.7" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="150.1" cy="145.3" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="166.3" cy="147.3" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="140.7" cy="154.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="185.7" cy="161.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="160.2" cy="163.3" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="117.2" cy="179.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="166.4" cy="149.3" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="120.6" cy="196.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="165.7" cy="152.2" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="135.5" cy="183.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="130.7" cy="171.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="188.7" cy="131.0" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="152.1" cy="156.5" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="221.1" cy="95.9" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="140.5" cy="163.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="128.3" cy="187.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="113.4" cy="158.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="197.8" cy="130.7" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="108.6" cy="222.6" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="147.6" cy="150.2" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="148.6" cy="194.5" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="137.9" cy="154.0" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="143.8" cy="206.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="176.9" cy="139.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="252.5" cy="51.9" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="131.6" cy="179.9" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="180.6" cy="132.9" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="140.9" cy="157.3" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="142.4" cy="146.2" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="134.7" cy="167.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="150.2" cy="145.2" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="188.4" cy="121.7" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="171.6" cy="131.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="180.7" cy="144.1" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="204.4" cy="112.2" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="194.7" cy="112.7" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="168.7" cy="129.0" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="154.5" cy="103.9" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="158.1" cy="152.0" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="158.6" cy="143.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="147.1" cy="153.7" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="131.9" cy="194.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="128.3" cy="181.6" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="151.8" cy="168.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="113.1" cy="184.7" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="146.5" cy="188.6" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="199.6" cy="109.7" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="167.0" cy="131.6" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="162.4" cy="157.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="119.7" cy="171.5" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="123.7" cy="171.6" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="188.8" cy="153.4" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="159.4" cy="177.2" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="146.8" cy="156.8" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="195.2" cy="98.6" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="138.7" cy="168.0" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="186.2" cy="137.0" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><circle cx="207.8" cy="98.2" r="2.6" fill="#5c6bc0" fill-opacity="0.65"/><text x="250.0" y="269.0" font-size="11" text-anchor="end" font-weight="normal" fill="currentColor" fill-opacity="0.8">体重 z_w</text><text x="60.0" y="51.0" font-size="11" text-anchor="start" font-weight="normal" fill="currentColor" fill-opacity="0.8">離乳日齢 z_x</text><text x="60.0" y="292.0" font-size="12" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">赤い縦線が「残り」 e_x</text><text x="400.0" y="32.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">② 残り同士を描く</text><line x1="400.0" y1="62.0" x2="400.0" y2="252.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><line x1="400.0" y1="252.0" x2="590.0" y2="252.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><line x1="400.0" y1="157.0" x2="590.0" y2="157.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.2"/><line x1="495.0" y1="62.0" x2="495.0" y2="252.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.2"/><circle cx="479.3" cy="220.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="489.3" cy="168.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="496.7" cy="117.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="504.6" cy="145.0" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="506.4" cy="127.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="513.1" cy="155.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="481.0" cy="143.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="468.5" cy="122.4" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="490.6" cy="149.3" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="506.0" cy="163.3" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="498.3" cy="145.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="492.4" cy="168.0" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="490.2" cy="146.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="491.8" cy="170.5" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="469.9" cy="167.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="497.7" cy="162.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="504.4" cy="119.5" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="502.5" cy="171.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="499.8" cy="171.0" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="476.0" cy="166.0" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="497.3" cy="178.8" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="468.0" cy="140.8" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="499.8" cy="152.5" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="496.8" cy="187.8" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="463.1" cy="168.0" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="477.2" cy="141.4" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="481.8" cy="147.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="495.4" cy="192.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="522.4" cy="166.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="488.7" cy="157.6" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="511.4" cy="140.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="493.8" cy="146.3" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="488.0" cy="109.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="487.2" cy="159.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="496.4" cy="172.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="492.4" cy="170.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="484.3" cy="150.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="477.8" cy="156.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="503.5" cy="160.4" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="510.9" cy="167.0" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="495.0" cy="133.3" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="509.4" cy="160.5" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="464.3" cy="187.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="484.3" cy="151.4" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="504.6" cy="124.4" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="493.0" cy="142.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="484.9" cy="154.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="490.7" cy="195.4" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="485.3" cy="174.3" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="501.7" cy="202.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="492.2" cy="166.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="498.0" cy="143.6" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="499.6" cy="144.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="501.0" cy="204.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="487.4" cy="173.3" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="529.4" cy="149.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="484.8" cy="153.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="469.0" cy="166.4" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="508.2" cy="165.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="463.0" cy="124.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="512.6" cy="146.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="454.7" cy="166.6" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="493.5" cy="155.6" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="516.8" cy="151.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="492.1" cy="148.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="497.2" cy="156.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="506.7" cy="171.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="516.5" cy="166.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="501.9" cy="165.0" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="510.9" cy="169.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="501.8" cy="147.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="506.0" cy="129.1" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="485.9" cy="164.8" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="497.5" cy="166.5" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="505.4" cy="136.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="511.3" cy="152.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="548.5" cy="128.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="497.4" cy="158.8" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="505.1" cy="147.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="505.1" cy="165.6" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="477.3" cy="140.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="493.2" cy="165.5" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="486.3" cy="162.0" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="503.1" cy="144.4" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="470.6" cy="130.3" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="504.2" cy="152.6" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="510.1" cy="162.4" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="487.9" cy="162.6" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="510.6" cy="148.2" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="507.2" cy="200.3" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="469.7" cy="165.0" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="471.1" cy="151.3" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="502.1" cy="180.8" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="519.1" cy="170.7" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="497.9" cy="139.8" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="488.4" cy="156.0" r="2.6" fill="#00897b" fill-opacity="0.65"/><circle cx="508.7" cy="117.9" r="2.6" fill="#00897b" fill-opacity="0.65"/><text x="590.0" y="269.0" font-size="11" text-anchor="end" font-weight="normal" fill="currentColor" fill-opacity="0.8">離乳の残り e_x</text><text x="400.0" y="51.0" font-size="11" text-anchor="start" font-weight="normal" fill="currentColor" fill-opacity="0.8">行動圏の残り e_y</text><text x="400.0" y="292.0" font-size="12" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">偏相関 = 0.051 ―― ほぼ無関係</text><text x="60.0" y="330.0" font-size="11.5" text-anchor="start" font-weight="normal" fill="currentColor" fill-opacity="0.85">見かけの相関 r = 0.657 のうち、ほとんどが体重で説明できてしまう。（相関構造を再現した模式図・n=97）</text></svg>

    **数値で確かめる。**3つの列すべてに値がある n=97種では、\( r_{xy}=0.6570 \)（離乳×行動圏）、\( r_{xw}=0.8543 \)（離乳×体重）、\( r_{yw}=0.7485 \)（行動圏×体重）。

    $$ \frac{0.6570 - 0.8543\times0.7485}{\sqrt{(1-0.8543^2)(1-0.7485^2)}} \;=\; \frac{0.0176}{0.3447} \;=\; 0.051 $$

    ノートブックが最小二乗で出した 0.0510 と一致する。**式でも、コードでも、同じ数にたどり着く。**

    **何が起きていたのか。**見かけの相関 0.6570 のうち、\( 0.8543 \times 0.7485 = 0.6394 \) は**体重を経由して説明できてしまう分**だった。引き算して残るのは 0.0176 しかない。それを残りのばらつき（0.3447）で割り直したのが 0.051 である。

    「乳離れが遅い種ほど広く動きまわる」の中身は、**ほとんど全部が「体が大きい」だった**ということだ。

    **使った数学**：二次式の平方完成と最小値（微I）、総和記号の展開と定数の括り出し（線I）、標準化というスケール変換（第3回）。新しい公式はひとつも使っていない ―― 導出①②で出した3つの事実と、かっこの展開だけである。

!!! danger "この分野では、これが最大の落とし穴である"
    生き物のデータでは、**体の大きさがほとんど全部に効く**。寿命も、妊娠期間も、行動圏も、集団サイズも、大きい種ほど大きい。だから種どうしを比べると、**何と何を組み合わせても相関が出る**。

    ノートブックでは全組み合わせを一括で比べている。強い相関が21組並び、**そのうち12組が体重を統制すると消える**。

    | 例 | 単純r | 体重統制後 |
    |---|---:|---:|
    | 頭胴長 × 行動圏 | +0.668 | −0.036 |
    | 妊娠期間 × 最長寿命 | +0.560 | +0.069 |
    | 行動圏 × 出産間隔 | +0.533 | −0.133 |

    これは統計の失敗ではなく、**世界のほうがそうできている**ということ。だから比較生物学では**「体サイズを統制したうえで、まだ残る関係は何か」**が本当の問いになる（第10回の回帰・第11回のモデル選択につながる）。

相関が因果でない代表的な理由：

1. **交絡**：第三の変数が両方を動かす（今回の例）
2. **逆因果**：原因と結果が逆かも（「運動するから健康」か「健康だから運動できる」か）
3. **偶然**：たまたま相関しただけ

---

## 5. r だけ見るな ―― アンスコムの四重奏

有名な例。**4つのまったく違うデータ**が、どれも r = 0.82、回帰直線もほぼ同じ。でも散布図は別物（直線・曲線・外れ値・1点が支配）。

> **r という1つの数だけで「関係あり」と報告するのは危険。必ず散布図を見る。**

さらに r が測れるのは**直線的な関係だけ**。`y = x²` のようなきれいな放物線でも r ≈ 0 になり、「関係なし」と誤解する。やはり**まず散布図**。

---

## まとめ

| 注意 | 中身 |
|---|---|
| 相関 ≠ 因果 | 一緒に動いても原因とは限らない |
| 交絡 | 隠れた第三の変数が両方を動かす |
| 逆因果 | 原因と結果が逆かも |
| 偶然 | たまたまの相関 |
| r だけ見ない | アンスコム・非線形・外れ値 → 必ず散布図 |

> **相関を見たら、まず散布図を描き、次に『第三の変数』を疑う。**
> 因果を本当に確かめるには **実験（ランダム化）** が要る。
> **「関係がありそうだ」と感じた瞬間に因果を読み込むのは、第1回の代表性ヒューリスティックと同じ癖である。もっともらしさは、証拠ではない。**

---

## 今日の課題（Moodle提出）

**配点：100点（選択40点 ＋ 記述60点）／ 提出先：Moodle ／ 提出期限：次回授業の開始時刻まで**

Colab `05_correlation.ipynb` を実行したうえで答えること。今回の記述は **「批判的に考える」ことが主役**。

---

### パートA：選択問題（各10点 ×4＝40点）

**A1.** 霊長類データで「体重」と「行動圏」（ともに対数）の相関係数 r に**最も近い**のは？

- (ア) 0.0　(イ) 0.7　(ウ) −0.7　(エ) 1.0

**A2.** 「離乳日齢」と「行動圏」は r≈0.66 だったが、**体重を統制すると相関がほぼ0（0.05）に**なった。この現象の説明として**最も適切**なのは？

- (ア) 乳離れが遅いことが、広い行動圏を直接もたらしている
- (イ) 「体の大きさ」という第三の変数が、離乳日齢と行動圏の両方を動かしていた（交絡）
- (ウ) 計算ミス

**A3.** アンスコムの四重奏が教えることとして**最も適切**なのは？

- (ア) 相関係数 r が同じなら、データの中身も同じ
- (イ) r が同じでも、散布図の形はまったく違うことがある。だから必ず図を見る
- (ウ) r は常に信用できない

**A4.** 「`y = x²` の放物線データで r ≈ 0 だった」。ここから言える、相関係数の**限界**は？

- (ア) r はデータ数が多いと0になる
- (イ) r は直線的な関係しか測れず、曲がった関係は見逃す
- (ウ) 放物線には関係がない

---

### パートB：記述問題（AIフィードバック対象・60点）

!!! tip "【第5回だけの扱い】数値の引用は任意です"
    この回の記述は**考え方そのもの**を見る問題なので、ほかの回と違い、**数値を引用しなくても満点になります。**

    - **B1**は、新聞の見出しという**架空の題材**を検討する問題です。朝食と成績のデータは手元にないので、数字は書けません。授業のデータ（「離乳日齢と行動圏はr=0.657だったが体重統制後は0.051」など）を**たとえとして**引ければ加点材料にしますが、必須ではありません。
    - **B2**は、身のまわりの例を**自分で作る**問題なので、はじめから数値は求めていません。

    満点の条件は数字ではなく、**対抗仮説（第三の変数）を1つ名指しし、それが両方を動かす仕組みを説明できているか**です。

**B1.（30点）** 次の見出しを読んで答えなさい。

> 「**朝食を毎日食べる子どもは、食べない子より成績が良い** ―― だから朝食を食べさせましょう」

この見出しは「朝食 → 成績」の**因果**を主張している。今日の授業をふまえ、**この主張をそのまま信じてよいか**を論じなさい。少なくとも、**朝食以外の『対抗仮説（第三の変数）』を1つ**挙げ、なぜそれが成績を説明しうるかを書くこと。

**B2.（30点）** 「相関 ≠ 因果」を、**自分の身のまわりの例**で1つ作りなさい。

1. 一緒に増減しそうな2つのこと（相関がありそうな例）
2. それを「Aが原因でBが起きる」と結論するのが危ういのはなぜか（交絡・逆因果・偶然のどれか）

> 目安：B1・B2あわせて350〜550字。**自分の言葉**で書くこと。
>
> **字数は目安です。多少の過不足で減点はしません。**見るのは、設問が挙げた要素（上の箇条書き）が書けているかどうかです。ただし要素が抜けていれば、その分は引きます。

!!! abstract "次回予告"
    第6回「確率分布と標本／中心極限定理」。なぜ数百人の調査で全国を語れるのか。一部から全体を推測する、推測統計への入り口。