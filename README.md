# nar.Scraper

## 準備するもの
OS:windows11  
Python:3.11  
module:bs4, selenium, ChromeDriverManager, lxml, os, datetime, pandas, matplotlib  
  
OSはなんでもよいかもしれません。  
***Pythonのバージョンは同じ***方がよいです。moduleの読み込みでエラーが起きる可能性があります。  
***moduleは全てインストール***してください。  

## 説明
地方競馬の予測を補助するため、nar.netkeiba.coｍをスクレイピングします。  
取得したデータをもとに、レースごとに出走馬の戦績を一括比較したグラフを出力します。  
（今のところ走破タイムのみ対応しています）  
  
また、次の条件に一致するものしか取得しません。
- 開催日は事前に指定したものと一致
- 開催場が該当レースと一致
- 馬場状態は事前に一括指定したものと一致（開催場ごとに指定することはできません）
- レース距離が該当レースと一致
- ダート/芝が該当レースと一致
- 走破タイムが記録されていないものは取得しない

## 使い方
main.pyを起動します。Windowsならコマンドプロンプトで次のようにします。  
```
python -m main
```
スクレイピングが終わったあとに、コマンドプロンプトで次のようにします。
```
python -m fig
```
すべて終わると、以下のようなディレクトリ構成になっているはずです。csvファイルはグラフを出力した後は削除してもよいです。  
目的のグラフはpngファイルです。  
  
log/date/track/***figure.png***  
log/data/track/race_number/horse.csv  
例）log/20221201/笠松/***1R.png***  
例）log/20221201/笠松/1R/1_馬の名前.csv  

## TIPS
過去にそのレースと同じ条件で走っていないとデータを取得できません。よって、***グラフに出力される出走馬の頭数が該当レースと一致しない***ことがあります。  
このスクリプトの目的は、走破タイムを一括比較することで***有力ではない馬を見つける***ことです。そして、***有力馬を検討する時間を増やす***ことです。また、走破タイムを比較する予測方法が通用しそうなレースを見分けることもできます。
