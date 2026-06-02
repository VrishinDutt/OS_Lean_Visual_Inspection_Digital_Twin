from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ProductPacket:
    product_id: str
    is_defective: bool
    frame_id: Optional[str] = None
    ai_result: Optional[str] = None
    rule_result: Optional[str] = None
    final_decision: Optional[str] = None
    rejected_product_id: Optional[str] = None
    race_condition: bool = False
    deadline_missed: bool = False

    def to_dict(self):
        return asdict(self)
