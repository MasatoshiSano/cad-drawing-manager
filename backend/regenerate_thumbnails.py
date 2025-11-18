"""
既存のサムネイルを再生成するスクリプト

Usage:
    python regenerate_thumbnails.py
"""

import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal
from app.models.drawing import Drawing
from app.utils.file_manager import FileManager

def regenerate_thumbnails():
    """既存のサムネイルを再生成"""
    db = SessionLocal()
    file_manager = FileManager()
    
    try:
        # すべての図面を取得
        drawings = db.query(Drawing).all()
        
        print(f"図面数: {len(drawings)}")
        
        for drawing in drawings:
            print(f"\n処理中: {drawing.pdf_filename} (ID: {drawing.id})")
            
            # PDFファイルのパスを取得
            pdf_path = file_manager.get_pdf_path(drawing.pdf_filename)
            if not pdf_path:
                print(f"  [ERROR] PDFファイルが見つかりません: {drawing.pdf_filename}")
                continue
            
            # 既存のサムネイルを削除
            if drawing.thumbnail_path:
                thumbnail_path = file_manager.thumbnails_path / drawing.thumbnail_path
                if thumbnail_path.exists():
                    thumbnail_path.unlink()
                    print(f"  [INFO] 既存のサムネイルを削除: {drawing.thumbnail_path}")
            
            # サムネイルを再生成
            try:
                new_thumbnail_path = file_manager.generate_thumbnail(
                    pdf_path, drawing.page_number
                )
                new_thumbnail_filename = Path(new_thumbnail_path).name
                
                # データベースを更新
                drawing.thumbnail_path = new_thumbnail_filename
                db.commit()
                
                print(f"  [OK] サムネイルを再生成: {new_thumbnail_filename}")
            except Exception as e:
                print(f"  [ERROR] サムネイル生成エラー: {e}")
                db.rollback()
        
        print("\n[OK] すべてのサムネイルの再生成が完了しました")
        
    except Exception as e:
        print(f"[ERROR] エラーが発生しました: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    regenerate_thumbnails()

