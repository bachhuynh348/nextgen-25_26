# -*- coding: utf-8 -*-
import sys
import hashlib
import os
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt6 import uic
from PyQt6.QtCore import QTimer

# Bước 1: Import pygame và mixer
import pygame
from pygame import mixer

# --- CÁC ĐƯỜNG DẪN VÀ HẰNG SỐ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE_PATH = os.path.join(BASE_DIR, "users.txt")
LOGIN_UI_PATH = os.path.join(BASE_DIR, "login_ui_fixed.ui")
REGISTER_UI_PATH = os.path.join(BASE_DIR, "register_ui_fixed.ui")
MUSIC_PLAYER_UI_PATH = os.path.join(BASE_DIR, "music_player_ui.ui")
SUPPORTED_FORMATS = "Audio Files (*.mp3 *.wav *.ogg)" # Pygame hỗ trợ tốt nhất các định dạng này

# --- CÁC LỚP GIAO DIỆN VÀ LOGIC ---

def ensure_users_file_exists():
    """Tạo tệp users.txt nếu nó không tồn tại."""
    if not os.path.exists(USERS_FILE_PATH):
        try:
            with open(USERS_FILE_PATH, 'w', encoding='utf-8') as f:
                pass
        except IOError as e:
            QMessageBox.critical(None, "Lỗi Tệp", f"Không thể tạo tệp người dùng: {e}")
            sys.exit(1)

class LoginWindow(QMainWindow):
    """Lớp xử lý cửa sổ Đăng nhập."""
    def __init__(self, controller):
        super().__init__()
        uic.loadUi(LOGIN_UI_PATH, self)
        self.controller = controller
        self.btn_login.clicked.connect(self.handle_login)
        self.btn_register_link.clicked.connect(self.controller.show_register)

    def handle_login(self):
        username = self.input_username.text()
        password = self.input_password.text()
        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        try:
            with open(USERS_FILE_PATH, "r", encoding='utf-8') as f:
                for line in f:
                    stripped_line = line.strip()
                    if not stripped_line: continue
                    try:
                        stored_username, stored_password_hash = stripped_line.split(',', 1)
                        if username == stored_username and hashed_password == stored_password_hash:
                            self.controller.show_music_player()
                            return
                    except ValueError:
                        continue
            QMessageBox.warning(self, "Lỗi Đăng Nhập", "Tên người dùng hoặc mật khẩu không đúng.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Lỗi", "Tệp người dùng không tồn tại. Vui lòng đăng ký trước.")

class RegisterWindow(QMainWindow):
    """Lớp xử lý cửa sổ Đăng ký."""
    def __init__(self, controller):
        super().__init__()
        uic.loadUi(REGISTER_UI_PATH, self)
        self.controller = controller
        self.btn_register.clicked.connect(self.handle_register)
        self.btn_login_link.clicked.connect(self.controller.show_login)

    def handle_register(self):
        username = self.input_username.text()
        password = self.input_password.text()
        confirm_password = self.input_confirm_password.text()
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Lỗi Đăng Ký", "Vui lòng điền đầy đủ thông tin.")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Lỗi Đăng Ký", "Mật khẩu xác nhận không khớp.")
            return
        try:
            with open(USERS_FILE_PATH, "r", encoding='utf-8') as f:
                for line in f:
                    stripped_line = line.strip()
                    if stripped_line and stripped_line.split(',')[0] == username:
                        QMessageBox.warning(self, "Lỗi Đăng Ký", "Tên người dùng này đã tồn tại.")
                        return
        except FileNotFoundError:
            pass
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        try:
            with open(USERS_FILE_PATH, "a", encoding='utf-8') as f:
                f.write(f"{username},{password_hash}\n")
            QMessageBox.information(self, "Thành Công", "Tài khoản đã được tạo thành công! Vui lòng đăng nhập.")
            self.controller.show_login()
        except IOError as e:
            QMessageBox.critical(self, "Lỗi Tệp", f"Không thể ghi vào tệp người dùng: {e}")

class MusicPlayerWindow(QMainWindow):
    """Lớp cửa sổ nghe nhạc sử dụng Pygame."""
    def __init__(self):
        super().__init__()
        uic.loadUi(MUSIC_PLAYER_UI_PATH, self)

        # Bước 2: Khởi tạo pygame và mixer
        pygame.init()
        mixer.init()

        # --- Các thuộc tính trạng thái ---
        self.playlist = []
        self.current_index = -1
        self.is_playing = False
        self.is_paused = False
        self.is_shuffled = False
        self.shuffled_indices = []
        self.repeat_mode = 0  # 0: No Repeat, 1: Repeat One, 2: Repeat All

        # --- Timer để cập nhật thanh tiến trình ---
        self.progress_timer = QTimer(self)
        self.progress_timer.setInterval(500) # Cập nhật mỗi 500ms
        self.progress_timer.timeout.connect(self.update_progress)

        self.setup_ui_improvements()
        self.connect_signals()

    def setup_ui_improvements(self):
        """Cải tiến giao diện người dùng."""
        self.menuButton.setText("➕ Thêm Nhạc")
        self.menuButton.setStyleSheet("padding: 5px; font-size: 14px;")
        self.songsListWidget.clear()

    def connect_signals(self):
        """Kết nối các tín hiệu (signals) với các khe (slots)."""
        self.playPauseButton.clicked.connect(self.toggle_play_pause)
        self.nextButton.clicked.connect(self.play_next)
        self.previousButton.clicked.connect(self.play_previous)
        self.shuffleButton.clicked.connect(self.toggle_shuffle)
        self.repeatButton.clicked.connect(self.toggle_repeat)
        self.menuButton.clicked.connect(self.add_media)
        self.songsListWidget.itemDoubleClicked.connect(self.play_from_list)
        self.progressBar.sliderMoved.connect(self.set_position)

    def add_media(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Chọn bài hát", "", SUPPORTED_FORMATS)
        if files:
            for file_path in files:
                song_title = os.path.basename(file_path)
                self.playlist.append({'title': song_title, 'path': file_path})
            self.update_playlist_ui()

    def update_playlist_ui(self):
        self.songsListWidget.clear()
        for song in self.playlist:
            self.songsListWidget.addItem(song['title'])
        self.toggle_shuffle(force_update=True)

    def play_from_list(self, item):
        self.current_index = self.songsListWidget.row(item)
        self.load_and_play()

    def load_and_play(self):
        """Tải và phát bài hát bằng pygame.mixer."""
        if self.current_index == -1 or not self.playlist:
            return

        song = self.playlist[self.current_index]
        mixer.music.load(song['path'])
        mixer.music.play()

        self.is_playing = True
        self.is_paused = False
        self.progress_timer.start()

        self.songTitleLabel.setText(song['title'])
        self.artistNameLabel.setText("Nghệ sĩ chưa xác định")
        self.songsListWidget.setCurrentRow(self.current_index)
        self.playPauseButton.setText("⏸️")

        # Cập nhật thời lượng (ước tính)
        try:
            song_obj = pygame.mixer.Sound(song['path'])
            duration_ms = song_obj.get_length() * 1000
            self.progressBar.setRange(0, int(duration_ms))
            self.totalTimeLabel.setText(self.format_time(duration_ms))
        except Exception as e:
            print(f"Không thể lấy thời lượng bài hát: {e}")
            self.progressBar.setRange(0, 0)
            self.totalTimeLabel.setText("00:00")


    def toggle_play_pause(self):
        """Chuyển đổi giữa phát, tạm dừng và tiếp tục."""
        if not self.playlist: return

        if self.is_playing:
            if self.is_paused: # Đang tạm dừng -> tiếp tục
                mixer.music.unpause()
                self.playPauseButton.setText("⏸️")
                self.progress_timer.start()
                self.is_paused = False
            else: # Đang phát -> tạm dừng
                mixer.music.pause()
                self.playPauseButton.setText("▶️")
                self.progress_timer.stop()
                self.is_paused = True
        else: # Chưa phát gì -> phát từ đầu
            if self.current_index == -1: self.current_index = 0
            self.load_and_play()

    def play_next(self):
        """Phát bài hát tiếp theo."""
        if not self.playlist: return

        if self.is_shuffled:
            current_shuffle_pos = self.shuffled_indices.index(self.current_index)
            next_shuffle_pos = (current_shuffle_pos + 1) % len(self.shuffled_indices)
            self.current_index = self.shuffled_indices[next_shuffle_pos]
        else:
            self.current_index = (self.current_index + 1) % len(self.playlist)
        self.load_and_play()

    def play_previous(self):
        """Phát bài hát trước đó."""
        if not self.playlist: return

        if self.is_shuffled:
            current_shuffle_pos = self.shuffled_indices.index(self.current_index)
            prev_shuffle_pos = (current_shuffle_pos - 1 + len(self.shuffled_indices)) % len(self.shuffled_indices)
            self.current_index = self.shuffled_indices[prev_shuffle_pos]
        else:
            self.current_index = (self.current_index - 1 + len(self.playlist)) % len(self.playlist)
        self.load_and_play()

    def toggle_shuffle(self, force_update=False):
        if not force_update: self.is_shuffled = not self.is_shuffled
        if self.is_shuffled:
            self.shuffled_indices = list(range(len(self.playlist)))
            random.shuffle(self.shuffled_indices)
            self.shuffleButton.setStyleSheet("color: #1DB954;")
        else:
            self.shuffleButton.setStyleSheet("color: white;")

    def toggle_repeat(self):
        self.repeat_mode = (self.repeat_mode + 1) % 3
        if self.repeat_mode == 0:
            self.repeatButton.setText("🔁"); self.repeatButton.setStyleSheet("color: white;")
        elif self.repeat_mode == 1:
            self.repeatButton.setText("🔂"); self.repeatButton.setStyleSheet("color: #1DB954;")
        else:
            self.repeatButton.setText("🔁"); self.repeatButton.setStyleSheet("color: #1DB954;")

    def update_progress(self):
        """Cập nhật thanh tiến trình và kiểm tra xem bài hát đã kết thúc chưa."""
        if mixer.music.get_busy(): # Nếu nhạc đang phát
            current_pos_ms = mixer.music.get_pos()
            self.progressBar.setValue(current_pos_ms)
            self.currentTimeLabel.setText(self.format_time(current_pos_ms))
        else: # Nhạc đã dừng
            self.progress_timer.stop()
            if self.is_playing and not self.is_paused: # Nếu nó dừng tự nhiên (hết bài)
                self.handle_media_end()

    def handle_media_end(self):
        """Xử lý khi bài hát kết thúc."""
        self.is_playing = False
        self.is_paused = False
        if self.repeat_mode == 1:
            self.load_and_play()
        else:
            is_last_song = self.current_index == len(self.playlist) - 1
            if not self.is_shuffled and is_last_song and self.repeat_mode == 0:
                self.playPauseButton.setText("▶️")
                self.progressBar.setValue(0)
                self.currentTimeLabel.setText("00:00")
                return
            self.play_next()

    def set_position(self, position):
        """Di chuyển đến vị trí cụ thể trong bài hát (tính bằng giây)."""
        # Dừng bài hát tạm thời để không bị gián đoạn khi tua
        self.progress_timer.stop()
        mixer.music.play(start=position / 1000)
        # Bắt đầu lại timer sau khi tua
        self.progress_timer.start()

    def format_time(self, ms):
        s = round(ms / 1000)
        m, s = divmod(s, 60)
        return f"{m:02d}:{s:02d}"

    def closeEvent(self, event):
        """Đảm bảo pygame được tắt khi đóng cửa sổ."""
        pygame.quit()
        event.accept()

class Controller:
    """Lớp điều khiển việc hiển thị các cửa sổ."""
    def __init__(self):
        self.login_window = LoginWindow(self)
        self.register_window = RegisterWindow(self)
        self.music_player_window = None

    def show_login(self):
        if self.music_player_window:
            mixer.music.stop()
            self.music_player_window.hide()
        self.register_window.hide()
        self.login_window.show()

    def show_register(self):
        self.login_window.hide()
        self.register_window.show()

    def show_music_player(self):
        self.login_window.hide()
        if not self.music_player_window:
            self.music_player_window = MusicPlayerWindow()
        self.music_player_window.show()

# --- Điểm khởi chạy ứng dụng ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ensure_users_file_exists()
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec())