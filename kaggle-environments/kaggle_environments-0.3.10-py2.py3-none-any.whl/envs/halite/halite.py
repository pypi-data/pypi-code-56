# Copyright 2020 Kaggle Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import json
import math
from os import path
from random import choice, randint, shuffle
import numpy as np


def get_col_row(size, pos):
    return pos % size, pos // size


def get_to_pos(size, pos, direction):
    col, row = get_col_row(size, pos)
    if direction == "NORTH":
        return pos - size if pos >= size else size ** 2 - size + col
    elif direction == "SOUTH":
        return col if pos + size >= size ** 2 else pos + size
    elif direction == "EAST":
        return pos + 1 if col < size - 1 else row * size
    elif direction == "WEST":
        return pos - 1 if col > 0 else (row + 1) * size - 1


class Board:
    def __init__(self, obs, config):
        self.action = {}
        self.obs = obs
        self.config = config
        size = config.size
        
        self.shipyards = [-1] * size ** 2
        self.shipyards_by_uid = {}
        self.ships = [None] * size ** 2
        self.ships_by_uid = {}
        self.possible_ships = [{} for _ in range(size ** 2)]
        
        for index, player in enumerate(obs.players):
            _, shipyards, ships = player
            for uid, pos in shipyards.items():
                self.shipyards[pos] = index
                self.shipyards_by_uid[uid] = {"player_index": index, "uid": uid, "pos": pos}
            for uid, ship in ships.items():
                pos, ship_halite = ship
                details = {"halite": ship_halite, "player_index": index, "uid": uid, "pos": pos}
                self.ships[pos] = details
                self.ships_by_uid[uid] = details
                for direction in ["NORTH", "EAST", "SOUTH", "WEST"]:
                    self.possible_ships[get_to_pos(size, pos, direction)][uid] = details
    
    def move(self, ship_uid, direction):
        self.action[ship_uid] = direction
        # Update the board.
        self.__remove_possibles(ship_uid)
        ship = self.ships_by_uid[ship_uid]
        pos = ship["pos"]
        to_pos = get_to_pos(self.config.size, pos, direction)
        ship["pos"] = to_pos
        self.ships[pos] = None
        self.ships[to_pos] = ship
    
    def convert(self, ship_uid):
        self.action[ship_uid] = "CONVERT"
        # Update the board.
        self.__remove_possibles(ship_uid)
        pos = self.ships_by_uid[ship_uid]["pos"]
        self.shipyards[pos] = self.obs.player
        self.ships[pos] = None
        del self.ships_by_uid[ship_uid]
    
    def spawn(self, shipyard_uid):
        self.action[shipyard_uid] = "SPAWN"
        # Update the board.
        temp_uid = f"Spawn_Ship_{shipyard_uid}"
        pos = self.shipyards_by_uid[shipyard_uid]["pos"]
        details = {"halite": 0, "player_index": self.obs.player, "uid": temp_uid, "pos": pos}
        self.ships[pos] = details
        self.ships_by_uid[temp_uid] = details
    
    def __remove_possibles(self, ship_uid):
        pos = self.ships_by_uid[ship_uid]["pos"]
        for d in ["NORTH", "EAST", "SOUTH", "WEST"]:
            to_pos = get_to_pos(self.config.size, pos, d)
            del self.possible_ships[to_pos][ship_uid]


def random_agent(obs, config):
    size = config.size
    halite = obs.halite
    board = Board(obs, config)
    player_halite, shipyards, ships = obs.players[obs.player]  

    # Move, Convert, or have ships collect halite.
    ships_items = list(ships.items())
    # shuffle so ship1 doesn't always have first moving dibs.
    shuffle(ships_items)
    for uid, ship in ships_items:
        pos, ship_halite = ship
        # Collect Halite (50% probability when cell halite > ship_halite).
        if board.shipyards[pos] == -1 and halite[pos] > ship_halite and randint(0,1) == 1:
            continue
        # Convert to Shipyard (50% probability when no shipyards, 5% otherwise).
        if board.shipyards[pos] == -1 and player_halite >= config.convertCost and randint(0, 20 if len(shipyards) else 1) == 1:
            player_halite -= config.convertCost
            board.convert(uid)
            continue
        # Move Ship (random between all available directions).
        move_choices = [None]
        for direction in ["NORTH", "EAST", "SOUTH", "WEST"]:
            to_pos = get_to_pos(size, pos, direction)
            # Enemy shipyard present.
            if board.shipyards[to_pos] != obs.player and board.shipyards[to_pos] != -1:
                continue
            # Larger ship most likely staying in place.
            if board.ships[to_pos] is not None and board.ships[to_pos]["halite"] >= ship_halite:
                continue
            # Weigh the direction based on number of possible larger ships that could be present.
            weight = 6
            if board.ships[to_pos] is not None and board.ships[to_pos]["player_index"] == obs.player:
                weight -= 1
            for s in board.possible_ships[to_pos].values():
                if s["halite"] > ship_halite:
                    weight -= 1
            move_choices += [direction] * weight
        move = choice(move_choices)
        if move is not None:
            board.move(uid, move)
            
    # Spawn ships (30% probability when possible, or 100% if no ships).
    for uid, pos in shipyards.items():
        if board.ships[pos] is None and player_halite >= config.spawnCost and (randint(0, 2) == 2 or len(ships_items) == 0):
            player_halite -= config.spawnCost
            board.spawn(uid)

    return board.action


agents = {"random": random_agent}


def interpreter(state, env):
    obs = state[0].observation
    config = env.configuration
    size = env.configuration.size

    # Update step index.
    obs.step = len(env.steps)

    # UID generator.
    uid_counter = 0

    def create_uid():
        nonlocal uid_counter
        uid_counter += 1
        return f"{obs.step}-{uid_counter}"

    # Initialize the board (place cell halite and starting ships).
    if env.done:
        # Set step for initialization to 0.
        obs.step = 0
        # Distribute Halite evenly into quartiles.
        half = math.ceil(size / 2)
        grid = [[0] * half for _ in range(half)]

        # Randomly place a few halite "seeds".
        for i in range(half):
            # random distribution across entire quartile
            grid[randint(0, half-1)][randint(0, half-1)] = i ** 2

            # as well as a particular distribution weighted toward the center of the map
            grid[randint(half//2, half-1)][randint(half//2, half-1)] = i ** 2

        # Spread the seeds radially.
        radius_grid = copy.deepcopy(grid)
        for r in range(half):
            for c in range(half):
                value = grid[r][c]
                if value == 0:
                    continue

                # keep initial seed values, but constrain radius of clusters
                radius = min(round((value / half) ** 0.5), 1)
                for r2 in range(r-radius+1, r+radius):
                    for c2 in range(c-radius+1, c+radius):
                        if 0 <= r2 < half and 0 <= c2 < half:
                            distance = (abs(r2-r) ** 2 + abs(c2-c) ** 2) ** 0.5
                            radius_grid[r2][c2] += int(value / max(1, distance) ** distance)

        # add some random sprouts of halite
        radius_grid = np.asarray(radius_grid)
        add_grid = np.random.gumbel(0, 300.0, size=(half, half)).astype(int)
        sparse_radius_grid = np.random.binomial(1, 0.5, size=(half, half))
        add_grid = np.clip(add_grid, 0, a_max=None) * sparse_radius_grid
        radius_grid += add_grid

        # add another set of random locations to the center corner
        corner_grid = np.random.gumbel(0, 500.0, size=(half//4, half//4)).astype(int)
        corner_grid = np.clip(corner_grid, 0, a_max=None)
        radius_grid[half - (half//4):, half - (half//4):] += corner_grid

        # Normalize the available halite against the defined configuration starting halite.
        total = sum([sum(row) for row in radius_grid])
        obs.halite = [0] * (size ** 2)
        for r, row in enumerate(radius_grid):
            for c, val in enumerate(row):
                val = int(val * config.halite / total / 4)
                obs.halite[size * r + c] = val
                obs.halite[size * r + (size - c - 1)] = val
                obs.halite[size * (size - 1) - (size * r) + c] = val
                obs.halite[size * (size - 1) - (size * r) +
                           (size - c - 1)] = val

        # Distribute the starting ships evenly.
        num_agents = len(state)
        starting_positions = [0] * num_agents
        if num_agents == 1:
            starting_positions[0] = size * (size // 2) + size // 2
        elif num_agents == 2:
            starting_positions[0] = size * (size // 2) + size // 4
            starting_positions[1] = size * \
                (size // 2) + math.ceil(3 * size / 4) - 1
        elif num_agents == 4:
            starting_positions[0] = size * (size // 4) + size // 4
            starting_positions[1] = size * (size // 4) + 3 * size // 4
            starting_positions[2] = size * (3 * size // 4) + size // 4
            starting_positions[3] = size * (3 * size // 4) + 3 * size // 4

        # Initialize the players.
        obs.players = []
        for i in range(num_agents):
            ships = {create_uid(): [starting_positions[i], 0]}
            obs.players.append([state[0].reward, {}, ships])

        return state

    spawn_moves = set()

    # Apply actions to create an updated observation.
    for index, agent in enumerate(state):
        player_halite, shipyards, ships = obs.players[index]
        if agent.action is None:
            continue
        for uid, action in agent.action.items():
            # Shipyard action (spawn ship):
            if action == "SPAWN":
                if uid in shipyards and player_halite >= config.spawnCost:
                    ships[create_uid()] = [shipyards[uid], 0]
                    player_halite -= int(config.spawnCost)
                continue
            # Ship Actions. Ship must be present.
            elif uid not in ships:
                continue
            ship_pos, ship_halite = ships[uid]

            # Create a Shipyard.
            if action == "CONVERT":
                if player_halite >= config.convertCost - ship_halite and ship_pos not in shipyards.values():
                    # Must have enough halite and must not be in a shipyard spot to convert
                    shipyards[create_uid()] = ship_pos
                    player_halite += int(ship_halite - config.convertCost)
                    obs.halite[ship_pos] = 0
                    del ships[uid]
                continue

            # Move Ship Actions.
            to_pos = get_to_pos(size, ship_pos, action)
            ships[uid] = [to_pos, int(ship_halite * (1 - config.moveCost))]

        # Update the player.
        obs.players[index] = [player_halite, shipyards, ships]

    # Detect collisions
    # 1. Ships into Foreign Shipyards.
    # 2. Ships into Ships.
    board = [[-1, {}, -1] for _ in range(size ** 2)]
    for index, agent in enumerate(state):
        if agent.status != "ACTIVE":
            continue
        _, shipyards, ships = obs.players[index]
        for uid, shipyard_pos in shipyards.items():
            board[shipyard_pos][0] = index
            board[shipyard_pos][2] = uid
        for uid, ship in ships.items():
            board[ship[0]][1][uid] = index
    for pos, cell in enumerate(board):
        shipyard, ships, shipyard_uid = cell
        # Detect Ship Collisions
        if len(ships) > 1:
            smallest_ships = [[i, uid, obs.players[i][2][uid][1]] for uid, i in ships.items()]
            smallest_ships.sort(key=lambda s: s[2])
            for i, l_ship in enumerate(smallest_ships):
                player_index, uid, ship_halite = l_ship
                # Remove collided ships.
                if i > 0 or ship_halite == smallest_ships[i+1][2]:
                    del ships[uid]
                    del obs.players[player_index][2][uid]
                # Reduce halite available with remaining ship.
                else:
                    obs.players[player_index][2][uid][1] += smallest_ships[i+1][2]
        # Detect Shipyard Collisions.
        if shipyard > -1:
            enemy_occupied = any(x != shipyard for x in ships.values())
            if enemy_occupied:
                del obs.players[shipyard][1][shipyard_uid]
                for uid, index in list(ships.items()):
                    del ships[uid]
                    del obs.players[index][2][uid]

    # Remove players with invalid status or insufficient potential.
    for index, agent in enumerate(state):
        player_halite, shipyards, ships = obs.players[index]
        if agent.status == "ACTIVE" and len(ships) == 0 and (len(shipyards) == 0 or player_halite < config.spawnCost):
            # Agent can no longer gather any halite
            agent.status = "DONE"
        if agent.status != "ACTIVE":
            obs.players[index] = [0, {}, {}]

    # Collect and Regenerate Halite.
    asset_positions = []
    for index, agent in enumerate(state):
        player_halite, shipyards, ships = obs.players[index]
        shipyard_positions = shipyards.values()
        asset_positions.extend(shipyard_positions)
        for uid, ship in ships.items():
            ship_pos, ship_halite = ship
            asset_positions.append(ship_pos)
            # Collect halite from ships into shipyards.
            if ship_pos in shipyard_positions:
                obs.players[index][0] += ship_halite
                ship[1] = 0
            # Collect halite from cells into ships, ensure ship didn't move this turn.
            elif obs.halite[ship_pos] * config.collectRate >= 1 and uid not in agent.action:
                # Ship halite is int based, so drop off that bit of fractional halite
                collect_halite = math.floor(obs.halite[ship_pos] * config.collectRate)
                obs.halite[ship_pos] -= collect_halite
                ship[1] += collect_halite
    for pos, halite in enumerate(obs.halite):
        if pos in asset_positions:
            continue
        obs.halite[pos] = min(500, halite * (1 + config.regenRate))

    # Check if done (< 2 players and num_agents > 1)
    if len(state) > 1 and sum(1 for agent in state if agent.status == "ACTIVE") < 2:
        for agent in state:
            if agent.status == "ACTIVE":
                agent.status = "DONE"

    # Update Rewards.
    for index, agent in enumerate(state):
        if agent.status == "ACTIVE" or agent.status == "DONE":
            agent.reward = obs.players[index][0]
        else:
            agent.reward = 0

    return state


def renderer(state, env):
    config = env.configuration
    size = config.size
    obs = state[0].observation

    board = [[h, -1, -1, -1] for h in obs.halite]
    for index, player in enumerate(obs.players):
        _, shipyards, ships = player
        for shipyard_pos in shipyards.values():
            board[shipyard_pos][1] = index
        for ship in ships.values():
            ship_pos, ship_halite = ship
            board[ship_pos][2] = index
            board[ship_pos][3] = ship_halite

    col_divider = "|"
    row_divider = "+" + "+".join(["----"] * size) + "+\n"

    out = row_divider
    for row in range(size):
        for col in range(size):
            _, _, ship, ship_halite = board[col + row * size]
            out += col_divider + (
                f"{min(int(ship_halite), 99)}S{ship}" if ship > -1 else ""
            ).ljust(4)
        out += col_divider + "\n"
        for col in range(size):
            halite, shipyard, _, _ = board[col + row * size]
            if shipyard > -1:
                out += col_divider + f"SY{shipyard}".ljust(4)
            else:
                out += col_divider + str(min(int(halite), 9999)).rjust(4)
        out += col_divider + "\n" + row_divider

    return out


dir_path = path.dirname(__file__)
json_path = path.abspath(path.join(dir_path, "halite.json"))
with open(json_path) as json_file:
    specification = json.load(json_file)


def html_renderer():
    js_path = path.abspath(path.join(dir_path, "halite.js"))
    with open(js_path) as js_file:
        return js_file.read()
