# 説明
### 目的
- 有力ではない馬を見分ける
- ***有力馬を検討する時間を増やす***
- 走破タイムを比較する予測方法が通用しそうなレースを見分ける
### 内容
nar.netkeiba.coｍをスクレイピングします。  
取得したデータをもとに、レースごとに出走馬の戦績を一括比較したグラフを出力します。  
今のところ走破タイム-日時のグラフの出力にのみ対応しています。
  
※次の条件に一致するデータを取得します。
- 開催日（default:次の日）    
- 馬場状態（default:良）  
- 開催場  
- レース距離  
- ダート/芝  
- 走破タイムが入力されている  

### 注意
過去にそのレースと同じ条件で走っていないとデータを取得できません。***グラフに出力される出走馬の頭数が該当レースと一致しない***ことがあります。  
このスクリプトの目的は、走破タイムを一括比較することで***有力ではない馬を見つける***ことです。そして、***有力馬を検討する時間を増やす***ことです。走破タイムを比較する予測方法が通用しそうなレースを見分けるためにも使えます。

# ***使い方***
### 準備するもの
OS:windows11  
Python:3.11  
module:bs4, selenium, ChromeDriverManager, lxml, os, datetime, pandas, matplotlib  
  
OSはなんでもよいかもしれません。  
***Pythonのバージョンは同じ***方がよいです。moduleの読み込みでエラーが起きる可能性があります。  
***moduleは全てインストール***してください。ないと動きません。  
### Windowsコマンドプロンプト
```
python -m main

>>[Default:良, 2:稍, 3:重, 4:不]
>>[Default:tomorrow, 1key:today, 8key:input date]
```
main.pyを起動します。  
  
<details><summary>>>[Default:良, 2:稍, 3:重, 4:不]</summary>
  
| 取得したい馬場状態 | 入力 |
|:-|-:|
| 良馬場 | 1 or any other |
| 稍重馬場 | 2 |
| 重馬場 | 3 |
| 不良馬場 | 4 |
</details>

<details><summary>>>[Default:tomorrow, 1key:today, 8key:input date]</summary>
  
| 分析したい日 | 入力の長さ |
|:-|-:|
| 明日 | 0 |
| 今日 | 1 |
| 指定日付 | 8 | 
</details>

```
python -m fig

>>[Default:tomorrow, 1key:today, 8key:input date]
```
fig.pyを起動します。※main.pyの後に実行してください。  
<details><summary>>>[Default:tomorrow, 1key:today, 8key:input date]</summary>
  
| 分析したい日 | 入力の長さ |
|:-|-:|
| 明日 | 0 |
| 今日 | 1 |
| 指定日付 | 8 |
</details>

<details><summary>コマンド例</summary>

明日のレースと同じ距離・同じ開催場で良馬場のものだけ取得して、そのグラフを作りたいときは、

```
>>python -m main
>>
>>

（スクレイピングが終わる）


>>python -m fig
>>
```
のように指示します。  
\>>の部分はなにも入力せず、エンターキーを押します。

2022年12月08日のレースと同じ距離・同じ開催場で重馬場のものだけ取得して、そのグラフを作りたいときは、

```
>>python -m main
>>3
>>20221208

（スクレイピングが終わる）


>>python -m fig
>>20221208
```
のように指示します。  
\>>の部分はなにも入力せず、エンターキーを押します。
</details>

  
### ファイルの場所
すべて終わると、以下のようなディレクトリ構成になっているはずです。csvファイルはグラフを出力した後は削除してもよいです。  
目的のグラフは***pngファイルに保存***されています。  
  
log/date/track/***figure.png***  
log/data/track/race_number/horse.csv  
例）log/20221201/笠松/***1R.png***  
例）log/20221201/笠松/1R/1_馬の名前.csv  
