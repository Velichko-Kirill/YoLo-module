import wx
import time
import sys
import cv2
import eval

from collections import Counter
import tensorflow as tf

# -*- coding: utf-8 -*-

class GeneralFrame(wx.Frame):

    def __init__(self, parent, id):

        wx.Frame.__init__(self, parent, id, 'VideoAnalysis', size=(600, 800))

        self.panel = wx.Panel(self)

        self.run_eval_button = wx.Button(self.panel, label="Пуск с вебкамеры", pos=(100, 15), size=(200, 150))
        self.Bind(wx.EVT_BUTTON, self.run_eval, self.run_eval_button)

        self.select_video_button = wx.Button(self.panel, label="Выбрать видео", pos=(350, 15), size=(200, 150))
        self.Bind(wx.EVT_BUTTON, self.select_video, self.select_video_button)

        self.select_classes_button = wx.Button(self.panel, label="Выбрать классы", pos=(600, 15), size=(200, 150))
        self.Bind(wx.EVT_BUTTON, self.select_classes, self.select_classes_button)

        self.exit_button = wx.Button(self.panel, label="Выйти", pos=(600, 100), size=(200, 150))
        self.Bind(wx.EVT_BUTTON, self.exit_program, self.exit_button)

        self.show_stats_button = wx.Button(self.panel, label="Показать статистику", pos=(100, 100), size=(200, 150))
        self.Bind(wx.EVT_BUTTON, self.show_stats, self.show_stats_button)

        self.take_screenshot_button = wx.Button(self.panel, label="Сделать скриншот", pos=(350, 100), size=(200, 150))
        self.Bind(wx.EVT_BUTTON, self.take_screenshot, self.take_screenshot_button)


    def exit_program(self, event):

       f1 = open('class_names', 'r+')
       f2 = open('chosen_classes', 'r+')
       f1.truncate()
       f2.truncate()
       f1.close()
       f2.close()
       sys.exit()

    def show_stats(self, event):
        f = open('class_names', 'r')
        obj_stats = f.readlines()
        obj_stats = [line.rstrip() for line in obj_stats]
        obj_stats = dict(Counter(obj_stats))
        stats = ''
        for item in obj_stats.items():
            if item[1] == 1:
                obj_n = ' объект '
            elif 1 < item[1] <= 4:
                obj_n = ' объектa '
            else:
                obj_n = ' объектов '
            stats += f'{str(item[1])}{obj_n}класса {str(item[0])} \n'
        wx.MessageBox(stats, "Распознанные классы объектов: ")

    def run_eval(self, event):
        eval.run_ev()

    def select_video(self, event):
        with wx.FileDialog(self, "Выберите видеофайл: ") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_OK:
                pathname = fileDialog.GetPath()
                wx.MessageBox(pathname, 'Выбранный файл: ')

        def run_ev(path):
            tf.flags.DEFINE_string('video', path, 'Path to the video file.')
            tf.flags.DEFINE_string('model_name', 'Yolo2Model', 'Model name to use.')

            tf.app.run(main=eval.evaluate)

        run_ev(pathname)

    def select_classes(self, event):
        classeswindow = SelectClassesWindow(self, -1)
        classeswindow.Show()

    def take_screenshot(self, event):
        try:
            self.workframe = eval.get_frame()
            cv2.imwrite('frame_{}.jpg'.format(time.time()), self.workframe)
        except AttributeError:
            wx.MessageBox("Запустите программу чтобы сделать скриншот видео.", "Ошибка")


class SelectClassesWindow(wx.Frame):
    def __init__(self, parent, id):

        wx.Frame.__init__(self, parent, id, 'VideoAnalysis', size=(600, 800))

        self.panel = wx.Panel(self)
        self.createButtons()
        self.chosen_classes_list = []

    def createButtons(self):
        all_classes_file = open('data/yolo2/yolo2.names', 'r')
        all_classes = all_classes_file.read().split()

        deltaxSize, deltaySize, c = 0, 0, 0

        self.buttons, num_classes = [], []
        for k, obj_class in enumerate(all_classes):
            self.buttons.append(wx.Button(self.panel, label=f'{obj_class}', pos=(50 + deltaxSize, 20 + deltaySize),
                                       size=(100, 20)))
            # self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[k].GetLabelText()), self.buttons[k])
            deltaySize += 20
            c += 1
            if c == 30:
                deltaxSize += 100
                deltaySize, c = 0, 0

        self.buttons.append(wx.Button(self.panel, label='Применить', pos=(50 + deltaxSize+10, 20 + deltaySize + 10),
                                       size=(100, 20)))
        self.Bind(wx.EVT_BUTTON, self.chosen_classes_processing, self.buttons[-1])

        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[0].GetLabelText()), self.buttons[0])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[1].GetLabelText()), self.buttons[1])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[2].GetLabelText()), self.buttons[2])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[3].GetLabelText()), self.buttons[3])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[4].GetLabelText()), self.buttons[4])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[5].GetLabelText()), self.buttons[5])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[6].GetLabelText()), self.buttons[6])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[7].GetLabelText()), self.buttons[7])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[8].GetLabelText()), self.buttons[8])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[9].GetLabelText()), self.buttons[9])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[10].GetLabelText()), self.buttons[10])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[11].GetLabelText()), self.buttons[11])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[12].GetLabelText()), self.buttons[12])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[13].GetLabelText()), self.buttons[13])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[14].GetLabelText()), self.buttons[14])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[15].GetLabelText()), self.buttons[15])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[16].GetLabelText()), self.buttons[16])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[17].GetLabelText()), self.buttons[17])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[18].GetLabelText()), self.buttons[18])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[19].GetLabelText()), self.buttons[19])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[20].GetLabelText()), self.buttons[20])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[21].GetLabelText()), self.buttons[21])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[22].GetLabelText()), self.buttons[22])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[23].GetLabelText()), self.buttons[23])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[24].GetLabelText()), self.buttons[24])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[25].GetLabelText()), self.buttons[25])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[26].GetLabelText()), self.buttons[26])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[27].GetLabelText()), self.buttons[27])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[28].GetLabelText()), self.buttons[28])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[29].GetLabelText()), self.buttons[29])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[30].GetLabelText()), self.buttons[30])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[31].GetLabelText()), self.buttons[31])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[32].GetLabelText()), self.buttons[32])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[33].GetLabelText()), self.buttons[33])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[34].GetLabelText()), self.buttons[34])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[35].GetLabelText()), self.buttons[35])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[36].GetLabelText()), self.buttons[36])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[37].GetLabelText()), self.buttons[37])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[38].GetLabelText()), self.buttons[38])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[39].GetLabelText()), self.buttons[39])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[40].GetLabelText()), self.buttons[40])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[41].GetLabelText()), self.buttons[41])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[42].GetLabelText()), self.buttons[42])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[43].GetLabelText()), self.buttons[43])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[44].GetLabelText()), self.buttons[44])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[45].GetLabelText()), self.buttons[45])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[46].GetLabelText()), self.buttons[46])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[47].GetLabelText()), self.buttons[47])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[48].GetLabelText()), self.buttons[48])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[49].GetLabelText()), self.buttons[49])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[50].GetLabelText()), self.buttons[50])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[51].GetLabelText()), self.buttons[51])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[52].GetLabelText()), self.buttons[52])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[53].GetLabelText()), self.buttons[53])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[54].GetLabelText()), self.buttons[54])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[55].GetLabelText()), self.buttons[55])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[56].GetLabelText()), self.buttons[56])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[57].GetLabelText()), self.buttons[57])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[58].GetLabelText()), self.buttons[58])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[59].GetLabelText()), self.buttons[59])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[60].GetLabelText()), self.buttons[60])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[61].GetLabelText()), self.buttons[61])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[62].GetLabelText()), self.buttons[62])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[63].GetLabelText()), self.buttons[63])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[64].GetLabelText()), self.buttons[64])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[65].GetLabelText()), self.buttons[65])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[66].GetLabelText()), self.buttons[66])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[67].GetLabelText()), self.buttons[67])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[68].GetLabelText()), self.buttons[68])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[69].GetLabelText()), self.buttons[69])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[70].GetLabelText()), self.buttons[70])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[71].GetLabelText()), self.buttons[71])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[72].GetLabelText()), self.buttons[72])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[73].GetLabelText()), self.buttons[73])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[74].GetLabelText()), self.buttons[74])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[75].GetLabelText()), self.buttons[75])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[76].GetLabelText()), self.buttons[76])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[77].GetLabelText()), self.buttons[77])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[78].GetLabelText()), self.buttons[78])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[79].GetLabelText()), self.buttons[79])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[80].GetLabelText()), self.buttons[80])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[81].GetLabelText()), self.buttons[81])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[82].GetLabelText()), self.buttons[82])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[83].GetLabelText()), self.buttons[83])
        self.Bind(wx.EVT_BUTTON, lambda event: self.chosen_classes_list.append(self.buttons[84].GetLabelText()), self.buttons[84])

        all_classes_file.close()

    def chosen_classes_processing(self, event):
        
        wx.MessageBox(str(set(self.chosen_classes_list)), 'Выбранные классы объектов: ')
        chosen_classes = open('chosen_classes', 'w')
        for obj_class in self.chosen_classes_list:
            chosen_classes.write(f'{obj_class}\n')
        chosen_classes.close()

if __name__ == "__main__":
    app = wx.App()
    frame = GeneralFrame(parent=None, id=-1)
    frame.SetSize(900, 400)
    frame.Show()

    app.MainLoop()
