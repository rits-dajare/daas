# DaaS

![CI](https://github.com/rits-dajare/daas/workflows/CI/badge.svg)
[![Twitter](https://img.shields.io/badge/Twitter-%40rits_dajare-blue?style=flat-square&logo=twitter)](https://twitter.com/rits_dajare)

![](https://raw.githubusercontent.com/Ritsumeikan-Dajare-Circle/media/d72e2dbf8459689384af0de9e8b8d3e2d36a9cd2/logo/source.svg?sanitize=true)

This project's objective is to spread puns posted on RDC official slack's #ダジャレ channel through an official [Twitter account](https://twitter.com/rits_dajare).<br>
Automatically determines whether a posted sentence is pun, and if true, gives a star with the rating engine.

## Requirements

- Python ~> 3.9
- pipenv

## Usage

### Install dependencies

```sh
pip install -U pip
pip install pipenv
pipenv install
```

### Running the application in dev mode

```shell
$ pipenv run start
```

If you want to know the details of how to use this, run the following command.

```sh
$ pipenv run help
```

### Running the application in production mode

If you want to specify version, you can see versions [here](https://github.com/rits-dajare/daas/pkgs/container/daas).

```shell
docker run -p 8000:8000 ghcr.io/rits-dajare/daas:latest
```