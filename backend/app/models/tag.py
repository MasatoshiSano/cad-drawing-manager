from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Tag(Base):
    """タグモデル"""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    drawing_id = Column(String, ForeignKey("drawings.id"), nullable=False)
    tag_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    # リレーションシップ
    drawing = relationship("Drawing", back_populates="tags")

    # インデックス
    __table_args__ = (
        Index("idx_tags_drawing", "drawing_id"),
        Index("idx_tags_name", "tag_name"),
    )

    def __repr__(self):
        return f"<Tag(drawing_id={self.drawing_id}, name={self.tag_name})>"
