import math
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


class MyBot:
    """
    (fr) Cette classe représente votre bot. Vous pouvez y définir des attributs et des méthodes qui
         seront conservées entre chaque appel de la méthode `on_tick`.

    (en) This class represents your bot. You can define attributes and methods in it that will be kept
         between each call of the `on_tick` method.
    """

    __map_state: MapState
    name: str

    def __init__(self):
        self.toggle: bool = True
        self.name = "Magellan"
        self.rad = 0
        self.history = {}

    def on_tick(
        self, game_state: GameState
    ) -> List[
        Union[
            MoveAction, SwitchWeaponAction, RotateBladeAction, ShootAction, SaveAction
        ]
    ]:
        """
        (fr)    Cette méthode est appelée à chaque tick de jeu. Vous pouvez y définir
                  le comportement de votre bot. Elle doit retourner une liste d'actions
                  qui sera exécutée par le serveur.

                  Liste des actions possibles:
                  - MoveAction((x, y))        permet de diriger son bot, il ira a vitesse
                                              constante jusqu'à ce point.

                  - ShootAction((x, y))       Si vous avez le fusil comme arme, cela va tirer
                                              à la coordonnée donnée.

                  - SaveAction([...])         Permet de storer 100 octets dans le serveur. Lors
                                              de votre reconnection, ces données vous seront
                                              redonnées par le serveur.

                  - SwitchWeaponAction(id)    Permet de changer d'arme. Par défaut, votre bot
                                              n'est pas armé, voici vos choix:
                                                     PlayerWeapon.PlayerWeaponNone
                                                     PlayerWeapon.PlayerWeaponCanon
                                                     PlayerWeapon.PlayerWeaponBlade

                  - BladeRotateAction(rad)    Si vous avez la lame comme arme, vous pouver mettre votre arme
                                              à la rotation donnée en radian.

        (en)    This method is called at each game tick. You can define your bot's behavior here. It must return a
                  list of actions that will be executed by the server.

                  Possible actions:
                  - MoveAction((x, y))        Directs your bot to move to the specified point at a constant speed.

                  - ShootAction((x, y))       If you have the gun equipped, it will shoot at the given coordinates.

                  - SaveAction([...])         Allows you to store 100 bytes on the server. When you reconnect, these
                                              data will be provided to you by the server.

                  - SwitchWeaponAction(id)    Allows you to change your weapon. By default, your bot is unarmed. Here
                                              are your choices:
                                                PlayerWeapon.PlayerWeaponNone
                                                PlayerWeapon.PlayerWeaponCanon
                                                PlayerWeapon.PlayerWeaponBlade

                  - BladeRotateAction(rad)    if you have the blade as a weapon, you can set your
                                              weapon to the given rotation in radians.

        Arguments:
             game_state (GameState): (fr): L'état de la partie.
                                      (en): The state of the game.
        """

        self.history[game_state.current_tick] = game_state

        aristo = self.get_player("aristochat45", -1)
        last_aristo = self.get_player("aristochat45", -2)

        last_coordinates = last_aristo.pos
        last_dir = last_aristo.dest
        expected_position = self.expect_position(
            0.0345, last_coordinates.x, last_coordinates.y, last_dir.x, last_dir.y
        )
        print(expected_position)
        print(
            self.hit_wall(
                aristo.pos.x, aristo.pos.y, expected_position[0], expected_position[1]
            )
        )

        if self.toggle:
            print(f"Current tick: {game_state.current_tick}")
            self.toggle = False
        self.rad += 0.35
        actions = [
            MoveAction((1000, 1000)),
            RotateBladeAction(self.rad),
            SaveAction(b"Hello World"),
        ]

        return actions

    def get_player(self, name, index):
        return list(
            filter(
                lambda player: player.name == name,
                self.history[list(self.history.keys())[index]].players,
            )
        )[0]

    def hit_wall(self, x, y, intended_x, intended_y):
        print(x, y, intended_x, intended_y)
        return not (x == intended_x and y == intended_y)

    def expect_position(self, speed, xi, yi, xf, yf):
        distance = [xf - xi, yf - yi]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = map(lambda d: d / norm, distance)

        move = list(map(lambda i: i * speed, direction))
        return [xi + move[0], yi + move[0]]

    def on_start(self, map_state: MapState):
        """
        (fr) Cette méthode est appelée une seule fois au début de la partie. Vous pouvez y définir des
             actions à effectuer au début de la partie.

        (en) This method is called once at the beginning of the game. You can define actions to be
             performed at the beginning of the game.

        Arguments:
             map_state (MapState): (fr) L'état de la carte.
                                 (en) The state of the map.
        """
        self.__map_state = map_state
        horizontal_walls = [
            [1 for i in range(Consts.Map.WIDTH)],
            *[
                [0 for i in range(Consts.Map.WIDTH)]
                for i in range(Consts.Map.HEIGHT - 1)
            ],
            [1 for i in range(Consts.Map.WIDTH)],
        ]

        vertical_walls = [
            [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] for i in range(Consts.Map.WIDTH)],
        ]

        pass

    def on_end(self):
        """
        (fr) Cette méthode est appelée une seule fois à la fin de la partie. Vous pouvez y définir des
             actions à effectuer à la fin de la partie.

        (en) This method is called once at the end of the game. You can define actions to be performed
             at the end of the game.
        """
        pass
