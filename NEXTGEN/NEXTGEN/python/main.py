# -*- coding: utf-8 -*-
import sys
import hashlib
import os
import random

# Sử dụng PyQt6 cho giao diện
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt6 import uic
from PyQt6.QtCore import QTimer

# Sử dụng pygame cho âm thanh (ổn định hơn)
import pygame
from pygame import mixer

# --- CÁC ĐƯỜNG DẪN VÀ HẰNG SỐ ---
# Lấy đường dẫn tới thư mục chứa file main.py để các file khác có thể được tìm thấy
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE_PATH = os.path.join(BASE_DIR, "users.txt")
LOGIN_UI_PATH = os.path.join(BASE_DIR, "login_ui_fixed.ui")
REGISTER_UI_PATH = os.path.join(BASE_DIR, "register_ui_fixed.ui")
MUSIC_PLAYER_UI_PATH = os.path.join(BASE_DIR, "music_player_ui.ui")
# Các định dạng file nhạc mà pygame hỗ trợ tốt
SUPPORTED_FORMATS = "Audio Files (*.mp3 *.wav *.ogg)"

# --- CÁC LỚP ỨNG DỤNG ---

def ensure_users_file_exists():
    """Hàm này đảm bảo tệp users.txt luôn tồn tại."""
    if not os.path.exists(USERS_FILE_PATH):
        try:
            # Tạo một file trống nếu nó chưa có
            with open(USERS_FILE_PATH, 'w', encoding='utf-8') as f:
                pass
        except IOError as e:
            QMessageBox.critical(None, "Lỗi Tệp", f"Không thể tạo tệp người dùng: {e}")
            sys.exit(1)

class LoginWindow(QMainWindow):
    """Lớp xử lý cửa sổ Đăng nhập."""
    def __init__(self, controller):
        super().__init__()
        # Tải giao diện từ tệp login_ui_fixed.ui
        uic.loadUi(LOGIN_UI_PATH, self)
        self.controller = controller

        # Kết nối các nút bấm với hàm xử lý tương ứng
        self.btn_login.clicked.connect(self.handle_login)
        self.btn_register_link.clicked.connect(self.controller.show_register)

    def handle_login(self):
        """Xử lý logic khi người dùng nhấn nút Đăng nhập."""
        username = self.input_username.text()
        password = self.input_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ tên người dùng và mật khẩu.")
            return

        # Băm mật khẩu người dùng nhập để so sánh với mật khẩu đã lưu
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        try:
            with open(USERS_FILE_PATH, "r", encoding='utf-8') as f:
                for line in f:
                    # Tách tên người dùng và mật khẩu đã băm từ mỗi dòng
                    stored_username, stored_password_hash = line.strip().split(',', 1)
                    if username == stored_username and hashed_password == stored_password_hash:
                        # Nếu khớp, chuyển sang cửa sổ nghe nhạc
                        self.controller.show_music_player()
                        return
            
            # Nếu không tìm thấy thông tin nào khớp sau khi duyệt hết file
            QMessageBox.warning(self, "Lỗi Đăng Nhập", "Tên người dùng hoặc mật khẩu không đúng.")
        except (FileNotFoundError, ValueError):
            QMessageBox.warning(self, "Lỗi", "Tệp người dùng bị lỗi hoặc không tồn tại. Vui lòng đăng ký.")


class RegisterWindow(QMainWindow):
    """Lớp xử lý cửa sổ Đăng ký."""
    def __init__(self, controller):
        super().__init__()
        # Tải giao diện từ tệp register_ui_fixed.ui
        uic.loadUi(REGISTER_UI_PATH, self)
        self.controller = controller

        # Kết nối các nút bấm
        self.btn_register.clicked.connect(self.handle_register)
        self.btn_login_link.clicked.connect(self.controller.show_login)

    def handle_register(self):
        """Xử lý logic khi người dùng nhấn nút Đăng ký."""
        username = self.input_username.text()
        password = self.input_password.text()
        confirm_password = self.input_confirm_password.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Lỗi Đăng Ký", "Vui lòng điền đầy đủ thông tin.")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Lỗi Đăng Ký", "Mật khẩu xác nhận không khớp.")
            return

        # Kiểm tra xem tên người dùng đã tồn tại chưa
        try:
            with open(USERS_FILE_PATH, "r", encoding='utf-8') as f:
                for line in f:
                    if line.strip().split(',')[0] == username:
                        QMessageBox.warning(self, "Lỗi Đăng Ký", "Tên người dùng này đã tồn tại.")
                        return
        except (FileNotFoundError, ValueError):
            # Bỏ qua nếu file chưa tồn tại hoặc trống
            pass

        # Băm mật khẩu trước khi lưu
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        # Lưu thông tin người dùng mới vào file
        try:
            with open(USERS_FILE_PATH, "a", encoding='utf-8') as f:
                f.write(f"{username},{password_hash}\n")
            
            QMessageBox.information(self, "Thành Công", "Tài khoản đã được tạo! Vui lòng đăng nhập.")
            self.controller.show_login()
        except IOError as e:
            QMessageBox.critical(self, "Lỗi Tệp", f"Không thể ghi vào tệp người dùng: {e}")


class MusicPlayerWindow(QMainWindow):
    """Lớp cửa sổ nghe nhạc chính, sử dụng Pygame để phát nhạc."""
    def __init__(self):
        super().__init__()
        # Tải giao diện từ tệp music_player_ui.ui
        uic.loadUi(MUSIC_PLAYER_UI_PATH, self)

        # Khởi tạo pygame và engine âm thanh (mixer)
        pygame.init()
        mixer.init()

        # Các biến để quản lý trạng thái của trình phát nhạc
        self.playlist = []
        self.current_index = -1
        self.is_playing = False
        self.is_paused = False
        self.is_shuffled = False
        self.shuffled_indices = []
        self.repeat_mode = 0  # 0: Không lặp, 1: Lặp 1 bài, 2: Lặp tất cả

        # Timer để cập nhật thanh tiến trình bài hát một cách đều đặn
        self.progress_timer = QTimer(self)
        self.progress_timer.setInterval(500) # Cập nhật mỗi nửa giây
        self.progress_timer.timeout.connect(self.update_progress)

        self.setup_ui_improvements()
        self.connect_signals()

    def setup_ui_improvements(self):
        """Thay đổi một vài chi tiết trên giao diện để thân thiện hơn."""
        self.menuButton.setText("➕ Thêm Nhạc")
        self.menuButton.setStyleSheet("padding: 5px; font-size: 14px;")
        # Xóa các bài hát mẫu có sẵn trong giao diện
        self.songsListWidget.clear()

    def connect_signals(self):
        """Kết nối tất cả các nút bấm trên giao diện với các hàm xử lý."""
        self.playPauseButton.clicked.connect(self.toggle_play_pause)
        self.nextButton.clicked.connect(self.play_next)
        self.previousButton.clicked.connect(self.play_previous)
        self.shuffleButton.clicked.connect(self.toggle_shuffle)
        self.repeatButton.clicked.connect(self.toggle_repeat)
        self.menuButton.clicked.connect(self.add_media)
        self.songsListWidget.itemDoubleClicked.connect(self.play_from_list)
        self.progressBar.sliderMoved.connect(self.set_position)

    def add_media(self):
        """Mở cửa sổ để người dùng chọn các file nhạc."""
        files, _ = QFileDialog.getOpenFileNames(self, "Chọn bài hát", "", SUPPORTED_FORMATS)
        if files:
            for file_path in files:
                song_title = os.path.basename(file_path)
                self.playlist.append({'title': song_title, 'path': file_path})
            self.update_playlist_ui()

    def update_playlist_ui(self):
        """Cập nhật danh sách bài hát trên giao diện."""
        self.songsListWidget.clear()
        for song in self.playlist:
            self.songsListWidget.addItem(song['title'])
        self.toggle_shuffle(force_update=True) # Cập nhật lại thứ tự ngẫu nhiên nếu cần

    def play_from_list(self, item):
        """Phát nhạc khi người dùng nháy đúp chuột vào một bài hát."""
        self.current_index = self.songsListWidget.row(item)
        self.load_and_play()

    def load_and_play(self):
        """Tải và phát bài hát được chọn bằng pygame.mixer."""
        if self.current_index == -1 or not self.playlist:
            return

        song = self.playlist[self.current_index]
        mixer.music.load(song['path'])
        mixer.music.play()

        # Cập nhật trạng thái và giao diện
        self.is_playing = True
        self.is_paused = False
        self.progress_timer.start()
        self.songTitleLabel.setText(song['title'])
        self.songsListWidget.setCurrentRow(self.current_index)
        self.playPauseButton.setText("⏸️")
        
        # Lấy và hiển thị tổng thời gian của bài hát
        try:
            song_obj = pygame.mixer.Sound(song['path'])
            duration_ms = song_obj.get_length() * 1000
            self.progressBar.setRange(0, int(duration_ms))
            self.totalTimeLabel.setText(self.format_time(duration_ms))
        except Exception as e:
            print(f"Lỗi khi lấy thời lượng bài hát: {e}")

    def toggle_play_pause(self):
        """Xử lý nút Phát/Tạm dừng."""
        if not self.playlist: return

        if self.is_playing:
            if self.is_paused:
                mixer.music.unpause()
                self.playPauseButton.setText("⏸️")
                self.is_paused = False
            else:
                mixer.music.pause()
                self.playPauseButton.setText("▶️")
                self.is_paused = True
        else:
            if self.current_index == -1: self.current_index = 0
            self.load_and_play()

    def play_next(self):
        """Phát bài hát tiếp theo trong danh sách."""
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
        """Bật/tắt chế độ phát ngẫu nhiên."""
        if not force_update: self.is_shuffled = not self.is_shuffled
        
        if self.is_shuffled:
            self.shuffled_indices = list(range(len(self.playlist)))
            random.shuffle(self.shuffled_indices)
            self.shuffleButton.setStyleSheet("color: #1DB954;") # Đổi màu để báo hiệu
        else:
            self.shuffleButton.setStyleSheet("color: white;")

    def toggle_repeat(self):
        """Chuyển đổi giữa các chế độ lặp lại."""
        self.repeat_mode = (self.repeat_mode + 1) % 3
        if self.repeat_mode == 0:
            self.repeatButton.setText("🔁"); self.repeatButton.setStyleSheet("color: white;")
        elif self.repeat_mode == 1:
            self.repeatButton.setText("🔂"); self.repeatButton.setStyleSheet("color: #1DB954;")
        else:
            self.repeatButton.setText("🔁"); self.repeatButton.setStyleSheet("color: #1DB954;")

    def update_progress(self):
        """Cập nhật thanh tiến trình và tự động chuyển bài khi hết."""
        if mixer.music.get_busy():
            current_pos_ms = mixer.music.get_pos()
            self.progressBar.setValue(current_pos_ms)
            self.currentTimeLabel.setText(self.format_time(current_pos_ms))
        elif self.is_playing and not self.is_paused:
            self.progress_timer.stop()
            self.handle_media_end()

    def handle_media_end(self):
        """Xử lý khi bài hát kết thúc."""
        self.is_playing = False
        self.is_paused = False
        if self.repeat_mode == 1: # Lặp lại 1 bài
            self.load_and_play()
        else: # Các trường hợp khác
            is_last_song = self.current_index == len(self.playlist) - 1
            if not self.is_shuffled and is_last_song and self.repeat_mode == 0:
                self.playPauseButton.setText("▶️") # Dừng lại nếu là bài cuối và không lặp
                return
            self.play_next()

    def set_position(self, position):
        """Tua nhạc đến vị trí được chọn trên thanh tiến trình."""
        if self.is_playing:
            mixer.music.play(start=position / 1000)

    def format_time(self, ms):
        """Chuyển đổi mili giây sang định dạng MM:SS."""
        s = round(ms / 1000)
        m, s = divmod(s, 60)
        return f"{m:02d}:{s:02d}"

    def closeEvent(self, event):
        """Hàm này được gọi khi người dùng đóng cửa sổ."""
        pygame.quit() # Tắt pygame để giải phóng tài nguyên
        event.accept()

class Controller:
    """Lớp trung tâm điều khiển việc hiển thị các cửa sổ."""
    def __init__(self):
        self.login_window = LoginWindow(self)
        self.register_window = RegisterWindow(self)
        self.music_player_window = None

    def show_login(self):
        """Hiển thị cửa sổ đăng nhập và ẩn các cửa sổ khác."""
        if self.music_player_window:
            mixer.music.stop() # Dừng nhạc khi đăng xuất
            self.music_player_window.hide()
        self.register_window.hide()
        self.login_window.show()

    def show_register(self):
        """Hiển thị cửa sổ đăng ký."""
        self.login_window.hide()
        self.register_window.show()

    def show_music_player(self):
        """Hiển thị cửa sổ nghe nhạc."""
        self.login_window.hide()
        if not self.music_player_window:
            self.music_player_window = MusicPlayerWindow()
        self.music_player_window.show()

# --- Điểm Bắt Đầu Chạy Ứng Dụng ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ensure_users_file_exists()
    controller = Controller()
    controller.show_login() # Hiển thị cửa sổ đăng nhập đầu tiên
    sys.exit(app.exec())