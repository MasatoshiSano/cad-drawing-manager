from sqlalchemy import Column, String, Text, Integer, Float, ForeignKey, Index
from sqlalchemy.orm import relationship

from ..database import Base


class Revision(Base):
    """改訂履歴モデル"""

    __tablename__ = "revisions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    drawing_id = Column(String, ForeignKey("drawings.id"), nullable=False)
    revision_number = Column(String)
    revision_date = Column(String)
    revision_content = Column(Text)
    reviser = Column(String)
    confidence = Column(Float)

    # リレーションシップ
    drawing = relationship("Drawing", back_populates="revisions")

    # インデックス
    __table_args__ = (Index("idx_revisions_drawing", "drawing_id"),)

    def __repr__(self):
        return f"<Revision(number={self.revision_number}, date={self.revision_date})>"
