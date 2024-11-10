# PixivImage-WebhookSender
Pixivから指定したユーザーのイラストを取得してwebhookで送信

# 実行
- まずこれ
```
pip install requests bs4 dotenv
```
※`bs4.FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?`がでたら
```
pip install lxml
```
しといてください
- つぎ.envにいれる
```
USER_ID= pixivのユーザーID
WEBHOOK_URL= webhookのURL
RANDOM= ランダムに取得する場合はtrue, 最新から順番に取得する場合はfalse
```
- 実行
```
python pixiv.py
```

# 備考
Pixivのスクレイピングは規約違反なので自己責任で。
このコードはあくまで元コードを参考にこういうのができるよっていうだけなので
# 参考
https://github.com/mizutama1233/Pixiv-Image-Scraper/
