#!/usr/bin/env python
# encoding=utf-8

# author        : seongcheol jeon
# created date  : 2024.02.17
# modified date : 2024.02.17
# description   :


class ProgressBar:
    DEFAULT_PROGRESS_STYLE = '''
    QProgressBar {
        text-align: center;
        height: 15px;
    }
    
    QProgressBar::chunk {
        width: 10px;
    }
    '''

    ORANGE_PROGRESS_STYLE = '''
    QProgressBar {
        text-align: center;
        height: 15px;
    }
    
    QProgressBar::chunk {
        background-color: orange;
        width: 10px;
        margin: 1px;
    }
    '''


class LineEdit:
    @staticmethod
    def get_iphone_style():
        return '''
            QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #C0C0C0; 
                border-radius: 10px; 
                padding: 5px; 
                color: #000000; 
                font-size: 64px; 
            }

            QLineEdit:focus {
                border-color: #0078D7; 
            }
        '''


class PushButton:
    @staticmethod
    def get_iphone_style(bg_color: str = '#E0E0E0'):
        return '''
            QPushButton {
                background-color: %s; 
                border-style: solid; 
                border-width: 0px; 
                border-radius: 50px;
                border-color: #C0C0C0;
                padding: 5px;
                max-width: 100px;
                max-height: 100px;
                min-width: 100px;
                min-height: 100px;
                
                color: #000000; 
                font-size: 28px;
            }
           
            QPushButton:hover {
                background-color: #D0D0D0; 
            }
            
            QPushButton:pressed {
                background-color: #A0A0A0; 
            }

            QPushButton:focus {
                outline: none;
                border-color: #0078D7; 
            }
        ''' % bg_color

    @staticmethod
    def get_round_style():
        return '''
            QPushButton{
                color: white;
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 190, 11, 255), stop:1 rgba(251, 86, 7, 255));
                border-radius: 20px;
            }
           
            QPushButton:hover {
                background-color: #EB4034; 
            }
            
            QPushButton:pressed {
                background-color: #EBC934; 
            }

            QPushButton:focus {
                outline: none;
                border-color: #0078D7; 
            }
        '''


if __name__ == '__main__':
    pass
