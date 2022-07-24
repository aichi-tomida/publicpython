# -*- coding: utf-8 -*-
##  Windows(8.1)での作業を想定しています
##   作成者はMacは未所持の為、Macでの実行を想定せずコーディングしております。

import os
import threading  # マルチスレッド
# Enum
from enum import Enum

import pyperclip
import wx  # wxPython のモジュール
import wx.adv

'''
  スクリプト名 :ttray_clip_main.py
  処理内容：  タスク常駐でクリップボード監視
  補足：自身の質問  https://teratail.com/questions/370250 の応用
                    フリーソフト、「!Mr.Clipboard」を自分の望む機能に改修したい
  その他： 作成中です
'''

'''
   終了をクリックした場合、本スクリプトが終了←OK

   NOW：1.起動直後＋継続クリックし、直後に１回のみ本処理が走る
          右クリックし、継続を押さないと本処理の監視が開始されない
        2.監視後、クリップボードを更新しない限り、右クリックでのポップアップメニューが表示されない

   TODO : 継続をクリックせずとも常駐が継続＋右クリックしてもメニューが出るようにしたい
          コンテキストメニュー、継続は無くす

'''

#-------------------------------------------------------------------------------
#   Enum
#-------------------------------------------------------------------------------

class Work(Enum):
    CONTINUED = 1
    END = 2

#-------------------------------------------------------------------------------
#   タスクトレイのクラス　(TaskBarIconを継承)
#-------------------------------------------------------------------------------
class SysTray(wx.adv.TaskBarIcon):
    _blwatch = False
    def __init__(self):
        # カレントディレクトリの変更
        os.chdir(os.path.dirname(__file__))

        # 初期起動
        wx.adv.TaskBarIcon.__init__(self)   # 継承元の初期化を呼び出す

        # アイコン設定
        icon = wx.Icon('icon.png', wx.BITMAP_TYPE_ANY )
        self.SetIcon(icon, "filewatcher")

    #---------------------------------------------------------------------------------------------------
    #   タスクトレイでアイコンをクリックしたときにメニューを表示させ、メニュー内をクリックしたら処理を行う
    #---------------------------------------------------------------------------------------------------
    def CreatePopupMenu(self):
        # タスクトレイメニューの作成
        menu = wx.Menu()
        menu.Append(Work.CONTINUED.value, "継続") # 本来は無くしたい
        menu.Append(Work.END.value, "終了")
        self.Bind(wx.EVT_MENU, self.click_item)
        return menu

    #-------------------------------------------------------------------------------
    #   メニュー項目をクリック
    #-------------------------------------------------------------------------------
    def click_item(self, event):
        event_id = event.GetId()    # IDを取得する

        # クリップ
        if event_id == Work.CONTINUED.value:
            clip()
        elif event_id == Work.END.value:
            self.exitTray(event)

    #-------------------------------------------------------------------------------
    #   終了処理
    #-------------------------------------------------------------------------------
    def exitTray(self, event):
        self.Destroy()
        wx.Exit()

#-------------------------------------------------------------------------------
#   clip
#-------------------------------------------------------------------------------
def clip():
    try:
        # 数字の秒数待機、超えるとexceptへ 指定なしの場合は無限
        # s = pyperclip.waitForNewPaste(2)
        s = pyperclip.waitForNewPaste()
    except pyperclip.PyperclipTimeoutException:
        s = 'No work'

    # 今後は、内容をチェックし、問題が無ければDBにinsertする機能を搭載予定
    # 現時点ではprintでよろし
    print(s)

    # 無限ループにするといつまでたってもコンテキストメニューは出なくなる
    # bl = True
    # while bl:
    #     try:
    #         # 数字の秒数待機、超えるとexceptへ 指定なしの場合は無限
    #         # s = pyperclip.waitForNewPaste(2)
    #         s = pyperclip.waitForNewPaste()
    #     except pyperclip.PyperclipTimeoutException:
    #         s = 'No change'
    #     print(s)

#-------------------------------------------------------------------------------
#　監視処理
#-------------------------------------------------------------------------------
def watchclip():
    clip()

    # 監視開始
    app.MainLoop()
#-------------------------------------------------------------------------------
#  メイン
#-------------------------------------------------------------------------------
if __name__ == "__main__":
   app = wx.App()
   # タスクトレイクラスの呼出
   taskttr = SysTray()
   # 右クリックでメニュー呼び出し
   SysTray.CreatePopupMenu(taskttr)

   # 監視の開始
   watchclip()
