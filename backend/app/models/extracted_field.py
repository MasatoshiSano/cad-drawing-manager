from sqlalchemy import Column, String, Text, Integer, Float, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship

from ..database import Base


class ExtractedField(Base):
    """抽出フィールドモデル"""

    __tablename__ = "extracted_fields"

    id = Column(Integer, primary_key=True, autoincrement=True)
    drawing_id = Column(String, ForeignKey("drawings.id"), nullable=False)
    field_name = Column(String, nullable=False)
    field_value = Column(Text)
    confidence = Column(Float)  # 0-100
    coordinates = Column(JSON)  # {"x": 100, "y": 200, "width": 50, "height": 20}

    # リレーションシップ
    drawing = relationship("Drawing", back_populates="extracted_fields")

    # インデックス
    __table_args__ = (Index("idx_extracted_fields_drawing", "drawing_id"),)

    def __repr__(self):
        return f"<ExtractedField(field_name={self.field_name}, value={self.field_value}, confidence={self.confidence})>"
