# Dockerコンテナ上で、Seleniumを動かす環境構築🐳

ローカルでscrapyを動かそうとしたところ、  
ライブラリの依存関係でscrapyが動かせなかったため、
Dockerに慣れる目的で作成。  


## コンテナ起動 STEP
```
$ docker-compose build (--no-cache)
```

```
$ docker-compose up -d
```

```
$ docker-compose exec crawl /bin/bash
```

```
$ docker-compose down
```

## Kill Process (chrome)
Selenium を頻繁に使っていると、
どうしても 「chromedriver」「Google Chrome」「Google Chrome Helper」 のプロセスが残ってしまうので
[参考](https://www.dev-dev.net/entry/2018/07/29/195444)  
seleniumに関しては特にコンテナ内でのみ使用したい