機械学習（ランダムフォレスト）を使用したFXトレード（Python側）サンプル

使用ツール

Anaconda・・・機械学習ライブラリー及びPython3,numpy,pandas

https://www.continuum.io/downloads

TA-LIB・・・・ローソク足--->MA.Rsi等の指標算出

http://mrjbq7.github.io/ta-lib/install.html

Python-MySQL・・・MySQL操作

 http://www.python-izm.com/contents/external/mysql.shtml

◎このサンプルソースは以下について掲載しております。

※機械学習（参照・・・main2.py)

１．PythonからMySQLのFXのローソク足取得

２．FXのローソク足を元にTA-LIB及び一目均衡表を元にした指標算出

３．指標値を元にxx期間のパターン算出

４．機械学習用データの正則化及び未来xx期間の値のラベル付け

５．ランダムフォレストによる機械学習４０種類＊３９パターン

６．機械学習結果のシリアライズ

