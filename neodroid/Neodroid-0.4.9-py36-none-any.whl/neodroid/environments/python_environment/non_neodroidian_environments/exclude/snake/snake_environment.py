#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 10/02/2020
           '''

from dataclasses import dataclass
from enum import Enum
from random import sample, randint

import cv2
import gym
import numpy
from gym import spaces
from gym.envs.classic_control import rendering
from gym.utils import play

def _rotate_image(cv_image, _rotation_angle):
  axes_order = (1, 0, 2) if len(cv_image.shape) == 3 else (1, 0)
  if _rotation_angle == -90:
    return numpy.transpose(cv_image, axes_order)[:, ::-1]

  if _rotation_angle == 90:
    return numpy.transpose(cv_image, axes_order)[::-1, :]

  if _rotation_angle in [-180, 180]:
    return cv_image[::-1, ::-1]

  return cv_image


@dataclass(eq=True, frozen=True)
class Point:
  x: int
  y: int

  def copy(self, xincr, yincr):
    return Point(self.x + xincr, self.y + yincr)

  def __repr__(self):
    return f"(x: {self.x}, y: {self.y})"

  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)


class SnakeGame:
  class SnakeState(Enum):
    OK = 1
    ATE = 2
    DEAD = 3
    WON = 4

  dir_map_to_angle = {
    Point(0, -1):0,
    Point(0, 1): 180,
    Point(-1, 0):90,
    Point(1, 0): -90,
    }

  sprites = {
    'head': cv2.imread('sprites/head.png', 0),
    'body': cv2.imread('sprites/body.png', 0),
    'turn': cv2.imread('sprites/turn.png', 0),
    'fruit':cv2.imread('sprites/fruit.png', 0),
    'tail': cv2.imread('sprites/tail.png', 0),
    }

  class Snake:
    action_dir_order = ['right', 'up', 'left', 'down']

    action_dir_map = {
      'up':   Point(0, -1),
      'down': Point(0, 1),
      'left': Point(-1, 0),
      'right':Point(1, 0),
      }

    def __init__(self):
      self.head = Point(0, 0)
      self.tail = []
      self.tail_size = 2
      self.direction = Point(1, 0)  # Need to add validation later
      self.dir_idx = 0

    def self_collision(self):
      for t in self.tail:
        if self.head.x == t.x and self.head.y == t.y:
          return True
      return False

    def update(self):
      new_head = self.head.copy(self.direction.x, self.direction.y)

      self.tail.append(self.head)  # OK direction? or do I need to add this to the top?
      self.head = new_head

    def shed(self):
      self.tail = self.tail[-self.tail_size:]

    def __repr__(self):
      return f"""Head: {self.head}
          Tail: {self.tail}
          Dir: {self.direction}
          """

    def apply_turn(self, turn_dir):
      if not turn_dir:
        return
      assert turn_dir in ['left', 'right']
      shift = 1 if turn_dir == 'left' else -1
      self.dir_idx = (self.dir_idx + shift) % 4
      action = self.action_dir_order[self.dir_idx]
      self.apply_direction(new_dir=action)

    def apply_direction(self, new_dir=None):
      if not new_dir:
        return
      assert new_dir in self.action_dir_map, f"Unknown direction {new_dir}"

      self.direction = self.action_dir_map[new_dir]

  def __init__(self, grid_size=10, main_gs=10, num_fruits=10):
    self.gs = grid_size
    self.subgrid_loc = None
    self.main_gs = main_gs
    self.num_fruits = num_fruits
    self.reset()

    self.update()

  def reset(self):
    self.step = 0
    self.last_ate = 0
    grid_size = self.gs
    self.subgrid_loc = Point(randint(0, self.main_gs - self.gs), randint(0, self.main_gs - self.gs))
    #if grid_size == 38:
    #  self.subgrid_loc = Point(1, 1)
    self.snake = self.Snake()
    self.snake.head = Point(self.gs // 2, self.gs // 2)

    pos_list = []
    for i in range(grid_size):
      for j in range(grid_size):
        pos_list.append(Point(i, j))

    self.pos_set = set(pos_list)
    self.fruit_locations = []
    self.set_fruits()

  @property
  def stamina(self):
    a = self.gs ** 2
    stamina = a + len(self.snake.tail) + 1
    stamina = min(a * 2, stamina)
    return stamina

  def update(self, direction=None):
    self.last_ate += 1
    snake = self.snake
    self.snake.apply_direction(direction)
    self.snake.update()
    out_enum = self.SnakeState.OK

    if snake.head in self.fruit_locations:
      self.fruit_locations.pop(self.fruit_locations.index(snake.head))
      self.last_ate = 0
      try:
        self.set_fruits()
        self.snake.tail_size += 1
        out_enum = self.SnakeState.ATE
      except IndexError:
        out_enum = self.SnakeState.WON
      if len(self.fruit_locations) == 0:
        out_enum = self.SnakeState.WON
    self.snake.shed()
    if not self._bounds_check(snake.head) or self.snake.self_collision():
      out_enum = self.SnakeState.DEAD
    elif self.last_ate > self.stamina:
      out_enum = self.SnakeState.DEAD

    return out_enum

  @property
  def fruit_loc(self):
    return self.fruit_locations

  def set_fruits(self):
    snake = self.snake
    snake_locs = set([snake.head] + snake.tail + self.fruit_locations)
    possible_positions = self.pos_set.difference(snake_locs)
    diff = self.num_fruits - len(self.fruit_locations)
    new_locs = sample(list(possible_positions), k=min(diff, len(possible_positions)))
    self.fruit_locations.extend(new_locs)

  def _bounds_check(self, pos):
    return pos.x >= 0 and pos.x < self.gs and pos.y >= 0 and pos.y < self.gs

  def to_image(self):
    snake = self.snake
    fl = self.fruit_loc
    scale = 8

    full_canvas = numpy.zeros((self.main_gs * scale, self.main_gs * scale), 'uint8')
    h, w = self.gs * 8, self.gs * 8
    canvas = full_canvas[self.subgrid_loc.y * scale:self.subgrid_loc.y * scale + h,
             self.subgrid_loc.x * scale:self.subgrid_loc.x * scale + w]
    canvas += 64

    def apply_rotation(im, angle):
      return _rotate_image(im, angle)

    def draw_sprite(canvas, y, x, stype, scale=8, rotation=0):
      s = scale
      canvas[y * s:(y + 1) * s, x * s:(x + 1) * s] = apply_rotation(self.sprites[stype], rotation)

    for f in fl:
      draw_sprite(canvas, f.y, f.x, 'fruit')

    if self._bounds_check(snake.head):
      draw_sprite(canvas, snake.head.y, snake.head.x, 'head',
                  rotation=self.dir_map_to_angle[self.snake.direction])

    limbs = [snake.head] + list(reversed(snake.tail))
    for nxt, curr, prev in zip(limbs, limbs[1:], limbs[2:]):
      d2 = curr - prev
      d1 = nxt - curr
      if d1 == d2:
        draw_sprite(canvas, curr.y, curr.x, 'body',
                    rotation=self.dir_map_to_angle[d2])
        continue

      rotation = None

      d2 = curr - prev
      d1 = nxt - curr

      if (d1.x > 0 and d2.y < 0) or (d1.y > 0 and d2.x < 0):
        rotation = 0
      elif (d1.y > 0 and d2.x > 0) or (d1.x < 0 and d2.y < 0):
        rotation = -90
      elif (d1.x > 0 and d2.y > 0) or (d1.y < 0 and d2.x < 0):
        rotation = 90
      elif (d1.y < 0 and d2.x > 0) or (d1.x < 0 and d2.y > 0):
        rotation = 180

      if rotation is not None:
        draw_sprite(canvas, curr.y, curr.x, 'turn',
                    rotation=rotation)

    if len(limbs) > 1:
      draw_sprite(canvas, limbs[-1].y, limbs[-1].x, 'tail',
                  rotation=self.dir_map_to_angle[limbs[-2] - limbs[-1]])

    return full_canvas


KEYWORD_TO_KEY = {
  (ord('j'),):1,
  (ord('l'),):2,
  }

action_map = {
  0:None,
  1:'left',
  2:'right'
  }

reward_map = {
  SnakeGame.SnakeState.OK:  -0.01,
  SnakeGame.SnakeState.ATE: 1,
  SnakeGame.SnakeState.DEAD:-1,
  SnakeGame.SnakeState.WON: 1
  }


class SnakeGymEnvironment(gym.Env):
  metadata = {'render.modes':['human', 'rgb_array']}

  def __init__(self, gs=10, main_gs=10, num_fruits=10, action_map=None):
    super().__init__()
    self.env = SnakeGame(gs, main_gs=main_gs, num_fruits=num_fruits)
    self.viewer = None
    self.action_map = {
      0:'up',
      1:'down',
      2:'left',
      3:'right'
      }
    if action_map is not None:
      self.action_map = action_map

    self.action_space = spaces.Discrete(len(self.action_map.keys()))
    self.observation_space = spaces.Box(
      low=0, high=255, shape=(self.env.gs, self.env.gs, 3),
      dtype=numpy.uint8)

  def step(self, action):
    enum = self.env.update(self.action_map[action])

    # if enum != SnakeState.DED:
    rew = reward_map[enum]
    # else:
    #     rew = reward_map[enum]*(self.env.gs**2)

    # rew /= (self.env.gs**2)

    is_done = (enum in [SnakeGame.SnakeState.DEAD, SnakeGame.SnakeState.WON])
    info_dict = {}
    if is_done:
      rew *= len(self.env.snake.tail) * 0.1
      info_dict['score'] = len(self.env.snake.tail)

    return numpy.expand_dims(self.env.to_image().astype('float32'), -1), rew, is_done, info_dict

  def reset(self):
    self.env.reset()
    return numpy.expand_dims(self.env.to_image().astype('float32'), -1)

  def render(self, mode='human', close=False):
    im = self.env.to_image()
    if mode == 'human':
      if self.viewer is None:
        self.viewer = rendering.SimpleImageViewer(maxwidth=640)
        self.viewer.height = 640
        self.viewer.width = 640

      im = cv2.resize(im, (640, 640), interpolation=0)
      im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)

      self.viewer.imshow(im)
      return self.viewer.isopen
    elif mode == 'jack':
      if self.viewer is None:
        self.viewer = rendering.SimpleImageViewer(maxwidth=640)
        self.viewer.height = 640
        self.viewer.width = 640

      self.viewer.imshow(cv2.resize(self.env.to_image(), (640, 640), interpolation=0))
      return self.viewer.isopen
    else:
      return cv2.cvtColor(cv2.resize(im, (640, 640), interpolation=0), cv2.COLOR_GRAY2BGR)




'''
if __name__ == '__main__':
  import cv2

  # s = Snake()
  env = SnakeGame(4)

  cv2.imwrite('/home/jack/test.png', cv2.resize(env.to_image(), (640, 640), interpolation=cv2.INTER_NEAREST))

  while True:
    n = input()
    print(env.update(n))
    cv2.imwrite('/home/jack/test.png',
                cv2.resize(env.to_image(), (640, 640), interpolation=cv2.INTER_NEAREST))

  # env controls the snake now

  # env.set_fruits(s)

  # for i in range(50):
  #     s.update()
  #     assert env.bounds_check(s.head)

  # s.apply_direction('down')
  # s.update()

  # import cv2

'''

if __name__ == '__main__':


  action_map = {
    0:None,
    1:'up',
    2:'down',
    3:'left',
    4:'right'
    }

  KEYWORD_TO_KEY = {
    (ord('i'),):1,
    (ord('j'),):3,
    (ord('k'),):2,
    (ord('l'),):4,
    }

  def callback(obs_t, obs_tp1, action, rew, done, info):
    try:
      callback.rew += rew
    except Exception:
      callback.rew = rew
    print(callback.rew)

  try:
    gym.envs.register(id="snakenv-v0", entry_point='snake_environment:SnakeGymEnvironment')
  except Exception:
    print('already done?')

  env = gym.make('snakenv-v0', gs=20, main_gs=40, action_map=action_map)
  play.keys_to_action = KEYWORD_TO_KEY
  play.play(env, fps=15, keys_to_action=KEYWORD_TO_KEY, callback=callback)
