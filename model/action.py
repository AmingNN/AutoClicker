import yaml
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class MouseAction:
    """鼠标动作数据模型"""
    action_type: str  # 'move' , 'click'
    delay: float      # 距离上一个动作的时间间隔
    x: int
    y: int
    button: str = 'left'   # 'left', 'right'
    pressed: bool = False  # True=按下, False=松开

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        return data

def save_actions_to_yaml(actions: List[MouseAction], filepath: str):
    """保存为 YAML"""
    data = [a.to_dict() for a in actions]
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def load_actions_from_yaml(filepath: str) -> List[MouseAction]:
    """从 YAML 读取"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not data:
        return []
    return [MouseAction(**d) for d in data]

