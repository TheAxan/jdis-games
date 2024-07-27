from typing import List, Union

from core.action import (
    MoveAction,
    ShootAction,
    RotateBladeAction,
    SwitchWeaponAction,
    SaveAction,
)
from core.consts import Consts
from core.game_state import GameState, PlayerWeapon, Point
from core.map_state import MapState

horizontal_walls = [
    [1 for i in range(Consts.Map.WIDTH)],
    *[[0 for i in range(Consts.Map.WIDTH)] for i in range(Consts.Map.HEIGHT - 1)],
    [1 for i in range(Consts.Map.WIDTH)],
]

vertical_walls = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] for i in range(Consts.Map.WIDTH)]


for i in vertical_walls:
    print(i)
