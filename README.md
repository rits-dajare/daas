# DaaS

[![build](https://github.com/rits-dajare/DaaS/workflows/build/badge.svg)](https://github.com/rits-dajare/DaaS/actions)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Twitter](https://img.shields.io/badge/Twitter-%40rits_dajare-blue?style=flat-square&logo=twitter)](https://twitter.com/rits_dajare)

<div align="center">

![](https://raw.githubusercontent.com/Ritsumeikan-Dajare-Circle/media/d72e2dbf8459689384af0de9e8b8d3e2d36a9cd2/logo/source.svg?sanitize=true)

</div>

## Description

This project's objective is to spread puns posted on RDC official slack's #ダジャレ channel through an official [Twitter account](https://twitter.com/rits_dajare).<br>
Automatically determines whether a posted sentence is pun, and if true, gives a star with the rating engine.

## Requiremenst

- Python ~> 3.8
- pipenv

## Installation

```sh
$ git clone <this repo>
$ cd <this repo>

$ cd app
$ pip install -U pip
$ pip install pipenv
$ pipenv install
```

## Usage

### Set token

```sh
$ echo "tokens(space delimited)" > app/.env
```

### Run

```sh
$ docker-compose up -d --build
```

## References

<div><a href="https://dajare.jp/" target="_blank"><img src="https://dajare.jp/library/image/Banner/Advertisement/Dajare180x28.png" alt="ダジャレ（だじゃれ）ステーション" border="0" vspace="8" onmouseover="this.src=this.src.replace('png','gif');" onmouseout="this.src=this.src.replace('gif','png');" /></a></div>

## Wiki

Please look at the [documents](https://github.com/rits-dajare/DaaS/wiki).

## Contributing

Bug reports and pull requests are welcome on GitHub at [https://github.com/rits-dajare/DaaS](https://github.com/rits-dajare/DaaS).

## Author

- [Averak](https://github.com/averak)
- `abe12<at>mccc.jp`
