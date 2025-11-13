"""
ファイル管理マネージャー

PDF保存、削除、サムネイル生成などのファイル操作を管理
"""

import shutil
import uuid
from pathlib import Path
from typing import Optional, Tuple
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO


class FileManager:
    """ファイル管理クラス"""

    def __init__(self, storage_path: Optional[str] = None):
        """
        初期化

        Args:
            storage_path: ストレージディレクトリのパス。Noneの場合はデフォルトパス
        """
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            # プロジェクトルート/storage
            project_root = Path(__file__).parent.parent.parent.parent
            self.storage_path = project_root / "storage"

        self.drawings_path = self.storage_path / "drawings"
        self.thumbnails_path = self.storage_path / "thumbnails"

        # ディレクトリを作成
        self.drawings_path.mkdir(parents=True, exist_ok=True)
        self.thumbnails_path.mkdir(parents=True, exist_ok=True)

    def save_pdf(self, pdf_bytes: bytes, original_filename: str) -> Tuple[str, str]:
        """
        PDFファイルを保存

        Args:
            pdf_bytes: PDFのバイトデータ
            original_filename: 元のファイル名

        Returns:
            (保存したファイル名, 保存先の絶対パス)
        """
        # UUIDでファイル名を生成
        file_id = str(uuid.uuid4())
        file_extension = Path(original_filename).suffix
        new_filename = f"{file_id}{file_extension}"

        # 保存先パス
        save_path = self.drawings_path / new_filename

        # ファイルを保存
        with open(save_path, "wb") as f:
            f.write(pdf_bytes)

        return new_filename, str(save_path)

    def delete_pdf(self, filename: str) -> bool:
        """
        PDFファイルを削除

        Args:
            filename: ファイル名

        Returns:
            削除成功: True, ファイルが存在しない: False
        """
        file_path = self.drawings_path / filename

        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def generate_thumbnail(
        self, pdf_path: str, max_size: Tuple[int, int] = (200, 300)
    ) -> str:
        """
        PDFのサムネイルを生成

        Args:
            pdf_path: PDFファイルのパス
            max_size: サムネイルの最大サイズ (width, height)

        Returns:
            サムネイルファイルのパス
        """
        pdf_path = Path(pdf_path)

        # サムネイルファイル名
        thumbnail_filename = pdf_path.stem + ".png"
        thumbnail_path = self.thumbnails_path / thumbnail_filename

        # PDFを開く
        doc = fitz.open(pdf_path)
        page = doc[0]  # 最初のページ

        # 50%のサイズで画像化
        mat = fitz.Matrix(0.5, 0.5)
        pix = page.get_pixmap(matrix=mat)

        # PIL Imageに変換
        img_bytes = pix.tobytes("png")
        img = Image.open(BytesIO(img_bytes))

        # サムネイルサイズに縮小
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # 保存
        img.save(thumbnail_path, "PNG")

        doc.close()

        return str(thumbnail_path)

    def delete_thumbnail(self, filename: str) -> bool:
        """
        サムネイルファイルを削除

        Args:
            filename: サムネイルファイル名

        Returns:
            削除成功: True, ファイルが存在しない: False
        """
        thumbnail_path = self.thumbnails_path / filename

        if thumbnail_path.exists():
            thumbnail_path.unlink()
            return True
        return False

    def get_pdf_path(self, filename: str) -> Optional[str]:
        """
        PDFファイルの絶対パスを取得

        Args:
            filename: ファイル名

        Returns:
            絶対パス。ファイルが存在しない場合はNone
        """
        file_path = self.drawings_path / filename

        if file_path.exists():
            return str(file_path)
        return None

    def get_thumbnail_path(self, filename: str) -> Optional[str]:
        """
        サムネイルファイルの絶対パスを取得

        Args:
            filename: サムネイルファイル名

        Returns:
            絶対パス。ファイルが存在しない場合はNone
        """
        thumbnail_path = self.thumbnails_path / filename

        if thumbnail_path.exists():
            return str(thumbnail_path)
        return None

    def check_disk_space(self) -> dict:
        """
        ディスク容量を確認

        Returns:
            {"total": 総容量, "used": 使用量, "free": 空き容量} (bytes)
        """
        stat = shutil.disk_usage(self.storage_path)
        return {"total": stat.total, "used": stat.used, "free": stat.free}

    def __repr__(self):
        return f"<FileManager(storage_path={self.storage_path})>"
