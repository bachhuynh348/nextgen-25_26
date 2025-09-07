
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(QtCore.QRect(0, 0, 800, 600))
        MainWindow.setWindowTitle("Ứng dụng Nghe Nhạc")
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: #121212;\n"
"    color: #FFFFFF;\n"
"    font-family: Arial, sans-serif; /* Fallback font */\n"
"    font-size: 14px;\n"
"}\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    color: #FFFFFF;\n"
"    font-size: 24px;\n"
"/* For icons */\n"
"    min-width: 30px;\n"
"    min-height: 30px;\n"
"}\n"
"QPushButton:hover {\n"
"    opacity: 0.8;\n"
"}\n"
"QLabel {\n"
"    color: #FFFFFF;\n"
"}\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid #444;\n"
"    background: #282828;\n"
"    height: 8px;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background: #1DB954;\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 7px;\n"
"    margin: -3px 0;\n"
"}\n"
"QSlider::add-page:horizontal {\n"
"    background: #1DB954;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::sub-page:horizontal {\n"
"    background: #282828;\n"
"    border-radius: 4px;\n"
"}\n"
"QTabWidget::pane {\n"
"    border: 1px solid #333;\n"
"    background-color: #121212;\n"
"}\n"
"QTabWidget::tab-bar {\n"
"    left: 5px;\n"
"}\n"
"QTabBar::tab {\n"
"    background-color: #282828;\n"
"    color: #B3B3B3;\n"
"    padding: 8px 15px;\n"
"    border: 1px solid #333;\n"
"    border-bottom: none;\n"
"    border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"    margin-right: 2px;\n"
"}\n"
"QTabBar::tab:selected {\n"
"    background-color: #1DB954;\n"
"    color: #FFFFFF;\n"
"    font-weight: bold;\n"
"}\n"
"QListWidget {\n"
"    background-color: #121212;\n"
"    color: #FFFFFF;\n"
"    border: none;\n"
"}\n"
"QListWidget::item {\n"
"    padding: 8px 5px;\n"
"}\n"
"QListWidget::item:selected {\n"
"    background-color: #333;\n"
"}\n"
"QLineEdit {\n"
"    border: 1px solid #555;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"    background-color: #282828;\n"
"    color: #FFFFFF;\n"
"}\n"
"")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerFrame = QtWidgets.QFrame(self.centralWidget)
        self.headerFrame.setMinimumSize(QtCore.QSize(0, 50))
        self.headerFrame.setStyleSheet("QFrame#headerFrame {\n"
"    background-color: #1a1a1a;\n"
"    border-bottom: 1px solid #333;\n"
"    padding: 5px;\n"
"}")
        self.headerFrame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.headerFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.headerFrame.setObjectName("headerFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.headerFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.menuButton = QtWidgets.QPushButton(self.headerFrame)
        self.menuButton.setObjectName("menuButton")
        self.horizontalLayout_2.addWidget(self.menuButton)
        self.horizontalSpacer_3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)
        self.searchLineEdit = QtWidgets.QLineEdit(self.headerFrame)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.horizontalLayout_2.addWidget(self.searchLineEdit)
        self.horizontalSpacer_4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)
        self.searchButton = QtWidgets.QPushButton(self.headerFrame)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_2.addWidget(self.searchButton)
        self.verticalLayout.addWidget(self.headerFrame)
        self.mainTabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.mainTabWidget.setCurrentIndex(0)
        self.mainTabWidget.setObjectName("mainTabWidget")
        self.songsTab = QtWidgets.QWidget()
        self.songsTab.setObjectName("songsTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.songsTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.songsListWidget = QtWidgets.QListWidget(self.songsTab)
        self.songsListWidget.setObjectName("songsListWidget")
        item = QtWidgets.QListWidgetItem()
        self.songsListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.songsListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.songsListWidget.addItem(item)
        self.verticalLayout_2.addWidget(self.songsListWidget)
        self.mainTabWidget.addTab(self.songsTab, "")
        self.playlistsTab = QtWidgets.QWidget()
        self.playlistsTab.setObjectName("playlistsTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.playlistsTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.newPlaylistButton = QtWidgets.QPushButton(self.playlistsTab)
        self.newPlaylistButton.setStyleSheet("QPushButton#newPlaylistButton {\n"
"    background-color: #1DB954;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"}")
        self.newPlaylistButton.setObjectName("newPlaylistButton")
        self.verticalLayout_3.addWidget(self.newPlaylistButton)
        self.playlistsListWidget = QtWidgets.QListWidget(self.playlistsTab)
        self.playlistsListWidget.setObjectName("playlistsListWidget")
        item = QtWidgets.QListWidgetItem()
        self.playlistsListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.playlistsListWidget.addItem(item)
        self.verticalLayout_3.addWidget(self.playlistsListWidget)
        self.mainTabWidget.addTab(self.playlistsTab, "")
        self.verticalLayout.addWidget(self.mainTabWidget)
        self.playerFrame = QtWidgets.QFrame(self.centralWidget)
        self.playerFrame.setMinimumSize(QtCore.QSize(0, 80))
        self.playerFrame.setStyleSheet("QFrame#playerFrame {\n"
"    background-color: #1a1a1a;\n"
"    border-top: 1px solid #333;\n"
"    padding: 5px;\n"
"}")
        self.playerFrame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.playerFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.playerFrame.setObjectName("playerFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.playerFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.albumArtLabel = QtWidgets.QLabel(self.playerFrame)
        self.albumArtLabel.setMinimumSize(QtCore.QSize(60, 60))
        self.albumArtLabel.setMaximumSize(QtCore.QSize(60, 60))
        self.albumArtLabel.setStyleSheet("background-color: #333;\n"
"border-radius: 5px;")
        self.albumArtLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.albumArtLabel.setObjectName("albumArtLabel")
        self.horizontalLayout.addWidget(self.albumArtLabel)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.songTitleLabel = QtWidgets.QLabel(self.playerFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.songTitleLabel.setFont(font)
        self.songTitleLabel.setObjectName("songTitleLabel")
        self.verticalLayout_4.addWidget(self.songTitleLabel)
        self.artistNameLabel = QtWidgets.QLabel(self.playerFrame)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.artistNameLabel.setFont(font)
        self.artistNameLabel.setObjectName("artistNameLabel")
        self.verticalLayout_4.addWidget(self.artistNameLabel)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.horizontalSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.currentTimeLabel = QtWidgets.QLabel(self.playerFrame)
        self.currentTimeLabel.setObjectName("currentTimeLabel")
        self.horizontalLayout_3.addWidget(self.currentTimeLabel)
        self.progressBar = QtWidgets.QSlider(self.playerFrame)
        self.progressBar.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.totalTimeLabel = QtWidgets.QLabel(self.playerFrame)
        self.totalTimeLabel.setObjectName("totalTimeLabel")
        self.horizontalLayout_3.addWidget(self.totalTimeLabel)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.shuffleButton = QtWidgets.QPushButton(self.playerFrame)
        self.shuffleButton.setObjectName("shuffleButton")
        self.horizontalLayout_4.addWidget(self.shuffleButton)
        self.previousButton = QtWidgets.QPushButton(self.playerFrame)
        self.previousButton.setObjectName("previousButton")
        self.horizontalLayout_4.addWidget(self.previousButton)
        self.playPauseButton = QtWidgets.QPushButton(self.playerFrame)
        self.playPauseButton.setMinimumSize(QtCore.QSize(30, 30))
        self.playPauseButton.setMaximumSize(QtCore.QSize(40, 40))
        self.playPauseButton.setStyleSheet("QPushButton#playPauseButton {\n"
"    background-color: #1DB954;\n"
"    border-radius: 20px;\n"
"    padding: 0;\n"
"}\n"
"QPushButton#playPauseButton:hover {\n"
"    background-color: #1ED760;\n"
"}")
        self.playPauseButton.setObjectName("playPauseButton")
        self.horizontalLayout_4.addWidget(self.playPauseButton)
        self.nextButton = QtWidgets.QPushButton(self.playerFrame)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout_4.addWidget(self.nextButton)
        self.repeatButton = QtWidgets.QPushButton(self.playerFrame)
        self.repeatButton.setObjectName("repeatButton")
        self.horizontalLayout_4.addWidget(self.repeatButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.horizontalSpacer_2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer_2)
        self.verticalLayout.addWidget(self.playerFrame)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.mainTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.menuButton.setText(_translate("MainWindow", "☰"))
        self.searchLineEdit.setPlaceholderText(_translate("MainWindow", "Tìm kiếm bài hát, nghệ sĩ..."))
        self.searchButton.setText(_translate("MainWindow", "🔍"))
        __sortingEnabled = self.songsListWidget.isSortingEnabled()
        self.songsListWidget.setSortingEnabled(False)
        item = self.songsListWidget.item(0)
        item.setText(_translate("MainWindow", "Bài hát mẫu 1 - Nghệ sĩ A"))
        item = self.songsListWidget.item(1)
        item.setText(_translate("MainWindow", "Bài hát mẫu 2 - Nghệ sĩ B"))
        item = self.songsListWidget.item(2)
        item.setText(_translate("MainWindow", "Bài hát mẫu 3 - Nghệ sĩ C"))
        self.songsListWidget.setSortingEnabled(__sortingEnabled)
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.songsTab), _translate("MainWindow", "Bài hát"))
        self.newPlaylistButton.setText(_translate("MainWindow", "+ Tạo Playlist Mới"))
        __sortingEnabled = self.playlistsListWidget.isSortingEnabled()
        self.playlistsListWidget.setSortingEnabled(False)
        item = self.playlistsListWidget.item(0)
        item.setText(_translate("MainWindow", "Playlist của tôi 1 (5 bài)"))
        item = self.playlistsListWidget.item(1)
        item.setText(_translate("MainWindow", "Playlist yêu thích (12 bài)"))
        self.playlistsListWidget.setSortingEnabled(__sortingEnabled)
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.playlistsTab), _translate("MainWindow", "Playlist"))
        self.albumArtLabel.setText(_translate("MainWindow", "Ảnh bìa"))
        self.songTitleLabel.setText(_translate("MainWindow", "Tên bài hát đang phát"))
        self.artistNameLabel.setText(_translate("MainWindow", "Tên nghệ sĩ"))
        self.currentTimeLabel.setText(_translate("MainWindow", "0:00"))
        self.totalTimeLabel.setText(_translate("MainWindow", "3:30"))
        self.shuffleButton.setText(_translate("MainWindow", "🔀"))
        self.previousButton.setText(_translate("MainWindow", "⏮️"))
        self.playPauseButton.setText(_translate("MainWindow", "▶️"))
        self.nextButton.setText(_translate("MainWindow", "⏭️"))
        self.repeatButton.setText(_translate("MainWindow", "🔁"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())