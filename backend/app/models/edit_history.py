from sqlalchemy import Column, String, Text, Integer, TIMESTAMP, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class EditHistory(Base):
    """編集履歴モデル"""

    __tablename__ = "edit_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    drawing_id = Column(String, ForeignKey("drawings.id"), nullable=False)
    user_id = Column(String, nullable=False)  # PCホスト名/ユーザー名
    field_name = Column(String, nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    timestamp = Column(TIMESTAMP, default=func.now())

    # リレーションシップ
    drawing = relationship("Drawing", back_populates="edit_history")

    # インデックス
    __table_args__ = (Index("idx_edit_history_drawing", "drawing_id"),)

    def __repr__(self):
        return f"<EditHistory(drawing_id={self.drawing_id}, field={self.field_name}, user={self.user_id})>"
