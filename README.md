# 麻雀対戦結果記録アプリ

## 概要

麻雀をプレイした際の各プレイヤーの順位や点数, ポイントを記録するアプリ.(Mリーグルールに基づく)

## 実行方法

Django, 仮想環境にて実装

Ubuntuで実行の際は`source mahjong/lib/activate`で仮想環境に移動

`python manage.py runserver`でアプリを実行

## アプリ画面(ツールバー)

上のツールバーにて

* 当日の対局結果

* 当日の総合成績

* 過去の通算成績

* 対局結果の記録

* プレイヤーの登録

を実行できる.

## アプリ画面(成績)

成績の一覧表示では

* 名前

* 平均着順

* 総合ポイント

* 最大の点棒

* 平均の点棒

* トップ率

* 4着回避率

* 相対局数

がみられる