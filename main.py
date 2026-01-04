import sys
import os
import io
import json
import base64

import requests
import pytesseract
from PIL import Image

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QComboBox,
    QSystemTrayIcon,
    QStyle,
    QMenu,
    QAction,
    QDialog,
    QLineEdit,
    QFormLayout,
    QDialogButtonBox,
)
from PyQt5.QtCore import (
    Qt,
    QRect,
    pyqtSignal,
    QObject,
    QBuffer,
    QIODevice,
    QThread,
    QTimer,
)
from PyQt5.QtGui import (
    QPainter,
    QPen,
    QColor,
    QPalette,
    QFont,
    QFontDatabase,
    QIcon,
    QPixmap,
)

import keyboard  # 全局快捷键


# ================== 图标 Base64（你自己填） ==================
# 可以填：
# - 纯 base64： "iVBORw0KGgoAAAANSUhEUgA..."
# - 或带前缀： "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA..."
ICON_BASE64 = "data:image/png;base64,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"  # TODO: 在这里粘你的 base64 字符串


def icon_from_base64(b64: str) -> QIcon:
    """从 base64 字符串创建 QIcon，如果为空则返回空图标。"""
    try:
        if not b64:
            return QIcon()
        if b64.startswith("data:image"):
            b64 = b64.split(",", 1)[1]
        data = base64.b64decode(b64)
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        return QIcon(pixmap)
    except Exception as e:
        print("解析 ICON_BASE64 失败：", e)
        return QIcon()


# ================== 配置读写 ==================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

DEFAULT_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEFAULT_MODEL = "deepseek-chat"

DEFAULT_CONFIG = {
    "api_key": "",
    "api_url": DEFAULT_API_URL,
    "model": DEFAULT_MODEL,
    "hotkey": "ctrl+d",  # 默认截屏快捷键
}


def load_config():
    cfg = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                for k in cfg.keys():
                    if k in data:
                        cfg[k] = data[k]
        except Exception as e:
            print("加载配置失败:", e)
    return cfg


def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("保存配置失败:", e)


# ================== DeepSeek 调用 ==================


def translate_with_deepseek(text: str, config: dict, mode: str = "to_zh") -> str:
    api_key = (config.get("api_key") or "").strip()
    api_url = (config.get("api_url") or DEFAULT_API_URL).strip()
    model = (config.get("model") or DEFAULT_MODEL).strip()

    if not api_key:
        raise RuntimeError("未设置 API Key，请在右上角 [设置] 中填写。")

    text = text.strip()
    if not text:
        return ""

    if mode == "to_zh":
        system_prompt = (
            "You are a translation engine. "
            "Translate the user content into Simplified Chinese. "
            "Output only the translated text, without explanations."
        )
    else:
        system_prompt = (
            "You are a translation engine. "
            "Translate the user content into natural English. "
            "Output only the translated text, without explanations."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "stream": False,
    }

    resp = requests.post(
        api_url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    if not resp.ok:
        print("DeepSeek 调用失败：", resp.status_code, resp.text)
        raise RuntimeError(
            f"HTTP {resp.status_code} 错误。\n"
            f"返回内容：{resp.text[:300]}..."
        )

    try:
        data = resp.json()
    except Exception as e:
        raise RuntimeError(f"解析 DeepSeek 返回 JSON 失败：{e}\n原始内容：{resp.text[:300]}")

    try:
        result = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"DeepSeek 返回格式异常：{data}") from e

    return result.strip()


# ================== 截屏选区控件 ==================


class SnipWidget(QWidget):
    snip_finished = pyqtSignal(object)  # QPixmap

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)

        screen = QApplication.primaryScreen()
        self.background = screen.grabWindow(0) if screen is not None else None

        self.begin_point_global = None
        self.end_point_global = None
        self.is_snipping = False

    def _selection_rect(self) -> QRect:
        if not self.begin_point_global or not self.end_point_global:
            return QRect()
        p1 = self.mapFromGlobal(self.begin_point_global)
        p2 = self.mapFromGlobal(self.end_point_global)
        x1 = min(p1.x(), p2.x())
        y1 = min(p1.y(), p2.y())
        x2 = max(p1.x(), p2.x())
        y2 = max(p1.y(), p2.y())
        return QRect(x1, y1, x2 - x1, y2 - y1)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_snipping = True
            self.begin_point_global = event.globalPos()
            self.end_point_global = event.globalPos()
            self.update()
        elif event.button() == Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, event):
        if self.is_snipping:
            self.end_point_global = event.globalPos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_snipping:
            self.is_snipping = False
            self.end_point_global = event.globalPos()
            rect = self._selection_rect()

            if rect.width() > 5 and rect.height() > 5 and self.background is not None:
                pix = self.background.copy(rect)
                self.hide()
                self.snip_finished.emit(pix)
                self.deleteLater()
            else:
                self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.background is not None:
            painter.drawPixmap(self.rect(), self.background)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 80))

        rect = self._selection_rect()
        if rect.isValid():
            pen = QPen(QColor(0, 180, 255))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(rect)


# ================== 全局热键桥接 ==================


class HotkeyBridge(QObject):
    hotkeyPressed = pyqtSignal()


# ================== QThread：OCR+翻译 & 文本翻译 ==================


class OcrTranslateThread(QThread):
    finished = pyqtSignal(str, str)  # ocr_text, translated_text
    error = pyqtSignal(str)

    def __init__(self, image: Image.Image, config: dict, mode: str, parent=None):
        super().__init__(parent)
        self.image = image
        self.config = config
        self.mode = mode

    def run(self):
        try:
            ocr_text = pytesseract.image_to_string(self.image, lang="eng+chi_sim")
            ocr_text = ocr_text.strip()
            translated = translate_with_deepseek(ocr_text, self.config, mode=self.mode)
            self.finished.emit(ocr_text, translated)
        except Exception as e:
            self.error.emit(str(e))


class TextTranslateThread(QThread):
    finished = pyqtSignal(str)  # translated_text
    error = pyqtSignal(str)

    def __init__(self, text: str, config: dict, mode: str, parent=None):
        super().__init__(parent)
        self.text = text
        self.config = config
        self.mode = mode

    def run(self):
        try:
            translated = translate_with_deepseek(self.text, self.config, mode=self.mode)
            self.finished.emit(translated)
        except Exception as e:
            self.error.emit(str(e))


# ================== Loading Spinner & Overlay ==================


class SpinnerWidget(QWidget):
    def __init__(self, size=48, parent=None):
        super().__init__(parent)
        self._angle = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_timeout)
        self._timer.start(80)
        self._size = size
        self.setFixedSize(size, size)

    def _on_timeout(self):
        self._angle = (self._angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        radius = min(self.width(), self.height()) / 2 - 4
        center = self.rect().center()

        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(3)
        painter.setPen(Qt.NoPen)

        steps = 12
        for i in range(steps):
            alpha = int(255 * (i + 1) / steps)
            color = QColor(255, 255, 255, alpha)
            painter.setBrush(color)
            angle = (self._angle + (360 / steps) * i) * 3.14159 / 180.0
            x = center.x() + radius * 0.7 * float(__import__("math").cos(angle))
            y = center.y() + radius * 0.7 * float(__import__("math").sin(angle))
            r = 4
            painter.drawEllipse(QRect(int(x - r), int(y - r), 2 * r, 2 * r))


class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 160);")
        self.setVisible(False)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.spinner = SpinnerWidget(48, self)
        self.label = QLabel("处理中…", self)
        self.label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(self.spinner, 0, Qt.AlignHCenter)
        layout.addSpacing(12)
        layout.addWidget(self.label, 0, Qt.AlignHCenter)

    def showMessage(self, text: str):
        self.label.setText(text)
        if self.parent() is not None:
            self.resize(self.parent().size())
            self.move(0, 0)
        self.raise_()
        self.show()

    def hideOverlay(self):
        self.hide()


# ================== 设置对话框 ==================


class SettingsDialog(QDialog):
    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setModal(True)
        self.resize(420, 240)

        self._config = config.copy()

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.edit_api_url = QLineEdit(self._config.get("api_url", DEFAULT_API_URL))
        self.edit_api_key = QLineEdit(self._config.get("api_key", ""))
        self.edit_api_key.setEchoMode(QLineEdit.Password)
        self.edit_model = QLineEdit(self._config.get("model", DEFAULT_MODEL))
        self.edit_hotkey = QLineEdit(self._config.get("hotkey", "ctrl+d"))

        form.addRow("API 地址：", self.edit_api_url)
        form.addRow("API Key：", self.edit_api_key)
        form.addRow("模型名称：", self.edit_model)
        form.addRow("截屏快捷键：", self.edit_hotkey)

        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def get_config(self) -> dict:
        self._config["api_url"] = self.edit_api_url.text().strip() or DEFAULT_API_URL
        self._config["api_key"] = self.edit_api_key.text().strip()
        self._config["model"] = self.edit_model.text().strip() or DEFAULT_MODEL
        hotkey = self.edit_hotkey.text().strip().lower()
        self._config["hotkey"] = hotkey or "ctrl+d"
        return self._config


# ================== 主窗口 ==================


class MainWindow(QMainWindow):
    def __init__(self, hotkey_bridge: HotkeyBridge, config: dict):
        super().__init__()

        self.setWindowTitle("DeepSeek OCR翻译工具")
        self.setMinimumSize(900, 520)

        if ICON_BASE64:
            self.setWindowIcon(icon_from_base64(ICON_BASE64))

        self.config = config
        self.hotkey_bridge = hotkey_bridge
        self.hotkey_bridge.hotkeyPressed.connect(self.on_hotkey_triggered)

        self.snip_widget = None
        self.worker_thread: OcrTranslateThread | None = None
        self.text_thread: TextTranslateThread | None = None

        self.hotkey_handle = None  # 当前注册的热键

        self._init_ui()
        self._init_tray()
        self.loading_overlay = LoadingOverlay(self)

        self._register_hotkey()

        self.statusBar().showMessage("就绪（按截屏快捷键可随时截屏翻译）")

    # ---------- UI ----------

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)

        # 顶部：按钮 + 语言 + 设置 + 复制 + 翻译当前文本
        top_layout = QHBoxLayout()
        self.btn_snip = QPushButton("截屏并翻译")
        self.btn_snip.clicked.connect(self.on_snip_clicked)

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("自动检测 → 简体中文", "to_zh")
        self.lang_combo.addItem("自动检测 → English", "to_en")

        self.btn_settings = QPushButton("设置")
        self.btn_settings.clicked.connect(self.on_settings_clicked)

        self.btn_copy = QPushButton("复制译文")
        self.btn_copy.clicked.connect(self.on_copy_clicked)

        self.btn_manual_translate = QPushButton("翻译当前文本")
        self.btn_manual_translate.clicked.connect(self.on_manual_translate_clicked)

        top_layout.addWidget(self.btn_snip)
        top_layout.addWidget(QLabel("翻译方向："))
        top_layout.addWidget(self.lang_combo)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_settings)
        top_layout.addWidget(self.btn_copy)
        top_layout.addWidget(self.btn_manual_translate)

        root_layout.addLayout(top_layout)

        # 中间：左右布局
        middle_layout = QHBoxLayout()

        # 左：OCR
        left_layout = QVBoxLayout()
        lbl_ocr = QLabel("OCR 识别结果：")
        self.text_ocr = QTextEdit()
        self.text_ocr.setPlaceholderText("截屏后会在这里显示识别出来的文字。")
        left_layout.addWidget(lbl_ocr)
        left_layout.addWidget(self.text_ocr)

        # 右：翻译
        right_layout = QVBoxLayout()
        lbl_trans = QLabel("翻译结果：")
        self.text_trans = QTextEdit()
        self.text_trans.setPlaceholderText("翻译结果会显示在这里。")
        right_layout.addWidget(lbl_trans)
        right_layout.addWidget(self.text_trans)

        middle_layout.addLayout(left_layout, stretch=1)
        middle_layout.addLayout(right_layout, stretch=1)

        root_layout.addLayout(middle_layout, stretch=1)

    def _init_tray(self):
        if ICON_BASE64:
            icon = icon_from_base64(ICON_BASE64)
        else:
            icon = self.style().standardIcon(QStyle.SP_ComputerIcon)

        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.setToolTip("DeepSeek OCR翻译工具")

        menu = QMenu()
        action_show = QAction("打开主窗口", self)
        action_quit = QAction("退出", self)
        action_show.triggered.connect(self.show_from_tray)
        action_quit.triggered.connect(self.quit_app)
        menu.addAction(action_show)
        menu.addSeparator()
        menu.addAction(action_quit)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    # ---------- Loading Overlay ----------

    def show_loading(self, message: str):
        self.loading_overlay.showMessage(message)

    def hide_loading(self):
        self.loading_overlay.hideOverlay()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "loading_overlay") and self.loading_overlay.isVisible():
            self.loading_overlay.resize(self.size())
            self.loading_overlay.move(0, 0)

    # ---------- 热键 ----------

    def _register_hotkey(self):
        hotkey = (self.config.get("hotkey") or "ctrl+d").strip().lower()
        if not hotkey:
            hotkey = "ctrl+d"
        self.config["hotkey"] = hotkey

        if self.hotkey_handle is not None:
            try:
                keyboard.remove_hotkey(self.hotkey_handle)
            except Exception as e:
                print("移除旧快捷键失败：", e)

        try:
            self.hotkey_handle = keyboard.add_hotkey(
                hotkey, lambda: self.hotkey_bridge.hotkeyPressed.emit()
            )
            self.statusBar().showMessage(f"就绪（当前截屏快捷键：{hotkey}）")
        except Exception as e:
            QMessageBox.warning(self, "快捷键错误", f"注册快捷键失败：\n{e}")
            self.statusBar().showMessage("快捷键注册失败")

    # ---------- 托盘相关 ----------

    def show_from_tray(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def quit_app(self):
        try:
            if self.hotkey_handle is not None:
                keyboard.remove_hotkey(self.hotkey_handle)
        except Exception:
            pass
        self.tray_icon.hide()
        QApplication.quit()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isMinimized() or not self.isVisible():
                self.show_from_tray()
            else:
                self.show_from_tray()

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.hide()
            self.statusBar().showMessage("已最小化到托盘，仍可使用截屏快捷键进行翻译")
            event.ignore()
        else:
            super().closeEvent(event)

    # ---------- 设置 ----------

    def on_settings_clicked(self):
        dlg = SettingsDialog(self.config, self)
        if dlg.exec_() == QDialog.Accepted:
            self.config = dlg.get_config()
            save_config(self.config)
            self._register_hotkey()
            self.statusBar().showMessage("配置已保存")

    # ---------- 热键触发 ----------

    def on_hotkey_triggered(self):
        self.on_snip_clicked()

    # ---------- 截图 & 线程 ----------

    def on_snip_clicked(self):
        if self.worker_thread is not None and self.worker_thread.isRunning():
            QMessageBox.information(self, "提示", "上一轮截屏翻译仍在进行中，请稍候。")
            return

        if self.snip_widget is not None:
            try:
                self.snip_widget.close()
            except Exception:
                pass

        self.snip_widget = SnipWidget()
        self.snip_widget.snip_finished.connect(self.on_snip_finished)
        self.snip_widget.show()

    def on_snip_finished(self, pixmap):
        QApplication.processEvents()

        try:
            image = self._qpixmap_to_pil(pixmap).convert("RGB")
        except Exception as e:
            QMessageBox.critical(self, "图像错误", f"图像处理失败：\n{e}")
            self.statusBar().showMessage("图像处理失败")
            self.snip_widget = None
            return

        if not (self.config.get("api_key") or "").strip():
            QMessageBox.warning(self, "提示", "尚未配置 API Key，请先点击右上角 [设置]。")
            self.statusBar().showMessage("未配置 API Key")
            self.snip_widget = None
            return

        self.text_ocr.clear()
        self.text_trans.clear()

        self.btn_snip.setEnabled(False)
        self.btn_manual_translate.setEnabled(False)
        self.show_loading("正在执行 OCR + 翻译，请稍候…")

        mode = self.lang_combo.currentData()
        self.worker_thread = OcrTranslateThread(image, dict(self.config), mode, parent=self)
        self.worker_thread.finished.connect(self.on_worker_finished)
        self.worker_thread.error.connect(self.on_worker_error)
        self.worker_thread.finished.connect(self.cleanup_ocr_thread)
        self.worker_thread.error.connect(self.cleanup_ocr_thread)
        self.worker_thread.start()

    def cleanup_ocr_thread(self):
        self.btn_snip.setEnabled(True)
        self.btn_manual_translate.setEnabled(True)
        self.worker_thread = None
        self.hide_loading()

    def on_worker_finished(self, ocr_text: str, translated: str):
        self.text_ocr.setPlainText(ocr_text or "[未识别到文字]")
        self.text_trans.setPlainText(translated)
        self.statusBar().showMessage("完成")
        self.snip_widget = None
        self.show_from_tray()

    def on_worker_error(self, message: str):
        QMessageBox.critical(self, "错误", message)
        self.statusBar().showMessage("出错")
        self.snip_widget = None
        self.show_from_tray()

    # ---------- 手动翻译按钮 ----------

    def on_manual_translate_clicked(self):
        if self.text_thread is not None and self.text_thread.isRunning():
            QMessageBox.information(self, "提示", "文本翻译正在进行中，请稍候。")
            return

        src = self.text_ocr.toPlainText().strip()
        if not src:
            QMessageBox.information(self, "提示", "左侧没有可翻译的文本。")
            return

        if not (self.config.get("api_key") or "").strip():
            QMessageBox.warning(self, "提示", "尚未配置 API Key，请先点击右上角 [设置]。")
            return

        mode = self.lang_combo.currentData()
        self.btn_manual_translate.setEnabled(False)
        self.show_loading("正在翻译当前文本，请稍候…")

        self.text_thread = TextTranslateThread(src, dict(self.config), mode, parent=self)
        self.text_thread.finished.connect(self.on_text_thread_finished)
        self.text_thread.error.connect(self.on_text_thread_error)
        self.text_thread.finished.connect(self.cleanup_text_thread)
        self.text_thread.error.connect(self.cleanup_text_thread)
        self.text_thread.start()

    def cleanup_text_thread(self):
        self.btn_manual_translate.setEnabled(True)
        self.text_thread = None
        self.hide_loading()

    def on_text_thread_finished(self, translated: str):
        self.text_trans.setPlainText(translated)
        self.statusBar().showMessage("文本翻译完成")

    def on_text_thread_error(self, message: str):
        QMessageBox.critical(self, "错误", message)
        self.statusBar().showMessage("文本翻译出错")

    # ---------- 复制 ----------

    def on_copy_clicked(self):
        text = self.text_trans.toPlainText().strip()
        if not text:
            QMessageBox.information(self, "提示", "当前没有可以复制的译文。")
            return
        QApplication.clipboard().setText(text)
        self.statusBar().showMessage("译文已复制到剪贴板")

    # ---------- 工具方法 ----------

    @staticmethod
    def _qpixmap_to_pil(pixmap) -> Image.Image:
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")
        byte_data = bytes(buffer.data())
        buffer.close()
        return Image.open(io.BytesIO(byte_data))


# ================== 暗色主题 & 自定义字体 ==================


def apply_dark_theme(app: QApplication):
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(37, 37, 38))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(45, 45, 48))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(45, 45, 48))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(0, 122, 204))
    palette.setColor(QPalette.Highlight, QColor(0, 122, 204))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)


def apply_custom_font(app: QApplication):
    font_path = os.path.join(BASE_DIR, "font.ttf")
    if not os.path.exists(font_path):
        return
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        return
    families = QFontDatabase.applicationFontFamilies(font_id)
    if not families:
        return
    font = QFont(families[0], 10)
    app.setFont(font)


# ================== 入口 ==================


def main():
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    apply_custom_font(app)

    if ICON_BASE64:
        app.setWindowIcon(icon_from_base64(ICON_BASE64))

    config = load_config()

    hotkey_bridge = HotkeyBridge()
    win = MainWindow(hotkey_bridge, config)
    win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
