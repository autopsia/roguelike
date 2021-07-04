from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from object.entity import Entity

MELEE_ATTACKS = ["punch", "kick"]


class Action:
    pass

    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Must be implemented by classes extending this class
        """
        raise NotImplementedError()


class EscapeAction(Action):
    pass

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            return  # No entity to attack

        print(f"You {random.choice(MELEE_ATTACKS)} {target.name}")


class MovementAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Entity out of bounds
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Entity is not in walkable terrain
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Entity is being blocked by another

        entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)