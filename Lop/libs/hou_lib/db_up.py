import datetime
import pathlib
import hou
import requests

from libs import db
from PySide2 import QtWidgets

__db = db.DBVersionUp()

DISCORD_WEBHOOK_URL = (
    'https://discord.com/api/webhooks/1219107362732769370/0APScAS-UK9gENKDLwG7KvfksYgQzWyT920M_dEZn_w5v_3MMQp9CFfvV1IjVd9tEuTY'
)


def update_file(fin_name, cache_path):
    try:
        existing_final = __db.get_version_by_cache_name(fin_name)

        user = hou.parm('username').eval()
        uid = __db.get_userid_by_user(user)[0][0]
        depart = __db.get_depart_by_name(user)[0][0]

        # final 파일이 이미 존재할 경우
        if existing_final:
            # 버전업 시간 / user 업데이트
            final_id = __db.update_version_time(fin_name, int(uid))
            print('update:', final_id)
        # final 파일이 없는 경우 (새로운 final 파일 생성)
        else:
            file_info_lst = [fin_name, datetime.datetime.now(), int(uid)]
            final_id = __db.add_version(file_info_lst)
            print('insert:', final_id)

        # cache_path = str(pathlib.Path(hou.parm(f'/stage/{fin_name}/lopoutput').eval()))
        if pathlib.Path(cache_path).exists():
            pass

        cache_id = __db.add_cache_and_get_id(final_id, cache_path)

        note = hou.parm('refnote').eval()
        if not len(note) == 0:
            __db.add_note(note, cache_id)
        elif len(note) == 0:
            note = 'None'
            __db.add_note(note, cache_id)

        slot_msg()
        done_msg()
    except IndexError:
        QtWidgets.QMessageBox.critical('', 'Warning',
                                       f'Render failed!!!!\nYou wrote invalid name\n>>>>>{user}<<<<<')
        return


def slot_msg():
    try:
        note = hou.parm('refnote').eval()
        user = hou.parm('username').eval()
        depart = f'** {__db.get_depart_by_name(user)[0][0]} Department **'
        msg = f'{depart}\n  {note}\n\n from {user}'
        set_msg(msg, 16711680)
    except AttributeError:
        return


def set_msg(msg, color):
    message = {
        "content": '** Version Up Notice **',
        "embeds": [
            {
                "title": msg,
                "color": color
            }
        ]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=message)


def done_msg():
    msg_box = QtWidgets.QMessageBox()
    msg_box.setWindowTitle('Done')
    msg_box.setText('Succeed!!!!\nWe just sent a message to the next team')
    msg_box.setIcon(QtWidgets.QMessageBox.NoIcon)
    msg_box.exec_()