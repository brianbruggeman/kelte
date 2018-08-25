#!/usr/bin/env python
import random
from dataclasses import astuple, dataclass, field
from typing import Generic, Dict, Iterable, List, Optional, Tuple, TypeVar, Union

import numpy

import tcod as tdl

from kelte import typeface


class Jsonable:

    def __json__(self):
        data = {}
        for key in self.__annotations__.keys():
            value = getattr(self, key)
            if hasattr(value, '__json__'):
                value = value.__json__
            data[key] = value
        return data


class ByteInteger(Jsonable):

    def __init__(self, value=0, name='value'):
        self._name = name
        self._value = self._validate_value(value, name)

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        self._value = self._validate_value(value, self.name)

    def __set_name__(self, owner, name):
        self._name = name
        setattr(owner, name, self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f'`name` is not of type str')
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Union[float, int]):
        if not isinstance(value, (float, int)):
            raise TypeError(f'`value` is not of type `float` or `int`: {value} | {value!r}')
        self._validate_value(value, self.name)

    @staticmethod
    def _validate_value(value, name):
        if value is None:
            value = 0
        elif not isinstance(value, (int, float)):
            raise TypeError(f'{name} must be of type `int` or `float` but is {value!r}.')
        elif isinstance(value, int) and not (0 <= value <= 255):
            raise ValueError(f'{name} must be between 0 and 255')
        elif isinstance(value, float):
            if not (0.0 <= value <= 1.0):
                raise ValueError(f'{name} must be between 0 and 255')
            value = int(value * 255)
        return value

class Renderable:

    def render(self, *args, **kwds):
        raise NotImplementedError


@dataclass
class Position(Jsonable):
    x: int = 0
    y: int = 0

    def __add__(self, other_position):
        try:
            x, y = other_position
        except TypeError:
            x, y = (0, 0)
        return Position(self.x + x, self.y + y)

    def __eq__(self, other_position):
        x, y = other_position
        return self.x == x and self.y == y

    def __hash__(self):
        return hash(astuple(self))

    def __iter__(self):
        yield from astuple(self)

    def __len__(self):
        return 2

    def __lt__(self, other):
        x, y = other
        return (self.x, self.y) < (x, y)

    def __sub__(self, other_position):
        x, y = other_position
        return Position(self.x - x, self.y - y)


@dataclass
class Size(Jsonable):
    width: int = 0
    height: int = 0

    def __get__(self, instance, owner):
        return self

    def __set__(self, instance, value):
        self.width, self.height = value

    def __set_name__(self, owner, name):
        setattr(owner, name, self)

    def __hash__(self):
        return hash(astuple(self))

    def __iter__(self):
        yield from astuple(self)

    def __len__(self):
        return len(astuple(self))

    def __contains__(self, item):
        contained = False
        if isinstance(item, Position):
            x, y = item
            if 0 <= y < self.height:
                if 0 <= x < self.width:
                    contained = True
        elif isinstance(item, Room):
            if all(0 <= y < self.height for y in [item.shape.y1, item.shape.y2]):
                if all(0 <= x < self.width for x in [item.shape.x1, item.shape.x2]):
                    contained = True
        return contained


@dataclass
class Color(Jsonable):
    red: Union[int, float, ByteInteger] = ByteInteger(0)
    green: Union[int, float, ByteInteger] = ByteInteger(0)
    blue: Union[int, float, ByteInteger] = ByteInteger(0)
    alpha: Union[int, float, ByteInteger] = ByteInteger(255)
    name: Optional[str] = None

    @property
    def rgb(self):
        return self.red, self.green, self.blue

    @property
    def rgba(self):
        return self.red, self.green, self.blue, self.alpha

    @property
    def term_bg(self):
        import sty
        return sty.bg(self.red, self.green, self.blue)

    @property
    def term_fg(self):
        import sty
        return sty.fg(self.red, self.green, self.blue)

    @property
    def term_reset_bg(self):
        import sty
        return sty.bg.rs

    @property
    def term_reset_fg(self):
        import sty
        return sty.fg.rs

    def __get__(self, instance, owner):
        return self

    def __iter__(self):
        yield from astuple(self)

    def __len__(self):
        return len(astuple(self))

    def __set__(self, instance, value):
        if len(value) == 3:
            self.red, self.green, self.blue = value
        if len(value) == 4:
            self.red, self.green, self.blue, self.alpha = value

    def __set_name__(self, owner, name):
        setattr(owner, name, self)


T = TypeVar('T')


@dataclass
class Node(Generic[T]):
    id: Optional[T] = None
    edges: List = field(default_factory=list)
    data: Dict = field(default_factory=dict)

    def __hash__(self):
        return hash(astuple(self))

    @property
    def neighbors(self) -> Iterable:
        for edge in self.edges:
            if edge.start == self:
                yield edge.end
            elif edge.end == self:
                yield edge.start


@dataclass
class Edge(Generic[T]):
    id: Tuple[T, T] = None
    start: Optional[Node] = None
    end: Optional[Node] = None
    data: Dict = field(default_factory=dict)

    def __hash__(self):
        return hash(astuple(self))


@dataclass
class Shape:
    anchor: Position = field(default_factory=Position)

    # post init
    points: List[Position] = field(init=False, repr=False)
    area: int = field(init=False)
    center: Position = field(default_factory=Position)

    def __hash__(self):
        return hash(astuple(self))

    def __iter__(self):
        raise NotImplementedError


@dataclass
class Rectangle(Shape):
    size: Size = field(default_factory=Size)
    padding: int = 1

    # post init
    width: int = 0
    height: int = 0
    center: Position = field(default_factory=Position)
    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0

    def __contains__(self, item):
        contained = False
        if isinstance(item, Room):
            item = item.shape
        if isinstance(item, (list, tuple, Position)):
            x, y = item
            if self.x1 <= x < self.x2 and self.y1 <= y < self.y2:
                contained = True
        elif isinstance(item, Rectangle):
            start_padding = min(0, self.padding)
            end_padding = min(0, self.padding - 1)
            if any(self.x1 - start_padding <= x < self.x2 + end_padding for x in [item.x1, item.x2]):
                if any(self.y1 - start_padding <= y < self.y2 + end_padding for y in [item.y1, item.y2]):
                    contained = True
        return contained

    def __hash__(self):
        return hash(astuple(self))

    def __iter__(self):
        for position in self.points:
            yield position

    def __post_init__(self):
        self.area = self.size.width * self.size.height
        self.width = self.size.width
        self.height = self.size.height
        self.x1 = self.anchor.x
        self.y1 = self.anchor.y
        self.x2 = self.anchor.x + self.size.width
        self.y2 = self.anchor.y + self.size.height
        self.center = Position(
            abs(self.x1 - self.x2) // 2 + self.x1,
            abs(self.y1 - self.y2) // 2 + self.y1,
            )
        start_padding = min(0, self.padding)
        end_padding = min(0, self.padding - 1)
        self.points = [
            Position(x, y)
            for x in range(self.x1 + start_padding, self.x2 - (end_padding - 1))
            for y in range(self.y1 + start_padding, self.y2 - (end_padding - 1))
            ]


@dataclass
class Tile:
    name: str = 'empty'
    character: Optional[str] = None
    code: Optional[int] = None

    lit_foreground_color: Color = Color(127, 127, 127)
    lit_background_color: Color = Color(20, 20, 20)
    unlit_foreground_color: Color = Color(96, 96, 96)
    unlit_background_color: Color = Color(0, 0, 0)

    def __post_init__(self):
        if self.character is None and self.code is None:
            self.character = ' '
            self.code = ord(self.character)

        elif self.character is None and self.code is not None:
            self.character = chr(self.code)

        elif self.character is not None and self.code is None:
            self.code = ord(self.character)

    def __hash__(self):
        return hash(astuple(self))


@dataclass
class Pane:
    name: str = 'main'
    size: Size = field(default_factory=Size)
    id: Optional[int] = None
    title: Optional[str] = None
    default_foreground: Color = field(default=Color(127, 127, 127))
    default_background: Color = field(default_factory=Color)

    data: Dict[Position, Optional[Tuple[str, Color, Color]]] = field(default_factory=dict)

    def __post_init__(self):
        for y in range(self.size.height):
            for x in range(self.size.width):
                pos = Position(x, y)
                self.data[pos] = None

        if self.name == 'main':
            self.id = tdl.console_init_root(self.size.width, self.size.height, self.title, False)
        else:
            self.id = tdl.console_new(self.size.width, self.size.height)

        tdl.console_set_default_foreground(self.id, self.default_foreground.rgb)
        tdl.console_set_default_background(self.id, self.default_background.rgb)

    def blit(self, other, anchor: Optional[Position] = None, offset: Optional[Position] = None):
        other_console = other.id if isinstance(other, Pane) else other
        x, y = anchor or Position()
        xdst, ydst = offset or Position()
        tdl.console_blit(
            src=self.id,
            x=x, y=y, w=self.size.width, h=self.size.height,
            dst=other_console, xdst=xdst, ydst=ydst,
            ffade=1.0,
            bfade=0.0,
            )
        for y in range(self.size.height):
            for x in range(self.size.width):
                pos = Position(x, y)
                val = self.data[pos]
                if val:
                    offset_pos = pos + offset
                    if offset_pos not in other.data:
                        continue
                    other.data[offset_pos] = val

    def clear(self):
        tdl.console_clear(self.id)

    def render(self, position: Position, character: str, foreground: Optional[Color] = None, background: Optional[Color] = None):
        foreground = foreground or self.default_foreground
        background = background or self.default_background
        x, y = position
        # 1 call - doesn't let us set the background with a flag - maybe that's not important?
        tdl.console_put_char_ex(self.id, x, y, character, foreground.rgb, background.rgb)
        self.data[Position(x, y)] = (character, foreground, background)

        # 3 calls - let's us set the background differently (see: http://roguecentral.org/doryen/data/libtcod/doc/1.4.2/console/bkgnd_flag.html)
        # background_flag = tdl.BKGND_SET  # if background.alpha == 255 else tdl.BKGND_OVERLAY
        # tdl.console_set_char_foreground(self.id, x, y, foreground.rgb)
        # tdl.console_set_char_background(self.id, x, y, background.rgb, background_flag)
        # tdl.console_set_char(self.id, x, y, character)

    def __str__(self):
        lines = []
        for y in range(self.size.height):
            row = []
            for x in range(self.size.width):
                pos = Position(x, y)
                val = self.data[pos]
                if val:
                    character, fore, back = val
                    row.append(f'{fore.term_fg}{back.term_bg}{character}{back.term_reset_bg}{fore.term_reset_fg}')
            lines.append(''.join(row))
        return '\n'.join(lines)


@dataclass
class Cell(Renderable):
    blocked: bool = True
    blocked_sight: bool = True
    lit: bool = False

    position: Position = field(default_factory=Position)
    entities: List = field(default_factory=list)

    tile: Tile = field(default_factory=Tile)
    character: Optional[str] = None
    lit_foreground_color: Optional[Color] = None
    lit_background_color: Optional[Color] = None
    unlit_foreground_color: Optional[Color] = None
    unlit_background_color: Optional[Color] = None

    def __post_init__(self):
        # copy the tile defaults to the cell.  But let the cell
        # be updated.  Not memory efficient, but easily more functional
        self.character = self.character if self.character is not None else self.tile.character
        self.lit_foreground_color = self.tile.lit_foreground_color
        self.lit_background_color = self.tile.lit_background_color
        self.unlit_foreground_color = self.tile.unlit_foreground_color
        self.unlit_background_color = self.tile.unlit_background_color

    @property
    def foreground_color(self):
        return self.lit_foreground_color if self.lit else self.unlit_foreground_color

    @foreground_color.setter
    def foreground_color(self, color: Color):
        if self.lit:
            self.lit_foreground_color = color
        else:
            self.unlit_foreground_color = color

    @property
    def background_color(self):
        return self.lit_background_color if self.lit else self.unlit_background_color

    @background_color.setter
    def background_color(self, color: Color):
        if self.lit:
            self.lit_background_color = color
        else:
            self.lit_background_color = color

    def render(self, pane: Pane, offset: Optional[Position] = None):
        new_position = self.position + offset if offset is not None else self.position
        pane.render(
            position=new_position,
            character=self.character,
            foreground=self.foreground_color,
            background=self.background_color,
            )

    def __getattr__(self, item):
        return getattr(self.tile, item)

    def __str__(self):
        character = f'{self.foreground_color.term_fg}{self.background_color.term_bg}{self.character}{self.foreground_color.term_reset_fg}{self.background_color.term_reset_bg}'
        return character


@dataclass
class Entity(Renderable):
    name: Optional[str] = None
    position: Position = field(default_factory=Position)
    tile: Cell = field(default_factory=Cell)

    @property
    def background_color(self):
        return self.tile.background_color

    @background_color.setter
    def background_color(self, value):
        self.tile.background_color = value

    @property
    def foreground_color(self):
        return self.tile.foreground_color

    @foreground_color.setter
    def foreground_color(self, value):
        self.tile.foreground_color = value

    @property
    def character(self):
        return self.tile.character

    @character.setter
    def character(self, value):
        self.tile.character = value

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def clear(self, pane: Pane, offset: Optional[Position] = None, empty=None):
        offset = offset or Position()
        empty = empty or ' '
        position = self.position + offset
        pane.render(position=position, character=empty, foreground=self.tile.foreground_color, background=self.tile.background_color)

    def move(self, offset: Position):
        # TODO: How do we handle rendering here?
        self.position += offset

    def move_to(self, position: Position):
        # TODO: How do we handle rendering here?
        self.position = position

    def render(self, pane: Pane, offset: Optional[Position] = None):
        self.tile.render(pane, offset=offset)

    def __hash__(self):
        return hash(astuple(self))


class Graph:
    pass


@dataclass
class Grid(Node, Rectangle, Renderable):

    cells: Dict[Position, Node] = field(default_factory=dict)
    entities: Dict[Position, Node] = field(default_factory=dict)

    updates: Dict[Position, Renderable] = field(default_factory=dict)

    def clear(self, pane: Pane, offset: Optional[Position] = None):
        self.updates = {}

    def render(self, pane: Pane, offset: Position):
        for position, item in self.updates.items():
            if isinstance(item, Renderable):
                item.render(pane=pane, offset=offset)

        self.clear(pane=pane, offset=offset)


@dataclass
class Room(Node):
    shape: Shape = field(default_factory=Rectangle)

    def connect_to(self, other):
        if isinstance(other, Room):
            Tunnel(self, other)

    @property
    def points(self):
        return self.shape.points

    @property
    def center(self):
        return self.shape.center

    @property
    def anchor(self):
        return self.shape.anchor

    @anchor.setter
    def anchor(self, position: Position):
        self.shape.anchor = position

    @property
    def area(self):
        return self.shape.area

    @area.setter
    def area(self, size: Size):
        self.shape.area = size

    def __contains__(self, item):
        return item in self.shape

    def __hash__(self):
        return hash(astuple(self))

    def __iter__(self):
        for pos in self.shape:
            yield pos


@dataclass
class Tunnel(Edge):
    start: Room = field(default_factory=Room)
    end: Room = field(default_factory=Room)

    def __hash__(self):
        return hash(astuple(self))

    def __post_init__(self):
        self.start.edges.append(self)
        self.end.edges.append(self)


@dataclass
class Level(Renderable):
    size: Size = field(default_factory=Size)
    tiles: List[List[Cell]] = field(default_factory=list, repr=False)
    grid: Graph = field(default_factory=Graph)
    center: Position = field(init=False)
    entities: Dict[Position, Entity] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        self.center = Position(self.size.width // 2, self.size.height // 2)
        self.clear()

    def __contains__(self, position):
        x, y = position
        if 0 <= x < self.size.width:
            if 0 <= y < self.size.height:
                return True

    def __getitem__(self, item):
        return self.get(item)

    def __iter__(self):
        if not self.tiles:
            self.clear()
        for y, row in enumerate(self.tiles):
            for x, cell in enumerate(row):
                yield Position(x, y), cell

    def clear(self) -> List[List[Cell]]:
        wall_tile = Tile(character='#', lit_foreground_color=Color(100, 100, 100))
        self.tiles = [
            [Cell(blocked=True, blocked_sight=True, position=Position(x, y), tile=wall_tile) for x in range(self.size.width)]
            for y in range(self.size.height)
            ]
        return self.tiles

    def get(self, item):
        if isinstance(item, (tuple, list, Position)):
            x, y = item
            return self.tiles[y][x]
        else:
            raise TypeError(f'{item!r} must be of type: tuple, list or Position')

    def is_blocked(self, position):
        x, y = position
        return self.tiles[y][x].blocked

    def is_opaque(self, position):
        x, y = position
        return self.tiles[y][x].blocked_sight

    def is_transparent(self, position):
        x, y = position
        return not self.tiles[y][x].blocked_sight

    def is_walkable(self, position):
        x, y = position
        return not self.tiles[y][x].blocked

    def render(self, pane, offset: Optional[Position] = None):
        offset = offset or Position()
        for position, cell in self:
            cell.render(pane, offset=offset)

    def set(self, item, value):
        if isinstance(item, (tuple, list, Position)):
            x, y = item
            self.tiles[y][x] = value
        else:
            raise TypeError(f'{item!r} must be of type: tuple, list or Position')

    def update(self, item):
        if isinstance(item, dict):
            for position, tile in item.items():
                x, y = position
                self.tiles[y][x] = tile

    def __setitem__(self, item, value):
        return self.set(item, value)

    def __str__(self):
        tiled = []
        for y, row in enumerate(self.tiles):
            new_row = ''
            for x, cell in enumerate(row):
                new_row += str(cell)
            tiled.append(new_row)
        return '\n'.join(tiled)


@dataclass
class Config:
    title: str = 'Basic Tutorial'

    font_name: Optional[str] = None
    font_layout: Optional[str] = None
    font_size: Optional[int] = None
    flags: int = tdl.lib.TCOD_FONT_LAYOUT_ASCII_INROW | tdl.lib.TCOD_FONT_TYPE_GREYSCALE
    font: Optional[typeface.Typeface] = None

    renderer: int = tdl.lib.TCOD_RENDERER_GLSL
    fps: int = 10
    fullscreen: bool = False

    seed: Optional[int] = None

    screen_size: Optional[Size] = None
    map_size: Optional[Size] = None
    message_size: Optional[Size] = None
    status_size: Optional[Size] = None

    room_max_size: int = 10
    room_min_size: int = 6
    max_rooms_per_level: int = 10

    debug: Optional[bool] = None
    verbose: Optional[int] = None

    def __post_init__(self):
        self.font_name = self.font_name or 'Deferral-Square'
        self.font_layout = self.font_layout or 'cp437'
        self.font_size = self.font_size or 18

        self.seed = self.seed or random.randint(1, 2 ** 16)

        self.screen_size = self.screen_size or Size(width=80, height=50)
        self.status_size = self.status_size or Size(width=20, height=self.screen_size.height)
        self.message_size = self.message_size or Size(width=self.screen_size.width - self.status_size.width, height=5)
        self.map_size = self.map_size or Size(width=self.screen_size.width - self.status_size.width, height=self.screen_size.height - self.message_size.height)


@dataclass
class State(Renderable):
    config: Config = field(default_factory=Config)

    panes: dict = field(default_factory=dict)

    colors: Dict[str, tdl.Color] = field(default_factory=dict)
    levels: List[Level] = field(default_factory=list)
    level: int = 0

    round: int = 0
    round_updated: Optional[bool] = None
    restart: bool = False

    messages: list = field(default_factory=list)

    @property
    def entities(self):
        return self.levels[self.level].entities

    @property
    def current_level(self):
        return self.levels[self.level]

    @property
    def player(self):
        return self.entities['player']

    @property
    def tf(self):
        return self.config.font

    @property
    def entity_pane(self):
        return self.panes['entity']

    @property
    def main_pane(self):
        return self.panes['main']

    @property
    def map_pane(self):
        return self.panes['map']

    @property
    def message_pane(self):
        return self.panes['message']

    @property
    def status_pane(self):
        return self.panes['status']

    def add_entity(self, name: str, x: Optional[int] = None, y: Optional[int] = None, char: Optional[str] = None, color: tdl.Color = None) -> Entity:
        entity = Entity()
        entity.name = name if name is not None else entity.name

        x = x if x is not None else entity.x
        y = y if y is not None else entity.y
        entity.position = Position(x, y)
        entity.character = char if char is not None else entity.character
        entity.color = color if color is not None else entity.color

        self.entities[name] = entity
        return entity

    def render(self):
        # Clear first not last.
        for pane in self.panes.values():
            pane.clear()

        main_pane = self.main_pane
        # offset = self.player.position - Rectangle(size=main_pane.size).center

        # build panes
        map_pane = self.panes['map']
        # self.current_level.render(pane=map_pane, offset=offset)
        self.current_level.render(pane=map_pane)

        entity_pane = self.panes['entity']
        for entity_name, entity in self.entities.items():
            # entity.render(pane=entity_pane, offset=offset)
            entity.render(pane=entity_pane)

        # message_pane = self.panes['message']
        # message_pane_size = self.config.message_size
        # render_messages(message_pane, message_pane_size, self)

        # status_pane = state.panes['status']
        # render_status(status_pane, state)

        # map panes to sub panes
        entity_pane.blit(map_pane)
        map_pane.blit(main_pane)
        # message_pane.blit(main_pane)
        # status_pane.blit(main_pane)

        # Flush last after everything is resolved
        tdl.console_flush()


def cycle(state: State, key, mouse):
    # capturing the user input _before_ rendering is required for some
    #   reason for libtcod to actually render the initial screen
    user_input = handle_user_input(state, key, mouse)
    if user_input:
        return user_input

    if state.round_updated or state.round == 0:
        state.round_updated = False
        state.render()
        state.round += 1


def clear_all(pane, state):
    for entity in state.entities.values():
        entity.clear(pane)


def connect_positions(start: Position, end: Position) -> Position:

    horizontal_then_vertical = True if random.randint(0, 1) else False
    start_x, end_x = min(start.x, end.x), max(start.x, end.x) + 1
    start_y, end_y = min(start.y, end.y), max(start.y, end.y) + 1

    if horizontal_then_vertical:
        yield from [
            Position(x, start.y)
            for x in range(start_x, end_x)
            ]
        yield from [
            Position(end.x, y)
            for y in range(start_y, end_y)
            ]

    else:
        yield from [
            Position(start.x, y)
            for y in range(start_y, end_y)
            ]
        yield from [
            Position(x, end.y)
            for x in range(start_x, end_x)
            ]


def create_level(state: State, map_size: Optional[Size] = None, rooms: dict = None) -> (Level, list):
    rooms = rooms or {}
    map_size = map_size or state.config.map_size

    level = Level(size=map_size)

    room_tiles = {}

    for attempt in range(state.config.max_rooms_per_level):
        room, tiles = create_room(config=state.config)
        if any(room in r for r in rooms.values()):
            continue
        if room not in padded(map_size, padding=1):
            continue

        rooms[room.center] = room
        room_tiles.update(tiles)

    connections = {}
    for room_center in rooms:
        room_distances = sorted((distance(room_center, center), center)
                                for center in rooms
                                if center not in connections
                                if center != room_center)

        room_distances = room_distances[0:random.randint(1, 3)]
        for d, r_center in room_distances:
            connections.setdefault(room_center, []).append(r_center)

    floor_tile = Tile(character='.')
    for room_center, others in connections.items():
        for other_center in others:
            room = rooms[room_center]
            other = rooms[other_center]
            room.connect_to(other)
            start_point = random.choice(room.points)
            end_point = random.choice(other.points)

            for pos in connect_positions(start_point, end_point):
                room_tiles[pos] = Cell(blocked=False, blocked_sight=False, position=pos, tile=floor_tile)

    level.update(room_tiles)
    return level, rooms


def create_room(config: Config, size: Optional[Size] = None, anchor: Position = None) -> tuple:
    max_room_size = config.room_max_size
    min_room_size = config.room_min_size

    if not size:
        width, height = [random.randint(min_room_size, max_room_size) for _ in range(2)]
        size = Size(width, height)

    if not anchor:
        map_width, map_height = config.map_size
        x = random.randint(size.width + 1, map_width - size.width)
        y = random.randint(size.height + 1, map_height - size.height)
        anchor = Position(x, y)

    rect = Rectangle(anchor=anchor, size=size)
    room = Room(shape=rect)

    tiles = {}
    floor_tile = Tile(character='.')
    for pos in room:
        tiles[pos] = Cell(blocked=False, blocked_sight=False, position=pos, tile=floor_tile)
    return room, tiles


def distance(a, b):
    ax, ay = a
    bx, by = b
    euclidean_distance = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
    return euclidean_distance


def display_key(key):
    print(f'{key.c} pressed={key.pressed} alt={key.lalt or key.ralt} ctr={key.lctrl or key.rctrl} shift={key.shift}')


def handle_keyboard_input(key):
    move = handle_movement_input(key)
    if move:
        return move

    if key.vk in [tdl.KEY_TEXT, tdl.KEY_CHAR]:
        if key.lalt or key.ralt:
            mappers = {
                'r': {'restart': True},
                'n': {'new': True},
                's': {'save': True},
                'l': {'load': True},
                }
            value = mappers.get(key.text, None) or mappers.get(chr(key.c), None)
            if value:
                return value

    if key.vk == tdl.KEY_ENTER:
        if key.lalt or key.ralt:
            return {'fullscreen': True}
        else:
            display_key(key)

    if key.vk == tdl.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_movement_input(key):
    # Libtcod origin is top left of the screen
    #   Each vector is x, y or width, height

    # Cardinal
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    # Diagonal
    UP_LEFT = (-1, -1)
    UP_RIGHT = (1, -1)
    DOWN_LEFT = (-1, 1)
    DOWN_RIGHT = (1, 1)

    # No movement
    NONE = (0, 0)

    if key.vk == tdl.KEY_TEXT:
        movement_c_mapper = {
            # Cardinal directions
            'k': UP,
            'j': DOWN,
            'h': LEFT,
            'l': RIGHT,
            # Diagonal directions
            'y': UP_LEFT,
            'u': UP_RIGHT,
            'b': DOWN_LEFT,
            'n': DOWN_RIGHT,
            # Wait a turn
            '.': NONE,
            }
        key_character = key.text
        move = movement_c_mapper.get(key_character)
    else:
        movement_vk_mapper = {
            # Keyboard arrows
            tdl.KEY_UP: UP,
            tdl.KEY_DOWN: DOWN,
            tdl.KEY_LEFT: LEFT,
            tdl.KEY_RIGHT: RIGHT,

            # Keypad
            tdl.KEY_1: DOWN_LEFT,
            tdl.KEY_2: DOWN,
            tdl.KEY_3: DOWN_RIGHT,
            tdl.KEY_4: LEFT,
            tdl.KEY_5: NONE,
            tdl.KEY_6: RIGHT,
            tdl.KEY_7: UP_LEFT,
            tdl.KEY_8: UP,
            tdl.KEY_9: UP_RIGHT,
            }
        move = movement_vk_mapper.get(key.vk)
    if move:
        return {'move': move}


def handle_user_input(state, key, mouse):
    tdl.sys_check_for_event(tdl.EVENT_KEY_PRESS, key, mouse)
    action = {}
    if key.vk != tdl.KEY_NONE:
        action = handle_keyboard_input(key)
    if not action:
        return

    move = action.get('move')
    if move:
        dx, dy = move
        player = state.player
        new_pos = player.x + dx, player.y + dy
        current_level = state.current_level
        if new_pos not in current_level:
            return

        blocked = state.current_level[new_pos].blocked
        if not blocked:
            for entity in state.entities.values():
                if entity == player:
                    continue
                if entity.position == new_pos:
                    blocked = True
                    break
        if not blocked:
            player.move(move)
        state.round_updated = True

    new = action.get('new')
    if new:
        state.config.seed = random.randint(1, 65535)
        state.restart = True
        return True

    restart = action.get('restart')
    if restart:
        state.restart = True
        return True

    exit_program = action.get('exit')
    if exit_program:
        return True

    fullscreen = action.get('fullscreen')
    if fullscreen:
        tdl.console_set_fullscreen(not tdl.console_is_fullscreen())
        # TODO: Figure out why the console is not drawing after a reset


def initialize(
        state: Optional[State] = None,
        config: Optional[Config] = None,
        seed: Optional[int] = None,
        fullscreen: Optional[bool] = None,
        font_name: Optional[str] = None,
        layout: Optional[str] = None,
        debug: Optional[bool] = None,
        verbose: Optional[int] = None,
        reinit: Optional[State] = None,
        ) -> State:
    if not state:
        if not config:
            cfg = {
                'debug': debug,
                'verbose': verbose,
                'seed': seed,
                'fullscreen': fullscreen,
                'font_name': font_name,
                'font_layout': layout
                }
            cfg = {k: v for k, v in cfg.items() if v is not None}
            config = Config(**cfg)
        state = state or State(config=config)

    random.seed(state.config.seed)
    state.config.font = typeface.Typeface(state.config.font_name)
    state.config.font.use(size=state.config.font_size, layout=state.config.font_layout)

    dark_brown = (36, 18, 5)
    dark_green = (18, 36, 5)

    state.colors = {
        'dark_wall': dark_brown,
        'dark_ground': dark_green,
        }

    if not reinit:
        tdl.sys_set_renderer(config.renderer)
        tdl.sys_set_fps(config.fps)

    state.panes['main'] = Pane('main', size=config.screen_size, title=config.title)
    state.panes['entity'] = Pane('entity', size=config.map_size)
    state.panes['map'] = Pane('map', size=config.map_size)
    state.panes['status'] = Pane('status', size=config.status_size)
    state.panes['message'] = Pane('message', size=config.message_size)

    starter_room = {}
    for attempt in range(2):
        level, rooms = create_level(state=state, rooms=starter_room)
        starter_room = random.choice(list(rooms.values()))
        starter_room = {starter_room.center: starter_room}
        state.levels.append(level)

    # levels must be created before entities can be added
    state.add_entity(
        'player',
        x=state.config.screen_size.width // 2, y=state.config.screen_size.height // 2,
        char=state.tf['@'], color=tdl.white
        )

    state.add_entity(
        'npc',
        x=state.config.screen_size.width // 2 - 5, y=state.config.screen_size.height // 2,
        char=state.tf['@'], color=tdl.yellow
        )

    if state.config.fullscreen:
        tdl.console_set_fullscreen(state.config.fullscreen)

    return state


def main(debug=None, verbose=None, seed=None, fullscreen=None, font_name=None, layout=None):
    key = tdl.Key()
    mouse = tdl.Mouse()

    restart = True
    reinit = None
    state = None
    while restart is True:
        state = initialize(state=reinit, debug=debug, verbose=verbose, seed=seed, fullscreen=fullscreen, font_name=font_name, layout=layout, reinit=state)
        play(state, key, mouse)
        restart = state.restart
        reinit = state


def padded(size: Size, padding: int = 0):
    if isinstance(padding, int):
        size = Size(size.width - padding * 2, size.height - padding * 2)
    return size


def play(state, key, mouse):

    # initial render
    state.render()
    tdl.console_flush()

    while not tdl.console_is_window_closed():
        if cycle(state=state, key=key, mouse=mouse):
            break


def render_all(state: State):
    # Clear first not last.
    for pane in state.panes.values():
        tdl.console_clear(pane)

    main_pane = state.main_pane

    # build panes
    map_pane = state.panes['map']
    render_level(map_pane, state)

    entity_pane = state.panes['entity']
    render_entities(entity_pane, state)

    message_pane = state.panes['message']
    message_pane_size = state.config.message_size
    render_messages(message_pane, message_pane_size, state)

    # status_pane = state.panes['status']
    # render_status(status_pane, state)

    # map panes to sub panes
    tdl.console_blit(
        src=entity_pane,
        x=0, y=0, w=state.config.map_size.width, h=state.config.map_size.height,
        dst=map_pane, xdst=0, ydst=0,
        ffade=1.0,
        bfade=0.0,
        )
    tdl.console_blit(
        src=map_pane,
        x=0, y=0, w=state.config.map_size.width, h=state.config.map_size.height,
        dst=main_pane, xdst=0, ydst=0,
        ffade=1.0,
        bfade=1.0,
        )

    # Flush last after everything is resolved
    tdl.console_flush()


def render_entities(pane: Pane, state: State, offset: Position = None):
    offset = offset or Position()
    for entity in state.entities.values():
        # render_tile(pane, new_position, entity.character, foreground=entity.foreground_color)
        entity.render(pane=pane, offset=offset)


def render_level(pane: int, state: State, level: Optional[Level] = None, offset: Optional[Position] = None):
    count = 0
    level = level or state.current_level
    offset = offset or (0, 0)
    print(level)
    for position, tile in level:
        color = state.colors.get('dark_ground')
        floor_index = 250
        character = chr(floor_index)
        if tile.blocked or tile.blocked_sight:
            color = state.colors.get('dark_wall')
            wall_index = 176
            character = chr(wall_index)
        offset_position = position + offset
        if offset_position in level:
            render_tile(pane, position, character, background=color)
            count += 1


def render_messages(pane: int, pane_size: Size, state: State):
    for y, message in state.messages:
        for x, character in enumerate(message):
            pos = Position(x, y)
            render_tile(pane, pos, character)
            if x >= pane_size.width:
                break
        if y >= pane_size.height:
            break


def render_status(pane: int, state: State):
    pass


def render_tile(pane: int, position: Position, character: str, foreground: tuple = None, background: tuple = None):
    default_foreground = (127, 127, 127)
    foreground = foreground or default_foreground
    tdl.console_set_char_foreground(pane, position.x, position.y, foreground)
    if background:
        tdl.console_set_char_background(pane, position.x, position.y, background, tdl.BKGND_SET)
    tdl.console_set_char(pane, position.x, position.y, character)


if __name__ == '__main__':
    import click

    @click.command()
    @click.option('-l', '--layout', type=click.Choice(['all', 'cp437', 'cp850', 'cp866']), default='cp437', show_default=True)
    @click.option('-f', '--font-name', metavar='NAME')
    @click.option('-d', '--debug', is_flag=True)
    @click.option('-v', '--verbose', count=True)
    @click.option('-s', '--seed', metavar='SEED', type=int)
    @click.option('-w', '--windowed', is_flag=True, default=None)
    def cli(debug, verbose, seed, windowed, font_name, layout):
        fullscreen = not windowed if windowed is not None else None
        main(debug=debug, verbose=verbose, seed=seed, fullscreen=fullscreen, font_name=font_name, layout=layout)

    cli()
