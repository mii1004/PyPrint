import tkinter
import urllib
import io

from escpos import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import wrap_slack_api

'''
Slackから情報を取得してレシートプリンターで出力するツール
'''

user_list = wrap_slack_api.get_user_list()
username_dict = {}

for user in user_list:
    username_dict.setdefault(user['name'], user['id'])

root = tkinter.Tk()
root.title(u"Seattle Bar Special!")
root.geometry("500x500")

label = tkinter.Label(root, text=u'Slackアカウントを選択してください')
label.pack(pady=20)

# listboxとscrollbarを描画
listbox_frame = tkinter.Frame(root, width=300, height=300)
listbox_frame.pack()
listbox_item = tkinter.StringVar(value=list(username_dict.keys()))
id_listbox = tkinter.Listbox(listbox_frame, listvariable=listbox_item)
id_listbox.pack(side=tkinter.LEFT)
id_listbox.configure(selectmode="extended")

listbox_scrollbar = tkinter.Scrollbar(listbox_frame, orient=tkinter.VERTICAL, command=id_listbox.yview)
listbox_scrollbar.pack(side=tkinter.RIGHT, fill="y")
# listboxとscrollbarを紐付け
id_listbox["yscrollcommand"] = listbox_scrollbar.set


# レシートを印刷する処理
def receipt_print(user_name, icon_url):
    # lsusbコマンドで取得したIDを設定
    p = escpos.printer.Usb(0x0416, 0x0511, 0)
    # 印刷用のイメージを作成(マルチバイト文字だとプリンタに直接出力できないため)
    width = 500
    height = 500
    image = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(image)
    fontpath = '使用するフォントのパスを設定'
    font = ImageFont.truetype(fontpath, 28, encoding='unic')
    draw.text((0,82), "SeattleBar Special\n", font=font, fill=0)
    draw.text((0,120), "20190925\n", font=font, fill=0)
    draw.text((0,148), user_name, font=font, fill=0)
    p.image(image)
    
    f = io.BytesIO(urllib.request.urlopen(icon_url).read())
    icon_img = Image.open(f)
    p.image(icon_img)
    p.cut()


# クリック時の処理を定義してbuttonを描画
def click_submit_button():
    print('submit clicked')
    # useridでユーザー検索してアイコンのURLを取得
    item_index = id_listbox.curselection()
    selected_name = id_listbox.get(item_index)
    user_detail = wrap_slack_api.get_user_detail(username_dict.get(selected_name))
    icon_url = (user_detail['user']['profile']['image_192'])

    receipt_print(selected_name, icon_url)


submit_button = tkinter.Button(text=u'決定', width=50, command=click_submit_button)
submit_button.pack(padx=200, pady=20)

# イベントを待機
root.mainloop()