# AHC interactive debug tool

## 概要
AtCoderのヒューリスティックコンテスト(AHC)で、インタラクティブ問題のデバッグを支援するツールです。

インタラクティブ問題では公式配布されているローカルテスタでテスト実行する場合、testerが回答プログラムを起動して実行する形式になっているため、回答プログラムのデバッグ実行ができない(または難しい)という問題がありました。

本ツールではこの問題を解消し、公式ローカルテスタを使いつつ、回答プログラムのデバッグ実行を可能としています。メカニズムについては以下の記事をご覧ください。

- [AtCoder AHCのインタラクティブ問題でデバッグ実行を実現する](https://qiita.com/tanaka-a/items/6856d7fcf78f2516f691)

## 動作確認環境
- MacOS Ventura
- python 3.11.4

## 使用方法
### 1. 準備
#### (1) 必要ライブラリのインストール
aioconsoleをインストールしてください。
```
pip install aioconsole
```

#### (2) 前提フォルダ構成
以下のようなフォルダ構成を前提として説明します。回答プログラムがPythonの場合の例を示しますが、他の言語でも応用可能なはずです(Javaは動作確認済み)。

```
ahcNNN
├─ main.py  (回答プログラム。自前で作成)
├─ main_wrapper.py  (回答プログラムのWrapper。手順2にて作成)
├─ interactive_sock_proxy.py  (本ツール)
└─ tools  (公式のローカルテスタ)
     ├─ in  (公式の入力ファイル)
     ├─ out  (出力ファイル用フォルダ)
     ├─ src  (公式ローカルテスタのソース)
     └─ target  (公式ローカルテスタのビルド先。手順1(3)にて作成)
```

#### (2) 公式testerのコンパイル
公式testerをコンパイルしてください。
```
cd tools
cargo build --release
cd ..
```

tools/target/release配下にtesterができていることを確認してください。

### 2. Wrapperの作成
回答プログラムの実装言語に応じて、回答プログラムのWrapperを作成します。以下のような機能を持つ必要があります。
- 本ツール(interactive_sock_proxy.py)をサーバーとしてソケット通信を実行。通信先はlocalhost(127.0.0.1)、ポートは任意(サーバ起動時に指定するポート番号と合わせる)です。
- 回答プログラムを呼び出す。その際に、標準入力をソケットサーバーからの入力に、標準出力への出力に置き換える。

Pythonでの実装例の抜粋
```
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  try:
    sock.connect(('127.0.0.1', PORT))
  except:
    sys.exit(1)
  with io.TextIOWrapper(SocketIO(sock), 'utf-8') as sio:
    # 標準入出力を置き換え
    sys.stdin = sio
    sys.stdout = sio

    # プログラム本体の実行
    import main
```

なお、Python版とJava版の実装例が以下にありますので、参考にしてください。

- sample_client_py/main_wrapper.py (Python版)
- sample_client_java/MainWrapper.java (Java版)

### 3. 実行
#### (1) 公式testerの実行
本ツール(interactive_sock_proxy.py)をテスト対象として公式testerを実行します。実行時の引数にソケット通信に使用するポート番号を指定します(以下の実行例では8888)。

```
./tools/target/release/tester python interactive_sock_proxy.py 8888 < ./tools/in/0000.txt > ./tools/out/0000.txt
```

#### (2) 回答プログラムのデバッグ実行
手順2で作成したWrapperプログラムを、VSCode等でデバッグ実行してください。標準入出力が(1)で起動したサーバとの通信に置き換えられて回答プログラムが実行されるため、実際に入出力を行いながらデバッグ実行を行うことができます。

## Windowsでの実行時の制限事項
Windows上で実行すると、回答プログラムが終了しても、interactive_sock_proxy.pyが自動的には終了しません。Ctrl+Cで終了させてください。