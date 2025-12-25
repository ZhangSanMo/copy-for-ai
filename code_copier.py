import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, 
                             QWidget, QPushButton, QLabel, QMessageBox, QProgressBar, 
                             QHBoxLayout, QFileDialog, QLineEdit, QHeaderView, QSizeGrip, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFileSystemModel

# 配置：忽略的目录和文件后缀
IGNORE_DIRS = {'.git', '.svn', '.hg', '.idea', '.vscode', '__pycache__', 'node_modules', 
               'venv', 'env', 'build', 'dist', 'bin', 'obj', 'target', '.mypy_cache', '.pytest_cache'}
IGNORE_EXTS = {'.exe', '.dll', '.so', '.dylib', '.class', '.jar', '.pyc', '.pyo', 
               '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.tar', '.gz', '.7z', '.rar',
               '.svg', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.mp3', '.wav'}

# Theme Definitions
DARK_THEME = """
QWidget {
    background-color: #2b2b2b;
    color: #e0e0e0;
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 10pt;
}
#RootWidget {
    border: 1px solid #3e3e3e;
    background-color: #2b2b2b;
}
QLineEdit {
    background-color: #383838;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 5px;
    selection-background-color: #0078d4;
    color: #e0e0e0;
}
QTreeWidget {
    background-color: #323232;
    border: 1px solid #444;
    border-radius: 4px;
    alternate-background-color: #383838;
}
QTreeWidget::item {
    padding: 4px;
}
QTreeWidget::item:hover {
    background-color: #3e3e3e;
}
QTreeWidget::item:selected {
    background-color: #4d4d4d;
    color: #ffffff;
}
QHeaderView::section {
    background-color: #404040;
    color: #ddd;
    padding: 4px;
    border: none;
    border-bottom: 1px solid #555;
}
QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #1084d9;
}
QPushButton:pressed {
    background-color: #006cc1;
}
QPushButton:disabled {
    background-color: #444;
    color: #888;
}
QProgressBar {
    border: 1px solid #444;
    border-radius: 4px;
    text-align: center;
    background-color: #333;
}
QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}
QScrollBar:vertical {
    border: none;
    background: #2b2b2b;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #555;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
/* Title Bar - Seamless Integration */
#TitleBar {
    background-color: transparent;
}
#TitleLabel {
    color: #ffffff;
    font-weight: bold;
    font-size: 11pt;
}
.TitleBtn {
    background-color: transparent;
    color: #e0e0e0;
    border: none;
    border-radius: 4px;
    padding: 0;
    font-size: 11px;
    margin-left: 2px;
}
.TitleBtn:hover {
    background-color: #444;
}
#ThemeBtn {
    font-size: 13px;
    font-weight: normal;
}
#CloseBtn:hover {
    background-color: #d32f2f;
    color: white;
}
"""

LIGHT_THEME = """
QWidget {
    background-color: #f9f9f9;
    color: #333333;
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 10pt;
}
#RootWidget {
    border: 1px solid #dcdcdc;
    background-color: #f9f9f9;
}
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 5px;
    selection-background-color: #0078d4;
    color: #333333;
}
QTreeWidget {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    alternate-background-color: #fcfcfc;
}
QTreeWidget::item {
    padding: 4px;
    color: #333;
}
QTreeWidget::item:hover {
    background-color: #e6f7ff;
}
QTreeWidget::item:selected {
    background-color: #cce8ff;
    color: #000;
}
QHeaderView::section {
    background-color: #f0f0f0;
    color: #333;
    padding: 4px;
    border: none;
    border-bottom: 1px solid #ccc;
}
QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #1084d9;
}
QPushButton:pressed {
    background-color: #006cc1;
}
QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}
QProgressBar {
    border: 1px solid #ccc;
    border-radius: 4px;
    text-align: center;
    background-color: #eee;
}
QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}
QScrollBar:vertical {
    border: none;
    background: #f9f9f9;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #c1c1c1;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
/* Title Bar - Seamless Integration */
#TitleBar {
    background-color: transparent;
}
#TitleLabel {
    color: #000000;
    font-weight: bold;
    font-size: 11pt;
}
.TitleBtn {
    background-color: transparent;
    color: #333;
    border: none;
    border-radius: 4px;
    padding: 0;
    font-size: 11px;
    margin-left: 2px;
}
.TitleBtn:hover {
    background-color: #e0e0e0;
}
#ThemeBtn {
    font-size: 13px;
    font-weight: normal;
}
#CloseBtn:hover {
    background-color: #e81123;
    color: white;
}
"""

class ThemeManager:
    def __init__(self, app):
        self.app = app
        self.is_dark = True
    
    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()
        return self.is_dark
        
    def apply_theme(self):
        if self.is_dark:
            self.app.setStyleSheet(DARK_THEME)
        else:
            self.app.setStyleSheet(LIGHT_THEME)

class TitleBar(QFrame):
    def __init__(self, parent_window, theme_manager):
        super().__init__()
        self.parent_window = parent_window
        self.theme_manager = theme_manager
        self.setObjectName("TitleBar")
        self.setFixedHeight(40)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0) # Symmetric alignment
        layout.setSpacing(0)
        
        # Title
        self.title_label = QLabel("Code Context Extractor")
        self.title_label.setObjectName("TitleLabel")
        layout.addWidget(self.title_label)
        
        layout.addStretch()
        
        # Theme Toggle
        self.btn_theme = QPushButton("☀/🌙")
        self.btn_theme.setObjectName("ThemeBtn") # Specific ID for styling
        self.btn_theme.setProperty("class", "TitleBtn")
        self.btn_theme.setFixedSize(60, 36) # Wider to avoid truncation
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.setToolTip("Toggle Theme")
        self.btn_theme.clicked.connect(self.toggle_theme)
        layout.addWidget(self.btn_theme)

        # Minimize
        self.btn_min = QPushButton("─")
        self.btn_min.setProperty("class", "TitleBtn")
        self.btn_min.setFixedSize(36, 36)
        self.btn_min.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(self.btn_min)

        # Maximize/Restore
        self.btn_max = QPushButton("☐")
        self.btn_max.setProperty("class", "TitleBtn")
        self.btn_max.setFixedSize(36, 36)
        self.btn_max.clicked.connect(self.toggle_max_restore)
        layout.addWidget(self.btn_max)

        # Close
        self.btn_close = QPushButton("✕")
        self.btn_close.setProperty("class", "TitleBtn")
        self.btn_close.setObjectName("CloseBtn") # Specific ID for red hover
        self.btn_close.setFixedSize(36, 36)
        self.btn_close.clicked.connect(self.parent_window.close)
        layout.addWidget(self.btn_close)

    def toggle_theme(self):
        self.theme_manager.toggle_theme()

    def toggle_max_restore(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.btn_max.setText("☐")
        else:
            self.parent_window.showMaximized()
            self.btn_max.setText("❐")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent_window.windowHandle().startSystemMove()

class Worker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, int)  # result_text, file_count
    
    def __init__(self, root_dir, selected_paths):
        """
        root_dir: 项目根目录
        selected_paths: 一个列表，包含 (path, type)
                        type 0 = 文件
                        type 1 = 文件夹 (全选)
        """
        super().__init__()
        self.root_dir = root_dir
        self.selected_paths = selected_paths
        self.is_running = True

    def decode_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            
            # 简单的二进制检测
            if b'\0' in raw_data[:8000]: 
                return None

            encodings = ['utf-8', 'gb18030', 'gbk', 'cp1252', 'latin-1']
            for enc in encodings:
                try:
                    return raw_data.decode(enc)
                except UnicodeDecodeError:
                    continue
            return None 
        except Exception:
            return None

    def run(self):
        output = []
        total_files = 0
        processed_files = set()

        # 待处理的文件队列
        # 如果是文件，直接处理
        # 如果是文件夹，遍历文件夹下所有文件
        
        final_file_list = []

        for path, item_type in self.selected_paths:
            if not self.is_running: break

            if item_type == 0: # 文件
                if path not in processed_files:
                    final_file_list.append(path)
                    processed_files.add(path)
            elif item_type == 1: # 文件夹 (递归添加所有内容)
                for root, dirs, files in os.walk(path):
                    # 过滤忽略的目录
                    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        # 过滤后缀
                        _, ext = os.path.splitext(file_path)
                        if ext.lower() in IGNORE_EXTS:
                            continue
                        
                        if file_path not in processed_files:
                            final_file_list.append(file_path)
                            processed_files.add(file_path)

        # 开始读取内容
        for file_path in final_file_list:
            if not self.is_running: break
            
            content = self.decode_file(file_path)
            if content is not None:
                rel_path = os.path.relpath(file_path, self.root_dir)
                output.append(f"## File: {rel_path}\n```\n{content}\n```\n")
                total_files += 1
                self.progress.emit(total_files)

        full_text = "\n".join(output)
        self.finished.emit(full_text, total_files)

    def stop(self):
        self.is_running = False

class FileTreeItem(QTreeWidgetItem):
    def __init__(self, path, is_dir):
        super().__init__()
        self.path = path
        self.is_dir = is_dir
        self.setText(0, os.path.basename(path) or path)
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.loaded = False # 懒加载标记
        
        if is_dir:
            self.setChildIndicatorPolicy(QTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator)
            self.setIcon(0, QApplication.style().standardIcon(
                QApplication.style().StandardPixmap.SP_DirIcon))
        else:
            self.setIcon(0, QApplication.style().standardIcon(
                QApplication.style().StandardPixmap.SP_FileIcon))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Context Extractor for AI")
        self.resize(900, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Theme Init
        self.theme_manager = ThemeManager(QApplication.instance())
        self.theme_manager.apply_theme()
        
        # Root Widget & Layout (Contains TitleBar + Content)
        root_widget = QWidget()
        root_widget.setObjectName("RootWidget") # Can be used for border
        self.setCentralWidget(root_widget)
        root_layout = QVBoxLayout(root_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1. Title Bar
        self.title_bar = TitleBar(self, self.theme_manager)
        root_layout.addWidget(self.title_bar)

        # 2. Content Widget
        content_widget = QWidget()
        root_layout.addWidget(content_widget)
        
        # Layout for content
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 10, 20, 10) # Symmetric alignment with TitleBar
        layout.setSpacing(15)

        # --- Content UI ---
        # 1. Top Selection Area
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Select project root directory...")
        self.path_edit.setReadOnly(True)
        self.path_edit.setMinimumHeight(35)
        top_layout.addWidget(self.path_edit)

        self.btn_browse = QPushButton("Browse")
        self.btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_browse.setMinimumHeight(35)
        self.btn_browse.clicked.connect(self.browse_directory)
        top_layout.addWidget(self.btn_browse)
        layout.addLayout(top_layout)

        # 2. File Tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Project Structure")
        self.tree.itemExpanded.connect(self.on_item_expanded)
        self.tree.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.tree)

        # 3. Bottom Operations
        self.btn_copy = QPushButton("Generate & Copy to Clipboard")
        self.btn_copy.setMinimumHeight(45)
        self.btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy.clicked.connect(self.start_processing)
        self.btn_copy.setEnabled(False)
        layout.addWidget(self.btn_copy)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status Label & SizeGrip Container
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Please select a project root directory to start.")
        self.status_label.setStyleSheet("color: #888; font-style: italic;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        status_layout.addWidget(self.status_label, 1) # Stretch
        
        # Size Grip
        self.size_grip = QSizeGrip(self)
        status_layout.addWidget(self.size_grip, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(status_layout)

        self.worker = None
        self.root_path = ""
        self._updating_checks = False

    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Project Root")
        if dir_path:
            self.root_path = dir_path
            self.path_edit.setText(dir_path)
            self.load_root_tree(dir_path)
            self.btn_copy.setEnabled(True)
            self.status_label.setText(f"Loaded: {dir_path}")

    def load_root_tree(self, root_path):
        self.tree.clear()
        # 获取第一层
        self.add_items(self.tree.invisibleRootItem(), root_path)

    def add_items(self, parent_item, dir_path):
        """加载指定目录下的直接子项到 parent_item"""
        try:
            entries = os.listdir(dir_path)
        except PermissionError:
            return

        # 排序：文件夹在前，文件在后
        dirs = []
        files = []
        for entry in entries:
            if entry in IGNORE_DIRS: continue
            
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                dirs.append(entry)
            else:
                _, ext = os.path.splitext(entry)
                if ext.lower() not in IGNORE_EXTS:
                    files.append(entry)
        
        dirs.sort()
        files.sort()

        for d in dirs:
            item = FileTreeItem(os.path.join(dir_path, d), is_dir=True)
            parent_item.addChild(item)
            # 继承父节点的勾选状态 (如果是初始加载且父节点被勾选)
            if parent_item != self.tree.invisibleRootItem() and parent_item.checkState(0) == Qt.CheckState.Checked:
                item.setCheckState(0, Qt.CheckState.Checked)

        for f in files:
            item = FileTreeItem(os.path.join(dir_path, f), is_dir=False)
            parent_item.addChild(item)
            if parent_item != self.tree.invisibleRootItem() and parent_item.checkState(0) == Qt.CheckState.Checked:
                item.setCheckState(0, Qt.CheckState.Checked)

    def on_item_expanded(self, item):
        if not item.is_dir or item.loaded:
            return
        
        # 懒加载：展开时加载子项
        self._updating_checks = True # 暂停信号处理，因为加载时会设置状态
        self.add_items(item, item.path)
        item.loaded = True
        
        # 再次确保子项状态正确同步（因为 add_items 里只是简单的继承）
        # 如果父节点是 Checked，子节点全部 Checked
        # 如果父节点是 Unchecked，子节点全部 Unchecked
        # 懒加载时，如果父节点是 PartiallyChecked，我们很难知道新加载的子节点应该是什么状态
        # 简单的逻辑：如果父节点是 Checked，新子节点全选；否则默认不选。
        if item.checkState(0) == Qt.CheckState.Checked:
             for i in range(item.childCount()):
                 item.child(i).setCheckState(0, Qt.CheckState.Checked)
        
        self._updating_checks = False

    def on_item_changed(self, item, column):
        if self._updating_checks: return
        
        self._updating_checks = True
        
        state = item.checkState(0)
        
        # 1. 向下传播：设置所有子节点
        self.set_children_state(item, state)

        # 2. 向上传播：更新父节点状态
        self.update_parent_state(item)

        self._updating_checks = False

    def set_children_state(self, item, state):
        # 只有在节点已加载的情况下才遍历子节点 (懒加载优化)
        # 如果节点未加载且被勾选，我们在真正加载它的时候会处理状态继承
        if item.childCount() > 0:
            for i in range(item.childCount()):
                child = item.child(i)
                child.setCheckState(0, state)
                self.set_children_state(child, state)

    def update_parent_state(self, item):
        parent = item.parent()
        if parent:
            checked_count = 0
            partial_count = 0
            count = parent.childCount()
            
            for i in range(count):
                child = parent.child(i)
                if child.checkState(0) == Qt.CheckState.Checked:
                    checked_count += 1
                elif child.checkState(0) == Qt.CheckState.PartiallyChecked:
                    partial_count += 1
            
            if checked_count == count:
                parent.setCheckState(0, Qt.CheckState.Checked)
            elif checked_count > 0 or partial_count > 0:
                parent.setCheckState(0, Qt.CheckState.PartiallyChecked)
            else:
                parent.setCheckState(0, Qt.CheckState.Unchecked)
            
            self.update_parent_state(parent)

    def start_processing(self):
        # 收集选中项
        # 策略：
        # 1. 遍历 Tree 的顶层节点
        # 2. 如果节点状态为 Checked (全选) -> 将其路径作为“全选目录”加入，不再递归
        # 3. 如果节点状态为 PartiallyChecked (部分) -> 递归查找子节点
        # 4. 如果节点状态为 Checked 且是文件 -> 加入文件
        
        selected_items = [] # list of (path, type), type 0=file, 1=dir(recursive) 
        
        root = self.tree.invisibleRootItem()
        self.collect_checked_paths(root, selected_items)
        
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select files or folders from the tree first.")
            return

        self.btn_copy.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0) # Indeterminate
        self.status_label.setText("Reading and decoding files...")
        
        self.worker = Worker(self.root_path, selected_items)
        self.worker.progress.connect(lambda c: self.status_label.setText(f"Processed {c} files..."))
        self.worker.finished.connect(self.process_finished)
        self.worker.start()

    def collect_checked_paths(self, item, result_list):
        count = item.childCount()
        for i in range(count):
            child = item.child(i)
            state = child.checkState(0)
            
            if state == Qt.CheckState.Checked:
                # 全选状态
                if child.is_dir:
                    result_list.append((child.path, 1)) # 1 = 整个目录
                else:
                    result_list.append((child.path, 0)) # 0 = 单个文件
            elif state == Qt.CheckState.PartiallyChecked:
                # 部分选中，必须是目录，需要递归
                if child.is_dir:
                    # 如果目录没展开（loaded=False），但在逻辑上是 PartiallyChecked
                    # (这在当前UI逻辑下不太可能发生，除非代码修改选中状态)
                    # 无论如何，如果它是 Partial，说明用户肯定展开过或者操作过
                    self.collect_checked_paths(child, result_list)

    def process_finished(self, text, count):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        
        self.btn_copy.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Done! Copied {count} files.")
        QMessageBox.information(self, "Success", f"Successfully extracted {count} files to clipboard!\nReady to paste.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())