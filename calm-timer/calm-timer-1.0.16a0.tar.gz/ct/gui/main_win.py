import os.path
import os
import logging

"""
try:
    # noinspection PyUnresolvedReferences
    from PyQt5 import QtMultimedia
except ImportError:
    logging.warning("ImportError for QtMultimedia (there may not be a sound card available)")

import playsound

"""
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import pydub.playback
import pydub
import ct.timer
import ct.ct_global

APPLICATION_TITLE_STR = "Calm Timer"


class AudioThread(QtCore.QThread):
    def __init__(self, i_parent, i_audio_filename: str):
        super().__init__(i_parent)
        self.audio_filename_str = i_audio_filename

    # overridden
    def run(self) -> None:
        abs_path_str = ct.ct_global.get_audio_path(self.audio_filename_str)
        if self.audio_filename_str.lower().endswith(ct.ct_global.WAV_SUFFIX_STR):
            audio_segment = pydub.AudioSegment.from_wav(abs_path_str)
        elif self.audio_filename_str.lower().endswith(ct.ct_global.OGG_SUFFIX_STR):
            audio_segment = pydub.AudioSegment.from_ogg(abs_path_str)
        else:
            raise Exception("Audio file not supported")
        pydub.playback.play(audio_segment)

    """
    playsound.playsound(i_audio_filename)

    if self.sound_effect is None:
        logging.warning("play_audio: sound_effect is None")
        return
    audio_path_str = ct.ct_global.get_audio_path(i_audio_filename)
    # noinspection PyCallByClass
    audio_source_qurl = QtCore.QUrl.fromLocalFile(audio_path_str)
    self.sound_effect.setSource(audio_source_qurl)
    self.sound_effect.setVolume(float(i_volume / 100))
    self.sound_effect.play()
    """


class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(40, 32, 1, 1)
        self.setWindowTitle(APPLICATION_TITLE_STR)
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.active_audio_file_name_str = ""

        self.audio_qaction_list = []

        # Widget setup
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        vbox_l2 = QtWidgets.QVBoxLayout()
        central_widget.setLayout(vbox_l2)

        upper_hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(upper_hbox_l3)

        selecting_vbox_l4 = QtWidgets.QVBoxLayout()
        upper_hbox_l3.addLayout(selecting_vbox_l4)

        hbox_l5 = QtWidgets.QHBoxLayout()
        selecting_vbox_l4.addLayout(hbox_l5)

        self.minutes_qll = QtWidgets.QLabel("Minutes: ")
        hbox_l5.addWidget(self.minutes_qll)

        self.minutes_qsb = QtWidgets.QSpinBox()
        self.minutes_qsb.valueChanged.connect(self.on_minutes_spin_changed)
        hbox_l5.addWidget(self.minutes_qsb)

        hbox_l5.addStretch(1)

        presets1to5_hbox_l5 = QtWidgets.QHBoxLayout()
        selecting_vbox_l4.addLayout(presets1to5_hbox_l5)
        presets6to10_hbox_l5 = QtWidgets.QHBoxLayout()
        selecting_vbox_l4.addLayout(presets6to10_hbox_l5)

        self.preset_widget_list = []
        self.preset_buttons_qbg = QtWidgets.QButtonGroup()
        self.preset_buttons_qbg.buttonClicked.connect(self.on_preset_button_clicked)

        for i in range(1, 11):
            x_qpb = QtWidgets.QPushButton(str(i))
            x_qpb.setFixedWidth(24)
            #x_qpb.clicked.connect(self.on_preset_button_clicked)
            self.preset_buttons_qbg.addButton(x_qpb, i)
            self.preset_widget_list.append(x_qpb)
            if i <= 5:
                presets1to5_hbox_l5.addWidget(x_qpb)
            else:
                presets6to10_hbox_l5.addWidget(x_qpb)

        ######presets1to5_hbox_l5.addStretch(1)

        self.time_left_qll = QtWidgets.QLabel("Secs")
        new_font = self.time_left_qll.font()
        new_font.setPointSize(72)
        self.time_left_qll.setFont(new_font)
        upper_hbox_l3.addWidget(self.time_left_qll)


        self.abs_time_qte = QtWidgets.QTimeEdit()
        self.abs_time_qte.setDisplayFormat("HH:mm")
        self.abs_time_qte.timeChanged.connect(self.on_abs_time_changed)
        selecting_vbox_l4.addWidget(self.abs_time_qte)


        controls_hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(controls_hbox_l3)

        """
        self.reset_qpb = QtWidgets.QPushButton("Reset")
        controls_hbox_l3.addWidget(self.reset_qpb)
        """

        self.stop_qpb = QtWidgets.QPushButton("Stop")
        self.stop_qpb.clicked.connect(self.on_stop_clicked)
        controls_hbox_l3.addWidget(self.stop_qpb)

        self.start_qpb = QtWidgets.QPushButton("Start")
        new_font = self.start_qpb.font()
        new_font.setBold(True)
        self.start_qpb.setFont(new_font)
        self.start_qpb.clicked.connect(self.on_start_clicked)
        controls_hbox_l3.addWidget(self.start_qpb)

        # Timer
        self.timer = ct.timer.Timer()
        self.timer.update_signal.connect(self.on_timer_update_signal_activated)

        # Audio
        """
        self.sound_effect = None
        try:
            self.sound_effect = QtMultimedia.QSoundEffect(self)
            # -a parent has to be given here
        except NameError:
            logging.warning("NameError: QtMultimedia has not been imported")
        except:
            logging.warning("Unknown error: QtMultimedia has not been imported")
        """

        # Creating the menu bar..
        self.menu_bar = self.menuBar()
        # ..file menu
        file_menu = self.menu_bar.addMenu("&File")
        exit_qaction = QtWidgets.QAction("Exit", self)
        exit_qaction.triggered.connect(self.close)
        file_menu.addAction(exit_qaction)
        # ..audio menu
        self.audio_group_qag = QtWidgets.QActionGroup(self)
        self.audio_group_qag.triggered.connect(self.audio_file_action_group_triggered)
        self.audio_menu = self.menu_bar.addMenu("&Audio")
        self.audio_menu.aboutToShow.connect(self.on_about_to_show_audio_menu)
        self.populate_audio_menu(ct.ct_global.DEFAULT_AUDIO_PATH_STR)

        # ..help menu
        help_menu = self.menu_bar.addMenu("&Help")
        about_qaction = QtWidgets.QAction("About", self)
        about_qaction.triggered.connect(self.show_about_box)
        help_menu.addAction(about_qaction)

        self.minutes_qsb.setValue(1)
        self.update_gui()
        self.show()

    def test_audio(self):
        self.play_audio(self.active_audio_file_name_str, 90)

    def play_audio(self, i_audio_filename: str, i_volume: int) -> None:
        thread = AudioThread(self, i_audio_filename)
        thread.start()

    def on_about_to_show_audio_menu(self):
        logging.debug("on_about_to_show_audio_menu")
        # self.populate_audio_menu()

    def populate_audio_menu(self, i_default_audio_file_name: str):
        # -for now this is only called from init
        """
        self.audio_qaction_list.clear()
        self.audio_menu.clear()
        self.audio_group_qag.
        """

        for file_name_str in os.listdir(ct.ct_global.get_audio_path()):
            is_wav_file_bool = file_name_str.lower().endswith(ct.ct_global.WAV_SUFFIX_STR.lower())
            is_ogg_file_bool = file_name_str.lower().endswith(ct.ct_global.OGG_SUFFIX_STR.lower())
            # os.path.isfile(file_name_str) and
            if is_wav_file_bool or is_ogg_file_bool:
                qaction = QtWidgets.QAction(file_name_str, self)
                ########qaction.triggered.connect(self.audio_file_action_triggered)
                qaction.setCheckable(True)
                #self.audio_qaction_list = qaction
                self.audio_qaction_list.append(qaction)
                self.audio_menu.addAction(qaction)
                self.audio_group_qag.addAction(qaction)
                if i_default_audio_file_name == qaction.text():
                    #####qaction.setChecked(True)
                    qaction.trigger()

        self.audio_menu.addSeparator()
        test_audio_qaction = QtWidgets.QAction("Test Audio", self)
        test_audio_qaction.triggered.connect(self.test_audio)
        self.audio_menu.addAction(test_audio_qaction)

    """
    def audio_file_action_triggered(self, i_checked: bool):
        logging.debug("audio_file_action_triggered")
    """

    def audio_file_action_group_triggered(self, i_action: QtWidgets.QAction):
        self.active_audio_file_name_str = i_action.text()
        logging.debug("audio_file_action_group_triggered: " + i_action.text())

    def show_about_box(self):
        message_box = QtWidgets.QMessageBox.about(
            self, "About " + "Calm Timer",
            (
                '<p>Concept and programming by Tord Dellsén (SunyataZero)'
                '<p>Software License: GPLv3</p>'
                '<p>Audio licenses: All are CC0 except for the following:</p>'
                '<ul>'
                '<li>110215__cheesepuff__a-soothing-song[CC0].wav - CC0 license</li>'
                '<li>332932__bbatv__gentle-glockenspiel.wav - created by <a href="https://freesound.org/people/bbatv/">bbatv</a> - licensed under <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0</a></li>'
                '<li>415328__eardeer__slumberfoam.wav - created by <a href="https://freesound.org/people/eardeer/">eardear</a> - licensed under <a href="https://creativecommons.org/licenses/by-nc/3.0/">CC BY-NC 3.0</a></li>'
                '</ul>'
                '<p>The phrase "Please smile, breathe and move slowly" has been inspired by the Thich Nhat Hanh quote "Smile, breathing and go slowly"</p>'
            )
        )
        # '<p>Photography (for icons) by Torgny Dellsén - '
        #                 '<a href="https://torgnydellsen.zenfolio.com/">torgnydellsen.zenfolio.com</a></p>'
        #                 '<p>Photo license: CC BY-SA 4.0</p>'
        #                 "<p>Art license: CC PD</p>"

    def on_minutes_spin_changed(self, i_new_value_mins: int):
        #new_value_mins_int = i_new_value_secs // 60
        formatted_time_str = self.get_formatted_time(i_new_value_mins*60)
        self.time_left_qll.setText(formatted_time_str)

    def on_abs_time_changed(self, i_qtime):
        logging.debug("on_abs_time_spin_changed")

    def on_stop_clicked(self):
        self.timer.stop()
        self.update_gui()

    def update_gui(self):
        is_timer_active_bool = self.timer.is_active()
        for preset_widget in self.preset_widget_list:
            preset_widget.setDisabled(is_timer_active_bool)
        self.minutes_qsb.setDisabled(is_timer_active_bool)
        self.stop_qpb.setEnabled(is_timer_active_bool)
        self.start_qpb.setDisabled(is_timer_active_bool)

    def on_start_clicked(self):
        countdown_time_seconds_int = self.minutes_qsb.value() * 60
        self.timer.start(countdown_time_seconds_int)
        self.update_gui()

    def on_preset_button_clicked(self, i_abstract_button):
        minutes_int = int(i_abstract_button.text())
        self.minutes_qsb.setValue(minutes_int)
        #####logging.debug("button with id " + str(minutes_int))

    def on_timer_update_signal_activated(self, i_completed: bool):
        if i_completed:
            self.setWindowTitle("Completed")
            self.play_audio(self.active_audio_file_name_str, 90)

            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle("Timer finished")
            msg_box.setText("<h3>Please smile, breathe and move slowly</h3>")
            # msg_box.setInformativeText("nowthere to go, nothing to do")
            msg_box.exec_()

            self.stop_audio()
            self.update_gui()

        time_remaining_str = self.get_formatted_time(self.timer.secs_remaining_int)
        self.time_left_qll.setText(time_remaining_str)
        self.setWindowTitle(APPLICATION_TITLE_STR + " " + time_remaining_str)

        """
        if is_timer_active_bool:
            time_remaining_str = self.get_formatted_time(self.timer.secs_remaining_int)
            self.setWindowTitle(APPLICATION_TITLE_STR + " " + time_remaining_str)
        """

    def get_formatted_time(self, i_total_secs: int):
        minutes_int = i_total_secs // 60
        seconds_remaining_int = i_total_secs % 60
        formatted_time_str = str(minutes_int) + ":" + str(seconds_remaining_int).zfill(2)
        return formatted_time_str

