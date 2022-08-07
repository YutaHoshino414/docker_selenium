# Dockerコンテナ上で、Seleniumを動かす環境構築🐳

ローカルでscrapyを動かそうとしたところ、  
ライブラリの依存関係でscrapyが動かせなかったため、
Dockerに慣れる目的で作成。  


## STEP
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