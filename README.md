# 説明
### 目的
- 有力ではない馬を見分ける
- 走破タイムを比較する予測方法が通用しそうなレースを見分ける
### 内容
nar.netkeiba.coｍをスクレイピングします。  
取得したデータをもとに、レースごとに出走馬の戦績を一括比較したグラフを出力します。  
今のところ、当日もしくは次の日のレースにおける各馬の戦績（日時‐走破タイム）のみ対応しています。
  
※次の条件に一致する戦績データを取得します。
- 開催日（default:次の日）    
- 馬場状態（default:良）  
- 開催場  
- レース距離  
- ダート/芝  
- 走破タイムが入力されている  

### 注意
過去にそのレースと同じ条件で走っていないとデータを取得できません。***グラフに出力される出走馬の頭数が該当レースと一致しない***ことがあります。  

# 使い方
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
  
<details><summary>コマンド説明</summary>
  
| 取得したい馬場状態 | 入力 |
|:-|-:|
| 良馬場 | 1 or any other |
| 稍重馬場 | 2 |
| 重馬場 | 3 |
| 不良馬場 | 4 |
</details>

<details><summary>コマンド説明</summary>
  
| 分析したい日 | 入力の長さ |
|:-|-:|
| 明日 | 0 |
| 今日 | 1 |
</details>

```
python -m fig

>>[Default:tomorrow, 1key:today, 8key:input date]
```
fig.pyを起動します。※main.pyの後に実行してください。  
<details><summary>コマンド説明</summary>
  
| 分析したい日 | 入力の長さ |
|:-|-:|
| 明日 | 0 |
| 今日 | 1 |
</details>
  
### ファイルの場所
すべて終わると、以下のようなディレクトリ構成になっているはずです。csvファイルはグラフを出力した後は削除してもよいです。  
目的のグラフは***pngファイルに保存***されています。  
  
log/date/track/***figure.png***  
log/data/track/race_number/horse.csv  
例）log/20221201/笠松/***1R.png***  
例）log/20221201/笠松/1R/1_馬の名前.csv  

***

<details><summary>手順の具体例</summary>

**明日**のレースと同じ距離・同じ開催場で**良馬場**のものだけ取得して、そのグラフを作りたいときは、

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
***
**今日**のレースと同じ距離・同じ開催場で**重馬場**のものだけ取得して、そのグラフを作りたいときは、

```
>>python -m main
>>3
>>a

（スクレイピングが終わる）


>>python -m fig
>>a
```
のように指示します。  
</details>
