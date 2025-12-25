import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, 
                             QWidget, QPushButton, QLabel, QMessageBox, QProgressBar, 
                             QHBoxLayout, QFileDialog, QLineEdit, QHeaderView)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFileSystemModel

# 配置：忽略的目录和文件后缀
IGNORE_DIRS = {'.git', '.svn', '.hg', '.idea', '.vscode', '__pycache__', 'node_modules', 
               'venv', 'env', 'build', 'dist', 'bin', 'obj', 'target', '.mypy_cache', '.pytest_cache'}
IGNORE_EXTS = {'.exe', '.dll', '.so', '.dylib', '.class', '.jar', '.pyc', '.pyo', 
               '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.tar', '.gz', '.7z', '.rar',
               '.svg', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.mp3', '.wav'}

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
        self.setWindowTitle("AI 代码上下文提取工具")
        self.resize(800, 600)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # 1. 顶部选择区域
        top_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("请选择项目根目录...")
        self.path_edit.setReadOnly(True)
        top_layout.addWidget(self.path_edit)

        self.btn_browse = QPushButton("选择目录")
        self.btn_browse.clicked.connect(self.browse_directory)
        top_layout.addWidget(self.btn_browse)
        layout.addLayout(top_layout)

        # 2. 中间文件树
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("文件结构")
        self.tree.itemExpanded.connect(self.on_item_expanded)
        self.tree.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.tree)

        # 3. 底部操作区
        self.btn_copy = QPushButton("生成并复制到剪贴板")
        self.btn_copy.setMinimumHeight(50)
        self.btn_copy.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.btn_copy.clicked.connect(self.start_processing)
        self.btn_copy.setEnabled(False) # 未选择目录前不可用
        layout.addWidget(self.btn_copy)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("请先选择项目根目录")
        layout.addWidget(self.status_label)

        self.worker = None
        self.root_path = ""
        self._updating_checks = False # 防止递归触发信号

    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择项目根目录")
        if dir_path:
            self.root_path = dir_path
            self.path_edit.setText(dir_path)
            self.load_root_tree(dir_path)
            self.btn_copy.setEnabled(True)
            self.status_label.setText(f"已加载: {dir_path}")

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
            QMessageBox.warning(self, "提示", "请先在左侧勾选需要复制的文件或文件夹！")
            return

        self.btn_copy.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0) # Indeterminate
        self.status_label.setText("正在读取并解码文件...")
        
        self.worker = Worker(self.root_path, selected_items)
        self.worker.progress.connect(lambda c: self.status_label.setText(f"已处理 {c} 个文件..."))
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
        self.status_label.setText(f"处理完成！共复制 {count} 个文件。")
        QMessageBox.information(self, "成功", f"成功提取 {count} 个文件的内容并复制到剪贴板！\n可直接粘贴使用。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())