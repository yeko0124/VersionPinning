import sys
import re
import pathlib
import importlib
import datetime

import requests
from PySide2 import QtGui, QtWidgets, QtCore

import hou
from libs import db
from libs.hou_lib import render
from ui import versionUp_ui

importlib.reload(versionUp_ui)

DISCORD_WEBHOOK_URL = ('https://discord.com/api/webhooks/1219107362732769370/0APScAS-UK9gENKDLwG7KvfksYgQzWyT920M_dEZn_w5v_3MMQp9CFfvV1IjVd9tEuTY')


class Status:
    DEPART = {
        1: 'Plate',
        2: 'Modeling',
        3: 'Animation',
        4: 'Rendering',
        5: 'Compositing',
        6: 'VFX Supervision',
        7: 'Effects',
        8: 'Lighting',
        9: 'Matchmove',
        10: 'Texturing',
        11: 'Shading',
        12: 'Concept Art',
        13: 'Digital Matte',
        14: 'Rigging',
        15: 'Software Development'
    }


class VersionUp(QtWidgets.QWidget, versionUp_ui.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.hou_ren = render.HRender()

        self.__db = db.DBVersionUp()
        if not self.__db.connect.is_connected():
            sys.stderr.write('not connected db...')
            return

        self.ver = 0
        self.__connector()
        self.__init()

    def __init(self):
        try:
            name = self.hou_ren.read_rop_name()
            self.ver = self.hou_ren.read_file_version_cnt()
            a = hou.parm(f'/stage/{name}/lopoutput')
            a.set(f"`$HIP`/geo/`$HIPNAME`/`$OS`/`$OS`_v00{self.ver}.usdnc")
            self.hou_ren.make_post_file(name)
        except AttributeError:
            print('not open file yet')

    def __connector(self):
        self.pushButton__render.clicked.connect(self.hou_ren.read_usd_rop)
        self.pushButton__render.clicked.connect(self.update_file)

    def update_file(self):
        try:
            cache_name = self.read_cache_ropname()
            existing_final = self.__db.get_version_by_cache_name(cache_name)

            self.user = [self.lineEdit__user.text()]
            self.uid = self.__db.get_userid_by_user(self.user)[0][0]
            self.depart = self.__db.get_depart_by_name(self.user)[0][0]

            # final 파일이 이미 존재할 경우
            if existing_final:
                # 버전업 시간 / user 업데이트
                final_id = self.__db.update_version_time(cache_name, int(self.uid))
                print('update:', final_id)
            # final 파일이 없는 경우 (새로운 final 파일 생성)
            else:
                file_info_lst = [cache_name, datetime.datetime.now(), int(self.uid)]
                # todo 파일이 진짜 생기면 등록이 되도록 ->> 이걸 어디서 해줘야 할지 고민....
                final_id = self.__db.add_version(file_info_lst)
                print('insert:', final_id)

            cache_path = str(pathlib.Path(hou.parm(f'/stage/{cache_name}/lopoutput').eval()))
            if pathlib.Path(cache_path).exists():
                pass

            cache_id = self.__db.add_cache_and_get_id(final_id, cache_path)

            note = self.textEdit__ref_note.toPlainText()
            if not len(note) == 0:
                self.__db.add_note(note, cache_id)
            elif len(note) == 0:
                note = 'None'
                self.__db.add_note(note, cache_id)

            self.slot_msg()
            self.done_msg()
        except IndexError:
            QtWidgets.QMessageBox.critical(self, 'Warning',f'Render failed!!!!\nYou wrote invalid name\n>>>>>{self.user[0]}<<<<<')
            return

    @staticmethod
    def read_cache_ropname():
        for item in hou.node("/stage").children():
            if item.type().name() == 'usd_rop':
                cache_name = item.name()
                return cache_name

    def done_msg(self):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle('Done')
        msg_box.setText('Succeed!!!!\nWe just sent a message to the next team')
        msg_box.setIcon(QtWidgets.QMessageBox.NoIcon)
        msg_box.exec_()

    def slot_msg(self):
        try:
            note = self.textEdit__ref_note.toPlainText()
            depart = f'** {self.depart} Department **'
            msg = f'{depart}\n  {note}\n\n from {self.user[0]}'
            self.set_msg(msg, 16711680)
        except AttributeError:
            return

    # notice version up through discord app
    def set_msg(self, msg, color):
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


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ver_up = VersionUp()
    ver_up.show()
    app.exec_()