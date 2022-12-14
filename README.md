## 目的
- 有力ではない馬を見分ける
- 走破タイムを比較する予測方法が通用しそうなレースを見分ける
## 内容
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

## 注意
過去にそのレースと同じ条件で走っていないとデータを取得できません。***グラフに出力される出走馬の頭数が該当レースと一致しない***ことがあります。  

## コマンド（Windowsコマンドプロンプトの場合）
<details>
<summary>

```
<input>
python -m main
```

</summary>

```
<output>
[Default:tomorrow, 1key:today]
```  
| 分析したい日 | 入力の長さ |
|:-|-:|
| 明日 | 0 |
| 今日 | 1 |

明日のグラフを作成したいときは何も入力しないでエンターキーを押します。今日のグラフなら、aでもkでもよいのでひとつキーを入力してエンターキーを押します。
</details>

<details>
<summary>

```
<input>
python -m fig
```
</summary>
  
```
<output>
[Default:tomorrow, 1key:today]
```
| 分析したい日 | 入力の長さ |
|:-|-:|
| 明日 | 0 |
| 今日 | 1 |

明日のグラフを作成したいときは何も入力しないでエンターキーを押します。今日のグラフなら、aでもkでもよいのでひとつキーを入力してエンターキーを押します。
</details>
  
## ファイルの場所  
log/date/track/***figure.png***  
log/data/track/race_number/horse.csv  
  
グラフを出力した後はcsvファイルを削除しても大丈夫です。
