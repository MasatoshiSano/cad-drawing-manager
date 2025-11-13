from sqlalchemy import Column, String, Integer, Float, ForeignKey, Index
from sqlalchemy.orm import relationship

from ..database import Base


class Balloon(Base):
    """風船情報モデル"""

    __tablename__ = "balloons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    drawing_id = Column(String, ForeignKey("drawings.id"), nullable=False)
    balloon_number = Column(String)
    part_name = Column(String)
    quantity = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    confidence = Column(Float)

    # リレーションシップ
    drawing = relationship("Drawing", back_populates="balloons")

    # インデックス
    __table_args__ = (Index("idx_balloons_drawing", "drawing_id"),)

    def __repr__(self):
        return f"<Balloon(number={self.balloon_number}, part={self.part_name}, qty={self.quantity})>"
