# 第08回　仮説検定(1)：帰無仮説とt検定

**12/1（火）Ⅱ講 10:35〜12:15・B402教室**

> 「差がある」とは何か ―― そして、p値という誤解されやすい数

---


<!-- LINKS:START -->
!!! info "今日のリンク"
    - [📊 スライドを開く](slides/08.html)
    - [📓 Colabノートを開く（08_ttest.ipynb）](https://colab.research.google.com/github/aonoa68/toukei-1/blob/main/colab/08_ttest.ipynb)
    - [📝 課題を提出する（Moodle・第8回）](https://moodle.hokusei.ac.jp/mod/assign/view.php?id=990629)
    - 課題の本文は**このページの末尾**にあります
<!-- LINKS:END -->

!!! tip "考え方をガイドで確かめる"
    この回の考え方は、統計の考え方ガイドの[「仮説検定とp値」](https://aonoa68.github.io/teaching/guide/testing/)でも解説しています。霊長類のデータを動かしながら確かめられます。

## この回のゴール

- **検定とは何をする道具か／いつ使うのか**を説明できる（全数調査には要らない）
- **検定が答えないこと**（差の大きさ・重要さ・帰無仮説が正しい確率）を挙げられる
- 帰無仮説・対立仮説と、検定の背理法的なロジックを説明できる
- t検定を実行し、p値を**正しく**解釈できる
- 「p値 ≠ 効果の大きさ」「有意 ≠ 重要」を理解し、効果量も見る習慣をつける
- **発展**：不偏分散がなぜ \( n-1 \) で割るのか、t 統計量がどこから来るのかを、自分で導ける

到達目標との対応：**G2（このコースの中核）**。

---

## 0. フック

> 保護区の中と外で、同じ種のサルの体重を測った。**保護区の中のほうが平均0.2kg重かった。**
> これは「保護区に効果があった」のか、「たまたま」なのか？

直感では決められない。0.2kgは大きい？小さい？――この問いに答えるのが**仮説検定**だ。

---

## 1. 検定とは何か ―― そして、いつ使うのか

### そもそも、何をする道具か

一行でいうと、こうである。

> **検定とは、目の前の差が「偶然のゆらぎだけで説明がつくかどうか」を判定する手続きである。**

上のフックで言えば、0.2 kg という差について「保護区の効果だ」と言いたいが、
**標本を取り直せば、効果がなくても多少の差は毎回出る**（第6回・第7回でさんざん見たとおりである）。
検定が答えるのは、**その「毎回出る程度のゆらぎ」で片がつく差なのかどうか**、ただ1点である。

### いつ使うのか ―― 3つがそろったとき

第7回の区間推定と同じで、**使う条件がある。**

1. 母集団の**一部しか見ていない**（＝標本である）
2. **2つ以上を比べたい**、または「ある値と違うか」を言いたい
3. その差が、**偶然で出る程度かどうか**を切り分けたい

!!! danger "いつ使わないか ―― 全数調査に検定はいらない"
    クラス30人全員と、別のクラス30人全員の平均点を比べたとき、
    その差は**推定ではなく事実**である。「偶然のゆらぎ」が入り込む余地がないので、検定する相手がいない。

    第7回の「**全数調査のデータに信頼区間を付けるのは誤用**」と、まったく同じ構造である。
    標本を取っていないのに p 値が書かれている表を見たら、
    **その人が何を母集団だと考えているのか**を確かめること。

### 🔴 検定が「答えないこと」が3つある

ここを取り違えるのが、このあと第3〜5節で扱う誤用のほぼすべてである。

| 検定は答えない | 代わりに見るもの |
|---|---|
| 差の**大きさ** | **効果量**（第5節）と信頼区間 |
| 差の**重要さ**（実務上の意味） | 分野の知識。統計では決まらない |
| 帰無仮説が**正しい確率** | ―― そもそも計算できない（第3節） |

とくに3つ目。p値は「**帰無仮説が正しいとしたら、このデータが出る確率**」であって、
「**このデータが出たとき、帰無仮説が正しい確率**」ではない。**向きが逆である。**

### 前回とのつながり ―― 検定と区間推定は、同じことの裏表

!!! success "先に区間を見れば、検定の答えは読める"
    2つのグループの差について **95%信頼区間** を作ったとする。

    - 区間が **0 を含まない** → 有意水準5%で「**有意差あり**」
    - 区間が **0 を含む** → 「**有意差なし**」

    この2つは、同じ計算を別の言い方で述べたものである。

    だとすれば、**どちらを報告すべきか。**

    | | 答えること |
    |---|---|
    | 検定（p値） | 偶然で説明がつくか（**イエスかノーか**だけ） |
    | 区間推定 | **どれくらいの差か**。ついでに偶然かどうかも分かる |

    > **区間のほうが、情報量が多い。**
    > 「有意差あり（p<0.05）」より「差は 0.1〜0.3 kg（95%信頼区間）」のほうが、
    > 読む人にとって役に立つ。医学や心理学の論文が信頼区間の併記を求めるのは、このためである。

### 帰無仮説 ―― 背理法で考える

検定は背理法に似ている。

1. まず「**差はない（偶然だ）**」と仮定する。これが **帰無仮説**。
2. その仮定のもとで、**観測されたような差が起きる確率**を計算する。これが **p値**。
3. p値がとても小さい（＝偶然ではめったに起きない）なら、「差はない」という仮定のほうが間違っていた、と考える。これを「**有意差がある**」という。

> 「差がある」＝「**偶然では説明しにくいほどの差だった**」の言い換え。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 346" role="img" aria-labelledby="nlt nld" style="width:100%;height:auto;max-width:720px;display:block;margin:0.8em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="nlt">帰無仮説が正しいとき、t はこの形で散らばる</title><desc id="nld">横軸は t の値。曲線は「差はない」と仮定したときに t が取る分布（自由度約60）。両端の塗った部分が棄却域で、面積は左右あわせて5%、境目は±2.00である。クモザル科との比較の t = -0.02 は中央にあり棄却域に入らない。オマキザル科との比較の t = 20.03 はこの図の右端のはるか外にあり、p は 8e-27 である。</desc><polygon points="48.0,250.0 48.0,250.0 50.6,250.0 53.3,250.0 55.9,250.0 58.6,250.0 61.2,250.0 63.9,250.0 66.5,250.0 69.1,249.9 71.8,249.9 74.4,249.9 77.1,249.9 79.7,249.9 82.4,249.9 85.0,249.9 87.7,249.8 90.3,249.8 92.9,249.8 95.6,249.8 98.2,249.7 100.9,249.7 103.5,249.7 106.2,249.6 108.8,249.5 111.4,249.5 114.1,249.4 116.7,249.3 119.4,249.2 122.0,249.1 124.7,249.0 127.3,248.9 129.9,248.7 132.6,248.6 135.2,248.4 137.9,248.2 140.5,247.9 143.2,247.7 145.8,247.4 148.5,247.1 151.1,246.7 153.7,246.3 156.4,245.9 159.0,245.4 161.7,244.9 164.3,244.3 167.0,243.7 169.6,243.0 172.2,242.2 174.9,241.4 177.5,240.5 180.2,239.5 182.8,238.5 185.5,237.3 188.1,236.0 190.7,234.7 193.4,233.2 196.0,231.7 198.7,230.0 201.3,228.2 204.0,226.2 204.0,250.0" fill="#c62828" fill-opacity="0.3" stroke="none"/><polygon points="444.0,250.0 444.0,226.2 446.7,228.2 449.3,230.0 452.0,231.7 454.6,233.2 457.3,234.7 459.9,236.0 462.5,237.3 465.2,238.5 467.8,239.5 470.5,240.5 473.1,241.4 475.8,242.2 478.4,243.0 481.0,243.7 483.7,244.3 486.3,244.9 489.0,245.4 491.6,245.9 494.3,246.3 496.9,246.7 499.5,247.1 502.2,247.4 504.8,247.7 507.5,247.9 510.1,248.2 512.8,248.4 515.4,248.6 518.1,248.7 520.7,248.9 523.3,249.0 526.0,249.1 528.6,249.2 531.3,249.3 533.9,249.4 536.6,249.5 539.2,249.5 541.8,249.6 544.5,249.7 547.1,249.7 549.8,249.7 552.4,249.8 555.1,249.8 557.7,249.8 560.3,249.8 563.0,249.9 565.6,249.9 568.3,249.9 570.9,249.9 573.6,249.9 576.2,249.9 578.9,249.9 581.5,250.0 584.1,250.0 586.8,250.0 589.4,250.0 592.1,250.0 594.7,250.0 597.4,250.0 600.0,250.0 600.0,250.0" fill="#c62828" fill-opacity="0.3" stroke="none"/><path d="M 48.0 250.0 L 49.4 250.0 L 50.8 250.0 L 52.2 250.0 L 53.5 250.0 L 54.9 250.0 L 56.3 250.0 L 57.7 250.0 L 59.1 250.0 L 60.5 250.0 L 61.8 250.0 L 63.2 250.0 L 64.6 250.0 L 66.0 250.0 L 67.4 249.9 L 68.8 249.9 L 70.1 249.9 L 71.5 249.9 L 72.9 249.9 L 74.3 249.9 L 75.7 249.9 L 77.1 249.9 L 78.4 249.9 L 79.8 249.9 L 81.2 249.9 L 82.6 249.9 L 84.0 249.9 L 85.4 249.9 L 86.7 249.9 L 88.1 249.8 L 89.5 249.8 L 90.9 249.8 L 92.3 249.8 L 93.7 249.8 L 95.0 249.8 L 96.4 249.8 L 97.8 249.7 L 99.2 249.7 L 100.6 249.7 L 102.0 249.7 L 103.3 249.7 L 104.7 249.6 L 106.1 249.6 L 107.5 249.6 L 108.9 249.5 L 110.3 249.5 L 111.6 249.5 L 113.0 249.4 L 114.4 249.4 L 115.8 249.4 L 117.2 249.3 L 118.6 249.3 L 119.9 249.2 L 121.3 249.2 L 122.7 249.1 L 124.1 249.0 L 125.5 249.0 L 126.9 248.9 L 128.2 248.8 L 129.6 248.8 L 131.0 248.7 L 132.4 248.6 L 133.8 248.5 L 135.2 248.4 L 136.5 248.3 L 137.9 248.2 L 139.3 248.1 L 140.7 247.9 L 142.1 247.8 L 143.5 247.7 L 144.8 247.5 L 146.2 247.4 L 147.6 247.2 L 149.0 247.0 L 150.4 246.8 L 151.8 246.6 L 153.1 246.4 L 154.5 246.2 L 155.9 246.0 L 157.3 245.7 L 158.7 245.5 L 160.1 245.2 L 161.4 245.0 L 162.8 244.7 L 164.2 244.4 L 165.6 244.0 L 167.0 243.7 L 168.4 243.3 L 169.7 243.0 L 171.1 242.6 L 172.5 242.2 L 173.9 241.7 L 175.3 241.3 L 176.7 240.8 L 178.0 240.3 L 179.4 239.8 L 180.8 239.3 L 182.2 238.7 L 183.6 238.1 L 185.0 237.5 L 186.3 236.9 L 187.7 236.2 L 189.1 235.5 L 190.5 234.8 L 191.9 234.1 L 193.3 233.3 L 194.6 232.5 L 196.0 231.7 L 197.4 230.8 L 198.8 229.9 L 200.2 229.0 L 201.6 228.0 L 202.9 227.0 L 204.3 226.0 L 205.7 224.9 L 207.1 223.8 L 208.5 222.6 L 209.9 221.5 L 211.2 220.2 L 212.6 219.0 L 214.0 217.7 L 215.4 216.4 L 216.8 215.0 L 218.2 213.6 L 219.5 212.1 L 220.9 210.6 L 222.3 209.1 L 223.7 207.5 L 225.1 205.9 L 226.5 204.3 L 227.8 202.6 L 229.2 200.8 L 230.6 199.1 L 232.0 197.3 L 233.4 195.4 L 234.8 193.6 L 236.2 191.6 L 237.5 189.7 L 238.9 187.7 L 240.3 185.7 L 241.7 183.6 L 243.1 181.5 L 244.5 179.4 L 245.8 177.3 L 247.2 175.1 L 248.6 172.9 L 250.0 170.7 L 251.4 168.4 L 252.8 166.2 L 254.1 163.9 L 255.5 161.6 L 256.9 159.2 L 258.3 156.9 L 259.7 154.6 L 261.1 152.2 L 262.4 149.8 L 263.8 147.5 L 265.2 145.1 L 266.6 142.7 L 268.0 140.4 L 269.4 138.0 L 270.7 135.6 L 272.1 133.3 L 273.5 131.0 L 274.9 128.7 L 276.3 126.4 L 277.7 124.1 L 279.0 121.9 L 280.4 119.6 L 281.8 117.5 L 283.2 115.3 L 284.6 113.2 L 286.0 111.1 L 287.3 109.1 L 288.7 107.1 L 290.1 105.2 L 291.5 103.3 L 292.9 101.5 L 294.3 99.7 L 295.6 98.0 L 297.0 96.3 L 298.4 94.8 L 299.8 93.2 L 301.2 91.8 L 302.6 90.4 L 303.9 89.1 L 305.3 87.9 L 306.7 86.8 L 308.1 85.7 L 309.5 84.7 L 310.9 83.8 L 312.2 83.0 L 313.6 82.3 L 315.0 81.7 L 316.4 81.1 L 317.8 80.7 L 319.2 80.3 L 320.5 80.0 L 321.9 79.8 L 323.3 79.8 L 324.7 79.8 L 326.1 79.8 L 327.5 80.0 L 328.8 80.3 L 330.2 80.7 L 331.6 81.1 L 333.0 81.7 L 334.4 82.3 L 335.8 83.0 L 337.1 83.8 L 338.5 84.7 L 339.9 85.7 L 341.3 86.8 L 342.7 87.9 L 344.1 89.1 L 345.4 90.4 L 346.8 91.8 L 348.2 93.2 L 349.6 94.8 L 351.0 96.3 L 352.4 98.0 L 353.7 99.7 L 355.1 101.5 L 356.5 103.3 L 357.9 105.2 L 359.3 107.1 L 360.7 109.1 L 362.0 111.1 L 363.4 113.2 L 364.8 115.3 L 366.2 117.5 L 367.6 119.6 L 369.0 121.9 L 370.3 124.1 L 371.7 126.4 L 373.1 128.7 L 374.5 131.0 L 375.9 133.3 L 377.3 135.6 L 378.6 138.0 L 380.0 140.4 L 381.4 142.7 L 382.8 145.1 L 384.2 147.5 L 385.6 149.8 L 386.9 152.2 L 388.3 154.6 L 389.7 156.9 L 391.1 159.2 L 392.5 161.6 L 393.9 163.9 L 395.2 166.2 L 396.6 168.4 L 398.0 170.7 L 399.4 172.9 L 400.8 175.1 L 402.2 177.3 L 403.5 179.4 L 404.9 181.5 L 406.3 183.6 L 407.7 185.7 L 409.1 187.7 L 410.5 189.7 L 411.8 191.6 L 413.2 193.6 L 414.6 195.4 L 416.0 197.3 L 417.4 199.1 L 418.8 200.8 L 420.2 202.6 L 421.5 204.3 L 422.9 205.9 L 424.3 207.5 L 425.7 209.1 L 427.1 210.6 L 428.5 212.1 L 429.8 213.6 L 431.2 215.0 L 432.6 216.4 L 434.0 217.7 L 435.4 219.0 L 436.8 220.2 L 438.1 221.5 L 439.5 222.6 L 440.9 223.8 L 442.3 224.9 L 443.7 226.0 L 445.1 227.0 L 446.4 228.0 L 447.8 229.0 L 449.2 229.9 L 450.6 230.8 L 452.0 231.7 L 453.4 232.5 L 454.7 233.3 L 456.1 234.1 L 457.5 234.8 L 458.9 235.5 L 460.3 236.2 L 461.7 236.9 L 463.0 237.5 L 464.4 238.1 L 465.8 238.7 L 467.2 239.3 L 468.6 239.8 L 470.0 240.3 L 471.3 240.8 L 472.7 241.3 L 474.1 241.7 L 475.5 242.2 L 476.9 242.6 L 478.3 243.0 L 479.6 243.3 L 481.0 243.7 L 482.4 244.0 L 483.8 244.4 L 485.2 244.7 L 486.6 245.0 L 487.9 245.2 L 489.3 245.5 L 490.7 245.7 L 492.1 246.0 L 493.5 246.2 L 494.9 246.4 L 496.2 246.6 L 497.6 246.8 L 499.0 247.0 L 500.4 247.2 L 501.8 247.4 L 503.2 247.5 L 504.5 247.7 L 505.9 247.8 L 507.3 247.9 L 508.7 248.1 L 510.1 248.2 L 511.5 248.3 L 512.8 248.4 L 514.2 248.5 L 515.6 248.6 L 517.0 248.7 L 518.4 248.8 L 519.8 248.8 L 521.1 248.9 L 522.5 249.0 L 523.9 249.0 L 525.3 249.1 L 526.7 249.2 L 528.1 249.2 L 529.4 249.3 L 530.8 249.3 L 532.2 249.4 L 533.6 249.4 L 535.0 249.4 L 536.4 249.5 L 537.7 249.5 L 539.1 249.5 L 540.5 249.6 L 541.9 249.6 L 543.3 249.6 L 544.7 249.7 L 546.0 249.7 L 547.4 249.7 L 548.8 249.7 L 550.2 249.7 L 551.6 249.8 L 553.0 249.8 L 554.3 249.8 L 555.7 249.8 L 557.1 249.8 L 558.5 249.8 L 559.9 249.8 L 561.3 249.9 L 562.6 249.9 L 564.0 249.9 L 565.4 249.9 L 566.8 249.9 L 568.2 249.9 L 569.6 249.9 L 570.9 249.9 L 572.3 249.9 L 573.7 249.9 L 575.1 249.9 L 576.5 249.9 L 577.9 249.9 L 579.2 249.9 L 580.6 249.9 L 582.0 250.0 L 583.4 250.0 L 584.8 250.0 L 586.2 250.0 L 587.5 250.0 L 588.9 250.0 L 590.3 250.0 L 591.7 250.0 L 593.1 250.0 L 594.5 250.0 L 595.8 250.0 L 597.2 250.0 L 598.6 250.0 L 600.0 250.0" fill="none" stroke="#5c6bc0" stroke-width="2.2" stroke-opacity="1.0"/><line x1="48.0" y1="250.0" x2="600.0" y2="250.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><line x1="84.0" y1="250.0" x2="84.0" y2="255.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><text x="84.0" y="270.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">-4</text><line x1="204.0" y1="250.0" x2="204.0" y2="255.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><text x="204.0" y="270.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">-2</text><line x1="324.0" y1="250.0" x2="324.0" y2="255.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><text x="324.0" y="270.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">0</text><line x1="444.0" y1="250.0" x2="444.0" y2="255.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><text x="444.0" y="270.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">2</text><line x1="564.0" y1="250.0" x2="564.0" y2="255.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><text x="564.0" y="270.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">4</text><text x="42.0" y="270.0" font-size="11.5" text-anchor="end" fill="currentColor" fill-opacity="0.8">t の値</text><line x1="204.0" y1="226.2" x2="204.0" y2="250.0" stroke="#c62828" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="3 3"/><text x="204.0" y="60.0" font-size="11.5" text-anchor="middle" font-weight="bold" fill="#c62828" fill-opacity="1.0">−2.00</text><line x1="444.0" y1="226.2" x2="444.0" y2="250.0" stroke="#c62828" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="3 3"/><text x="444.0" y="60.0" font-size="11.5" text-anchor="middle" font-weight="bold" fill="#c62828" fill-opacity="1.0">+2.00</text><text x="108.0" y="100.0" font-size="12" text-anchor="middle" font-weight="bold" fill="#c62828" fill-opacity="1.0">棄却域</text><text x="108.0" y="116.0" font-size="11" text-anchor="middle" fill="#c62828" fill-opacity="1.0">2.5%</text><text x="540.0" y="100.0" font-size="12" text-anchor="middle" font-weight="bold" fill="#c62828" fill-opacity="1.0">棄却域</text><text x="540.0" y="116.0" font-size="11" text-anchor="middle" fill="#c62828" fill-opacity="1.0">2.5%</text><text x="0.0" y="34.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">「差はない」と仮定したとき、t はこう散らばる</text><line x1="322.6" y1="250.0" x2="322.6" y2="73.8" stroke="#00897b" stroke-width="2" stroke-opacity="1.0"/><circle cx="322.6" cy="73.8" r="4" fill="#00897b" fill-opacity="1.0"/><text x="243.0" y="152.0" font-size="12" text-anchor="end" font-weight="bold" fill="#00897b" fill-opacity="1.0">クモザル科との比較</text><text x="243.0" y="170.0" font-size="12" text-anchor="end" fill="#00897b" fill-opacity="1.0">t = -0.02　ど真ん中</text><text x="243.0" y="188.0" font-size="11.5" text-anchor="end" fill="#00897b" fill-opacity="0.9">p = 0.98 ―― 偶然で説明がつく</text><text x="620.0" y="168.0" font-size="12" text-anchor="middle" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">オマキザル科との比較</text><line x1="576.0" y1="188.0" x2="702.0" y2="188.0" stroke="#ef6c00" stroke-width="2" stroke-opacity="0.9"/><polygon points="702.0,188.0 693.8,191.7 693.8,184.3" fill="#ef6c00" fill-opacity="0.9"/><text x="620.0" y="212.0" font-size="12.5" text-anchor="middle" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">t = 20.03</text><text x="620.0" y="228.0" font-size="11.5" text-anchor="middle" fill="#ef6c00" fill-opacity="1.0">この図の外、ずっと右</text><text x="0.0" y="296.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.9">p値は「塗った裾と同じ側にどれだけ入るか」の面積。t = 20.03 では面積が 8×10⁻²⁷ しか残らない。</text><text x="0.0" y="318.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.9">同じデータ・同じ手法でも、比べる相手を変えるだけでt はこれだけ動く。</text><text x="0.0" y="340.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.7">（Welch の t検定。自由度は約 60。体重は第3回のとおり常用対数で扱っている。）</text></svg>

---

## 2. t検定をやってみる（明確な差の例）

霊長類の進化を語るとき、大きな区分が **旧世界ザル**（アフリカ・アジア）と **新世界ザル**（中南米）である。両者は3,000万年以上前に分かれた。この2つの科で**体重に差があるか**を調べる。第3回のとおり体重は対数で扱う。

| 科 | 体重の中央値（n） |
|---|---|
| オナガザル科（旧世界） | 7,226 g（92種） |
| オマキザル科（新世界） | 492 g（39種） |

t検定の結果：**t = 20.03、p ≈ 8.4 × 10⁻²⁷**（ほぼ0）。

「差はない」と仮定すると、これほどの差（中央値で約15倍）は偶然ではまず起きない → **有意差あり**。

### 対照：差がない例も、同じデータの中にある

今度は **オナガザル科（旧世界）と クモザル科（新世界）** を比べる。クモザル科も新世界ザルだが、大型の種が多い。

| 科 | 体重の中央値（n） |
|---|---|
| オナガザル科 | 7,226 g（92種） |
| クモザル科 | 6,652 g（16種） |

**t = −0.02、p = 0.98。** まったく差があると言えない。

!!! warning "何と何を比べるかは、検定の外側"
    旧世界か新世界かで決まるのではない。**新世界ザルの中に、小型のオマキザル科と大型のクモザル科が両方いる**からである。

    **同じデータ・同じ手法で、比べる相手を変えただけで結論が正反対になる。**「何と何を比べるか」は検定にかける前の**あなたの判断**であり、統計は「その比較が妥当か」を教えてくれない。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 352" role="img" aria-labelledby="gpt gpd" style="width:100%;height:auto;max-width:720px;display:block;margin:0.8em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="gpt">比べる相手を変えると、結論は正反対になる</title><desc id="gpd">横軸は体重の常用対数。点は1種ずつ。オナガザル科（92種）の平均とクモザル科（16種）の平均はほとんど同じ位置に重なるが、オマキザル科（39種）はまるごと左にずれている。どちらもオナガザル科との比較なのに、結論が逆になる理由がこれである。</desc><text x="0.0" y="32.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">同じ「オナガザル科との比較」でも、相手でこれだけ違う</text><line x1="92.0" y1="62.0" x2="92.0" y2="262.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.12"/><text x="92.0" y="282.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">2</text><text x="92.0" y="297.0" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.6">(100g)</text><line x1="305.6" y1="62.0" x2="305.6" y2="262.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.12"/><text x="305.6" y="282.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">3</text><text x="305.6" y="297.0" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.6">(1,000g)</text><line x1="519.1" y1="62.0" x2="519.1" y2="262.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.12"/><text x="519.1" y="282.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">4</text><text x="519.1" y="297.0" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.6">(10,000g)</text><line x1="92.0" y1="262.0" x2="690.0" y2="262.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.4"/><text x="690.0" y="282.0" font-size="11.5" text-anchor="end" fill="currentColor" fill-opacity="0.8">体重の常用対数 log10(g)</text><text x="82.0" y="96.0" font-size="12" text-anchor="end" font-weight="bold" fill="#5c6bc0" fill-opacity="1.0">オナガザル科</text><text x="82.0" y="112.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">n = 92</text><circle cx="450.1" cy="87.5" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="487.4" cy="104.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="485.3" cy="87.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="487.1" cy="99.5" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="489.9" cy="101.6" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="422.8" cy="89.2" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="425.1" cy="90.4" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="420.3" cy="88.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="442.1" cy="81.8" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="400.5" cy="91.5" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="420.3" cy="85.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="415.0" cy="85.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="460.4" cy="83.8" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="455.6" cy="84.0" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="433.7" cy="100.2" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="460.7" cy="90.0" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="459.5" cy="85.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="414.4" cy="94.4" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="423.8" cy="94.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="457.3" cy="95.8" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="409.5" cy="102.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="459.5" cy="82.9" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="415.0" cy="88.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="426.8" cy="86.4" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="509.3" cy="79.4" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="518.5" cy="83.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="507.3" cy="89.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="509.9" cy="89.2" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="494.9" cy="95.0" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="498.1" cy="90.8" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="491.4" cy="94.8" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="479.3" cy="84.8" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="513.0" cy="82.5" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="504.6" cy="87.6" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="467.8" cy="81.5" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="446.5" cy="88.5" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="520.2" cy="91.0" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="489.8" cy="97.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="478.5" cy="101.5" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="496.3" cy="80.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="490.7" cy="103.9" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="399.2" cy="97.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="445.8" cy="104.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="454.9" cy="82.1" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="471.7" cy="88.8" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="448.2" cy="92.1" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="531.9" cy="98.4" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="524.5" cy="87.1" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="519.5" cy="90.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="552.0" cy="86.2" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="566.6" cy="90.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="326.2" cy="92.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="538.1" cy="93.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="572.3" cy="97.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="561.7" cy="85.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="550.4" cy="95.4" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="573.8" cy="81.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="572.3" cy="94.9" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="503.3" cy="90.9" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="488.1" cy="82.5" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="527.1" cy="85.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="508.0" cy="80.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="498.8" cy="88.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="479.9" cy="89.5" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="486.4" cy="91.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="473.2" cy="80.8" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="476.0" cy="97.6" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="478.3" cy="87.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="478.5" cy="86.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="477.0" cy="102.2" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="470.1" cy="94.6" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="481.9" cy="96.1" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="433.6" cy="92.8" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="513.5" cy="84.6" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="522.2" cy="82.9" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="510.3" cy="83.8" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="528.0" cy="87.9" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="538.1" cy="83.4" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="546.7" cy="91.4" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="541.2" cy="104.2" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="519.4" cy="98.2" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="491.1" cy="87.1" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="562.5" cy="87.0" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="516.5" cy="99.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="488.4" cy="104.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="500.1" cy="95.0" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="502.5" cy="85.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="524.5" cy="90.7" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="489.3" cy="83.1" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="494.7" cy="90.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="529.8" cy="102.2" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><circle cx="488.7" cy="84.3" r="2.8" fill="#5c6bc0" fill-opacity="0.55"/><line x1="486.0" y1="70.0" x2="486.0" y2="114.0" stroke="#5c6bc0" stroke-width="2.2" stroke-opacity="1.0"/><text x="486.0" y="64.0" font-size="11" text-anchor="middle" font-weight="bold" fill="#5c6bc0" fill-opacity="1.0">平均 3.84</text><text x="82.0" y="164.0" font-size="12" text-anchor="end" font-weight="bold" fill="#00897b" fill-opacity="1.0">クモザル科</text><text x="82.0" y="180.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">n = 16</text><circle cx="474.2" cy="158.5" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="465.0" cy="163.4" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="458.3" cy="171.7" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="480.3" cy="163.4" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="488.3" cy="158.5" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="480.8" cy="164.0" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="477.7" cy="154.7" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="481.9" cy="149.6" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="486.8" cy="168.6" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="510.1" cy="159.1" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="493.5" cy="171.1" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="475.2" cy="151.9" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="506.2" cy="147.3" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="524.0" cy="160.4" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="475.8" cy="165.5" r="2.8" fill="#00897b" fill-opacity="0.55"/><circle cx="501.1" cy="172.7" r="2.8" fill="#00897b" fill-opacity="0.55"/><line x1="486.2" y1="138.0" x2="486.2" y2="182.0" stroke="#00897b" stroke-width="2.2" stroke-opacity="1.0"/><text x="486.2" y="132.0" font-size="11" text-anchor="middle" font-weight="bold" fill="#00897b" fill-opacity="1.0">平均 3.85</text><text x="82.0" y="232.0" font-size="12" text-anchor="end" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">オマキザル科</text><text x="82.0" y="248.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">n = 39</text><circle cx="251.5" cy="231.6" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="216.5" cy="217.4" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="217.3" cy="229.5" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="196.8" cy="225.0" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="214.1" cy="219.8" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="206.1" cy="236.3" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="214.6" cy="233.6" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="190.8" cy="236.0" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="214.6" cy="230.9" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="230.2" cy="233.1" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="220.8" cy="232.9" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="205.5" cy="221.6" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="111.9" cy="229.6" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="390.9" cy="237.7" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="399.7" cy="224.6" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="407.7" cy="219.3" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="407.5" cy="215.6" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="400.7" cy="217.1" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="258.8" cy="226.3" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="253.9" cy="215.5" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="266.5" cy="232.6" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="257.0" cy="233.8" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="234.5" cy="239.3" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="219.2" cy="234.3" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="239.9" cy="226.1" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="222.4" cy="235.2" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="285.2" cy="234.7" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="242.8" cy="216.7" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="232.9" cy="215.7" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="248.5" cy="220.0" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="251.1" cy="239.7" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="231.5" cy="224.9" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="234.0" cy="236.3" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="217.0" cy="224.5" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="284.8" cy="231.9" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="274.3" cy="224.7" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="278.8" cy="236.3" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="294.4" cy="228.4" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><circle cx="283.0" cy="239.6" r="2.8" fill="#ef6c00" fill-opacity="0.55"/><line x1="256.6" y1="206.0" x2="256.6" y2="250.0" stroke="#ef6c00" stroke-width="2.2" stroke-opacity="1.0"/><text x="256.6" y="200.0" font-size="11" text-anchor="middle" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">平均 2.77</text><circle cx="8.0" cy="314.0" r="3.4" fill="#00897b" fill-opacity="0.9"/><text x="20.0" y="318.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.95">オナガザル科 と クモザル科 → 差があるとは言えない（t = −0.02, p = 0.98）</text><circle cx="8.0" cy="336.0" r="3.4" fill="#ef6c00" fill-opacity="0.9"/><text x="20.0" y="340.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.95">オナガザル科 と オマキザル科 → はっきり差がある（t = 20.03, p ≒ 8×10⁻²⁷）</text></svg>

### 導出①：なぜ \( n-1 \) で割るのか（不偏分散）

標本からばらつきを見積もるとき、分散は \( s^2 = \frac{1}{n-1}\sum (X_i-\bar{X})^2 \) と、\( n \) ではなく \( n-1 \) で割る。なぜか。

**二乗和の期待値を、最後まで計算してみれば分かる。**

!!! tip "下のボタンで、1行ずつ送れる"
    「次の式へ ▶」を押すと、変形が1段ずつ現れる。**各行には、何をしたのかが付いている。**

<div class="deriv" markdown>

<div markdown>

$$ \sum_{i=1}^{n}(X_i-\bar{X})^2 \quad\text{の期待値を求めたい} $$

**目標。**これが \( n\sigma^2 \) になるなら \( n \) で割ればよいし、\( (n-1)\sigma^2 \) になるなら \( n-1 \) で割ればよい。

</div>

<div markdown>

$$ X_i-\bar{X} \;=\; (X_i-\mu)-(\bar{X}-\mu) $$

**μ を足して引いただけ。**μ は未知だが、**期待値を計算するときには使える**（\( \mathbb{E}[(X_i-\mu)^2]=\sigma^2 \) が分かっているので）。

</div>

<div markdown>

$$ \sum_{i=1}^{n}(X_i-\bar{X})^2 \;=\; \sum_{i=1}^{n}(X_i-\mu)^2 \;-\; 2(\bar{X}-\mu)\sum_{i=1}^{n}(X_i-\mu) \;+\; n(\bar{X}-\mu)^2 $$

**二乗して和を取った。**\( (a-b)^2 = a^2-2ab+b^2 \) をそのまま使っただけ。
\( (\bar{X}-\mu) \) は \( i \) によらないので、**和の外に出せる**（最後の項が \( n \) 倍になるのもそのため）。

</div>

<div markdown>

$$ \sum_{i=1}^{n}(X_i-\mu) \;=\; \sum_{i=1}^{n}X_i - n\mu \;=\; n\bar{X}-n\mu \;=\; n(\bar{X}-\mu) $$

**交差項の中身を先に片づける。**\( \sum X_i = n\bar{X} \)（標本平均の定義）を使った。
**ここが、この導出の山である。**

</div>

<div markdown>

$$ \sum_{i=1}^{n}(X_i-\bar{X})^2 \;=\; \sum_{i=1}^{n}(X_i-\mu)^2 \;-\; 2n(\bar{X}-\mu)^2 \;+\; n(\bar{X}-\mu)^2 $$

**いまの結果を交差項に代入した。**\( -2(\bar{X}-\mu)\cdot n(\bar{X}-\mu) = -2n(\bar{X}-\mu)^2 \)。

</div>

<div markdown>

$$ \sum_{i=1}^{n}(X_i-\bar{X})^2 \;=\; \sum_{i=1}^{n}(X_i-\mu)^2 \;-\; n(\bar{X}-\mu)^2 $$

**同類項をまとめた。**\( -2n + n = -n \)。
ここまでは**確率も期待値も出てこない。ただの式変形**である。

</div>

<div markdown>

$$ \mathbb{E}[X] \;=\; \sum_x x \cdot \Pr(X=x) $$

**ここから期待値を使う。まず定義に戻る。**
「**取りうる値 × その確率** を、全部足したもの」＝平均のこと。
次の段で使う「線形性」は、この定義から出てくる。

</div>

<div markdown>

$$ \mathbb{E}[aX+bY] \;=\; a\,\mathbb{E}[X] + b\,\mathbb{E}[Y] $$

**期待値の線形性。**定義に入れて和の順番を入れ替えるだけで出る。
\( \sum_{x,y}(ax+by)\Pr(x,y) = a\sum_{x,y}x\Pr(x,y) + b\sum_{x,y}y\Pr(x,y) \)。

🔴 **ここでは独立を使っていない。**分散の加法性（第6回 導出①の9段目）は独立が要ったが、
**期待値の線形性は、連動していても成り立つ。**だから相関したデータにも、そのまま使える。

</div>

<div markdown>

$$ \mathbb{E}\!\left[\sum_{i=1}^{n}(X_i-\bar{X})^2\right] \;=\; \sum_{i=1}^{n}\mathbb{E}\!\left[(X_i-\mu)^2\right] \;-\; n\,\mathbb{E}\!\left[(\bar{X}-\mu)^2\right] $$

**両辺の期待値を取った。**期待値は和と定数倍について線形なので、そのまま中に入れられる。

</div>

<div markdown>

$$ \mathbb{E}\!\left[\sum_{i=1}^{n}(X_i-\bar{X})^2\right] \;=\; n\sigma^2 \;-\; n\cdot\frac{\sigma^2}{n} $$

**2つの期待値を、既に知っている値で置き換えた。**

- \( \mathbb{E}[(X_i-\mu)^2]=\sigma^2 \) …… 母分散の定義。それが \( n \) 個
- \( \mathbb{E}[(\bar{X}-\mu)^2]=\mathrm{Var}[\bar{X}]=\sigma^2/n \) …… **第7回の導出②**で出したもの

</div>

<div markdown>

$$ \mathbb{E}\!\left[\sum_{i=1}^{n}(X_i-\bar{X})^2\right] \;=\; n\sigma^2-\sigma^2 \;=\; (n-1)\,\sigma^2 $$

**答え。**二乗和の期待値は \( n\sigma^2 \) ではなく \( (n-1)\sigma^2 \) だった。

</div>

<div markdown>

$$ \mathbb{E}\!\left[\frac{1}{n-1}\sum_{i=1}^{n}(X_i-\bar{X})^2\right] \;=\; \sigma^2 $$

**だから \( n-1 \) で割る。**こうして初めて、期待値がちょうど母分散 \( \sigma^2 \) に一致する。
\( n \) で割ると \( \frac{n-1}{n}\sigma^2 \) となり、**系統的に小さめに出る**。

</div>

</div>

**なぜ1つ減るのか**：二乗和の中心に、母平均 \( \mu \) ではなく**データから計算した** \( \bar{X} \) を使っている。\( \bar{X} \) はデータに一番近い位置に自分で寄っていくので、ズレが本来より小さく見える。その「使ってしまった1つ分」が自由度 \( n-1 \) である。

**数値で確かめる**：この母集団から n=30 を20万回とると、\( \sum(X_i-\bar{X})^2 \) の平均は 4,979,270,647。\( (n-1)\sigma^2 = 29\sigma^2 \) は 4,984,114,411（比 0.999）。n で割ると 165,975,688 となり母分散 171,866,014 を下回るが、n−1 で割ると 171,698,988 でほぼ一致する。

**使った数学**：二乗和の展開と総和の記号操作（線I）、期待値の線形性（微I）、第7回で導いた \( \mathrm{Var}[\bar{X}]=\sigma^2/n \)。

???+ note "導出②：t 統計量はどこから来るか"

    第7回の導出③で、母標準偏差 \( \sigma \) が既知なら

    $$ Z \;=\; \frac{\bar{X}-\mu}{\sigma/\sqrt{n}} \;\approx\; N(0,1) $$

    が使えることを見た。しかし実際に \( \sigma \) が分かっていることはまずない。そこで導出①の \( s \) を代わりに置く。

    $$ t \;=\; \frac{\bar{X}-\mu}{s/\sqrt{n}} $$

    形は同じでも、中身が変わっている。\( Z \) では分母が**定数**だったが、\( t \) では分母の \( s \) も標本ごとに揺れる**確率変数**である。分子と分母の両方が揺れるぶん、この比は \( Z \) より極端な値を取りやすい。つまり**裾が重い**。これが自由度 \( n-1 \) の **t 分布**である。自由度が \( n-1 \) なのは、導出①と同じ理由で \( s \) が \( \bar{X} \) を使って計算されているからだ。

    2群の差を見るときも発想は同じで、分子を「2群の平均の差」、分母を「その差の標準誤差」に置き換える。

    $$ t \;=\; \frac{\bar{X}_1-\bar{X}_2}{\;\widehat{SE}(\bar{X}_1-\bar{X}_2)\;} $$

    n が大きくなると \( s \) は \( \sigma \) に近づくので、t 分布は正規分布に近づく。第7回で使った 1.96 は、その極限の値である。

    !!! note "分母の作り方は一通りではない"
        2群の \( \widehat{SE} \) には流儀がある。両群の分散が等しいと仮定してまとめる形（Student）と、仮定せずに別々に扱う形（**Welch**）である。上の「オナガザル科 vs オマキザル科」の t = 20.03 は Welch で計算した値で、等分散を仮定すると t = 23.03 になる。実際この2群は標本分散が 0.046 と 0.093 で2倍ほど違うため、仮定を置かない Welch のほうが安全である。

        なお t 分布の密度関数そのものを導くには、\( \chi^2 \) 分布と確率変数の比の分布が必要になる。**このコースでは扱わない**（統計学Ⅱ 第7回で形を確認する）。

    **使った数学**：標準化（線I的なスケール変換）、確率変数の比という見方（微I）。


---

## 3. p値の意味を、正しく

ここで誤解を3つ、はっきり打ち消す。

- ❌ **p値は「帰無仮説が正しい確率」ではない**。p値は「帰無仮説が正しいと**仮定したとき**に、観測以上の差が出る確率」。
- ❌ **p値は「効果の大きさ」ではない**。p=0.001 でも差は小さいことがある。
- ❌ **「有意（p<0.05）＝重要」ではない**。有意は「偶然では説明しにくい」だけ。

---

## 4. p値の脆さ ―― 同じ差でも n で変わる

冒頭のフックに戻る。保護区の外6.0kg・中6.2kg、**真の差はたった0.2kgで固定**。そこから n 頭ずつ捕獲して測る、をくりかえし、有意（p<0.05）になった割合を見る。

| 各群の頭数 n | 有意になった割合 |
|---|---|
| 20 | **8.6%** |
| 100 | **24.5%** |
| 500 | **81.1%** |

（両側5%・等分散のt検定の理論値。20万回のシミュレーションでも同じ値になる。）

!!! danger "効果は同じ。n が違うだけ"
    真の差は常に0.2kg。なのに **n を増やすほど「有意」になりやすい**。
    つまり、サンプルを増やすだけで小さな差でも「有意差あり」を作れてしまう。
    **「p<0.05だった」だけでは、効果が大きいことの証明にはならない。**

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 374" role="img" aria-labelledby="pwt pwd" style="width:100%;height:auto;max-width:720px;display:block;margin:0.8em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="pwt">差の大きさは同じ。増やしたのは人数だけ</title><desc id="pwd">横軸は各群の頭数（対数目盛り）、縦軸は「有意（p&lt;0.05）になる割合」。真の差は常に0.2kg（効果量 d = 0.18）で固定されている。それでも各群20頭なら8.6%、100頭で24.5%、500頭で81.1%が有意になる。人数を増やすだけで「有意差あり」は作れてしまう。</desc><text x="0.0" y="32.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">真の差は 0.2kg のまま。増やしたのは人数だけ</text><line x1="58.0" y1="258.0" x2="600.0" y2="258.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><text x="50.0" y="262.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">0%</text><line x1="58.0" y1="210.0" x2="600.0" y2="210.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="50.0" y="214.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">25%</text><line x1="58.0" y1="162.0" x2="600.0" y2="162.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="50.0" y="166.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">50%</text><line x1="58.0" y1="114.0" x2="600.0" y2="114.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="50.0" y="118.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">75%</text><line x1="58.0" y1="66.0" x2="600.0" y2="66.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="50.0" y="70.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">100%</text><line x1="58.0" y1="66.0" x2="58.0" y2="258.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.1"/><text x="58.0" y="277.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">10</text><line x1="329.0" y1="66.0" x2="329.0" y2="258.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.1"/><text x="329.0" y="277.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">100</text><line x1="600.0" y1="66.0" x2="600.0" y2="258.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.1"/><text x="600.0" y="277.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">1000</text><line x1="58.0" y1="66.0" x2="58.0" y2="258.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><text x="329.0" y="298.0" font-size="11.5" text-anchor="middle" fill="currentColor" fill-opacity="0.8">各群の頭数（対数目盛り）</text><text x="50.0" y="252.4" font-size="11" text-anchor="end" fill="#c62828" fill-opacity="0.9">5%</text><line x1="58.0" y1="248.4" x2="600.0" y2="248.4" stroke="#c62828" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="4 3"/><text x="587.6" y="238.4" font-size="11" text-anchor="end" fill="#c62828" fill-opacity="0.9">差が無いときでも有意になる割合（＝5%）</text><path d="M 58.0 245.2 L 69.2 244.8 L 79.5 244.4 L 88.9 244.1 L 97.6 243.7 L 105.7 243.3 L 113.3 243.0 L 120.5 242.6 L 127.2 242.2 L 133.5 241.9 L 139.6 241.5 L 145.3 241.1 L 150.8 240.8 L 156.0 240.4 L 161.0 240.0 L 165.8 239.6 L 170.5 239.3 L 174.9 238.9 L 179.2 238.5 L 183.3 238.1 L 187.3 237.8 L 191.2 237.4 L 194.9 237.0 L 198.5 236.6 L 202.0 236.3 L 205.4 235.9 L 208.8 235.5 L 212.0 235.1 L 215.1 234.8 L 218.2 234.4 L 221.2 234.0 L 224.1 233.6 L 226.9 233.2 L 229.7 232.9 L 232.4 232.5 L 235.0 232.1 L 237.6 231.7 L 240.1 231.3 L 242.6 231.0 L 245.0 230.6 L 247.4 230.2 L 249.8 229.8 L 252.0 229.4 L 254.3 229.1 L 256.5 228.7 L 258.6 228.3 L 260.8 227.9 L 262.8 227.5 L 264.9 227.1 L 266.9 226.8 L 268.9 226.4 L 270.8 226.0 L 272.7 225.6 L 274.6 225.2 L 276.5 224.8 L 278.3 224.5 L 280.1 224.1 L 281.9 223.7 L 283.6 223.3 L 285.3 222.9 L 287.0 222.5 L 288.7 222.2 L 290.3 221.8 L 292.0 221.4 L 293.6 221.0 L 295.1 220.6 L 296.7 220.2 L 298.2 219.9 L 299.8 219.5 L 301.3 219.1 L 302.7 218.7 L 304.2 218.3 L 305.6 217.9 L 307.1 217.5 L 308.5 217.2 L 309.9 216.8 L 311.2 216.4 L 312.6 216.0 L 314.0 215.6 L 315.3 215.2 L 316.6 214.9 L 317.9 214.5 L 319.2 214.1 L 320.5 213.7 L 321.7 213.3 L 323.0 212.9 L 324.2 212.6 L 325.4 212.2 L 326.6 211.8 L 327.8 211.4 L 329.0 211.0 L 330.2 210.6 L 331.3 210.3 L 332.5 209.9 L 333.6 209.5 L 334.7 209.1 L 335.9 208.7 L 337.0 208.3 L 338.1 208.0 L 339.1 207.6 L 340.2 207.2 L 341.3 206.8 L 342.3 206.4 L 343.4 206.1 L 344.4 205.7 L 345.4 205.3 L 346.5 204.9 L 347.5 204.5 L 348.5 204.2 L 349.5 203.8 L 350.5 203.4 L 351.4 203.0 L 352.4 202.7 L 353.4 202.3 L 354.3 201.9 L 355.3 201.5 L 356.2 201.2 L 357.1 200.8 L 358.1 200.4 L 359.0 200.0 L 359.9 199.7 L 360.8 199.3 L 361.7 198.9 L 362.6 198.5 L 363.4 198.2 L 364.3 197.8 L 365.2 197.4 L 366.1 197.0 L 366.9 196.7 L 367.8 196.3 L 368.6 195.9 L 369.4 195.6 L 370.3 195.2 L 371.1 194.8 L 371.9 194.4 L 372.7 194.1 L 373.5 193.7 L 374.3 193.3 L 375.1 193.0 L 375.9 192.6 L 376.7 192.2 L 377.5 191.9 L 378.3 191.5 L 379.1 191.1 L 379.8 190.8 L 380.6 190.4 L 381.3 190.0 L 382.1 189.7 L 382.8 189.3 L 383.6 188.9 L 384.3 188.6 L 385.0 188.2 L 385.8 187.9 L 386.5 187.5 L 387.2 187.1 L 387.9 186.8 L 388.6 186.4 L 389.4 186.1 L 390.1 185.7 L 390.8 185.3 L 391.5 185.0 L 392.1 184.6 L 392.8 184.3 L 393.5 183.9 L 394.2 183.6 L 394.9 183.2 L 395.5 182.9 L 396.2 182.5 L 396.9 182.1 L 397.5 181.8 L 398.2 181.4 L 398.8 181.1 L 399.5 180.7 L 400.1 180.4 L 400.8 180.0 L 401.4 179.7 L 402.0 179.3 L 402.7 179.0 L 403.3 178.6 L 403.9 178.3 L 404.5 177.9 L 405.2 177.6 L 405.8 177.3 L 406.4 176.9 L 407.0 176.6 L 407.6 176.2 L 408.2 175.9 L 408.8 175.5 L 409.4 175.2 L 410.0 174.9 L 410.6 174.5 L 411.2 174.2 L 411.8 173.8 L 412.3 173.5 L 412.9 173.2 L 413.5 172.8 L 414.1 172.5 L 414.6 172.1 L 415.2 171.8 L 415.8 171.5 L 416.3 171.1 L 416.9 170.8 L 417.4 170.5 L 418.0 170.1 L 418.5 169.8 L 419.1 169.5 L 419.6 169.1 L 420.2 168.8 L 420.7 168.5 L 421.3 168.2 L 421.8 167.8 L 422.3 167.5 L 422.9 167.2 L 423.4 166.8 L 423.9 166.5 L 424.4 166.2 L 425.0 165.9 L 425.5 165.5 L 426.0 165.2 L 426.5 164.9 L 427.0 164.6 L 427.5 164.3 L 428.0 163.9 L 428.6 163.6 L 429.1 163.3 L 429.6 163.0 L 430.1 162.7 L 430.6 162.3 L 431.1 162.0 L 431.5 161.7 L 432.0 161.4 L 432.5 161.1 L 433.0 160.8 L 433.5 160.4 L 434.0 160.1 L 434.5 159.8 L 434.9 159.5 L 435.4 159.2 L 435.9 158.9 L 436.4 158.6 L 436.8 158.3 L 437.3 158.0 L 437.8 157.7 L 438.2 157.3 L 438.7 157.0 L 439.2 156.7 L 439.6 156.4 L 440.1 156.1 L 440.5 155.8 L 441.0 155.5 L 441.5 155.2 L 441.9 154.9 L 442.4 154.6 L 442.8 154.3 L 443.3 154.0 L 443.7 153.7 L 444.1 153.4 L 444.6 153.1 L 445.0 152.8 L 445.5 152.5 L 445.9 152.2 L 446.3 151.9 L 446.8 151.7 L 447.2 151.4 L 447.6 151.1 L 448.1 150.8 L 448.5 150.5 L 448.9 150.2 L 449.3 149.9 L 449.8 149.6 L 450.2 149.3 L 450.6 149.0 L 451.0 148.8 L 451.4 148.5 L 451.8 148.2 L 452.3 147.9 L 452.7 147.6 L 453.1 147.3 L 453.5 147.0 L 453.9 146.8 L 454.3 146.5 L 454.7 146.2 L 455.1 145.9 L 455.5 145.6 L 455.9 145.4 L 456.3 145.1 L 456.7 144.8 L 457.1 144.5 L 457.5 144.3 L 457.9 144.0 L 458.3 143.7 L 458.7 143.4 L 459.1 143.2 L 459.5 142.9 L 459.9 142.6 L 460.2 142.4 L 460.6 142.1 L 461.0 141.8 L 461.4 141.5 L 461.8 141.3 L 462.2 141.0 L 462.5 140.7 L 462.9 140.5 L 463.3 140.2 L 463.7 139.9 L 464.0 139.7 L 464.4 139.4 L 464.8 139.2 L 465.2 138.9 L 465.5 138.6 L 465.9 138.4 L 466.3 138.1 L 466.6 137.9 L 467.0 137.6 L 467.4 137.3 L 467.7 137.1 L 468.1 136.8 L 468.4 136.6 L 468.8 136.3 L 469.2 136.1 L 469.5 135.8 L 469.9 135.6 L 470.2 135.3 L 470.6 135.1 L 470.9 134.8 L 471.3 134.6 L 471.6 134.3 L 472.0 134.1 L 472.3 133.8 L 472.7 133.6 L 473.0 133.3 L 473.4 133.1 L 473.7 132.8 L 474.1 132.6 L 474.4 132.3 L 474.7 132.1 L 475.1 131.9 L 475.4 131.6 L 475.8 131.4 L 476.1 131.1 L 476.4 130.9 L 476.8 130.7 L 477.1 130.4 L 477.4 130.2 L 477.8 129.9 L 478.1 129.7 L 478.4 129.5 L 478.8 129.2 L 479.1 129.0 L 479.4 128.8 L 479.8 128.5 L 480.1 128.3 L 480.4 128.1 L 480.7 127.8 L 481.1 127.6 L 481.4 127.4 L 481.7 127.2 L 482.0 126.9 L 482.3 126.7 L 482.7 126.5 L 483.0 126.2 L 483.3 126.0 L 483.6 125.8 L 483.9 125.6 L 484.2 125.4 L 484.6 125.1 L 484.9 124.9 L 485.2 124.7 L 485.5 124.5 L 485.8 124.2 L 486.1 124.0 L 486.4 123.8 L 486.7 123.6 L 487.0 123.4 L 487.4 123.2 L 487.7 122.9 L 488.0 122.7 L 488.3 122.5 L 488.6 122.3 L 488.9 122.1 L 489.2 121.9 L 489.5 121.7 L 489.8 121.4 L 490.1 121.2 L 490.4 121.0 L 490.7 120.8 L 491.0 120.6 L 491.3 120.4 L 491.6 120.2 L 491.9 120.0 L 492.2 119.8 L 492.5 119.6 L 492.7 119.4 L 493.0 119.2 L 493.3 119.0 L 493.6 118.8 L 493.9 118.6 L 494.2 118.4 L 494.5 118.2 L 494.8 118.0 L 495.1 117.8 L 495.4 117.6 L 495.6 117.4 L 495.9 117.2 L 496.2 117.0 L 496.5 116.8 L 496.8 116.6 L 497.1 116.4 L 497.3 116.2 L 497.6 116.0 L 497.9 115.8 L 498.2 115.6 L 498.5 115.4 L 498.7 115.2 L 499.0 115.0 L 499.3 114.8 L 499.6 114.6 L 499.8 114.4 L 500.1 114.3 L 500.4 114.1 L 500.7 113.9 L 500.9 113.7 L 501.2 113.5 L 501.5 113.3 L 501.8 113.1 L 502.0 113.0 L 502.3 112.8 L 502.6 112.6 L 502.8 112.4 L 503.1 112.2 L 503.4 112.0 L 503.6 111.9 L 503.9 111.7 L 504.2 111.5 L 504.4 111.3 L 504.7 111.1 L 505.0 111.0 L 505.2 110.8 L 505.5 110.6 L 505.8 110.4 L 506.0 110.3 L 506.3 110.1 L 506.5 109.9 L 506.8 109.7 L 507.1 109.6 L 507.3 109.4 L 507.6 109.2 L 507.8 109.0 L 508.1 108.9 L 508.4 108.7 L 508.6 108.5 L 508.9 108.4 L 509.1 108.2 L 509.4 108.0 L 509.6 107.9 L 509.9 107.7 L 510.1 107.5 L 510.4 107.4 L 510.6 107.2 L 510.9 107.0 L 511.1 106.9 L 511.4 106.7 L 511.6 106.5 L 511.9 106.4 L 512.1 106.2 L 512.4 106.1 L 512.6 105.9 L 512.9 105.7 L 513.1 105.6 L 513.4 105.4 L 513.6 105.3 L 513.9 105.1 L 514.1 104.9 L 514.3 104.8 L 514.6 104.6 L 514.8 104.5 L 515.1 104.3 L 515.3 104.2 L 515.6 104.0 L 515.8 103.9 L 516.0 103.7 L 516.3 103.5 L 516.5 103.4 L 516.8 103.2 L 517.0 103.1 L 517.2 102.9 L 517.5 102.8 L 517.7 102.6 L 517.9 102.5 L 518.2 102.3 L 518.4 102.2 L 518.7 102.0 L 518.9 101.9 L 519.1 101.8 L 519.4 101.6 L 519.6 101.5 L 519.8 101.3 L 520.1 101.2 L 520.3 101.0 L 520.5 100.9 L 520.8 100.7 L 521.0 100.6 L 521.2 100.5 L 521.4 100.3 L 521.7 100.2 L 521.9 100.0 L 522.1 99.9 L 522.4 99.8 L 522.6 99.6 L 522.8 99.5 L 523.0 99.3 L 523.3 99.2 L 523.5 99.1 L 523.7 98.9 L 523.9 98.8 L 524.2 98.7 L 524.4 98.5 L 524.6 98.4 L 524.8 98.3 L 525.1 98.1 L 525.3 98.0 L 525.5 97.9 L 525.7 97.7 L 525.9 97.6 L 526.2 97.5 L 526.4 97.3 L 526.6 97.2 L 526.8 97.1 L 527.0 96.9 L 527.3 96.8 L 527.5 96.7 L 527.7 96.6 L 527.9 96.4 L 528.1 96.3 L 528.3 96.2 L 528.6 96.1 L 528.8 95.9 L 529.0 95.8 L 529.2 95.7 L 529.4 95.6 L 529.6 95.4 L 529.9 95.3 L 530.1 95.2 L 530.3 95.1 L 530.5 94.9 L 530.7 94.8 L 530.9 94.7 L 531.1 94.6 L 531.3 94.5 L 531.5 94.3 L 531.8 94.2 L 532.0 94.1 L 532.2 94.0 L 532.4 93.9 L 532.6 93.8 L 532.8 93.6 L 533.0 93.5 L 533.2 93.4 L 533.4 93.3 L 533.6 93.2 L 533.8 93.1 L 534.0 92.9 L 534.3 92.8 L 534.5 92.7 L 534.7 92.6 L 534.9 92.5 L 535.1 92.4 L 535.3 92.3 L 535.5 92.2 L 535.7 92.0 L 535.9 91.9 L 536.1 91.8 L 536.3 91.7 L 536.5 91.6 L 536.7 91.5 L 536.9 91.4 L 537.1 91.3 L 537.3 91.2 L 537.5 91.1 L 537.7 91.0 L 537.9 90.8 L 538.1 90.7 L 538.3 90.6 L 538.5 90.5 L 538.7 90.4 L 538.9 90.3 L 539.1 90.2 L 539.3 90.1 L 539.5 90.0 L 539.7 89.9 L 539.9 89.8 L 540.1 89.7 L 540.3 89.6 L 540.5 89.5 L 540.7 89.4 L 540.9 89.3 L 541.1 89.2 L 541.2 89.1 L 541.4 89.0 L 541.6 88.9 L 541.8 88.8 L 542.0 88.7 L 542.2 88.6 L 542.4 88.5 L 542.6 88.4 L 542.8 88.3 L 543.0 88.2 L 543.2 88.1 L 543.4 88.0 L 543.5 87.9 L 543.7 87.8 L 543.9 87.7 L 544.1 87.7 L 544.3 87.6 L 544.5 87.5 L 544.7 87.4 L 544.9 87.3 L 545.1 87.2 L 545.2 87.1 L 545.4 87.0 L 545.6 86.9 L 545.8 86.8 L 546.0 86.7 L 546.2 86.6 L 546.4 86.6 L 546.6 86.5 L 546.7 86.4 L 546.9 86.3 L 547.1 86.2 L 547.3 86.1 L 547.5 86.0 L 547.7 85.9 L 547.8 85.8 L 548.0 85.8 L 548.2 85.7 L 548.4 85.6 L 548.6 85.5 L 548.8 85.4 L 548.9 85.3 L 549.1 85.2 L 549.3 85.2 L 549.5 85.1 L 549.7 85.0 L 549.8 84.9 L 550.0 84.8 L 550.2 84.7 L 550.4 84.7 L 550.6 84.6 L 550.7 84.5 L 550.9 84.4 L 551.1 84.3 L 551.3 84.3 L 551.5 84.2 L 551.6 84.1 L 551.8 84.0 L 552.0 83.9 L 552.2 83.9 L 552.3 83.8 L 552.5 83.7 L 552.7 83.6 L 552.9 83.5 L 553.0 83.5 L 553.2 83.4 L 553.4 83.3 L 553.6 83.2 L 553.7 83.2 L 553.9 83.1 L 554.1 83.0 L 554.3 82.9 L 554.4 82.9 L 554.6 82.8 L 554.8 82.7 L 555.0 82.6 L 555.1 82.6 L 555.3 82.5 L 555.5 82.4 L 555.6 82.3 L 555.8 82.3 L 556.0 82.2 L 556.2 82.1 L 556.3 82.1 L 556.5 82.0 L 556.7 81.9 L 556.8 81.8 L 557.0 81.8 L 557.2 81.7 L 557.3 81.6 L 557.5 81.6 L 557.7 81.5 L 557.9 81.4 L 558.0 81.4 L 558.2 81.3 L 558.4 81.2 L 558.5 81.2 L 558.7 81.1 L 558.9 81.0 L 559.0 80.9 L 559.2 80.9 L 559.4 80.8 L 559.5 80.7 L 559.7 80.7 L 559.9 80.6 L 560.0 80.6 L 560.2 80.5 L 560.4 80.4 L 560.5 80.4 L 560.7 80.3 L 560.8 80.2 L 561.0 80.2 L 561.2 80.1 L 561.3 80.0 L 561.5 80.0 L 561.7 79.9 L 561.8 79.8 L 562.0 79.8 L 562.2 79.7 L 562.3 79.7 L 562.5 79.6 L 562.6 79.5 L 562.8 79.5 L 563.0 79.4 L 563.1 79.4 L 563.3 79.3 L 563.4 79.2 L 563.6 79.2 L 563.8 79.1 L 563.9 79.1 L 564.1 79.0 L 564.2 78.9 L 564.4 78.9 L 564.6 78.8 L 564.7 78.8 L 564.9 78.7 L 565.0 78.6 L 565.2 78.6 L 565.4 78.5 L 565.5 78.5 L 565.7 78.4 L 565.8 78.4 L 566.0 78.3 L 566.1 78.3 L 566.3 78.2 L 566.5 78.1 L 566.6 78.1 L 566.8 78.0 L 566.9 78.0 L 567.1 77.9 L 567.2 77.9 L 567.4 77.8 L 567.5 77.8 L 567.7 77.7 L 567.9 77.7 L 568.0 77.6 L 568.2 77.5 L 568.3 77.5 L 568.5 77.4 L 568.6 77.4 L 568.8 77.3 L 568.9 77.3 L 569.1 77.2 L 569.2 77.2 L 569.4 77.1 L 569.5 77.1 L 569.7 77.0 L 569.8 77.0 L 570.0 76.9 L 570.2 76.9 L 570.3 76.8 L 570.5 76.8 L 570.6 76.7 L 570.8 76.7 L 570.9 76.6 L 571.1 76.6 L 571.2 76.5 L 571.4 76.5 L 571.5 76.4 L 571.7 76.4 L 571.8 76.3 L 572.0 76.3 L 572.1 76.2 L 572.3 76.2 L 572.4 76.2 L 572.6 76.1 L 572.7 76.1 L 572.9 76.0 L 573.0 76.0 L 573.1 75.9 L 573.3 75.9 L 573.4 75.8 L 573.6 75.8 L 573.7 75.7 L 573.9 75.7 L 574.0 75.6 L 574.2 75.6 L 574.3 75.6 L 574.5 75.5 L 574.6 75.5 L 574.8 75.4 L 574.9 75.4 L 575.1 75.3 L 575.2 75.3 L 575.3 75.3 L 575.5 75.2 L 575.6 75.2 L 575.8 75.1 L 575.9 75.1 L 576.1 75.0 L 576.2 75.0 L 576.4 75.0 L 576.5 74.9 L 576.6 74.9 L 576.8 74.8 L 576.9 74.8 L 577.1 74.8 L 577.2 74.7 L 577.4 74.7 L 577.5 74.6 L 577.6 74.6 L 577.8 74.5 L 577.9 74.5 L 578.1 74.5 L 578.2 74.4 L 578.4 74.4 L 578.5 74.4 L 578.6 74.3 L 578.8 74.3 L 578.9 74.2 L 579.1 74.2 L 579.2 74.2 L 579.3 74.1 L 579.5 74.1 L 579.6 74.0 L 579.8 74.0 L 579.9 74.0 L 580.0 73.9 L 580.2 73.9 L 580.3 73.9 L 580.5 73.8 L 580.6 73.8 L 580.7 73.7 L 580.9 73.7 L 581.0 73.7 L 581.1 73.6 L 581.3 73.6 L 581.4 73.6 L 581.6 73.5 L 581.7 73.5 L 581.8 73.5 L 582.0 73.4 L 582.1 73.4 L 582.2 73.4 L 582.4 73.3 L 582.5 73.3 L 582.7 73.3 L 582.8 73.2 L 582.9 73.2 L 583.1 73.2 L 583.2 73.1 L 583.3 73.1 L 583.5 73.1 L 583.6 73.0 L 583.7 73.0 L 583.9 73.0 L 584.0 72.9 L 584.1 72.9 L 584.3 72.9 L 584.4 72.8 L 584.6 72.8 L 584.7 72.8 L 584.8 72.7 L 585.0 72.7 L 585.1 72.7 L 585.2 72.6 L 585.4 72.6 L 585.5 72.6 L 585.6 72.5 L 585.8 72.5 L 585.9 72.5 L 586.0 72.4 L 586.2 72.4 L 586.3 72.4 L 586.4 72.4 L 586.5 72.3 L 586.7 72.3 L 586.8 72.3 L 586.9 72.2 L 587.1 72.2 L 587.2 72.2 L 587.3 72.1 L 587.5 72.1 L 587.6 72.1 L 587.7 72.1 L 587.9 72.0 L 588.0 72.0 L 588.1 72.0 L 588.3 71.9 L 588.4 71.9 L 588.5 71.9 L 588.6 71.9 L 588.8 71.8 L 588.9 71.8 L 589.0 71.8 L 589.2 71.7 L 589.3 71.7 L 589.4 71.7 L 589.5 71.7 L 589.7 71.6 L 589.8 71.6 L 589.9 71.6 L 590.1 71.6 L 590.2 71.5 L 590.3 71.5 L 590.4 71.5 L 590.6 71.5 L 590.7 71.4 L 590.8 71.4 L 591.0 71.4 L 591.1 71.3 L 591.2 71.3 L 591.3 71.3 L 591.5 71.3 L 591.6 71.2 L 591.7 71.2 L 591.8 71.2 L 592.0 71.2 L 592.1 71.1 L 592.2 71.1 L 592.3 71.1 L 592.5 71.1 L 592.6 71.0 L 592.7 71.0 L 592.8 71.0 L 593.0 71.0 L 593.1 71.0 L 593.2 70.9 L 593.3 70.9 L 593.5 70.9 L 593.6 70.9 L 593.7 70.8 L 593.8 70.8 L 594.0 70.8 L 594.1 70.8 L 594.2 70.7 L 594.3 70.7 L 594.5 70.7 L 594.6 70.7 L 594.7 70.7 L 594.8 70.6 L 595.0 70.6 L 595.1 70.6 L 595.2 70.6 L 595.3 70.5 L 595.4 70.5 L 595.6 70.5 L 595.7 70.5 L 595.8 70.5 L 595.9 70.4 L 596.1 70.4 L 596.2 70.4 L 596.3 70.4 L 596.4 70.3 L 596.5 70.3 L 596.7 70.3 L 596.8 70.3 L 596.9 70.3 L 597.0 70.2 L 597.1 70.2 L 597.3 70.2 L 597.4 70.2 L 597.5 70.2 L 597.6 70.1 L 597.7 70.1 L 597.9 70.1 L 598.0 70.1 L 598.1 70.1 L 598.2 70.0 L 598.3 70.0 L 598.5 70.0 L 598.6 70.0 L 598.7 70.0 L 598.8 69.9 L 598.9 69.9 L 599.1 69.9 L 599.2 69.9 L 599.3 69.9 L 599.4 69.8 L 599.5 69.8 L 599.6 69.8 L 599.8 69.8 L 599.9 69.8 L 600.0 69.8" fill="none" stroke="#5c6bc0" stroke-width="2.4" stroke-opacity="1.0"/><circle cx="139.6" cy="241.5" r="4.6" fill="#c62828" fill-opacity="1.0"/><line x1="139.6" y1="241.5" x2="139.6" y2="258.0" stroke="#c62828" stroke-width="1" stroke-opacity="0.4" stroke-dasharray="3 3"/><text x="139.6" y="229.5" font-size="12" text-anchor="middle" font-weight="bold" fill="#c62828" fill-opacity="1.0">8.6%</text><circle cx="329.0" cy="211.0" r="4.6" fill="#c62828" fill-opacity="1.0"/><line x1="329.0" y1="211.0" x2="329.0" y2="258.0" stroke="#c62828" stroke-width="1" stroke-opacity="0.4" stroke-dasharray="3 3"/><text x="329.0" y="199.0" font-size="12" text-anchor="middle" font-weight="bold" fill="#c62828" fill-opacity="1.0">24.5%</text><circle cx="518.4" cy="102.2" r="4.6" fill="#c62828" fill-opacity="1.0"/><line x1="518.4" y1="102.2" x2="518.4" y2="258.0" stroke="#c62828" stroke-width="1" stroke-opacity="0.4" stroke-dasharray="3 3"/><text x="518.4" y="90.2" font-size="12" text-anchor="middle" font-weight="bold" fill="#c62828" fill-opacity="1.0">81.1%</text><text x="612.0" y="110.0" font-size="12" text-anchor="start" font-weight="bold" fill="#00897b" fill-opacity="1.0">効果量 d = 0.18</text><text x="612.0" y="128.0" font-size="11.5" text-anchor="start" fill="#00897b" fill-opacity="0.9">（小さい効果）</text><text x="612.0" y="152.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.85">は、どの人数でも</text><text x="612.0" y="170.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.85">まったく動かない</text><text x="0.0" y="322.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.9">「有意差あり」と書いてあったら、まず n を見る。n が大きければ、小さな差でも有意になる。</text><text x="0.0" y="344.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.9">逆に n が小さいと、本当にある差も見逃す（各群20頭では91%を見逃している）。</text><text x="0.0" y="366.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.7">（両側5%・等分散のt検定の理論値。20万回のシミュレーションでも 8.6%・24.5%・81.1% と一致した。）</text></svg>

---

## 5. 効果量（Cohen's d）―― 「大きさ」を測る

p値とは別に、差の大きさ自体を標準化したのが **効果量 d**（差が標準偏差いくつ分か）。目安：0.2小・0.5中・0.8大。

| 比較 | 効果量 d |
|---|---|
| 旧世界 vs 新世界（オマキザル科） | **4.40**（けた外れに大きい） |
| 旧世界 vs クモザル科 | **−0.00**（実質ゼロ） |
| 保護区の内外（0.2kgの差） | **0.18**（小さい効果） |

d = 4.40 は目安の「0.8で大」をはるかに超えている。群内のばらつき4個分以上も離れているということ。

一方、保護区の例は d = 0.18。**n さえ増やせば有意にできるが、生物学的にはごくわずかな差**である。**有意 ≠ 効果が大きい。** だから検定では、p値と一緒に**必ず効果量も見る**。

> **p値は「偶然かどうか」、効果量は「どれくらいか」。**論文でも報告書でも、**両方を書く**。

### 導出③：なぜ効果量は単位を変えても動かないのか

Cohen's d は、2群の平均の差を、群内のばらつき（合併標準偏差 \( s_p \)）で割ったものである。

!!! tip "下のボタンで、1行ずつ送れる"
    g を kg に直したときに何が起きるかを、式の上で追う。

<div class="deriv" markdown>

<div markdown>

$$ d \;=\; \frac{\bar{x}_1-\bar{x}_2}{s_p}, \qquad s_p=\sqrt{\frac{(n_1-1)s_1^2+(n_2-1)s_2^2}{n_1+n_2-2}} $$

**定義。**分子は「差」、分母は「群内のばらつき」。どちらも**同じ単位**（この例なら g）である。

</div>

<div markdown>

$$ x \;\longmapsto\; c\,x \qquad (c = 1/1000) $$

**単位を変える＝全データを \( c \) 倍する。**g を kg に直すとは、そういうことである。

</div>

<div markdown>

$$ \bar{x} \;\longmapsto\; c\,\bar{x}, \qquad s \;\longmapsto\; c\,s $$

**平均も標準偏差も、同じ \( c \) 倍になる。**
平均は \( \frac{1}{n}\sum cx_i = c\bar{x} \)。標準偏差は \( \mathrm{Var}[cX]=c^2\mathrm{Var}[X] \) の平方根なので \( c\,s \)（第3回）。

</div>

<div markdown>

$$ d' \;=\; \frac{c\bar{x}_1-c\bar{x}_2}{c\,s_p} \;=\; \frac{c(\bar{x}_1-\bar{x}_2)}{c\,s_p} $$

**新しい単位での d を書き下した。**分子を \( c \) でくくる。

</div>

<div markdown>

$$ d' \;=\; \frac{\cancel{c}\,(\bar{x}_1-\bar{x}_2)}{\cancel{c}\,s_p} \;=\; \frac{\bar{x}_1-\bar{x}_2}{s_p} \;=\; d $$

**分子と分母で \( c \) が約分された。**
\( d \) は「**標準偏差何個分の差か**」という比なので、ものさしの目盛りを取り替えても変わらない。
これが「**標準化された**効果量」と呼ばれる理由である。

</div>

</div>

### なぜ \( t \) は \( n \) で動き、\( d \) は動かないのか

ここが p値との決定的な違いになる。**2つの式を並べて割ってみれば、関係がそのまま出る。**

<div class="deriv" markdown>

<div markdown>

$$ t \;=\; \frac{\bar{x}_1-\bar{x}_2}{s_p\sqrt{\dfrac{1}{n_1}+\dfrac{1}{n_2}}}, \qquad d \;=\; \frac{\bar{x}_1-\bar{x}_2}{s_p} $$

**2つを並べた。分子はまったく同じ**（2群の平均の差）。
違うのは**分母だけ**で、\( t \) のほうには根号の因子が余計に付いている。

</div>

<div markdown>

$$ \bar{x}_1-\bar{x}_2 \;=\; d \cdot s_p $$

**\( d \) の式を、差について解いた。**両辺に \( s_p \) を掛けただけ。
これを \( t \) の分子に代入する。

</div>

<div markdown>

$$ t \;=\; \frac{d\,s_p}{s_p\sqrt{\dfrac{1}{n_1}+\dfrac{1}{n_2}}} \;=\; \frac{d}{\sqrt{\dfrac{1}{n_1}+\dfrac{1}{n_2}}} $$

**代入して \( s_p \) が約分された。**
ばらつきの大きさは \( t \) と \( d \) の両方に同じように入っているので、**消える**。
残るのは \( d \) と、**人数だけでできた因子**である。

</div>

<div markdown>

$$ \frac{1}{n_1}+\frac{1}{n_2} \;=\; \frac{n_2+n_1}{n_1 n_2} \qquad\Longrightarrow\qquad \frac{1}{\sqrt{\dfrac{1}{n_1}+\dfrac{1}{n_2}}} \;=\; \sqrt{\frac{n_1 n_2}{n_1+n_2}} $$

**分母を通分して、逆数の平方根に直した。**ただの分数の整理である。

</div>

<div markdown>

$$ t \;=\; d \times \sqrt{\frac{n_1 n_2}{n_1+n_2}} $$

🔴 **これが答え。**合併標準偏差を使う定義なら、これは**近似ではなく等式**である。

- **右辺の \( d \) に \( n \) は入っていない** …… 人数を増やしても動かない
- **右辺の根号は \( n \) だけでできている** …… 人数を増やすと大きくなる

</div>

<div markdown>

$$ n_1=n_2=n \;\Longrightarrow\; t \;=\; d\sqrt{\frac{n^2}{2n}} \;=\; d\sqrt{\frac{n}{2}} $$

**2群が同じ人数のときは、もっと簡単になる。**
\( t \) は \( \sqrt{n} \) に比例する。**n を4倍にすれば t は2倍**、p値はそのぶん小さくなる。
差の大きさ \( d \) は1ミリも変わっていないのに、である。

</div>

</div>

**d が同じでも、n を増やせば t は大きくなり、p は小さくなる。** 第4節で「真の差は常に0.2kgなのに n を増やすほど有意になった」のは、この式そのものである。d は n を含まないので動かない。だから両方を見る必要がある。
**数値で確かめる**：オナガザル科とオマキザル科の体重で、g のまま計算しても kg に直しても d = 2.2464 で同じ。対数スケールでも log10(g) と log10(kg) のどちらでも d = 4.4012 で一致する（対数では単位の変更が平行移動になるため、差も標準偏差も変わらない）。

**使った数学**：定数倍に対する平均と標準偏差の振る舞い（微I）、約分という比の性質。


---

## 6. 2種類の誤り

検定は完璧ではない。間違え方が2つある。

| | 本当は差がない | 本当は差がある |
|---|---|---|
| 「差あり」と判定 | **第一種の誤り（偽陽性）** | 正解 |
| 「差なし」と判定 | 正解 | **第二種の誤り（見逃し）** |

- **有意水準 α = 0.05**：本当は差がないのに「差あり」と誤る確率を5%まで許す基準。
- だから「有意」でも、**20回に1回は偶然の偽陽性**かもしれない。検定を何度も繰り返せば偽陽性は増える（→第9回）。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 356" role="img" aria-labelledby="ert erd" style="width:100%;height:auto;max-width:720px;display:block;margin:0.8em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="ert">2種類の誤り ―― 偽陽性と見逃し</title><desc id="erd">左の青い曲線が「本当は差がない」ときの t の分布、右の緑の曲線が「本当は0.2kgの差がある」ときの t の分布（各群100頭）。縦の赤い線が有意かどうかの境目 t = 1.97 である。青い曲線のうち境目より右（赤）が第一種の誤り＝偽陽性で2.5%、緑の曲線のうち境目より左（灰）が第二種の誤り＝見逃しで76%を占める。見逃しのほうがずっと大きい。</desc><polygon points="461.7,250.0 461.7,228.1 463.2,229.1 464.8,230.0 466.3,230.9 467.8,231.8 469.4,232.6 470.9,233.5 472.4,234.2 474.0,235.0 475.5,235.7 477.0,236.4 478.6,237.1 480.1,237.7 481.6,238.3 483.2,238.9 484.7,239.5 486.2,240.0 487.7,240.5 489.3,241.0 490.8,241.5 492.3,241.9 493.9,242.4 495.4,242.8 496.9,243.2 498.5,243.5 500.0,243.9 501.5,244.2 503.1,244.6 504.6,244.9 506.1,245.2 507.7,245.4 509.2,245.7 510.7,245.9 512.3,246.2 513.8,246.4 515.3,246.6 516.9,246.8 518.4,247.0 519.9,247.2 521.5,247.4 523.0,247.5 524.5,247.7 526.1,247.8 527.6,248.0 529.1,248.1 530.6,248.2 532.2,248.3 533.7,248.4 535.2,248.5 536.8,248.6 538.3,248.7 539.8,248.8 541.4,248.9 542.9,249.0 544.4,249.0 546.0,249.1 547.5,249.2 549.0,249.2 550.6,249.3 552.1,249.3 553.6,249.4 555.2,249.4 556.7,249.5 558.2,249.5 559.8,249.5 561.3,249.6 562.8,249.6 564.4,249.6 565.9,249.7 567.4,249.7 569.0,249.7 570.5,249.7 572.0,249.7 573.6,249.8 575.1,249.8 576.6,249.8 578.1,249.8 579.7,249.8 581.2,249.8 582.7,249.9 584.3,249.9 585.8,249.9 587.3,249.9 588.9,249.9 590.4,249.9 591.9,249.9 593.5,249.9 595.0,249.9 596.5,249.9 598.1,249.9 599.6,249.9 601.1,249.9 602.7,250.0 604.2,250.0 605.7,250.0 607.3,250.0 608.8,250.0 610.3,250.0 611.9,250.0 613.4,250.0 614.9,250.0 616.5,250.0 618.0,250.0 619.5,250.0 621.1,250.0 622.6,250.0 624.1,250.0 625.6,250.0 627.2,250.0 628.7,250.0 630.2,250.0 631.8,250.0 633.3,250.0 634.8,250.0 636.4,250.0 637.9,250.0 639.4,250.0 641.0,250.0 642.5,250.0 644.0,250.0 645.6,250.0 647.1,250.0 648.6,250.0 650.2,250.0 651.7,250.0 653.2,250.0 654.8,250.0 656.3,250.0 657.8,250.0 659.4,250.0 660.9,250.0 662.4,250.0 664.0,250.0 665.5,250.0 667.0,250.0 668.5,250.0 670.1,250.0 671.6,250.0 673.1,250.0 674.7,250.0 676.2,250.0 677.7,250.0 679.3,250.0 680.8,250.0 682.3,250.0 683.9,250.0 685.4,250.0 686.9,250.0 688.5,250.0 690.0,250.0 690.0,250.0" fill="#c62828" fill-opacity="0.45" stroke="none"/><polygon points="48.0,250.0 48.0,250.0 49.5,250.0 51.1,250.0 52.6,250.0 54.1,250.0 55.7,250.0 57.2,250.0 58.7,250.0 60.3,250.0 61.8,250.0 63.3,250.0 64.9,250.0 66.4,250.0 67.9,250.0 69.5,250.0 71.0,250.0 72.5,250.0 74.0,250.0 75.6,250.0 77.1,250.0 78.6,250.0 80.2,250.0 81.7,250.0 83.2,250.0 84.8,250.0 86.3,250.0 87.8,250.0 89.4,250.0 90.9,250.0 92.4,250.0 94.0,250.0 95.5,250.0 97.0,250.0 98.6,250.0 100.1,250.0 101.6,250.0 103.2,250.0 104.7,250.0 106.2,250.0 107.8,250.0 109.3,250.0 110.8,250.0 112.4,250.0 113.9,250.0 115.4,250.0 116.9,250.0 118.5,250.0 120.0,250.0 121.5,250.0 123.1,250.0 124.6,250.0 126.1,250.0 127.7,250.0 129.2,250.0 130.7,250.0 132.3,250.0 133.8,250.0 135.3,250.0 136.9,250.0 138.4,250.0 139.9,250.0 141.5,250.0 143.0,250.0 144.5,249.9 146.1,249.9 147.6,249.9 149.1,249.9 150.7,249.9 152.2,249.9 153.7,249.9 155.3,249.9 156.8,249.9 158.3,249.9 159.9,249.9 161.4,249.9 162.9,249.9 164.4,249.8 166.0,249.8 167.5,249.8 169.0,249.8 170.6,249.8 172.1,249.8 173.6,249.7 175.2,249.7 176.7,249.7 178.2,249.7 179.8,249.6 181.3,249.6 182.8,249.6 184.4,249.5 185.9,249.5 187.4,249.5 189.0,249.4 190.5,249.4 192.0,249.3 193.6,249.3 195.1,249.2 196.6,249.2 198.2,249.1 199.7,249.1 201.2,249.0 202.8,248.9 204.3,248.8 205.8,248.7 207.4,248.6 208.9,248.6 210.4,248.4 211.9,248.3 213.5,248.2 215.0,248.1 216.5,248.0 218.1,247.8 219.6,247.7 221.1,247.5 222.7,247.4 224.2,247.2 225.7,247.0 227.3,246.8 228.8,246.6 230.3,246.4 231.9,246.1 233.4,245.9 234.9,245.6 236.5,245.4 238.0,245.1 239.5,244.8 241.1,244.5 242.6,244.1 244.1,243.8 245.7,243.4 247.2,243.0 248.7,242.6 250.3,242.2 251.8,241.8 253.3,241.3 254.8,240.8 256.4,240.3 257.9,239.8 259.4,239.2 261.0,238.6 262.5,238.0 264.0,237.4 265.6,236.7 267.1,236.0 268.6,235.3 270.2,234.6 271.7,233.8 273.2,233.0 274.8,232.2 276.3,231.3 277.8,230.4 279.4,229.5 280.9,228.5 282.4,227.5 284.0,226.5 285.5,225.4 287.0,224.3 288.6,223.2 290.1,222.0 291.6,220.8 293.2,219.6 294.7,218.3 296.2,217.0 297.8,215.7 299.3,214.3 300.8,212.9 302.3,211.4 303.9,209.9 305.4,208.4 306.9,206.8 308.5,205.2 310.0,203.6 311.5,201.9 313.1,200.2 314.6,198.5 316.1,196.7 317.7,194.9 319.2,193.0 320.7,191.2 322.3,189.3 323.8,187.3 325.3,185.4 326.9,183.4 328.4,181.4 329.9,179.4 331.5,177.3 333.0,175.3 334.5,173.2 336.1,171.1 337.6,169.0 339.1,166.8 340.7,164.7 342.2,162.6 343.7,160.4 345.3,158.2 346.8,156.1 348.3,153.9 349.8,151.8 351.4,149.6 352.9,147.4 354.4,145.3 356.0,143.2 357.5,141.1 359.0,139.0 360.6,136.9 362.1,134.8 363.6,132.8 365.2,130.8 366.7,128.8 368.2,126.9 369.8,124.9 371.3,123.1 372.8,121.2 374.4,119.5 375.9,117.7 377.4,116.0 379.0,114.4 380.5,112.8 382.0,111.2 383.6,109.8 385.1,108.3 386.6,107.0 388.2,105.7 389.7,104.4 391.2,103.3 392.7,102.2 394.3,101.1 395.8,100.2 397.3,99.3 398.9,98.5 400.4,97.8 401.9,97.1 403.5,96.5 405.0,96.0 406.5,95.6 408.1,95.3 409.6,95.0 411.1,94.8 412.7,94.8 414.2,94.7 415.7,94.8 417.3,95.0 418.8,95.2 420.3,95.5 421.9,95.9 423.4,96.4 424.9,96.9 426.5,97.5 428.0,98.3 429.5,99.0 431.1,99.9 432.6,100.8 434.1,101.8 435.7,102.9 437.2,104.0 438.7,105.2 440.2,106.5 441.8,107.8 443.3,109.2 444.8,110.7 446.4,112.2 447.9,113.8 449.4,115.4 451.0,117.0 452.5,118.7 454.0,120.5 455.6,122.3 457.1,124.1 458.6,126.0 460.2,127.9 460.2,250.0" fill="currentColor" fill-opacity="0.22" stroke="none"/><path d="M 48.0 250.0 L 49.5 250.0 L 51.1 250.0 L 52.6 250.0 L 54.1 250.0 L 55.7 250.0 L 57.2 249.9 L 58.7 249.9 L 60.3 249.9 L 61.8 249.9 L 63.3 249.9 L 64.9 249.9 L 66.4 249.9 L 67.9 249.9 L 69.5 249.9 L 71.0 249.9 L 72.5 249.9 L 74.0 249.9 L 75.6 249.9 L 77.1 249.8 L 78.6 249.8 L 80.2 249.8 L 81.7 249.8 L 83.2 249.8 L 84.8 249.8 L 86.3 249.7 L 87.8 249.7 L 89.4 249.7 L 90.9 249.7 L 92.4 249.6 L 94.0 249.6 L 95.5 249.6 L 97.0 249.6 L 98.6 249.5 L 100.1 249.5 L 101.6 249.4 L 103.2 249.4 L 104.7 249.4 L 106.2 249.3 L 107.8 249.3 L 109.3 249.2 L 110.8 249.1 L 112.4 249.1 L 113.9 249.0 L 115.4 248.9 L 116.9 248.9 L 118.5 248.8 L 120.0 248.7 L 121.5 248.6 L 123.1 248.5 L 124.6 248.4 L 126.1 248.3 L 127.7 248.2 L 129.2 248.1 L 130.7 247.9 L 132.3 247.8 L 133.8 247.6 L 135.3 247.5 L 136.9 247.3 L 138.4 247.1 L 139.9 247.0 L 141.5 246.8 L 143.0 246.5 L 144.5 246.3 L 146.1 246.1 L 147.6 245.9 L 149.1 245.6 L 150.7 245.3 L 152.2 245.0 L 153.7 244.7 L 155.3 244.4 L 156.8 244.1 L 158.3 243.8 L 159.9 243.4 L 161.4 243.0 L 162.9 242.6 L 164.4 242.2 L 166.0 241.8 L 167.5 241.3 L 169.0 240.8 L 170.6 240.3 L 172.1 239.8 L 173.6 239.2 L 175.2 238.7 L 176.7 238.1 L 178.2 237.5 L 179.8 236.8 L 181.3 236.1 L 182.8 235.4 L 184.4 234.7 L 185.9 233.9 L 187.4 233.2 L 189.0 232.3 L 190.5 231.5 L 192.0 230.6 L 193.6 229.7 L 195.1 228.8 L 196.6 227.8 L 198.2 226.8 L 199.7 225.7 L 201.2 224.6 L 202.8 223.5 L 204.3 222.4 L 205.8 221.2 L 207.4 220.0 L 208.9 218.7 L 210.4 217.5 L 211.9 216.1 L 213.5 214.8 L 215.0 213.4 L 216.5 211.9 L 218.1 210.5 L 219.6 209.0 L 221.1 207.4 L 222.7 205.8 L 224.2 204.2 L 225.7 202.6 L 227.3 200.9 L 228.8 199.2 L 230.3 197.4 L 231.9 195.7 L 233.4 193.8 L 234.9 192.0 L 236.5 190.1 L 238.0 188.2 L 239.5 186.3 L 241.1 184.3 L 242.6 182.4 L 244.1 180.4 L 245.7 178.3 L 247.2 176.3 L 248.7 174.2 L 250.3 172.1 L 251.8 170.0 L 253.3 167.9 L 254.8 165.8 L 256.4 163.7 L 257.9 161.5 L 259.4 159.4 L 261.0 157.2 L 262.5 155.0 L 264.0 152.9 L 265.6 150.7 L 267.1 148.6 L 268.6 146.4 L 270.2 144.3 L 271.7 142.2 L 273.2 140.1 L 274.8 138.0 L 276.3 135.9 L 277.8 133.9 L 279.4 131.8 L 280.9 129.8 L 282.4 127.9 L 284.0 125.9 L 285.5 124.0 L 287.0 122.2 L 288.6 120.4 L 290.1 118.6 L 291.6 116.9 L 293.2 115.2 L 294.7 113.6 L 296.2 112.0 L 297.8 110.5 L 299.3 109.0 L 300.8 107.6 L 302.3 106.2 L 303.9 105.0 L 305.4 103.7 L 306.9 102.6 L 308.5 101.5 L 310.0 100.5 L 311.5 99.6 L 313.1 98.7 L 314.6 97.9 L 316.1 97.2 L 317.7 96.6 L 319.2 96.0 L 320.7 95.6 L 322.3 95.2 L 323.8 94.9 L 325.3 94.6 L 326.9 94.5 L 328.4 94.4 L 329.9 94.4 L 331.5 94.5 L 333.0 94.7 L 334.5 95.0 L 336.1 95.3 L 337.6 95.7 L 339.1 96.2 L 340.7 96.8 L 342.2 97.5 L 343.7 98.2 L 345.3 99.0 L 346.8 99.9 L 348.3 100.9 L 349.8 101.9 L 351.4 103.0 L 352.9 104.2 L 354.4 105.4 L 356.0 106.7 L 357.5 108.1 L 359.0 109.5 L 360.6 111.0 L 362.1 112.6 L 363.6 114.2 L 365.2 115.8 L 366.7 117.5 L 368.2 119.3 L 369.8 121.0 L 371.3 122.9 L 372.8 124.8 L 374.4 126.7 L 375.9 128.6 L 377.4 130.6 L 379.0 132.6 L 380.5 134.6 L 382.0 136.7 L 383.6 138.8 L 385.1 140.8 L 386.6 143.0 L 388.2 145.1 L 389.7 147.2 L 391.2 149.4 L 392.7 151.5 L 394.3 153.7 L 395.8 155.8 L 397.3 158.0 L 398.9 160.2 L 400.4 162.3 L 401.9 164.5 L 403.5 166.6 L 405.0 168.7 L 406.5 170.8 L 408.1 172.9 L 409.6 175.0 L 411.1 177.1 L 412.7 179.1 L 414.2 181.1 L 415.7 183.1 L 417.3 185.1 L 418.8 187.0 L 420.3 188.9 L 421.9 190.8 L 423.4 192.7 L 424.9 194.5 L 426.5 196.3 L 428.0 198.1 L 429.5 199.8 L 431.1 201.5 L 432.6 203.2 L 434.1 204.8 L 435.7 206.4 L 437.2 208.0 L 438.7 209.5 L 440.2 211.0 L 441.8 212.5 L 443.3 213.9 L 444.8 215.3 L 446.4 216.6 L 447.9 217.9 L 449.4 219.2 L 451.0 220.5 L 452.5 221.7 L 454.0 222.8 L 455.6 224.0 L 457.1 225.1 L 458.6 226.1 L 460.2 227.2 L 461.7 228.1 L 463.2 229.1 L 464.8 230.0 L 466.3 230.9 L 467.8 231.8 L 469.4 232.6 L 470.9 233.5 L 472.4 234.2 L 474.0 235.0 L 475.5 235.7 L 477.0 236.4 L 478.6 237.1 L 480.1 237.7 L 481.6 238.3 L 483.2 238.9 L 484.7 239.5 L 486.2 240.0 L 487.7 240.5 L 489.3 241.0 L 490.8 241.5 L 492.3 241.9 L 493.9 242.4 L 495.4 242.8 L 496.9 243.2 L 498.5 243.5 L 500.0 243.9 L 501.5 244.2 L 503.1 244.6 L 504.6 244.9 L 506.1 245.2 L 507.7 245.4 L 509.2 245.7 L 510.7 245.9 L 512.3 246.2 L 513.8 246.4 L 515.3 246.6 L 516.9 246.8 L 518.4 247.0 L 519.9 247.2 L 521.5 247.4 L 523.0 247.5 L 524.5 247.7 L 526.1 247.8 L 527.6 248.0 L 529.1 248.1 L 530.6 248.2 L 532.2 248.3 L 533.7 248.4 L 535.2 248.5 L 536.8 248.6 L 538.3 248.7 L 539.8 248.8 L 541.4 248.9 L 542.9 249.0 L 544.4 249.0 L 546.0 249.1 L 547.5 249.2 L 549.0 249.2 L 550.6 249.3 L 552.1 249.3 L 553.6 249.4 L 555.2 249.4 L 556.7 249.5 L 558.2 249.5 L 559.8 249.5 L 561.3 249.6 L 562.8 249.6 L 564.4 249.6 L 565.9 249.7 L 567.4 249.7 L 569.0 249.7 L 570.5 249.7 L 572.0 249.7 L 573.6 249.8 L 575.1 249.8 L 576.6 249.8 L 578.1 249.8 L 579.7 249.8 L 581.2 249.8 L 582.7 249.9 L 584.3 249.9 L 585.8 249.9 L 587.3 249.9 L 588.9 249.9 L 590.4 249.9 L 591.9 249.9 L 593.5 249.9 L 595.0 249.9 L 596.5 249.9 L 598.1 249.9 L 599.6 249.9 L 601.1 249.9 L 602.7 250.0 L 604.2 250.0 L 605.7 250.0 L 607.3 250.0 L 608.8 250.0 L 610.3 250.0 L 611.9 250.0 L 613.4 250.0 L 614.9 250.0 L 616.5 250.0 L 618.0 250.0 L 619.5 250.0 L 621.1 250.0 L 622.6 250.0 L 624.1 250.0 L 625.6 250.0 L 627.2 250.0 L 628.7 250.0 L 630.2 250.0 L 631.8 250.0 L 633.3 250.0 L 634.8 250.0 L 636.4 250.0 L 637.9 250.0 L 639.4 250.0 L 641.0 250.0 L 642.5 250.0 L 644.0 250.0 L 645.6 250.0 L 647.1 250.0 L 648.6 250.0 L 650.2 250.0 L 651.7 250.0 L 653.2 250.0 L 654.8 250.0 L 656.3 250.0 L 657.8 250.0 L 659.4 250.0 L 660.9 250.0 L 662.4 250.0 L 664.0 250.0 L 665.5 250.0 L 667.0 250.0 L 668.5 250.0 L 670.1 250.0 L 671.6 250.0 L 673.1 250.0 L 674.7 250.0 L 676.2 250.0 L 677.7 250.0 L 679.3 250.0 L 680.8 250.0 L 682.3 250.0 L 683.9 250.0 L 685.4 250.0 L 686.9 250.0 L 688.5 250.0 L 690.0 250.0" fill="none" stroke="#5c6bc0" stroke-width="2.2" stroke-opacity="1.0"/><path d="M 48.0 250.0 L 49.5 250.0 L 51.1 250.0 L 52.6 250.0 L 54.1 250.0 L 55.7 250.0 L 57.2 250.0 L 58.7 250.0 L 60.3 250.0 L 61.8 250.0 L 63.3 250.0 L 64.9 250.0 L 66.4 250.0 L 67.9 250.0 L 69.5 250.0 L 71.0 250.0 L 72.5 250.0 L 74.0 250.0 L 75.6 250.0 L 77.1 250.0 L 78.6 250.0 L 80.2 250.0 L 81.7 250.0 L 83.2 250.0 L 84.8 250.0 L 86.3 250.0 L 87.8 250.0 L 89.4 250.0 L 90.9 250.0 L 92.4 250.0 L 94.0 250.0 L 95.5 250.0 L 97.0 250.0 L 98.6 250.0 L 100.1 250.0 L 101.6 250.0 L 103.2 250.0 L 104.7 250.0 L 106.2 250.0 L 107.8 250.0 L 109.3 250.0 L 110.8 250.0 L 112.4 250.0 L 113.9 250.0 L 115.4 250.0 L 116.9 250.0 L 118.5 250.0 L 120.0 250.0 L 121.5 250.0 L 123.1 250.0 L 124.6 250.0 L 126.1 250.0 L 127.7 250.0 L 129.2 250.0 L 130.7 250.0 L 132.3 250.0 L 133.8 250.0 L 135.3 250.0 L 136.9 250.0 L 138.4 250.0 L 139.9 250.0 L 141.5 250.0 L 143.0 250.0 L 144.5 249.9 L 146.1 249.9 L 147.6 249.9 L 149.1 249.9 L 150.7 249.9 L 152.2 249.9 L 153.7 249.9 L 155.3 249.9 L 156.8 249.9 L 158.3 249.9 L 159.9 249.9 L 161.4 249.9 L 162.9 249.9 L 164.4 249.8 L 166.0 249.8 L 167.5 249.8 L 169.0 249.8 L 170.6 249.8 L 172.1 249.8 L 173.6 249.7 L 175.2 249.7 L 176.7 249.7 L 178.2 249.7 L 179.8 249.6 L 181.3 249.6 L 182.8 249.6 L 184.4 249.5 L 185.9 249.5 L 187.4 249.5 L 189.0 249.4 L 190.5 249.4 L 192.0 249.3 L 193.6 249.3 L 195.1 249.2 L 196.6 249.2 L 198.2 249.1 L 199.7 249.1 L 201.2 249.0 L 202.8 248.9 L 204.3 248.8 L 205.8 248.7 L 207.4 248.6 L 208.9 248.6 L 210.4 248.4 L 211.9 248.3 L 213.5 248.2 L 215.0 248.1 L 216.5 248.0 L 218.1 247.8 L 219.6 247.7 L 221.1 247.5 L 222.7 247.4 L 224.2 247.2 L 225.7 247.0 L 227.3 246.8 L 228.8 246.6 L 230.3 246.4 L 231.9 246.1 L 233.4 245.9 L 234.9 245.6 L 236.5 245.4 L 238.0 245.1 L 239.5 244.8 L 241.1 244.5 L 242.6 244.1 L 244.1 243.8 L 245.7 243.4 L 247.2 243.0 L 248.7 242.6 L 250.3 242.2 L 251.8 241.8 L 253.3 241.3 L 254.8 240.8 L 256.4 240.3 L 257.9 239.8 L 259.4 239.2 L 261.0 238.6 L 262.5 238.0 L 264.0 237.4 L 265.6 236.7 L 267.1 236.0 L 268.6 235.3 L 270.2 234.6 L 271.7 233.8 L 273.2 233.0 L 274.8 232.2 L 276.3 231.3 L 277.8 230.4 L 279.4 229.5 L 280.9 228.5 L 282.4 227.5 L 284.0 226.5 L 285.5 225.4 L 287.0 224.3 L 288.6 223.2 L 290.1 222.0 L 291.6 220.8 L 293.2 219.6 L 294.7 218.3 L 296.2 217.0 L 297.8 215.7 L 299.3 214.3 L 300.8 212.9 L 302.3 211.4 L 303.9 209.9 L 305.4 208.4 L 306.9 206.8 L 308.5 205.2 L 310.0 203.6 L 311.5 201.9 L 313.1 200.2 L 314.6 198.5 L 316.1 196.7 L 317.7 194.9 L 319.2 193.0 L 320.7 191.2 L 322.3 189.3 L 323.8 187.3 L 325.3 185.4 L 326.9 183.4 L 328.4 181.4 L 329.9 179.4 L 331.5 177.3 L 333.0 175.3 L 334.5 173.2 L 336.1 171.1 L 337.6 169.0 L 339.1 166.8 L 340.7 164.7 L 342.2 162.6 L 343.7 160.4 L 345.3 158.2 L 346.8 156.1 L 348.3 153.9 L 349.8 151.8 L 351.4 149.6 L 352.9 147.4 L 354.4 145.3 L 356.0 143.2 L 357.5 141.1 L 359.0 139.0 L 360.6 136.9 L 362.1 134.8 L 363.6 132.8 L 365.2 130.8 L 366.7 128.8 L 368.2 126.9 L 369.8 124.9 L 371.3 123.1 L 372.8 121.2 L 374.4 119.5 L 375.9 117.7 L 377.4 116.0 L 379.0 114.4 L 380.5 112.8 L 382.0 111.2 L 383.6 109.8 L 385.1 108.3 L 386.6 107.0 L 388.2 105.7 L 389.7 104.4 L 391.2 103.3 L 392.7 102.2 L 394.3 101.1 L 395.8 100.2 L 397.3 99.3 L 398.9 98.5 L 400.4 97.8 L 401.9 97.1 L 403.5 96.5 L 405.0 96.0 L 406.5 95.6 L 408.1 95.3 L 409.6 95.0 L 411.1 94.8 L 412.7 94.8 L 414.2 94.7 L 415.7 94.8 L 417.3 95.0 L 418.8 95.2 L 420.3 95.5 L 421.9 95.9 L 423.4 96.4 L 424.9 96.9 L 426.5 97.5 L 428.0 98.3 L 429.5 99.0 L 431.1 99.9 L 432.6 100.8 L 434.1 101.8 L 435.7 102.9 L 437.2 104.0 L 438.7 105.2 L 440.2 106.5 L 441.8 107.8 L 443.3 109.2 L 444.8 110.7 L 446.4 112.2 L 447.9 113.8 L 449.4 115.4 L 451.0 117.0 L 452.5 118.7 L 454.0 120.5 L 455.6 122.3 L 457.1 124.1 L 458.6 126.0 L 460.2 127.9 L 461.7 129.9 L 463.2 131.9 L 464.8 133.9 L 466.3 135.9 L 467.8 137.9 L 469.4 140.0 L 470.9 142.1 L 472.4 144.2 L 474.0 146.3 L 475.5 148.4 L 477.0 150.5 L 478.6 152.7 L 480.1 154.8 L 481.6 157.0 L 483.2 159.1 L 484.7 161.2 L 486.2 163.3 L 487.7 165.5 L 489.3 167.6 L 490.8 169.7 L 492.3 171.7 L 493.9 173.8 L 495.4 175.9 L 496.9 177.9 L 498.5 179.9 L 500.0 181.9 L 501.5 183.8 L 503.1 185.8 L 504.6 187.7 L 506.1 189.6 L 507.7 191.4 L 509.2 193.3 L 510.7 195.1 L 512.3 196.8 L 513.8 198.6 L 515.3 200.3 L 516.9 202.0 L 518.4 203.6 L 519.9 205.2 L 521.5 206.8 L 523.0 208.3 L 524.5 209.8 L 526.1 211.3 L 527.6 212.7 L 529.1 214.1 L 530.6 215.5 L 532.2 216.8 L 533.7 218.1 L 535.2 219.3 L 536.8 220.6 L 538.3 221.7 L 539.8 222.9 L 541.4 224.0 L 542.9 225.1 L 544.4 226.1 L 546.0 227.1 L 547.5 228.1 L 549.0 229.1 L 550.6 230.0 L 552.1 230.9 L 553.6 231.7 L 555.2 232.6 L 556.7 233.4 L 558.2 234.1 L 559.8 234.9 L 561.3 235.6 L 562.8 236.3 L 564.4 236.9 L 565.9 237.6 L 567.4 238.2 L 569.0 238.7 L 570.5 239.3 L 572.0 239.8 L 573.6 240.4 L 575.1 240.8 L 576.6 241.3 L 578.1 241.8 L 579.7 242.2 L 581.2 242.6 L 582.7 243.0 L 584.3 243.4 L 585.8 243.7 L 587.3 244.1 L 588.9 244.4 L 590.4 244.7 L 591.9 245.0 L 593.5 245.3 L 595.0 245.6 L 596.5 245.8 L 598.1 246.1 L 599.6 246.3 L 601.1 246.5 L 602.7 246.7 L 604.2 246.9 L 605.7 247.1 L 607.3 247.3 L 608.8 247.4 L 610.3 247.6 L 611.9 247.7 L 613.4 247.9 L 614.9 248.0 L 616.5 248.1 L 618.0 248.2 L 619.5 248.4 L 621.1 248.5 L 622.6 248.6 L 624.1 248.7 L 625.6 248.7 L 627.2 248.8 L 628.7 248.9 L 630.2 249.0 L 631.8 249.0 L 633.3 249.1 L 634.8 249.2 L 636.4 249.2 L 637.9 249.3 L 639.4 249.3 L 641.0 249.4 L 642.5 249.4 L 644.0 249.5 L 645.6 249.5 L 647.1 249.5 L 648.6 249.6 L 650.2 249.6 L 651.7 249.6 L 653.2 249.6 L 654.8 249.7 L 656.3 249.7 L 657.8 249.7 L 659.4 249.7 L 660.9 249.8 L 662.4 249.8 L 664.0 249.8 L 665.5 249.8 L 667.0 249.8 L 668.5 249.8 L 670.1 249.8 L 671.6 249.9 L 673.1 249.9 L 674.7 249.9 L 676.2 249.9 L 677.7 249.9 L 679.3 249.9 L 680.8 249.9 L 682.3 249.9 L 683.9 249.9 L 685.4 249.9 L 686.9 249.9 L 688.5 249.9 L 690.0 249.9" fill="none" stroke="#00897b" stroke-width="2.2" stroke-opacity="1.0"/><line x1="48.0" y1="250.0" x2="690.0" y2="250.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><text x="61.4" y="269.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">-4</text><text x="195.1" y="269.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">-2</text><text x="328.9" y="269.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">0</text><text x="462.6" y="269.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">2</text><text x="596.4" y="269.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">4</text><text x="686.0" y="269.0" font-size="11.5" text-anchor="end" fill="currentColor" fill-opacity="0.8">t の値</text><line x1="460.8" y1="70.0" x2="460.8" y2="250.0" stroke="#c62828" stroke-width="1.6" stroke-opacity="0.85" stroke-dasharray="4 3"/><text x="460.8" y="64.0" font-size="11.5" text-anchor="middle" font-weight="bold" fill="#c62828" fill-opacity="1.0">有意かどうかの境目  t = 1.97</text><text x="0.0" y="32.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">間違え方は2つある ―― 偽陽性と、見逃し</text><text x="235.2" y="112.0" font-size="12" text-anchor="middle" font-weight="bold" fill="#5c6bc0" fill-opacity="1.0">本当は差がない</text><text x="569.6" y="100.0" font-size="12" text-anchor="middle" font-weight="bold" fill="#00897b" fill-opacity="1.0">本当は0.2kgの差がある</text><text x="569.6" y="116.0" font-size="11" text-anchor="middle" fill="#00897b" fill-opacity="0.9">（各群100頭のとき）</text><circle cx="10.0" cy="288.0" r="5" fill="#c62828" fill-opacity="0.45"/><text x="24.0" y="292.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="1.0">第一種の誤り（偽陽性）＝ 差がないのに「あり」と言う。片側 2.5%、両側あわせて 5%。</text><circle cx="10.0" cy="312.0" r="5" fill="currentColor" fill-opacity="0.22"/><text x="24.0" y="316.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="1.0">第二種の誤り（見逃し）＝ 差があるのに「なし」と言う。ここでは 76%。有意になるのは残りの 24% だけ。</text><text x="0.0" y="348.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.7">αは5%と決め打ちできるが、見逃しの大きさは効果量と人数で決まる。小さい差を小さい標本で追うと、ほとんど見逃す。</text></svg>

---

## まとめ

| 概念 | ひとこと |
|---|---|
| 帰無仮説 | まず「差はない（偶然）」と仮定する |
| p値 | 帰無仮説のもとで観測以上の差が出る確率 |
| 有意差 | p<0.05 ＝「偶然では説明しにくい」 |
| ❌ よくある誤り | p値=帰無仮説が正しい確率／有意=効果大／n増やせば必ず有意 |
| 効果量 d | 差の大きさ。有意とは別に必ず見る |
| α・2種の誤り | 偽陽性5%を許す基準。検定の繰り返しに注意 |

> **「差がある」＝「偶然では説明しにくい」。それ以上でも以下でもない。**
> p値の小ささは効果の大きさを意味しない。**必ず効果量も見る。**

---

## 今日の課題（Moodle提出）

**配点：100点（選択40点 ＋ 記述60点）／ 提出先：Moodle ／ 提出期限：次回授業の開始時刻まで**

Colab `08_ttest.ipynb` を実行したうえで答えること。

---

### パートA：選択問題（各10点 ×4＝40点）

**A1.** 帰無仮説とは何か。**最も適切**なのは？

- (ア) 「差がある」とまず仮定すること
- (イ) 「差はない（偶然だ）」とまず仮定すること
- (ウ) 効果量のこと

**A2.** p値の意味として**最も正しい**のは？

- (ア) 帰無仮説が正しい確率
- (イ) 帰無仮説が正しいと仮定したとき、観測以上の差が出る確率
- (ウ) 効果がどれくらい大きいかを表す値

**A3.** 真の差が「0.2kg」で固定のまま、各群の頭数 n を 20→100→500 と増やすと、有意（p<0.05）になる割合はどう変わったか。

- (ア) 8%→23%→80% と増えた
- (イ) ずっと5%で変わらない
- (ウ) 80%→23%→8% と減った

**A4.** 「旧世界ザル vs 新世界ザルの体重差は効果量 d=4.40、保護区の内外の差は d=0.18」。ここから言えることは？

- (ア) p値さえ小さければ効果量は見なくてよい
- (イ) 有意であることと効果が大きいことは別で、効果量も見る必要がある
- (ウ) d が小さいほど効果が大きい

---

### パートB：記述問題（AIフィードバック対象・60点）

!!! warning "【全記述に共通・重要】自分の出力を引用すること"
    記述には、**今日のColabであなたのノートが出した数値**を最低1つ引用すること。**ここには値を書かない。自分の画面に出た値を使うこと。**
    引ける量の例：「n=500のときに有意になった割合」「旧世界 vs 新世界の効果量 d」「t検定のp値」。
    **引用がない記述は満点になりません。**

**B1.（30点）** あるニュースが次のように報じた。

> 「サプリXを飲んだ群は飲まない群より体重が**0.2kg**多く減り、**統計的に有意（p<0.01）**だった。だからサプリXには**大きなダイエット効果**がある。」

この主張の**どこが問題か**を、今日学んだ「p値」「効果量」「サンプルサイズ」の観点から指摘しなさい。（ヒント：p<0.01 は何を意味し、何を意味しないか。0.2kgは大きいか）

**B2.（30点）** 「t検定で p<0.05 が出た。これで帰無仮説が間違いだと**証明**できた」。この言い方の、**言い過ぎ**な点を説明しなさい。p値と「証明」、第一種の誤り（偽陽性）の言葉を使うこと。

> 目安：B1・B2あわせて350〜550字。**自分の言葉**で書くこと。
>
> **字数は目安です。多少の過不足で減点はしません。**見るのは、設問が挙げた要素（上の箇条書き）が書けているかどうかです。ただし要素が抜けていれば、その分は引きます。

!!! abstract "次回予告"
    第9回「仮説検定(2)：分散分析（ANOVA）」。3つ以上の群を比べるとき、t検定を繰り返すと何が起きるか。偽陽性が爆発する罠と、その回避法へ。