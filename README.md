# 鉄道模型シミュレーターNX お天候くん
![VRMONLINE-NX 2022_10_08 21_38_12](https://user-images.githubusercontent.com/79089755/194708015-c8aaddaf-a14b-49e6-9b8e-4d2f6d11426d.png)
## 注意
BUILD 305以降に対応
## アプデ情報
Ver1.2　2022.10.13　リソース読み込みにJPEG追加
## 概要
右記サンプル動画参照　https://youtu.be/YCCVklamQJE
## 利用方法
レイアウトファイルと同じフォルダ階層に「otenko.py」ファイルを配置します。  

フォルダ構成：
```
C:\VRMNX（一例）
├ otenko.py
└ VRMNXレイアウトファイル.vrmnx
```

対象レイアウトのレイアウトスクリプトに以下の★内容を追記します。  

```py
import vrmapi
import otenko # ★インポート

def vrmevent(obj,ev,param):
    otenko.vrmevent(obj,ev,param) # ★メイン処理
    if ev == 'init':
        dummy = 1
    elif ev == 'broadcast':
        dummy = 1
    elif ev == 'timer':
        dummy = 1
    elif ev == 'time':
        dummy = 1
    elif ev == 'after':
        dummy = 1
    elif ev == 'frame':
        dummy = 1
    elif ev == 'keydown':
        dummy = 1
```

ファイル読み込みに成功するとビュワー起動直後にスクリプトログへ下記メッセージが表示されます。

```
お天候くん開始！　Version.x.x
```
