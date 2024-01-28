# DaaS

![CI](https://github.com/rits-dajare/DaaS/workflows/ci/badge.svg)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Twitter](https://img.shields.io/badge/Twitter-%40rits_dajare-blue?style=flat-square&logo=twitter)](https://twitter.com/rits_dajare)

<div align="center">

![](https://raw.githubusercontent.com/Ritsumeikan-Dajare-Circle/media/d72e2dbf8459689384af0de9e8b8d3e2d36a9cd2/logo/source.svg?sanitize=true)

</div>

## Description

This project's objective is to spread puns posted on RDC official slack's #ダジャレ channel through an official [Twitter account](https://twitter.com/rits_dajare).<br>
Automatically determines whether a posted sentence is pun, and if true, gives a star with the rating engine.

## Requiremenst

- Python ~> 3.9
- pipenv

## Installation

```sh
$ git clone <this repo>
$ cd <this repo>

$ pip install -U pip
$ pip install pipenv
$ pipenv install
```

## Usage

### Run

```sh
$ pipenv run start
```

If you want to know the details of how to use this, run the following command.

```sh
$ pipenv run help
```

## Contributing

Bug reports and pull requests are welcome on GitHub at [https://github.com/rits-dajare/DaaS](https://github.com/rits-dajare/DaaS).

## Refarence

- [Swagger UI](https://dajare.abelab.dev/docs)
- [ダジャレステーション](https://dajare.jp/) - used dajare data as teacher in this project.
