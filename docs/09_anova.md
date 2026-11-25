# 第09回　仮説検定(2)：分散分析（ANOVA）

**12/8（火）Ⅱ講 10:35〜12:15・B402教室**

> 3つ以上を比べるとき、t検定を繰り返してはいけない ―― 偽陽性の罠

---


<!-- LINKS:START -->
!!! info "今日のリンク"
    - [📊 スライドを開く](slides/09.html)
    - [📓 Colabノートを開く（09_anova.ipynb）](https://colab.research.google.com/github/aonoa68/toukei-1/blob/main/colab/09_anova.ipynb)
    - [📝 課題を提出する（Moodle・第9回）](https://moodle.hokusei.ac.jp/mod/assign/view.php?id=990630)
    - 課題の本文は**このページの末尾**にあります
<!-- LINKS:END -->

!!! tip "考え方をガイドで確かめる"
    この回の考え方は、統計の考え方ガイドの[「仮説検定とp値」](https://aonoa68.github.io/teaching/guide/testing/)でも解説しています。霊長類のデータを動かしながら確かめられます。

## この回のゴール

- 検定を繰り返すと偽陽性（多重比較の罠）が増えることを説明できる
- ANOVA（分散分析）で3群以上を一括判定できる
- F値の意味と、事後検定・補正の必要性を理解する
- **発展**：偽陽性が増える式と、平方和の分解 \( SS_{\text{全体}}=SS_{\text{群間}}+SS_{\text{群内}} \) を、自分で導ける

到達目標との対応：**G2**。

---

## 0. フック

> 3つの科（オマキザル科・クモザル科・コビトキツネザル科）で体重に差があるか調べたい。
> 「じゃあ、オマキvsクモ・クモvsコビト・オマキvsコビト と、**全ペアで t検定**すればいいよね？」

――この『全ペアでt検定』が、実は危ない。

---

## 1. なぜ「繰り返し」がダメなのか

1回のt検定は「本当は差がないのに、まぐれで有意」と誤る確率を **5%（α）** 許している。

では検定を何回もやったら？　毎回5%の落とし穴があるのだから、回数が増えるほど「どれか1つはまぐれで有意」になりやすい。

---

## 2. 多重比較の罠（シミュレーション）

**本当はすべて同じ母集団（＝差がまったくない）** の k 個の群に、全ペアで t検定する。「最低1つでも有意」になる割合を数えると：

| 群数 k | ペア数 | まぐれで有意になった割合 |
|---|---|---|
| 2 | 1 | **4.9%** |
| 3 | 3 | **12.2%** |
| 5 | 10 | **29.1%** |
| 10 | 45 | **63.2%** |

（各群20個体・2万回のシミュレーション。k=2 は検定1回なので、理論どおり約5%になる。）
!!! danger "差がないのに『発見』が増える"
    差はまったくないのに、群が増える（＝検定回数が増える）ほど「最低1つ有意」が増える。
    10群なら6割以上がまぐれの「発見」。**検定の回数を増やすほど、偽の発見が紛れ込む。**

だから3群以上を「全ペアt検定」してはいけない。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 372" role="img" aria-labelledby="mct mcd" style="width:100%;height:auto;max-width:720px;display:block;margin:0.8em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="mct">検定を繰り返すほど、まぐれの「発見」が増える</title><desc id="mcd">横軸は群の数、縦軸は「差がまったく無いのに、全ペアのt検定で最低1つが有意になる割合」。実測（各群20個体・2万回）は3群で12%、5群で29%、10群で63%まで上がる。検定を独立と仮定した式 1−0.95^m はさらに上を行くが、全ペア検定は同じ群のデータを使い回すので独立ではなく、実測はこの式より低く出る。</desc><text x="0.0" y="32.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">差がまったく無いのに「どれかは有意」になる割合</text><line x1="58.0" y1="258.0" x2="560.0" y2="258.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><text x="50.0" y="262.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">0%</text><line x1="58.0" y1="210.0" x2="560.0" y2="210.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="50.0" y="214.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">25%</text><line x1="58.0" y1="162.0" x2="560.0" y2="162.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="50.0" y="166.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">50%</text><line x1="58.0" y1="114.0" x2="560.0" y2="114.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="50.0" y="118.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">75%</text><line x1="58.0" y1="66.0" x2="560.0" y2="66.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="50.0" y="70.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">100%</text><text x="58.0" y="277.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">2</text><text x="158.4" y="277.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">4</text><text x="258.8" y="277.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">6</text><text x="359.2" y="277.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">8</text><text x="459.6" y="277.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">10</text><text x="560.0" y="277.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">12</text><line x1="58.0" y1="66.0" x2="58.0" y2="258.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><text x="574.0" y="277.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.8">群の数 k</text><line x1="58.0" y1="248.4" x2="560.0" y2="248.4" stroke="#c62828" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="4 3"/><text x="556.0" y="240.4" font-size="11" text-anchor="end" fill="#c62828" fill-opacity="0.9">検定1回ぶんの 5%</text><path d="M 58.0 248.4 L 108.2 230.6 L 158.4 207.1 L 208.6 181.0 L 258.8 155.0 L 309.0 131.4 L 359.2 111.7 L 409.4 96.3 L 459.6 85.1 L 509.8 77.4 L 560.0 72.5" fill="none" stroke="#ef6c00" stroke-width="2.2" stroke-opacity="1.0" stroke-dasharray="6 4"/><path d="M 58.0 248.7 L 108.2 234.5 L 158.4 218.5 L 208.6 202.1 L 258.8 187.8 L 309.0 173.3 L 359.2 160.9 L 409.4 148.8 L 459.6 136.7 L 509.8 128.0 L 560.0 119.8" fill="none" stroke="#5c6bc0" stroke-width="2.6" stroke-opacity="1.0"/><circle cx="108.2" cy="234.5" r="4.4" fill="#5c6bc0" fill-opacity="1.0"/><text x="98.2" y="238.5" font-size="12" text-anchor="end" font-weight="bold" fill="#5c6bc0" fill-opacity="1.0">12%</text><circle cx="208.6" cy="202.1" r="4.4" fill="#5c6bc0" fill-opacity="1.0"/><text x="208.6" y="190.1" font-size="12" text-anchor="middle" font-weight="bold" fill="#5c6bc0" fill-opacity="1.0">29%</text><circle cx="459.6" cy="136.7" r="4.4" fill="#5c6bc0" fill-opacity="1.0"/><text x="459.6" y="124.7" font-size="12" text-anchor="middle" font-weight="bold" fill="#5c6bc0" fill-opacity="1.0">63%</text><line x1="574.0" y1="96.0" x2="604.0" y2="96.0" stroke="#ef6c00" stroke-width="2.2" stroke-opacity="1.0" stroke-dasharray="6 4"/><text x="610.0" y="100.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="1.0">検定が独立だと</text><text x="610.0" y="115.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="1.0">仮定した式</text><text x="610.0" y="130.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.8">1−0.95ᵐ</text><line x1="574.0" y1="160.0" x2="604.0" y2="160.0" stroke="#5c6bc0" stroke-width="2.6" stroke-opacity="1.0"/><text x="610.0" y="164.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="1.0">実測（各群20個体・</text><text x="610.0" y="179.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="1.0">2万回）</text><text x="0.0" y="302.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.9">3群で全ペアを検定すると、差が無くても 12% は「どれか有意」になる。10群なら 63%。</text><text x="0.0" y="324.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.9">実測が式より低いのは、同じ群のデータを使い回していて検定どうしが独立でないため。式は増え方の勢いを示す目安である。</text><text x="0.0" y="346.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.7">（各群20個体・正規分布・2万回。等分散のt検定を両側5%で。k=2 では理論どおり 4.9% になる。）</text></svg>

???+ note "導出①：偽陽性はなぜ増えるのか（そして、この式の限界）"

    1回の検定で「本当は差がないのに有意」と誤る確率を \( \alpha \) とする。誤らない確率は \( 1-\alpha \)。

    いま \( m \) 回の検定を行い、**それらが互いに独立だと仮定する**。すると「m回とも誤らない」確率は積になる。

    $$ \Pr(\text{1つも誤らない}) \;=\; (1-\alpha)^m $$

    よって「少なくとも1つはまぐれで有意」になる確率は、その余事象で

    $$ \Pr(\text{最低1つ有意}) \;=\; 1-(1-\alpha)^m $$

    群数が \( k \) なら、全ペアの数は \( m = \binom{k}{2} = \dfrac{k(k-1)}{2} \)。k が増えると m は二次で増えるので、この確率は急速に1に近づく。**「検定を繰り返すほど偽の発見が増える」は、この積の形の帰結である。**

    !!! warning "この式は『独立』を使っている。だが全ペア検定は独立ではない"
        上の式は m 回の検定が互いに独立なときのものである。しかし**全ペアt検定は独立ではない**。オマキ vs クモ と オマキ vs コビト は、どちらも同じオマキザル科のデータを共有している。片方がたまたま外れた標本を引けば、もう片方も同じ方向に引きずられる。検定どうしが正に相関するのだ。

        実際、上の表の実測値と式の値はずれている。

        | 2 | 1 | 5.0% | **4.9%** |
        | 3 | 3 | 14.3% | **12.2%** |
        | 5 | 10 | 40.1% | **29.1%** |
        | 10 | 45 | 90.1% | **63.2%** |
        | 5 | 10 | 40.1% | 約 30% |
        | 10 | 45 | 90.1% | 約 64% |

        k が大きいほど実測が式を下回る。検定が正に相関していると「どれか1つが当たる」機会は独立のときより少なくなるからである。**この式は増え方の勢いを示す目安であって、正確な偽陽性率ではない。** 正確に扱うには、検定統計量の同時分布を考える必要がある（テューキー法などはそれを行っている）。

    **使った数学**：余事象の確率と積の法則（微I・確率の基礎）、組み合わせ \( \binom{k}{2} \)（線I・離散数学）。


---

## 3. ANOVA ―― まず1回で「どこかに差があるか」

分散分析（ANOVA）は、3群以上を**一度の検定**で「**どこかに差があるか**」だけを判定する。検定を繰り返さないので偽陽性が増えない。

3つの科の体重で実行すると（対数スケール）：

| 科 | 体重の中央値（n） |
|---|---|
| オマキザル科 | 492 g（39種） |
| クモザル科 | 6,652 g（16種） |
| コビトキツネザル科 | 69 g（13種） |

**ANOVA：F = 151.89、p = 3×10⁻²⁵**

圧倒的に有意。中央値が桁で違うのだから当然である。F=151.89 は「グループ間の差が、群内のばらつきの150倍」という意味。

### 対照実験 ―― F が1前後だと、どう見えるか

同じ科の枠組みで、**差がなさそうな量**を調べる。「科によって、生息地の降水量に差はあるか？」

| 科 | 月降水量の平均（n） |
|---|---|
| オナガザル科 | 158.7 mm（130種） |
| クモザル科 | 161.3 mm（24種） |
| サキ科 | 154.8 mm（26種） |

**ANOVA：F = 0.08、p = 0.92**

平均値の見かけの違いは、群内のばらつきに完全に埋もれている。（見かけの平均差にだまされない、という第2〜3回の教訓ともつながる。）

!!! note "「有意でなかった」も立派な結果"
    ただしこれは「差がないことの証明」ではない。**「この種数・このばらつきでは、差を検出できなかった」**が正確な言い方である。

### F値の気持ち

ANOVAは2種類のばらつきを比べる。

$$ F = \frac{\text{群間のばらつき（グループの平均どうしの違い）}}{\text{群内のばらつき（同じグループ内の個人差）}} $$

- F が大きい ＝ グループ間の差が個人差より大きい → 「差がある」
- F が1前後 ＝ グループの違いは個人差の範囲 → 「差があるとは言えない」（今回）

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 378" role="img" aria-labelledby="fvt fvd" style="width:100%;height:auto;max-width:720px;display:block;margin:0.8em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="fvt">F が151のときと、0.08のときの見え方</title><desc id="fvd">左は3科の体重（常用対数）で F = 151.89。群の平均（太い横線）が互いに大きく離れていて、群の中の散らばりではとても埋められない。右は同じ枠組みで月降水量を見たもので F = 0.08。平均はほとんど同じ高さに並び、群内の散らばりに完全に埋もれている。F は「群の平均どうしの離れ方」を「群の中の散らばり」で割った比である。</desc><text x="0.0" y="30.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">F は「平均どうしの離れ方」を「群の中の散らばり」で割った比</text><text x="10.0" y="74.0" font-size="13" text-anchor="start" font-weight="bold" fill="#5c6bc0" fill-opacity="1.0">体重（常用対数）　F = 151.89</text><text x="10.0" y="91.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.8">p = 3×10⁻²⁵　平均が大きく離れている</text><line x1="10.0" y1="188.8" x2="330.0" y2="188.8" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="5 3"/><text x="330.0" y="182.8" font-size="10.5" text-anchor="end" fill="currentColor" fill-opacity="0.7">全体平均</text><circle cx="87.0" cy="195.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="49.7" cy="204.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="69.9" cy="204.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="81.1" cy="209.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="77.2" cy="205.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="89.9" cy="207.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="86.4" cy="205.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="90.1" cy="211.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="33.0" cy="205.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="59.3" cy="201.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="62.4" cy="203.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="35.5" cy="207.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="31.7" cy="231.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="84.5" cy="159.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="94.3" cy="157.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="81.5" cy="155.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="51.5" cy="155.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="76.5" cy="156.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="50.5" cy="193.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="78.7" cy="195.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="49.2" cy="191.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="81.4" cy="194.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="94.5" cy="200.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="94.5" cy="204.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="87.8" cy="198.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="89.8" cy="203.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="76.7" cy="186.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="66.8" cy="197.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="90.4" cy="200.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="37.1" cy="196.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="55.0" cy="195.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="70.1" cy="200.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="61.9" cy="200.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="82.1" cy="204.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="43.8" cy="187.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="35.3" cy="189.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="39.4" cy="188.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="93.0" cy="184.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="39.8" cy="187.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><line x1="24.9" y1="194.3" x2="101.7" y2="194.3" stroke="#5c6bc0" stroke-width="2.6" stroke-opacity="1.0"/><text x="63.3" y="300.0" font-size="10.5" text-anchor="middle" fill="currentColor" fill-opacity="0.85">オマキザル</text><text x="63.3" y="314.0" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.6">n=39</text><circle cx="152.5" cy="137.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="162.1" cy="140.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="177.9" cy="141.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="188.1" cy="136.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="143.0" cy="134.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="197.6" cy="136.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="186.8" cy="136.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="158.5" cy="135.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="150.1" cy="134.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="176.1" cy="128.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="176.1" cy="132.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="155.1" cy="137.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="148.8" cy="129.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="187.1" cy="124.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="181.1" cy="137.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="189.2" cy="130.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><line x1="131.6" y1="134.7" x2="208.4" y2="134.7" stroke="#5c6bc0" stroke-width="2.6" stroke-opacity="1.0"/><text x="170.0" y="300.0" font-size="10.5" text-anchor="middle" fill="currentColor" fill-opacity="0.85">クモザル</text><text x="170.0" y="314.0" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.6">n=16</text><circle cx="258.7" cy="243.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="291.0" cy="201.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="249.4" cy="220.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="245.1" cy="263.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="256.2" cy="245.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="294.7" cy="246.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="279.2" cy="265.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="284.1" cy="250.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="282.6" cy="254.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="285.4" cy="254.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="265.3" cy="246.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="290.8" cy="208.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="245.6" cy="203.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><line x1="238.3" y1="238.6" x2="315.1" y2="238.6" stroke="#5c6bc0" stroke-width="2.6" stroke-opacity="1.0"/><text x="276.7" y="300.0" font-size="10.5" text-anchor="middle" fill="currentColor" fill-opacity="0.85">コビトキツネザル</text><text x="276.7" y="314.0" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.6">n=13</text><line x1="10.0" y1="282.0" x2="330.0" y2="282.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/><text x="390.0" y="74.0" font-size="13" text-anchor="start" font-weight="bold" fill="#00897b" fill-opacity="1.0">月降水量（mm）　F = 0.08</text><text x="390.0" y="91.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.8">p = 0.92　平均は散らばりに埋もれている</text><line x1="390.0" y1="215.6" x2="710.0" y2="215.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="5 3"/><text x="710.0" y="209.6" font-size="10.5" text-anchor="end" fill="currentColor" fill-opacity="0.7">全体平均</text><circle cx="435.5" cy="216.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="414.8" cy="224.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="419.4" cy="203.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="469.2" cy="218.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="449.9" cy="260.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="462.0" cy="252.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="450.1" cy="208.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="447.9" cy="252.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="462.2" cy="227.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="451.2" cy="186.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="444.0" cy="219.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="447.0" cy="223.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="447.7" cy="182.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="433.2" cy="243.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="454.1" cy="214.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="437.4" cy="224.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="453.2" cy="191.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="442.4" cy="229.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="459.2" cy="237.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="455.7" cy="228.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="413.9" cy="228.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="461.4" cy="236.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="468.7" cy="225.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="432.5" cy="224.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="458.2" cy="220.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="465.4" cy="211.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="443.3" cy="220.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="419.6" cy="183.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="458.1" cy="230.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="465.0" cy="200.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="431.3" cy="209.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="425.3" cy="222.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="460.4" cy="252.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="444.4" cy="239.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="412.3" cy="255.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="423.9" cy="255.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="425.2" cy="236.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="448.6" cy="242.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="447.1" cy="230.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="444.4" cy="236.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="433.2" cy="206.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="436.4" cy="212.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="443.4" cy="237.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="447.7" cy="251.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="447.5" cy="222.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="457.1" cy="215.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="475.0" cy="226.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="459.3" cy="213.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="442.7" cy="220.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="473.9" cy="214.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="419.3" cy="189.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="472.3" cy="220.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="443.4" cy="188.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="442.3" cy="211.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="465.7" cy="184.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="450.3" cy="233.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="463.9" cy="178.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="434.9" cy="184.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="446.8" cy="184.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="452.9" cy="179.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="426.5" cy="243.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="460.2" cy="138.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="421.3" cy="245.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="419.9" cy="222.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="428.6" cy="263.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="463.2" cy="232.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="441.8" cy="188.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="413.6" cy="196.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="424.0" cy="214.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="447.4" cy="214.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="415.2" cy="238.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="431.6" cy="173.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="424.9" cy="241.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="455.5" cy="246.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="420.6" cy="263.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="435.0" cy="210.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="440.1" cy="265.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="469.0" cy="214.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="437.2" cy="228.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="420.0" cy="251.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="438.3" cy="215.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="435.1" cy="186.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="447.7" cy="257.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="419.3" cy="240.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="438.4" cy="215.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="453.2" cy="162.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="437.6" cy="190.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="471.9" cy="197.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="434.6" cy="176.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="467.2" cy="162.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="432.7" cy="164.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="436.9" cy="172.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="456.5" cy="138.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="445.8" cy="172.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="471.0" cy="191.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="468.0" cy="221.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="429.5" cy="203.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="432.0" cy="206.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="452.6" cy="202.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="462.1" cy="215.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="418.5" cy="227.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="469.3" cy="205.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="434.0" cy="234.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="420.5" cy="251.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="428.3" cy="243.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="462.4" cy="237.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="427.7" cy="249.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="418.9" cy="236.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="449.5" cy="201.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="469.8" cy="237.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="431.4" cy="214.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="444.0" cy="138.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="436.2" cy="243.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="471.6" cy="197.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="466.6" cy="124.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="442.6" cy="179.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="474.0" cy="227.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="425.6" cy="212.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="438.1" cy="230.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="447.4" cy="220.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="460.6" cy="207.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="456.4" cy="210.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="438.1" cy="228.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="471.4" cy="211.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="474.2" cy="197.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="465.8" cy="221.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="440.4" cy="202.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="463.8" cy="216.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="428.4" cy="217.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="422.4" cy="222.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><line x1="404.9" y1="215.5" x2="481.7" y2="215.5" stroke="#00897b" stroke-width="2.6" stroke-opacity="1.0"/><text x="443.3" y="300.0" font-size="10.5" text-anchor="middle" fill="currentColor" fill-opacity="0.85">オナガザル</text><text x="443.3" y="314.0" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.6">n=130</text><circle cx="522.8" cy="213.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="569.3" cy="233.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="580.5" cy="214.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="537.0" cy="226.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="564.1" cy="214.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="534.9" cy="210.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="567.4" cy="204.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="528.7" cy="226.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="551.2" cy="236.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="568.7" cy="205.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="580.1" cy="186.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="561.1" cy="200.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="562.0" cy="189.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="544.0" cy="217.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="528.9" cy="234.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="569.6" cy="211.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="523.1" cy="216.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="565.9" cy="226.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="537.8" cy="230.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="521.3" cy="208.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="527.5" cy="186.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="552.1" cy="233.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="538.3" cy="192.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="526.4" cy="228.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><line x1="511.6" y1="214.4" x2="588.4" y2="214.4" stroke="#00897b" stroke-width="2.6" stroke-opacity="1.0"/><text x="550.0" y="300.0" font-size="10.5" text-anchor="middle" fill="currentColor" fill-opacity="0.85">クモザル</text><text x="550.0" y="314.0" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.6">n=24</text><circle cx="645.3" cy="192.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="675.8" cy="184.8" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="671.2" cy="222.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="654.4" cy="251.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="648.3" cy="209.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="688.1" cy="206.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="657.3" cy="235.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="667.9" cy="199.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="678.3" cy="236.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="657.1" cy="215.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="664.7" cy="218.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="653.2" cy="224.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="678.2" cy="232.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="673.5" cy="209.0" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="653.4" cy="228.5" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="677.8" cy="223.6" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="639.9" cy="232.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="647.1" cy="227.4" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="667.7" cy="246.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="632.9" cy="237.3" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="684.1" cy="208.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="626.1" cy="171.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="684.2" cy="208.1" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="643.1" cy="207.9" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="681.7" cy="200.7" r="2.6" fill="#00897b" fill-opacity="0.5"/><circle cx="644.3" cy="216.2" r="2.6" fill="#00897b" fill-opacity="0.5"/><line x1="618.3" y1="217.2" x2="695.1" y2="217.2" stroke="#00897b" stroke-width="2.6" stroke-opacity="1.0"/><text x="656.7" y="300.0" font-size="10.5" text-anchor="middle" fill="currentColor" fill-opacity="0.85">サキ</text><text x="656.7" y="314.0" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.6">n=26</text><line x1="390.0" y1="282.0" x2="710.0" y2="282.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/><text x="0.0" y="346.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.9">同じ3群という形でも、平均の離れ方が群内の散らばりに対して大きいか小さいかで、F はこれだけ違う。</text><text x="0.0" y="368.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.7">（左右で縦軸の単位も目盛りも別。点は1種、太い横線が群の平均、破線が全体平均。）</text></svg>

???+ note "導出②：ばらつきは、群間と群内にきれいに分かれる"

    全体のばらつき（総平方和）を、全体平均 \( \bar{x} \) からのズレの二乗和で測る。各データ \( x_{ij} \)（第 i 群の j 番目）のズレを、**群平均 \( \bar{x}_i \) を経由して**2つに分ける。

    $$ x_{ij}-\bar{x} \;=\; \underbrace{(x_{ij}-\bar{x}_i)}_{\text{群内のズレ}} \;+\; \underbrace{(\bar{x}_i-\bar{x})}_{\text{群間のズレ}} $$

    両辺を二乗して全データで合計すると、交差項が現れる。

    $$ \sum_i\sum_j (x_{ij}-\bar{x})^2 = \sum_i\sum_j (x_{ij}-\bar{x}_i)^2 + \sum_i\sum_j(\bar{x}_i-\bar{x})^2 + 2\sum_i (\bar{x}_i-\bar{x})\sum_j (x_{ij}-\bar{x}_i) $$

    ここで最後の項に注目する。内側の \( \sum_j (x_{ij}-\bar{x}_i) \) は、**その群の中での偏差の和**である。第3回で見たとおり、平均からの偏差を足すと必ず 0 になる。だから交差項は丸ごと消える。残るのは

    $$ SS_{\text{全体}} \;=\; SS_{\text{群内}} \;+\; SS_{\text{群間}} $$

    **ばらつきは、群の中のばらつきと、群どうしのばらつきに、余りなく分解できる。** ANOVA という名前（分散分析）はこの分解に由来する。差を見るのに「分散」を調べるのは遠回りに見えるが、実際にはこの等式があるからこそ、1回の比較で全群をまとめて扱える。

    **数値で確かめる**：3科の体重（対数）では \( SS_{\text{全体}} = 31.6682 \)、\( SS_{\text{群間}} = 26.0865 \)、\( SS_{\text{群内}} = 5.5817 \)。後者2つの和は 31.6682 で、総和と小数点以下14桁まで一致する。

    **使った数学**：二乗の展開と二重和の入れ替え（線I）、偏差の和がゼロという性質（第3回）。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 388" role="img" aria-labelledby="sst ssd" style="width:100%;height:auto;max-width:720px;display:block;margin:0.8em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="sst">ばらつきを、群の中と群どうしに分ける</title><desc id="ssd">左は3科の体重（常用対数）。1つの点について、全体平均からのズレが「その群の平均までのズレ（群間）」と「群の平均から点までのズレ（群内）」の和にちょうど分かれる。右の帯はそれを全データで合計したもので、総平方和 31.6682 が群間 26.0865 と群内 5.5817 に余りなく分かれている（群間が 82.4%）。</desc><text x="0.0" y="30.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">全体のばらつきは、群間と群内にちょうど分かれる</text><line x1="10.0" y1="162.5" x2="340.0" y2="162.5" stroke="#c62828" stroke-width="1.6" stroke-opacity="0.8" stroke-dasharray="5 3"/><text x="340.0" y="155.5" font-size="11" text-anchor="end" font-weight="bold" fill="#c62828" fill-opacity="1.0">全体平均 2.87</text><circle cx="42.1" cy="170.8" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="65.0" cy="181.8" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="71.3" cy="181.5" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="36.0" cy="187.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="43.3" cy="182.5" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="91.4" cy="185.0" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="38.5" cy="182.4" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="42.2" cy="189.8" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="92.6" cy="182.4" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="72.5" cy="177.5" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="56.9" cy="180.4" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="65.7" cy="185.2" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="75.0" cy="214.5" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="51.2" cy="127.1" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="42.7" cy="124.3" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="82.7" cy="121.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="75.5" cy="121.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="65.8" cy="124.0" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="84.5" cy="168.5" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="68.0" cy="170.0" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="94.6" cy="166.1" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="46.8" cy="169.1" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="68.3" cy="176.1" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="64.0" cy="180.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="56.0" cy="174.4" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="70.6" cy="179.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="48.7" cy="160.2" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="83.6" cy="173.5" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="87.6" cy="176.6" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="42.1" cy="171.7" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="63.0" cy="170.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="51.3" cy="177.1" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="39.3" cy="176.3" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="89.4" cy="181.6" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="60.7" cy="160.4" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="43.3" cy="163.6" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="75.7" cy="162.2" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="46.7" cy="157.3" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="89.7" cy="160.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><line x1="27.6" y1="169.2" x2="102.4" y2="169.2" stroke="#00897b" stroke-width="2.6" stroke-opacity="1.0"/><text x="65.0" y="286.0" font-size="10.5" text-anchor="middle" fill="currentColor" fill-opacity="0.85">オマキザル</text><circle cx="157.6" cy="101.0" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="146.2" cy="103.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="156.6" cy="106.0" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="165.5" cy="99.1" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="173.1" cy="96.6" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="200.0" cy="98.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="187.2" cy="99.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="165.1" cy="98.6" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="145.2" cy="97.1" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="154.0" cy="89.8" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="205.6" cy="95.0" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="172.5" cy="100.7" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="186.8" cy="91.0" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="147.6" cy="100.5" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="146.3" cy="92.6" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><line x1="137.6" y1="97.2" x2="212.4" y2="97.2" stroke="#00897b" stroke-width="2.6" stroke-opacity="1.0"/><text x="175.0" y="286.0" font-size="10.5" text-anchor="middle" fill="currentColor" fill-opacity="0.85">クモザル</text><circle cx="306.3" cy="228.0" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="290.4" cy="177.3" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="273.2" cy="201.1" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="273.8" cy="252.6" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="259.7" cy="231.1" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="264.8" cy="231.6" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="255.7" cy="254.6" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="305.9" cy="236.3" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="282.9" cy="241.9" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="262.0" cy="241.5" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="299.7" cy="232.0" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="266.3" cy="186.4" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="258.0" cy="179.8" r="2.6" fill="#5c6bc0" fill-opacity="0.45"/><line x1="247.6" y1="222.6" x2="322.4" y2="222.6" stroke="#00897b" stroke-width="2.6" stroke-opacity="1.0"/><text x="285.0" y="286.0" font-size="10.5" text-anchor="middle" fill="currentColor" fill-opacity="0.85">コビトキツネザル</text><circle cx="219.0" cy="85.4" r="4.6" fill="#ef6c00" fill-opacity="1.0"/><line x1="219.0" y1="85.4" x2="219.0" y2="97.2" stroke="#ef6c00" stroke-width="2.2" stroke-opacity="1.0"/><line x1="219.0" y1="97.2" x2="219.0" y2="162.5" stroke="#c62828" stroke-width="2.2" stroke-opacity="1.0"/><text x="227.0" y="95.3" font-size="11" text-anchor="start" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">群内のズレ</text><text x="227.0" y="133.9" font-size="11" text-anchor="start" font-weight="bold" fill="#c62828" fill-opacity="1.0">群間のズレ</text><line x1="10.0" y1="268.0" x2="340.0" y2="268.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/><text x="10.0" y="306.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.9">ある1種のズレ ＝ 群内のズレ ＋ 群間のズレ</text><rect x="400.0" y="110.0" width="247.1" height="54.0" rx="4" ry="4" fill="#c62828" fill-opacity="0.25" stroke="#c62828" stroke-width="1" stroke-opacity="0.7"/><rect x="647.1" y="110.0" width="52.9" height="54.0" rx="4" ry="4" fill="#ef6c00" fill-opacity="0.25" stroke="#ef6c00" stroke-width="1" stroke-opacity="0.7"/><text x="400.0" y="96.0" font-size="12" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">総平方和 SS全体 ＝ 31.6682</text><text x="523.6" y="142.0" font-size="12.5" text-anchor="middle" font-weight="bold" fill="#c62828" fill-opacity="1.0">群間</text><text x="673.6" y="142.0" font-size="12" text-anchor="middle" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">群内</text><text x="400.0" y="192.0" font-size="12" text-anchor="start" fill="#c62828" fill-opacity="1.0">群間 26.0865（82.4%）</text><text x="400.0" y="214.0" font-size="12" text-anchor="start" fill="#ef6c00" fill-opacity="1.0">群内 5.5817（17.6%）</text><line x1="400.0" y1="228.0" x2="700.0" y2="228.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.4"/><text x="400.0" y="250.0" font-size="12" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">合計 31.6682</text><text x="400.0" y="270.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.75">総平方和と小数点以下14桁まで一致する</text><text x="0.0" y="362.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.9">交差項が消えるので、この分解には余りが出ない。「分散分析」という名前はこの等式に由来する。</text><text x="0.0" y="382.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.7">（3科の体重を常用対数で。点は1種、太い横線が群の平均。）</text></svg>

???+ note "導出③：F は「ばらつきの比」――なぜ1が基準になるのか"

    平方和は、足すデータが多いほど大きくなる。そのまま比べては不公平なので、それぞれの**自由度**で割って1個あたりに直す。これが平均平方である。

    $$ MS_{\text{群間}} = \frac{SS_{\text{群間}}}{k-1}, \qquad MS_{\text{群内}} = \frac{SS_{\text{群内}}}{N-k}, \qquad F = \frac{MS_{\text{群間}}}{MS_{\text{群内}}} $$

    自由度が \( k-1 \) と \( N-k \) なのは、導出①（第8回）と同じ理由である。群間では全体平均を、群内では各群の平均を、データから計算して使ってしまっている。

    ここが要点である。**帰無仮説（どの群も同じ母集団）が正しいとき、分子と分母はどちらも同じ \( \sigma^2 \) の不偏推定になる。** 第8回の導出①で見たとおり、自由度で割った二乗和の期待値は \( \sigma^2 \) だからだ。同じものを2通りに見積もって割り算しているのだから、比は 1 のあたりに来る。

    群に本当の差があると、\( \bar{x}_i \) どうしが離れるので分子だけが膨らむ。分母は群内の個人差のままである。だから **F が大きい＝群間のばらつきが個人差では説明しきれない**、となる。

    **数値で確かめる**：3科の体重では \( MS_{\text{群間}} = 13.0433 \)（自由度2）、\( MS_{\text{群内}} = 0.0859 \)（自由度65）で、比は F = 151.89。また、差のない3群を同じ標本サイズで2万回つくると F の平均は 1.037 となり、理論値 \( df_2/(df_2-2) = 1.032 \) とほぼ一致する（中央値は 0.698 で、分布が右に裾を引いているため平均より小さい）。

    !!! note "F 分布そのものは扱わない"
        「F がいくつ以上なら有意か」を決めるには F 分布の密度関数が要る。これは2つの \( \chi^2 \) 分布の比として定まるもので、**このコースでは扱わない**。ここで導けるのは F の**作り方**と、なぜ1が基準になるのかまでである。

    **使った数学**：自由度による標準化（微I）、期待値の線形性、第8回の導出①。


---

## 4. ANOVAが有意だったら ―― 事後検定と補正

ANOVAが教えるのは「**どこかに**差がある」まで。**どのペアか**は別途調べる（事後検定）。その際も検定を繰り返すので、有意水準を厳しくする補正をかける。

- **ボンフェローニ補正**：α を検定回数で割る。例：5群=10ペアなら α=0.05/10=0.005 を各検定の基準に。これで全体の偽陽性を5%に抑える。

!!! warning "よくある誤り"
    「ANOVAが有意 ＝ すべての群が互いに違う」――**ちがう。**
    ANOVAが言うのは「**どこかに**差がある」だけ。どのペアかは事後検定で確かめる。

---

## まとめ

| 概念 | ひとこと |
|---|---|
| 多重比較の罠 | 検定を繰り返すほど、まぐれの有意（偽陽性）が増える |
| ANOVA | 3群以上を1回で「どこかに差があるか」判定。偽陽性が増えない |
| F値 | 群間のばらつき ÷ 群内のばらつき。大きいほど差あり |
| 事後検定＋補正 | どのペアかは別途。ボンフェローニ補正で α を回数で割る |
| ❌ 誤り | 全ペアt検定でOK／ANOVA有意＝全群が違う |

> **群が3つ以上なら、t検定を繰り返さない。まずANOVAで一括判定。**
> 「有意」は『どこかに差』であって『全部違う』ではない。
> **何度も試せばいつか「当たる」。これは第1回の大数の法則の裏返しで、少数の偶然に意味を見てしまう癖そのものだ。繰り返すなら、繰り返した回数の分だけ厳しくする。**

---

## 今日の課題（Moodle提出）

**配点：100点（選択40点 ＋ 記述60点）／ 提出先：Moodle ／ 提出期限：次回授業の開始時刻まで**

Colab `09_anova.ipynb` を実行したうえで答えること。

---

### パートA：選択問題（各10点 ×4＝40点）

**A1.** 本当はどの群も差がないのに、群（検定回数）を 2→3→5→10 と増やして全ペアt検定すると、「最低1つ有意」になった割合はどうなったか。

- (ア) ずっと5%で変わらない
- (イ) 約6%→12%→30%→64% と増えた
- (ウ) 約64%→30%→12%→6% と減った

**A2.** なぜ3群以上で「全ペアt検定」を避けるべきか。**最も適切**なのは？

- (ア) 計算が面倒だから
- (イ) 検定を繰り返すほど、まぐれで有意になる偽陽性が増えるから
- (ウ) t検定は2群でも使えないから

**A3.** ANOVA（分散分析）が判定するのは何か。**最も適切**なのは？

- (ア) どの2つの群が違うかを正確に特定する
- (イ) 「どこかに差があるか」を1回でまとめて判定する
- (ウ) 効果量を計算する

**A4.** 「ANOVAが有意（p<0.05）だった」。ここから**正しく言える**のは？

- (ア) すべての群が互いに異なる
- (イ) どこかに差がある。どのペアかは事後検定で確かめる必要がある
- (ウ) 群1が最も大きい

---

### パートB：記述問題（AIフィードバック対象・60点）

!!! warning "【全記述に共通・重要】自分の出力を引用すること"
    記述には、**今日のColabであなたのノートが出した数値**を最低1つ引用すること。**ここには値を書かない。自分の画面に出た値を使うこと。**
    引ける量の例：「10群でまぐれに有意が出た割合」「3科の体重のANOVAのF値」「月降水量のF値とp値」。
    **引用がない記述は満点になりません。**

**B1.（30点）** ある研究者が、**6種類のダイエット食品**それぞれについて「食べた群 vs 食べない群」で個別にt検定を行い、「6つのうち1つで p<0.05 が出たので、その食品には効果がある」と発表した。この分析の**何が問題か**を、今日学んだ多重比較の観点から指摘し、**どうすべきだったか**を述べなさい。

**B2.（30点）** 3つの科の生息地の月降水量は、**平均が少し違って見えた**のに、ANOVAでは「差があるとは言えない」という結果になった。**あなたのノートに出た3つの平均とF値・p値を書いたうえで**、**見かけの平均差があるのに「差なし」**になるのはなぜか、F値（群間のばらつきと群内のばらつき）の考え方を使って説明しなさい。

> 目安：B1・B2あわせて350〜550字。**自分の言葉**で書くこと。
>
> **字数は目安です。多少の過不足で減点はしません。**見るのは、設問が挙げた要素（上の箇条書き）が書けているかどうかです。ただし要素が抜けていれば、その分は引きます。

!!! abstract "次回予告"
    第10回「回帰分析：単回帰と重回帰」。2変数の関係を**数式（モデル）**で表す。データを式で説明する試みと、その限界へ。