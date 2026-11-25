# 第10回　回帰分析：単回帰と重回帰

**12/15（火）Ⅱ講 10:35〜12:15・B402教室**

> データを「数式（モデル）」で説明する ―― ただし、当てはまりの良さは良いモデルの証明ではない

---


<!-- LINKS:START -->
!!! info "今日のリンク"
    - [📊 スライドを開く](slides/10.html)
    - [📓 Colabノートを開く（10_regression.ipynb）](https://colab.research.google.com/github/aonoa68/toukei-1/blob/main/colab/10_regression.ipynb)
    - [📝 課題を提出する（Moodle・第10回）](https://moodle.hokusei.ac.jp/mod/assign/view.php?id=990631)
    - 課題の本文は**このページの末尾**にあります
<!-- LINKS:END -->

!!! tip "考え方をガイドで確かめる"
    この回の考え方は、統計の考え方ガイドの[「回帰とモデル」](https://aonoa68.github.io/teaching/guide/regression/)でも解説しています。霊長類のデータを動かしながら確かめられます。

## この回のゴール

- 単回帰の式（切片・傾き）と決定係数 R² を読める
- 重回帰で「他を一定にしたときの関連（統制）」を理解する
- **R²の罠・係数の罠・外挿の罠**を知り、回帰結果を批判的に解釈できる
- **発展**：最小二乗法から傾き \( b=S_{xy}/S_{xx} \) と切片 \( a=\bar{y}-b\bar{x} \) を導き、単回帰では \( R^2=r^2 \) になることを、自分で示せる

到達目標との対応：**G3（Pythonで解析）・G2（批判的検証）**。

---

## 0. フック

> 「**草食か雑食か**が分かれば、その種の**行動圏の広さ**を予測できるだろうか？」

散布図に直線を引いて予測してみると――**R² = 0.0001**。栄養段階では行動圏をまったく説明できなかった。

では**体重**なら？

!!! note "今日も対数で扱う"
    体重も行動圏も種によって数千倍違う。第3回・第5回と同じ理由で、両方とも対数の目盛りで扱う。

---

## 1. 単回帰

体重で行動圏を予測すると（n=153種）：

$$ \log(\text{行動圏}) \approx -3.883 + 0.933 \times \log(\text{体重}) \qquad (R^2 = 0.462) $$

- **回帰直線**：データに最もよく当てはまる直線（最小二乗法＝縦のズレの二乗和を最小に）
- **切片 = −3.883**：log体重が0（＝1g）のときの予測値
- **決定係数 R² = 0.462**：行動圏のばらつきの約46%をモデルが説明

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 392" role="img" aria-labelledby="fitt fitd" style="width:100%;height:auto;max-width:720px;display:block;margin:0.8em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="fitt">体重で行動圏を予測する ―― 直線と、そこからの縦のズレ</title><desc id="fitd">横軸は体重の常用対数、縦軸は行動圏の常用対数で、点は153種。赤い直線が回帰直線で、傾き0.933・切片-3.883、決定係数は0.462である。細い縦線が残差（実測と予測の差）で、最小二乗法はこの縦線の二乗和をいちばん小さくする直線を選んでいる。最も大きく外れているのはパタスモンキーで、予測の49倍の行動圏を使っている。</desc><text x="0.0" y="30.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">最小二乗法は「縦のズレの二乗和」を最小にする直線を選ぶ</text><line x1="125.2" y1="64.0" x2="125.2" y2="268.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="125.2" y="287.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">2</text><line x1="261.0" y1="64.0" x2="261.0" y2="268.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="261.0" y="287.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">3</text><line x1="396.8" y1="64.0" x2="396.8" y2="268.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="396.8" y="287.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">4</text><line x1="532.6" y1="64.0" x2="532.6" y2="268.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="532.6" y="287.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">5</text><line x1="62.0" y1="229.0" x2="560.0" y2="229.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="54.0" y="233.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">-2</text><line x1="62.0" y1="185.6" x2="560.0" y2="185.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="54.0" y="189.6" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">-1</text><line x1="62.0" y1="142.2" x2="560.0" y2="142.2" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="54.0" y="146.2" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">0</text><line x1="62.0" y1="98.8" x2="560.0" y2="98.8" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="54.0" y="102.8" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">1</text><line x1="62.0" y1="268.0" x2="560.0" y2="268.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.4"/><line x1="62.0" y1="64.0" x2="62.0" y2="268.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.4"/><text x="311.0" y="308.0" font-size="11.5" text-anchor="middle" fill="currentColor" fill-opacity="0.8">体重 log10(g)</text><text x="54.0" y="52.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.8">行動圏 log10(km²)</text><line x1="358.1" y1="208.3" x2="358.1" y2="160.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="370.5" y1="185.6" x2="370.5" y2="156.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="376.2" y1="139.4" x2="376.2" y2="154.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="266.2" y1="229.0" x2="266.2" y2="187.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="373.2" y1="176.7" x2="373.2" y2="155.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="280.5" y1="208.3" x2="280.5" y2="183.4" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="204.9" y1="189.8" x2="204.9" y2="205.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="188.0" y1="215.9" x2="188.0" y2="210.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="137.8" y1="258.2" x2="137.8" y2="225.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="325.9" y1="162.0" x2="325.9" y2="169.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="335.6" y1="176.7" x2="335.6" y2="166.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="347.8" y1="138.0" x2="347.8" y2="163.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="358.9" y1="139.5" x2="358.9" y2="160.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="165.1" y1="215.9" x2="165.1" y2="217.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="396.4" y1="175.6" x2="396.4" y2="148.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="381.4" y1="165.5" x2="381.4" y2="153.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="292.3" y1="198.6" x2="292.3" y2="179.8" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="294.7" y1="198.6" x2="294.7" y2="179.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="100.7" y1="229.0" x2="100.7" y2="237.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="148.1" y1="229.0" x2="148.1" y2="222.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="255.8" y1="229.0" x2="255.8" y2="190.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="362.4" y1="163.6" x2="362.4" y2="158.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="362.0" y1="169.9" x2="362.0" y2="159.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="318.0" y1="198.6" x2="318.0" y2="172.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="230.1" y1="167.6" x2="230.1" y2="198.4" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="237.3" y1="253.4" x2="237.3" y2="196.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="371.5" y1="162.5" x2="371.5" y2="156.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="397.5" y1="135.4" x2="397.5" y2="148.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="355.9" y1="144.6" x2="355.9" y2="160.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="404.9" y1="123.9" x2="404.9" y2="146.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="82.4" y1="229.0" x2="82.4" y2="242.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="408.9" y1="135.8" x2="408.9" y2="145.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="248.7" y1="182.1" x2="248.7" y2="192.9" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="430.6" y1="112.5" x2="430.6" y2="138.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="430.6" y1="100.5" x2="430.6" y2="138.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="386.7" y1="158.5" x2="386.7" y2="151.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="383.9" y1="198.6" x2="383.9" y2="152.5" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="371.9" y1="180.6" x2="371.9" y2="156.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="370.9" y1="182.1" x2="370.9" y2="156.4" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="373.1" y1="187.6" x2="373.1" y2="155.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="372.0" y1="171.6" x2="372.0" y2="156.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="402.4" y1="85.3" x2="402.4" y2="147.0" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="206.1" y1="172.5" x2="206.1" y2="205.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="221.1" y1="173.5" x2="221.1" y2="201.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="213.9" y1="168.3" x2="213.9" y2="203.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="244.0" y1="149.4" x2="244.0" y2="194.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="401.6" y1="170.7" x2="401.6" y2="147.3" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="133.9" y1="235.3" x2="133.9" y2="227.1" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="395.1" y1="208.3" x2="395.1" y2="149.2" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="400.2" y1="189.8" x2="400.2" y2="147.7" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><line x1="403.6" y1="170.7" x2="403.6" y2="146.6" stroke="#c62828" stroke-width="0.8" stroke-opacity="0.3"/><circle cx="358.1" cy="208.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="372.1" cy="173.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="377.2" cy="164.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="370.5" cy="185.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="255.6" cy="215.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="373.1" cy="126.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="376.2" cy="139.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="380.5" cy="148.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="388.6" cy="136.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="266.2" cy="229.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="249.9" cy="229.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="399.9" cy="141.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="373.2" cy="176.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="251.5" cy="202.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="258.5" cy="215.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="280.5" cy="208.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="272.2" cy="183.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="226.6" cy="163.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="204.9" cy="189.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="202.8" cy="170.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="203.1" cy="185.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="188.0" cy="215.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="203.1" cy="195.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="197.4" cy="229.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="137.8" cy="258.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="315.3" cy="154.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="320.9" cy="144.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="325.9" cy="162.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="321.5" cy="132.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="376.4" cy="154.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="335.6" cy="176.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="337.0" cy="229.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="334.0" cy="169.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="347.8" cy="138.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="356.4" cy="185.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="359.6" cy="195.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="358.9" cy="139.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="336.2" cy="139.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="213.4" cy="215.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="165.1" cy="215.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="321.6" cy="129.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="325.2" cy="134.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="396.4" cy="175.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="389.3" cy="179.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="391.0" cy="157.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="381.4" cy="165.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="320.3" cy="195.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="383.4" cy="79.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="292.3" cy="198.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="312.1" cy="198.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="314.3" cy="208.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="294.7" cy="198.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="302.3" cy="180.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="182.9" cy="174.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="100.7" cy="229.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="163.7" cy="202.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="170.4" cy="189.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="148.1" cy="229.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="539.6" cy="115.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="287.3" cy="171.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="255.8" cy="229.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="365.0" cy="173.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="364.9" cy="179.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="362.4" cy="163.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="365.3" cy="182.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="365.8" cy="167.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="362.0" cy="169.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="387.7" cy="182.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="369.2" cy="122.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="318.0" cy="198.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="228.1" cy="169.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="236.1" cy="145.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="230.1" cy="167.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="249.4" cy="232.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="230.9" cy="259.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="237.3" cy="253.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="244.5" cy="235.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="379.2" cy="129.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="371.5" cy="162.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="179.0" cy="235.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="350.6" cy="156.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="397.5" cy="135.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="371.0" cy="108.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="382.3" cy="131.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="355.9" cy="144.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="366.6" cy="144.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="351.7" cy="159.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="404.9" cy="123.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="427.0" cy="80.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="103.3" cy="229.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="82.4" cy="229.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="274.1" cy="146.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="195.0" cy="208.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="408.9" cy="135.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="370.6" cy="141.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="272.1" cy="195.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="248.7" cy="182.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="470.9" cy="79.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="485.5" cy="97.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="430.6" cy="112.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="423.9" cy="91.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="416.7" cy="88.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="430.6" cy="100.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="265.6" cy="183.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="208.4" cy="215.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="386.7" cy="158.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="377.1" cy="158.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="389.7" cy="159.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="383.9" cy="198.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="291.2" cy="202.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="495.6" cy="116.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="371.9" cy="180.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="376.0" cy="192.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="369.4" cy="172.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="370.9" cy="182.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="370.9" cy="182.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="370.0" cy="155.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="373.1" cy="187.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="342.4" cy="175.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="302.8" cy="151.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="372.0" cy="171.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="335.4" cy="195.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="336.4" cy="208.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="402.4" cy="85.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="408.9" cy="104.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="414.3" cy="82.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="206.1" cy="172.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="219.2" cy="176.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="208.1" cy="170.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="221.1" cy="173.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="224.7" cy="198.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="226.4" cy="171.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="213.9" cy="168.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="215.5" cy="195.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="241.1" cy="185.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="244.0" cy="149.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="410.8" cy="137.2" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="379.0" cy="185.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="401.6" cy="170.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="133.1" cy="229.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="131.0" cy="246.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="133.9" cy="235.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="155.8" cy="215.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="424.4" cy="139.4" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="395.1" cy="208.3" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="377.3" cy="182.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="386.2" cy="127.1" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="400.2" cy="189.8" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="377.8" cy="174.5" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="381.3" cy="175.6" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="403.6" cy="170.7" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="377.5" cy="215.9" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><circle cx="340.5" cy="136.0" r="2.6" fill="#5c6bc0" fill-opacity="0.5"/><path d="M 62.0 248.5 L 560.0 100.0" fill="none" stroke="#c62828" stroke-width="2.4" stroke-opacity="1.0"/><circle cx="383.4" cy="79.2" r="5.4" fill="#ef6c00" fill-opacity="1.0"/><line x1="383.4" y1="79.2" x2="383.4" y2="152.7" stroke="#ef6c00" stroke-width="2" stroke-opacity="0.9"/><text x="393.4" y="73.2" font-size="11.5" text-anchor="start" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">パタスモンキー</text><text x="393.4" y="89.2" font-size="11.5" text-anchor="start" fill="#ef6c00" fill-opacity="1.0">予測の 49倍</text><text x="576.0" y="110.0" font-size="12.5" text-anchor="start" font-weight="bold" fill="#c62828" fill-opacity="1.0">傾き 0.933</text><text x="576.0" y="130.0" font-size="12.5" text-anchor="start" fill="#c62828" fill-opacity="1.0">切片 −3.883</text><text x="576.0" y="154.0" font-size="12.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">R² = 0.462</text><text x="576.0" y="174.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.8">n = 153種</text><text x="576.0" y="204.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.8">細い縦線が</text><text x="576.0" y="220.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.8">残差（3つに</text><text x="576.0" y="236.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.8">1つを表示）</text><text x="0.0" y="330.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.95">両方とも対数なので、傾き 0.933 は「体重が10倍になると行動圏は約 8.6倍」という意味になる。</text><text x="0.0" y="354.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.95">残差の大きい点は「外れ」ではなく、モデルが捉えていない何かの合図である。パタスモンキーはサバンナで地上生活する。</text><text x="0.0" y="386.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.7">（体重・行動圏がそろう153種。どちらも常用対数で扱っている。）</text></svg>

### 導出①：傾きと切片は、どこから出てくるのか（最小二乗法）

直線 \( y = a + bx \) を引くとき、「当てはまりが良い」を**縦のズレの二乗和が最小**と決める。この決め方が最小二乗法である。

!!! tip "下のボタンで、1行ずつ送れる"
    「次の式へ ▶」を押すと、1段ずつ現れる。**各行には、何をしたのかが付いている。**
    最後の2段は、**微分を使わない道**（平方完成）である。

<div class="deriv" markdown>

<div markdown>

$$ Q(a,b) \;=\; \sum_{i=1}^{n}\bigl(y_i - a - b x_i\bigr)^2 $$

**出発点。**各点の**縦のズレ**（実際の \( y_i \) と直線の値 \( a+bx_i \) の差）を二乗して、全部足したもの。
これを最小にする \( a,b \) を探す。\( Q \) は \( a,b \) についての**二次式**である。

</div>

<div markdown>

$$ \frac{\partial Q}{\partial a} \;=\; -2\sum_{i=1}^{n}\bigl(y_i-a-bx_i\bigr) \;=\; 0 $$

**まず \( a \) について。**二次式が最小になるのは、傾きが 0 になるところ。
（合成関数の微分で、中身の \( -a \) から \( -1 \) が出て、全体に \( 2 \) が掛かる。）

</div>

<div markdown>

$$ \sum y_i - na - b\sum x_i \;=\; 0 \qquad\Longrightarrow\qquad n\bar{y} - na - b\,n\bar{x} \;=\; 0 $$

**和をばらした。**\( a \) は \( n \) 個足されるので \( na \)。
\( \sum y_i = n\bar{y} \)、\( \sum x_i = n\bar{x} \)（平均の定義）を入れる。

</div>

<div markdown>

$$ a \;=\; \bar{y} - b\bar{x} $$

**両辺を \( n \) で割って \( a \) について解いた。**
これを直線の式に戻すと \( y=\bar{y}+b(x-\bar{x}) \) となり、\( x=\bar{x} \) のとき \( y=\bar{y} \)。
🔴 **回帰直線は必ず点 \( (\bar{x},\bar{y}) \) を通る。**

</div>

<div markdown>

$$ \frac{\partial Q}{\partial b} \;=\; -2\sum_{i=1}^{n} x_i\bigl(y_i-a-bx_i\bigr) \;=\; 0 \qquad\Longrightarrow\qquad \sum x_iy_i - a\sum x_i - b\sum x_i^2 \;=\; 0 $$

**次に \( b \) について。**同じことをする。中身の \( -bx_i \) から \( -x_i \) が出るので、\( x_i \) が掛かる。
そのあと、かっこを展開して和をばらした。

</div>

<div markdown>

$$ \sum x_iy_i - (\bar{y}-b\bar{x})\,n\bar{x} - b\sum x_i^2 \;=\; 0 $$

**いま求めた \( a=\bar{y}-b\bar{x} \) を代入した。**
\( \sum x_i = n\bar{x} \) も同時に使っている。**これで未知数は \( b \) だけになった。**

</div>

<div markdown>

$$ \sum x_iy_i - n\bar{x}\bar{y} \;=\; b\left(\sum x_i^2 - n\bar{x}^2\right) $$

**かっこを展開して、\( b \) の項を右辺に集めた。**
左辺から \( +b\,n\bar{x}^2 \) が出るので、それを右辺の \( -b\sum x_i^2 \) と合わせている。

</div>

<div markdown>

$$ \sum (x_i-\bar{x})(y_i-\bar{y}) \;=\; \sum x_iy_i - \bar{y}\sum x_i - \bar{x}\sum y_i + n\bar{x}\bar{y} \;=\; \sum x_iy_i - n\bar{x}\bar{y} \;=\; S_{xy} $$

**左辺が何者かを確かめる。**かっこを展開すると、真ん中の2項がどちらも \( -n\bar{x}\bar{y} \) になり、
最後の \( +n\bar{x}\bar{y} \) と合わせて \( -n\bar{x}\bar{y} \) がひとつ残る。
**つまり左辺は、\( x \) と \( y \) の偏差の積の和 \( S_{xy} \) そのものである。**

</div>

<div markdown>

$$ \sum (x_i-\bar{x})^2 \;=\; \sum x_i^2 - n\bar{x}^2 \;=\; S_{xx} $$

**右辺のかっこも同じ形。**上の式で \( y \) を \( x \) に置き換えただけである。
**\( x \) の偏差平方和 \( S_{xx} \) になる。**

</div>

<div markdown>

$$ b \;=\; \frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{\sum (x_i-\bar{x})^2} \;=\; \frac{S_{xy}}{S_{xx}} $$

🔴 **答え。傾きは「\( x \) と \( y \) の共分散 ÷ \( x \) の分散」**である
（分子分母を \( n \) で割れば、そのまま共分散と分散になる）。

</div>

<div markdown>

$$ Q \;=\; S_{yy} - 2b\,S_{xy} + b^2 S_{xx} \;=\; S_{xx}\left(b - \frac{S_{xy}}{S_{xx}}\right)^2 + \left(S_{yy} - \frac{S_{xy}^{\,2}}{S_{xx}}\right) $$

**微分を使わない道。**\( a=\bar{y}-b\bar{x} \) を \( Q \) に戻すと、\( b \) だけの**二次式**になる。
それを **平方完成**した形がこれである（\( S_{xx}>0 \) なので下に凸）。

</div>

<div markdown>

$$ b \;=\; \frac{S_{xy}}{S_{xx}} \quad\text{のとき}\quad Q \;=\; S_{yy} - \frac{S_{xy}^{\,2}}{S_{xx}} \quad(\text{最小}) $$

**頂点を読むだけ。**二乗の部分が 0 になるときが最小で、そのときの \( b \) は**微分で出した答えと同じ**。
🔴 **微分を知らなくても、平方完成だけで最小二乗法は終わる。**
（ここで出た最小値 \( S_{yy}-S_{xy}^2/S_{xx} \) は、次の導出②でそのまま使う。）

</div>

</div>

**数値で確かめる**：この回のデータ（n=153種、両対数）で \( S_{xy}/S_{xx} = 0.9333 \)、\( \bar{y}-b\bar{x} = -3.8830 \)。本文の傾き 0.933・切片 −3.883 に一致する。

**使った数学**：二次式の最小化（微I：偏微分、または平方完成）。総和の記号操作（線I）。

### 導出②：単回帰の \( R^2 \) は、相関係数 r の二乗にすぎない

決定係数は「全体のばらつきのうち、モデルが説明できた割合」と定義される。

!!! tip "下のボタンで、1行ずつ送れる"
    導出①の最後で出した \( Q \) の最小値が、そのまま残差平方和である。

<div class="deriv" markdown>

<div markdown>

$$ R^2 \;=\; 1 - \frac{\sum (y_i-\hat{y}_i)^2}{\sum (y_i-\bar{y})^2} \;=\; 1 - \frac{SS_{\text{残差}}}{SS_{\text{全体}}} $$

**定義。**「説明できなかった割合」を 1 から引いたもの。
分母 \( SS_{\text{全体}} = S_{yy} \) は、直線を引かずに \( \bar{y} \) だけで予測したときの外れ具合である。

</div>

<div markdown>

$$ y_i-\hat{y}_i \;=\; (y_i-\bar{y}) - b(x_i-\bar{x}) $$

**残差を書き下した。**導出①より \( \hat{y}_i = \bar{y} + b(x_i-\bar{x}) \) なので、引き算すればこうなる。

</div>

<div markdown>

$$ \sum (y_i-\hat{y}_i)^2 \;=\; S_{yy} - 2b\,S_{xy} + b^2 S_{xx} $$

**二乗して和を取った。**\( (A-B)^2=A^2-2AB+B^2 \) をそのまま使っただけ。
3つの和がそれぞれ \( S_{yy},\ S_{xy},\ S_{xx} \) になる。
（導出①の最後に出てきた式と**同じもの**である。）

</div>

<div markdown>

$$ -2b\,S_{xy} \;=\; -\frac{2S_{xy}^{\,2}}{S_{xx}}, \qquad b^2S_{xx} \;=\; \frac{S_{xy}^{\,2}}{S_{xx}^{\,2}}\cdot S_{xx} \;=\; \frac{S_{xy}^{\,2}}{S_{xx}} $$

**\( b=S_{xy}/S_{xx} \) を、後ろの2項に別々に代入した。**
第2項では \( S_{xx} \) が1つ約分される。
**2つとも \( S_{xy}^2/S_{xx} \) の形になった。**

</div>

<div markdown>

$$ \sum (y_i-\hat{y}_i)^2 \;=\; S_{yy} - \frac{2S_{xy}^{\,2}}{S_{xx}} + \frac{S_{xy}^{\,2}}{S_{xx}} \;=\; S_{yy} - \frac{S_{xy}^{\,2}}{S_{xx}} $$

**足し合わせた。**\( -2 + 1 = -1 \) なので、\( S_{xy}^2/S_{xx} \) がひとつ残る。

</div>

<div markdown>

$$ R^2 \;=\; 1 - \frac{S_{yy} - S_{xy}^{\,2}/S_{xx}}{S_{yy}} \;=\; \frac{S_{xy}^{\,2}/S_{xx}}{S_{yy}} \;=\; \frac{S_{xy}^{\,2}}{S_{xx}S_{yy}} $$

**定義に戻した。**\( 1 - (1 - X) = X \) の形で、きれいに約分される。

</div>

<div markdown>

$$ R^2 \;=\; \frac{S_{xy}^{\,2}}{S_{xx}S_{yy}} \;=\; \left(\frac{S_{xy}}{\sqrt{S_{xx}S_{yy}}}\right)^2 \;=\; r^2 $$

🔴 **かっこの中は、相関係数 \( r \) の定義そのもの**（第5回）。
**説明変数が1つのとき、\( R^2 \) は相関係数 r を二乗しただけのものである。**
第5回で見た r と、今日の \( R^2 \) は別々の量ではない。

</div>

</div>

**数値で確かめる**：この回のデータで \( r = 0.6799 \)、その二乗は 0.4623。本文の \( R^2 = 0.462 \) に一致する。

!!! warning "これは『R² が何を測っているか』を示しただけ"
    この導出が言っているのは「\( R^2 \) は r の二乗である」ということだけで、**\( R^2 \) が高いモデルが正しい、という意味はまったく含まない**。

    しかも説明変数が2つ以上になれば \( R^2 \) はもう \( r^2 \) ではなくなり、**変数を足すだけで必ず上がる**ようになる。なぜそうなるかは、次の §3「R²の罠」で見る。

**使った数学**：平方の展開と総和（線I）。相関係数の定義（第5回）。

### 両対数のときの傾きは「何倍になるか」を表す

傾き **0.933** は、両方を対数にしているので**足し算ではなくかけ算**の関係を意味する。

| 体重が | 行動圏は |
|---|---|
| 2倍 | 1.9倍 |
| 10倍 | **8.6倍** |
| 100倍 | 73.5倍 |

傾きが1.0ちょうどなら「体重10倍で行動圏も10倍」。0.933はそれよりわずかに小さい ＝ **大きい種ほど体重あたりの行動圏はやや狭い**。

この傾き（**スケーリング指数**）は生物学では意味のある量として扱われる。「体が大きいほど広い範囲が要る」ことは分かりきっているが、**どういう比率で増えるのか**を1つの数で表せるのが回帰の力である。

!!! warning "係数は因果ではない"
    「体重10倍で行動圏8.6倍」は**予測上の関連**であって、「体重を増やせば行動圏が広がる」という**因果の保証ではない**（第5回）。観察データの回帰係数を因果効果と読んではいけない。

---

## 2. 重回帰 ―― 複数の説明変数で

体重だけでなく**集団サイズ**も一緒に使う（n=149種）：

$$ \log(\text{行動圏}) \approx -3.358 + 0.568\times\log(\text{体重}) + 0.828\times\log(\text{集団サイズ}) \quad (R^2=0.601) $$

重回帰では各係数が「**他の変数を一定にしたときの**、その変数の関連」を表す（＝統制）。

R² が 0.46 → 0.60 に上がった。集団サイズには、体重だけでは説明できない情報がある。

!!! success "注目：体重の係数が 0.933 → 0.568 に下がった"
    「集団サイズが同じ種どうしで比べたときの、体重の効果」はもっと小さい。単回帰のときの0.933には、**集団サイズの効果が混ざり込んでいた**（大きい種は大きな群れを作りがち）。

    これが第5回でやった**統制**そのものである。**重回帰は、統制を式の中で行う道具でもある。**

さらに `個体群密度` を足すと **R² = 0.746**（n=137種）。個体群密度の係数は **−0.573** で負 ―― 密に住んでいる種ほど、一頭あたりの行動圏は狭い。

よく当てはまっている ―― ように見える。**ここで立ち止まる。**

---

## 3. R²の罠 ―― 変数を足せば、必ず上がる

ここが今日の核心。**説明変数を足すと、R²は必ず上がる（決して下がらない）。** たとえそれが**まったく無意味な数字**でも。

行動圏と無関係な「でたらめな乱数の列」を体重に足していくと：

| 足したでたらめ列 | R² |
|---|---|
| 0本 | 0.462 |
| 1本 | 0.472 |
| 5本 | 0.501 |
| 20本 | 0.509 |
| 50本 | **0.665** |

!!! danger "R²が高い ≠ 良いモデル"
    中身がゴミの乱数を50本足すだけで、R²は 0.46 → 0.67 に上がった。
    当てはまり（R²）を上げたいだけなら、変数をたくさん入れればいい。だがそれは**手元のデータに合わせすぎた**だけで、**未来の予測は良くならない**。これが **過学習** の入り口。

    しかも今回は n=153種しかない。**データの数に対して変数が多いほど、この効き方は激しくなる。**

    §2でR²が0.75まで上がったのを見て「良いモデルだ」と思ったなら ―― いま同じことが起きていないと、どうやって言えるだろうか。

「当てはまりの良さ」と「モデルの複雑さ」をどう釣り合わせるか ―― それが**次回（第11回 AIC）**のテーマ。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 400" role="img" aria-labelledby="r2t r2d" style="width:100%;height:auto;max-width:720px;display:block;margin:0.8em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="r2t">中身が乱数でも、変数を足せば R² は必ず上がる</title><desc id="r2d">横軸は行動圏と何の関係もない「でたらめな乱数の列」を足した本数、縦軸は決定係数 R²。帯は60回くりかえしたときの10〜90%の幅、太い線はその中央値。1本も足さないときの0.462から、50本足すと中央値で0.622まで上がる。R²は決して下がらない。当てはまりの良さは、良いモデルの証拠にならない。</desc><text x="0.0" y="30.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">足したのは、行動圏と何の関係もない乱数の列だけ</text><line x1="62.0" y1="262.0" x2="560.0" y2="262.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="54.0" y="266.0" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">0.4</text><line x1="62.0" y1="218.4" x2="560.0" y2="218.4" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="54.0" y="222.4" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">0.5</text><line x1="62.0" y1="174.9" x2="560.0" y2="174.9" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="54.0" y="178.9" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">0.6</text><line x1="62.0" y1="131.3" x2="560.0" y2="131.3" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="54.0" y="135.3" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">0.7</text><line x1="62.0" y1="87.8" x2="560.0" y2="87.8" stroke="currentColor" stroke-width="1" stroke-opacity="0.13"/><text x="54.0" y="91.8" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.75">0.8</text><text x="62.0" y="281.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">0</text><text x="161.6" y="281.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">10</text><text x="261.2" y="281.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">20</text><text x="360.8" y="281.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">30</text><text x="460.4" y="281.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">40</text><text x="560.0" y="281.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.75">50</text><line x1="62.0" y1="262.0" x2="560.0" y2="262.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/><line x1="62.0" y1="66.0" x2="62.0" y2="262.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/><text x="311.0" y="302.0" font-size="11.5" text-anchor="middle" fill="currentColor" fill-opacity="0.8">足した「でたらめな列」の本数</text><text x="54.0" y="54.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.8">R²</text><polygon points="62.0,234.9 72.0,231.4 81.9,228.5 91.9,227.6 101.8,222.5 111.8,221.4 121.8,220.4 131.7,218.1 141.7,216.3 151.6,214.2 161.6,211.2 171.6,211.0 181.5,209.6 191.5,207.6 201.4,206.1 211.4,204.6 221.4,203.0 231.3,199.9 241.3,198.9 251.2,198.7 261.2,198.2 271.2,195.6 281.1,193.8 291.1,191.6 301.0,190.6 311.0,189.3 321.0,185.9 330.9,183.6 340.9,180.7 350.8,178.8 360.8,178.3 370.8,177.4 380.7,177.0 390.7,175.3 400.6,172.7 410.6,171.2 420.6,170.4 430.5,168.7 440.5,167.5 450.4,166.2 460.4,162.6 470.4,161.4 480.3,159.8 490.3,157.4 500.2,156.2 510.2,155.9 520.2,155.7 530.1,155.4 540.1,153.0 550.0,152.0 560.0,148.8 560.0,179.0 550.0,179.6 540.1,180.9 530.1,182.8 520.2,184.0 510.2,185.0 500.2,185.6 490.3,186.6 480.3,188.5 470.4,188.9 460.4,190.6 450.4,191.1 440.5,193.0 430.5,196.7 420.6,197.8 410.6,198.0 400.6,199.7 390.7,200.0 380.7,203.8 370.8,204.3 360.8,204.7 350.8,205.2 340.9,206.1 330.9,206.8 321.0,207.7 311.0,209.2 301.0,209.9 291.1,211.5 281.1,213.2 271.2,215.3 261.2,215.9 251.2,217.1 241.3,218.2 231.3,220.0 221.4,220.8 211.4,221.7 201.4,222.6 191.5,224.3 181.5,225.2 171.6,225.9 161.6,227.6 151.6,228.9 141.7,229.3 131.7,230.3 121.8,231.2 111.8,232.7 101.8,233.4 91.9,234.1 81.9,234.7 72.0,234.8 62.0,234.9" fill="#5c6bc0" fill-opacity="0.16" stroke="none"/><path d="M 62.0 234.9 L 72.0 234.2 L 81.9 233.3 L 91.9 232.2 L 101.8 230.1 L 111.8 229.2 L 121.8 227.6 L 131.7 225.8 L 141.7 224.7 L 151.6 223.9 L 161.6 222.0 L 171.6 220.3 L 181.5 219.1 L 191.5 217.4 L 201.4 216.2 L 211.4 215.0 L 221.4 212.5 L 231.3 211.2 L 241.3 210.0 L 251.2 208.9 L 261.2 207.7 L 271.2 206.9 L 281.1 206.3 L 291.1 204.0 L 301.0 201.5 L 311.0 200.9 L 321.0 200.4 L 330.9 196.8 L 340.9 195.6 L 350.8 193.4 L 360.8 193.0 L 370.8 191.7 L 380.7 190.8 L 390.7 189.8 L 400.6 188.0 L 410.6 186.7 L 420.6 184.0 L 430.5 182.0 L 440.5 181.1 L 450.4 180.0 L 460.4 178.9 L 470.4 177.6 L 480.3 176.7 L 490.3 174.7 L 500.2 173.6 L 510.2 172.3 L 520.2 170.9 L 530.1 169.6 L 540.1 167.3 L 550.0 166.8 L 560.0 165.4" fill="none" stroke="#5c6bc0" stroke-width="2.6" stroke-opacity="1.0"/><circle cx="62.0" cy="234.9" r="4.6" fill="#c62828" fill-opacity="1.0"/><text x="72.0" y="250.9" font-size="12" text-anchor="start" font-weight="bold" fill="#c62828" fill-opacity="1.0">0.462</text><circle cx="560.0" cy="165.4" r="4.6" fill="#c62828" fill-opacity="1.0"/><text x="550.0" y="153.4" font-size="12" text-anchor="end" font-weight="bold" fill="#c62828" fill-opacity="1.0">0.622</text><text x="576.0" y="110.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="1.0">帯は60回ぶんの</text><text x="576.0" y="126.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="1.0">10〜90%の幅</text><text x="576.0" y="150.0" font-size="11.5" text-anchor="start" font-weight="bold" fill="#5c6bc0" fill-opacity="1.0">太線は中央値</text><text x="576.0" y="182.0" font-size="11.5" text-anchor="start" fill="#ef6c00" fill-opacity="1.0">n = 153種に対して</text><text x="576.0" y="198.0" font-size="11.5" text-anchor="start" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">変数50本</text><text x="0.0" y="322.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.95">当てはまりを上げたいだけなら、変数をたくさん入れればよい。だがそれは手元のデータに合わせただけで、未来の予測は良くならない。</text><text x="0.0" y="346.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.95">だから「R²が高いから良いモデル」とは言えない。複雑さの代金をどう払うかが、次回（第11回 AIC）のテーマになる。</text><text x="0.0" y="380.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.7">（本文の表は1回ぶんの実行例。ここでは乱数の種を変えて60回くりかえし、散らばりの幅と中央値を描いている。）</text></svg>

---

## 4. 残差を見る習慣 ／ 外挿の危険

**残差**＝実際の値 − 予測値。残差を予測値に対してプロットし、偏った模様がないか確認するのが作法（ランダムに散っていれば良い兆候）。

???+ note "導出③：残差の和が 0 になるのは、偶然ではない"

    導出①で a と b を決めたとき、実は次の2本の式を 0 とおいていた（\( e_i = y_i - a - bx_i \) は残差）。

    $$ \sum_{i=1}^{n} e_i \;=\; 0, \qquad \sum_{i=1}^{n} x_i e_i \;=\; 0 $$

    上は a についての条件、下は b についての条件そのものである。つまり**最小二乗法で引いた直線では、残差の和は必ず 0 になり、残差と x の積和も必ず 0 になる**。2本を合わせると \( \sum (x_i-\bar{x})e_i = 0 \)、すなわち**残差と x は必ず無相関**である。

    ここが大事なところだ。残差と x が無相関であることは、**モデルが良いことの証拠ではない**。どんなに見当違いな直線でも、最小二乗法で引いた以上は必ずそうなる。最初から保証されていることを確認しても、何も分からない。

    だから残差プロットで探すのは「相関があるかどうか」ではない。**直線では捉えられない形**、つまり曲がり・ばらつきの偏り・飛び抜けた点である。これらは残差と x の相関が 0 のままでも、平気で現れる。

    **数値で確かめる**：この回の回帰で、残差の和も、残差と log体重 の相関も、絶対値が \( 10^{-12} \) より小さくなる。どちらも数値計算の丸め誤差の範囲で 0 である（細かい桁は計算環境によって変わる）。

    **使った数学**：最小化の条件式（微I）。積和が 0 ＝ 直交（線I）。

### 残差は「外れ」ではなく「発見」でもある

予測から最も外れているのは **Erythrocebus patas（パタスモンキー）**。8kgの体格から予測される行動圏の **約49倍**（28.2km²）を使っている。

これはデータの誤りだろうか。**そうではない。**パタスモンキーは森林ではなく**サバンナで地上生活する**霊長類で、散在する食物を求めて広大な範囲を移動することが知られている。

!!! success "残差の大きい点は、モデルが捉えていない何かを教えてくれる"
    「当てはまりが悪い」で終わらせず、**なぜ外れたのかを見に行く**。そこにこそ、平均的な傾向では見えない現象がある。

### 外挿の危険

モデルを当てはめた体重の範囲は **48g 〜 112,589g**。その外を予測してはいけない。

| 式に入れる体重 | 予測される行動圏 | |
|---|---|---|
| 1,000,000 g | 52.1 km² | 1トンの霊長類 |
| 1 g | 0.0001 km² | 1gの霊長類 |
| 3,000,000 g | 145.2 km² | アフリカゾウ（霊長類ですらない） |

**式はどんな数字を入れても答えを返す。エラーは出ない。**しかし1トンの霊長類も1gの霊長類も存在しない。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 398" role="img" aria-labelledby="ext exd" style="width:100%;height:auto;max-width:720px;display:block;margin:0.8em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="ext">式はどんな数字を入れても答えを返す</title><desc id="exd">横軸を1gから300万gまで広げて描いた図。データが実際にある範囲は48gから112,589gまでで、図の中央の帯の部分しかない。その外側に直線を伸ばせば、1gの霊長類にも3トンのゾウにも予測値が出るが、確かめる相手が存在しない。外挿は外れ値とは別の問題である。</desc><text x="0.0" y="30.0" font-size="13.5" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">データがあるのは、この帯の中だけ</text><rect x="209.0" y="70.0" width="262.5" height="184.0" rx="3" ry="3" fill="#00897b" fill-opacity="0.1" stroke="#00897b" stroke-width="1" stroke-opacity="0.45"/><text x="340.2" y="60.0" font-size="11.5" text-anchor="middle" font-weight="bold" fill="#00897b" fill-opacity="1.0">データのある範囲　48g 〜 112,589g</text><text x="77.6" y="273.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">0</text><text x="155.6" y="273.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">1</text><text x="233.5" y="273.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">2</text><text x="311.5" y="273.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">3</text><text x="389.5" y="273.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">4</text><text x="467.4" y="273.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">5</text><text x="545.4" y="273.0" font-size="11" text-anchor="middle" fill="currentColor" fill-opacity="0.7">6</text><line x1="62.0" y1="238.7" x2="600.0" y2="238.7" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="54.0" y="242.7" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">-4</text><line x1="62.0" y1="187.6" x2="600.0" y2="187.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="54.0" y="191.6" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">-2</text><line x1="62.0" y1="136.4" x2="600.0" y2="136.4" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="54.0" y="140.4" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">0</text><line x1="62.0" y1="85.3" x2="600.0" y2="85.3" stroke="currentColor" stroke-width="1" stroke-opacity="0.09"/><text x="54.0" y="89.3" font-size="11" text-anchor="end" fill="currentColor" fill-opacity="0.7">2</text><line x1="62.0" y1="254.0" x2="600.0" y2="254.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.4"/><line x1="62.0" y1="70.0" x2="62.0" y2="254.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.4"/><text x="331.0" y="294.0" font-size="11.5" text-anchor="middle" fill="currentColor" fill-opacity="0.8">体重 log10(g)</text><text x="54.0" y="58.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.8">行動圏 log10(km²)</text><circle cx="367.3" cy="175.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="375.3" cy="154.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="378.2" cy="149.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="374.4" cy="162.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="308.4" cy="179.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="375.9" cy="127.3" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="377.7" cy="134.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="380.1" cy="139.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="384.8" cy="133.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="314.5" cy="187.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="305.2" cy="187.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="391.3" cy="136.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="375.9" cy="156.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="306.0" cy="172.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="310.1" cy="179.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="322.7" cy="175.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="318.0" cy="160.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="291.8" cy="149.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="279.3" cy="164.5" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="278.1" cy="153.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="278.3" cy="162.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="269.6" cy="179.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="278.3" cy="167.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="275.0" cy="187.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="240.8" cy="204.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="342.7" cy="143.5" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="345.9" cy="137.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="348.8" cy="148.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="346.2" cy="130.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="377.8" cy="143.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="354.3" cy="156.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="355.1" cy="187.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="353.4" cy="152.3" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="361.4" cy="134.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="366.3" cy="162.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="368.1" cy="167.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="367.7" cy="134.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="354.7" cy="134.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="284.2" cy="179.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="256.5" cy="179.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="346.3" cy="128.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="348.3" cy="132.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="389.2" cy="156.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="385.1" cy="158.3" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="386.1" cy="145.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="380.6" cy="150.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="345.5" cy="167.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="381.8" cy="99.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="329.5" cy="169.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="340.8" cy="169.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="342.1" cy="175.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="330.9" cy="169.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="335.2" cy="159.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="266.7" cy="155.5" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="219.5" cy="187.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="255.6" cy="172.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="259.5" cy="164.5" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="246.7" cy="187.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="471.5" cy="121.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="326.6" cy="153.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="308.5" cy="187.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="371.2" cy="154.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="371.2" cy="158.3" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="369.7" cy="149.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="371.4" cy="160.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="371.7" cy="151.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="369.5" cy="152.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="384.2" cy="160.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="373.6" cy="124.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="344.2" cy="169.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="292.6" cy="152.3" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="297.2" cy="138.5" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="293.8" cy="151.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="304.9" cy="189.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="294.2" cy="205.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="297.9" cy="201.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="302.0" cy="191.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="379.4" cy="128.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="374.9" cy="148.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="264.5" cy="191.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="363.0" cy="145.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="389.9" cy="132.5" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="374.7" cy="116.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="381.2" cy="130.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="366.0" cy="137.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="372.2" cy="137.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="363.6" cy="146.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="394.1" cy="125.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="406.8" cy="100.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="221.0" cy="187.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="209.0" cy="187.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="319.0" cy="138.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="273.6" cy="175.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="396.4" cy="132.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="374.4" cy="135.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="317.9" cy="167.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="304.4" cy="160.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="432.0" cy="99.5" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="440.4" cy="110.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="408.9" cy="119.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="405.0" cy="106.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="400.9" cy="104.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="408.9" cy="111.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="314.2" cy="160.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="281.3" cy="179.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="383.7" cy="146.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="378.2" cy="146.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="385.4" cy="146.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="382.1" cy="169.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="328.8" cy="172.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="446.2" cy="121.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="375.2" cy="159.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="377.5" cy="166.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="373.7" cy="154.3" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="374.6" cy="160.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="374.6" cy="160.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="374.1" cy="144.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="375.9" cy="163.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="358.3" cy="156.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="335.5" cy="141.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="375.2" cy="153.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="354.2" cy="167.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="354.8" cy="175.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="392.7" cy="103.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="396.4" cy="114.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="399.5" cy="101.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="280.0" cy="154.3" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="287.5" cy="156.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="281.1" cy="153.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="288.6" cy="154.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="290.7" cy="169.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="291.6" cy="153.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="284.5" cy="151.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="285.4" cy="167.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="300.1" cy="162.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="301.7" cy="140.7" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="397.5" cy="133.5" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="379.3" cy="162.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="392.2" cy="153.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="238.1" cy="187.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="236.9" cy="198.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="238.5" cy="191.3" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="251.1" cy="179.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="405.3" cy="134.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="388.5" cy="175.4" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="378.2" cy="160.0" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="383.4" cy="127.6" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="391.4" cy="164.5" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="378.6" cy="155.5" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="380.5" cy="156.1" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="393.4" cy="153.2" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="378.4" cy="179.9" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><circle cx="357.2" cy="132.8" r="2.4" fill="#5c6bc0" fill-opacity="0.45"/><path d="M 209.0 195.5 L 471.5 115.2" fill="none" stroke="#c62828" stroke-width="2.6" stroke-opacity="1.0"/><path d="M 62.0 240.4 L 209.0 195.5" fill="none" stroke="#c62828" stroke-width="2" stroke-opacity="0.75" stroke-dasharray="6 4"/><path d="M 471.5 115.2 L 600.0 75.9" fill="none" stroke="#c62828" stroke-width="2" stroke-opacity="0.75" stroke-dasharray="6 4"/><circle cx="77.6" cy="235.7" r="4.6" fill="#ef6c00" fill-opacity="1.0"/><text x="85.6" y="239.7" font-size="11.5" text-anchor="start" fill="#ef6c00" fill-opacity="1.0">0.0001 km²（1gの霊長類）</text><circle cx="545.4" cy="92.6" r="4.6" fill="#ef6c00" fill-opacity="1.0"/><text x="545.4" y="80.6" font-size="11.5" text-anchor="middle" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">52.1 km²</text><text x="545.4" y="64.6" font-size="11" text-anchor="middle" fill="#ef6c00" fill-opacity="1.0">1トンの霊長類</text><circle cx="582.6" cy="81.2" r="4.6" fill="#ef6c00" fill-opacity="1.0"/><text x="592.6" y="101.2" font-size="11.5" text-anchor="end" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">145.2 km²</text><text x="592.6" y="117.2" font-size="11" text-anchor="end" fill="#ef6c00" fill-opacity="1.0">アフリカゾウ（霊長類ですらない）</text><text x="0.0" y="316.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.95">外れ値は「ありえない値か」を人間が判断できた。外挿は、出てきた数字を確かめる相手がそもそも存在しない。</text><text x="0.0" y="340.0" font-size="11.5" text-anchor="start" fill="currentColor" fill-opacity="0.95">エラーは出ない。だから自分で範囲を見張るしかない。</text><text x="0.0" y="374.0" font-size="11" text-anchor="start" fill="currentColor" fill-opacity="0.7">（回帰式は log(行動圏) = −3.883 + 0.933 × log(体重)。破線はデータの外へ伸ばした部分。）</text></svg>

!!! danger "外れ値と外挿は、違う"
    外れ値は「ありえない値かどうか」を人間が判断できた（第2回：ゴリラ149kgは本物、−999gは誤り）。
    **外挿は、出てきた数字が正しいかどうか確かめる相手がそもそも存在しない。**

---

## まとめ

| 概念 | ひとこと |
|---|---|
| 単回帰 | y ≈ 切片 + 傾き×x。傾き＝xが1増えると予測がいくつ増えるか |
| 両対数の傾き | 「何倍になるか」を表す（体重10倍 → 行動圏8.6倍） |
| 決定係数 R² | ばらつきのうちモデルが説明できた割合（0〜1） |
| 重回帰 | 複数の説明変数。各係数は「他を一定にしたとき」の関連（＝統制） |
| ❌ R²の罠 | 変数を足せばR²は必ず上がる。**でたらめ50本で0.46→0.67** |
| ❌ 係数の罠 | 回帰係数＝予測上の関連。因果の保証ではない |
| ❌ 外挿の罠 | データ範囲の外は予測できない（1トンの霊長類はいない） |
| 残差 | 実際−予測。偏りを見る。**大きな残差は発見の入り口**（パタスモンキー） |

> **モデルは現実の近似。「当てはまりの良さ」は「良いモデル」ではない。**
> 係数を因果と読まず、範囲外を予測せず、残差を見る。

---

## 今日の課題（Moodle提出）

**配点：100点（選択40点 ＋ 記述60点）／ 提出先：Moodle ／ 提出期限：次回授業の開始時刻まで**

Colab `10_regression.ipynb` を実行したうえで答えること。

---

### パートA：選択問題（各10点 ×4＝40点）

**A1.** 単回帰「log行動圏 ≈ −3.883 + 0.933 × log体重」の **傾き0.933** の意味として**最も正しい**のは？

- (ア) 体重が0.933倍の種の行動圏
- (イ) 体重が10倍になると、予測される行動圏は約8.6倍になる
- (ウ) 行動圏が必ず0.933km²になる

**A2.** 「体重」だけのモデルに、行動圏と**無関係なでたらめの乱数列**を50本足すと、R²はどうなったか。

- (ア) 0.46 のまま変わらない　(イ) 0.46 → 0.67 に上がった　(ウ) 0.46 → 0.10 に下がった

**A3.** A2の結果から言えることとして**最も適切**なのは？

- (ア) R²が高いほど常に良いモデルだ
- (イ) 変数を足せばR²は上がるので、R²の高さだけでモデルの良さは判断できない
- (ウ) でたらめな乱数は行動圏を予測できる

**A4.** この回帰式に体重 1,000,000 g（1トン）を入れると、予測される行動圏は 52.1 km² になった。ここから分かることは？

- (ア) 1トンの霊長類の行動圏は 52.1 km² である
- (イ) データの範囲外（外挿）では予測は信用できない
- (ウ) モデルが間違っている

---

### パートB：記述問題（AIフィードバック対象・60点）

!!! warning "【全記述に共通・重要】自分の出力を引用すること"
    記述には、**今日のColabであなたのノートが出した数値**を最低1つ引用すること。**ここには値を書かない。自分の画面に出た値を使うこと。**
    引ける量の例：「体重の傾き」「でたらめな列を足す前と後のR²」「外挿したときの予測値」。
    **引用がない記述は満点になりません。**

**B1.（30点）** ある人が「重回帰でR²=0.95の高いモデルができた。変数を30個入れたら当てはまりが良くなった。これは素晴らしいモデルだ」と言った。この主張の**問題点**を、今日学んだ「R²と変数の数の関係」「過学習」の観点から指摘しなさい。

**B2.（30点）** 「体重→行動圏」の回帰式（**傾きはあなたのノートの出力を見ること**）について、**この予測を使ってはいけない場面・信じすぎてはいけない点**を2つ挙げ、それぞれなぜかを説明しなさい。（ヒント：因果・外挿・残差・R²のうちから）

> 目安：B1・B2あわせて350〜550字。**自分の言葉**で書くこと。
>
> **字数は目安です。多少の過不足で減点はしません。**見るのは、設問が挙げた要素（上の箇条書き）が書けているかどうかです。ただし要素が抜けていれば、その分は引きます。

!!! abstract "次回予告"
    第11回「モデル選択とAIC」。R²の罠を乗り越える。「当てはまりの良さ」と「モデルの複雑さ」のトレードオフを、AICで定量化する。オッカムの剃刀。