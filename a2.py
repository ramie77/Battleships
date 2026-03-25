import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Optional

from support import *

# Implement the classes, methods & functions described in the task sheet here
class Weapon(object):

    def __init__(self) -> None:
        
        self._name = 'AbstractWeapon'
        self._symbol = WEAPON_SYMBOL
        self._effects = {}
        self._range = 0 

    def get_name(self) -> str:
        
        return self._name
    
    def get_symbol(self) -> str:
        
        return self._symbol

    def get_effect(self) -> dict[str, int]:
        
        return self._effects

    def get_targets(self, position: Position) -> list[Position]:

        if self._range == 0:
            
            return []

        else:

            Target_Positions = adjacent_positions(position, self._range)
            return Target_Positions

    def __str__(self) -> str:
        
        return self._name

    def __repr__(self) -> str:

        if self._symbol == WEAPON_SYMBOL:
            return 'Weapon()'

        else:
            return f'{self._name}()'
        
class PoisonDart(Weapon):

    def __init__(self) -> None:
        
        self._name = 'PoisonDart'
        self._symbol = POISON_DART_SYMBOL
        self._effects = {'poison': 2}
        self._range = 2

    def __repr__(self) -> str:
        
        return 'PoisonDart()'

class PoisonSword(Weapon):

    def __init__(self) -> None:
        
        self._name = 'PoisonSword'
        self._symbol = POISON_SWORD_SYMBOL
        self._effects = {'damage': 2, 'poison': 1}
        self._range = 1

    def __repr__(self) -> str:
        
        return 'PoisonSword()'

class HealingRock(Weapon):

    def __init__(self) -> None:
        
        self._name = 'HealingRock'
        self._symbol = HEALING_ROCK_SYMBOL
        self._effects = {'healing': 2}
        self._range = 2

    def __repr__(self) -> str:
        
        return 'HealingRock()'

class Tile():

    def __init__(self, symbol: str, is_blocking: bool) -> None:
        
        self._symbol = symbol
        self._is_blocking = is_blocking
        self._weapon = None

    def is_blocking(self) -> bool:
        
        return self._is_blocking

    def get_weapon(self) -> Optional[Weapon]:
        
        return self._weapon

    def set_weapon(self, weapon: Weapon) -> None:
        
        self._weapon = weapon

    def remove_weapon(self) -> None:
        
        self._weapon = None

    def __str__(self) -> str:
        
        return self._symbol

    def __repr__(self) -> str:
        
        return f"Tile('{self._symbol}', {self._is_blocking})"

def create_tile(symbol: str):
    """Creates a new Tile object according to the given symbol of Tile type

    Args:
        symbol (str): The symbol of the Tile type

    Returns:
        A Tile object

    """
    
    if symbol == WALL_TILE:
        
        return Tile(WALL_TILE, True)

    elif symbol in [POISON_DART_SYMBOL, POISON_SWORD_SYMBOL,
                    HEALING_ROCK_SYMBOL]:
        
        tile = Tile(' ', False)

        if symbol == POISON_DART_SYMBOL:
            
            tile.set_weapon(PoisonDart())

        elif symbol == POISON_SWORD_SYMBOL:
            
            tile.set_weapon(PoisonSword())

        elif symbol == HEALING_ROCK_SYMBOL:
            
            tile.set_weapon(HealingRock())

        return tile

    elif symbol == GOAL_TILE:
        
        return Tile(GOAL_TILE, False)

    else:
        return Tile(' ', False)

def create_slug(symbol: str):
    """Creates a new Slug subclass object according to the given symbol of Slug class

    Args:
        symbol (str): The symbol of a Slug subclass

    Returns:
        A Slug subclass object

    """

    if symbol == NICE_SLUG_SYMBOL:
        
        return NiceSlug()

    elif symbol == ANGRY_SLUG_SYMBOL:
        
        return AngrySlug()

    elif symbol == SCARED_SLUG_SYMBOL:
        
        return ScaredSlug()

def adjacent_positions(center, pos_range):
    """Finds the positions adjacent to the given position according to range of up, down, left and right.

    Args:
        center (Position): The central position of the adjacent positions
        pos_range (int): The range of adjacent positions away from the given position

    Returns:
        A list of positions that are adjacent to the given central position with range away from it.

    """
    
    adj_pos = []
    
    for step in range(1, pos_range + 1):

        for delta in POSITION_DELTAS:
        
            adj_pos.append((center[0] + step*delta[0],
                            center[1] + step*delta[1]))

    return adj_pos

def get_dist(position1, position2):
    """Finds the euclidean distance between two positions

    Args:
        position1 (Position): The first position to find the distance
        position2 (Position): The second position to find the distance

    Returns:
        The euclidean distance between the two positions

    """

    if not position1:
        
        position1 = (0, 0)

    if not position2:
        
        position2 = (0, 0)
        
    dist = ((position2[0] - position1[0])**2 +
            (position2[1] - position1[1])**2)**(1/2)
    
    return dist

class Entity():
    
    def __init__(self, max_health: int) -> None:
        
        self._name = 'Entity'
        self._health = max_health
        self._max_health = max_health
        self._symbol = ENTITY_SYMBOL
        self._poison = 0
        self._weapon = None

    def get_name(self) -> str:
        
        return self._name
    
    def get_symbol(self) -> str:
        
        return self._symbol

    def get_health(self) -> int:
        
        return self._health

    def get_poison(self) -> int:
        
        return self._poison

    def get_weapon(self) -> Optional[Weapon]:
        
        return self._weapon

    def equip(self, weapon: Weapon) -> None:
        
        self._weapon = weapon

    def get_weapon_targets(self, position: Position) -> list[Position]:

        if self._weapon:
            
            return self._weapon.get_targets(position)
        
        else:
            
            return []

    def get_weapon_effect(self) -> dict[str, int]:

        if self._weapon:
            
            return self._weapon.get_effect()
        
        else:
            
            return {}

    def apply_effects(self, effects: dict[str, int]) -> None:

        for effect, value in effects.items():

            if effect == 'healing':
                
                self._health += value

                if self._health > self._max_health:
                    
                    self._health = self._max_health

            if effect == 'damage':
                
                self._health -= value

                if self._health < 0:
                    
                    self._health = 0 

            if effect == 'poison':
                
                self._poison += value

    def apply_poison(self) -> None:
        
        if not self._poison == 0:
            
            self._health -= self._poison
            
            if self._health < 0:
                
                self._health = 0
                
            if self._poison != 0:
                
                self._poison -= 1

    def is_alive(self) -> bool:
        
        return bool(self._health)

    def __str__(self) -> str:
        
        return self._name

    def __repr__(self) -> str:
        
        return f"{self._name}({self._max_health})"

class Player(Entity):
    
    def __init__(self, max_health) -> None:
        
        Entity.__init__(self, max_health)
        self._name = 'Player'
        self._symbol = PLAYER_SYMBOL
        
class Slug(Entity):
    
    def __init__(self, max_health) -> None:
        
        Entity.__init__(self, max_health)
        self._name = 'Slug'
        self._symbol = SLUG_SYMBOL
        self._can_move = True

    def choose_move(self, candidates: list[Position], current_position: Position, player_position: Position) -> Position:
        
        raise NotImplementedError("Slug subclasses must implement a choose_move method.")

    def can_move(self) -> bool:
        
        return self._can_move

    def end_turn(self) -> None:
        
        self._can_move = not self._can_move

class NiceSlug(Slug):
    
    def __init__(self) -> None:
        
        Slug.__init__(self, 10)
        self._name = 'NiceSlug'
        self.equip(HealingRock())
        self._symbol = NICE_SLUG_SYMBOL

    def choose_move(self, candidates: list[Position], current_position: Position, player_position: Position) -> Position:
        
        return current_position

    def __repr__(self) -> str:
        
        return f"{self._name}()"

class AngrySlug(Slug):
    
    def __init__(self) -> None:
        
        Slug.__init__(self, 5)
        self._name = 'AngrySlug'
        self.equip(PoisonSword())
        self._symbol = ANGRY_SLUG_SYMBOL

    def choose_move(self, candidates: list[Position], current_position:
                    Position, player_position: Position) -> Position:
        closest_position = current_position
        min_distance = float("inf")

        for candidate in candidates:
            euclidean_distance = (
                (candidate[0] - player_position[0]) ** 2 +
                (candidate[1] - player_position[1]) ** 2) **0.5
            if (euclidean_distance < min_distance) or \
               (euclidean_distance == min_distance and
                candidate < closest_position):
                closest_position = candidate
                min_distance = euclidean_distance
        return closest_position

    """
    def choose_move(self, candidates: list[Position], current_position: Position, player_position: Position) -> Position:
        
        position = ()

        if not candidates:
            
            return current_position
        
        all_candidates = candidates + [current_position]

        #Returns the position closest to the player
        return min(all_candidates, key=lambda pos: get_dist(pos, player_position))
    """

    def __repr__(self) -> str:
        
        return f"{self._name}()"

class ScaredSlug(Slug):
    
    def __init__(self) -> None:
        
        Slug.__init__(self, 3)
        self._name = 'ScaredSlug'
        self.equip(PoisonDart())
        self._symbol = SCARED_SLUG_SYMBOL

    def choose_move(self, candidates: list[Position], current_position: Position, player_position: Position) -> Position:

        position = ()

        if not candidates:
            
            return current_position
        
        all_candidates = candidates + [current_position]

        #Returns the position furthest from the player
        return max(all_candidates, key=lambda pos: get_dist(pos, player_position))
        
    def __repr__(self) -> str:
        
        return f"{self._name}()"

class SlugDungeonModel():
    
    def __init__(self, tiles: list[list[Tile]], slugs: dict[Position, Slug], player: Player, player_position: Position) -> None:
        
        self._tiles = tiles
        self.slugs = slugs
        self._player = player
        self.player_position = player_position
        self._old_player_position = self.player_position

    def get_tiles(self) -> list[list[Tile]]:
        
        return self._tiles

    def get_slugs(self) -> dict[Position, Slug]:
        
        return self.slugs

    def get_player(self) -> Player:
        
        return self._player

    def get_player_position(self) -> Position:
        
        return self.player_position

    def get_tile(self, position: Position) -> Tile:
        
        return self._tiles[position[0]][position[1]]

    def get_dimensions(self) -> tuple[int, int]:
        
        return (len(self._tiles), len(self._tiles[0]))


    def get_valid_slug_positions(self, slug: Slug) -> list[Position]:

        if not slug.can_move():
            
            return []

        #Finding the position of the slug instance through the slug dictionary
        for slugs_pos, slugs in self.slugs.items():

            if slug == slugs and slug.is_alive():

                slug_position = slugs_pos
                
        adj_positions = adjacent_positions(slug_position, 1)
        move_positions = adj_positions.copy()

        for position in adj_positions:

            #Remove positions containing a Slug
            if position in self.slugs.keys() and position != slug_position: 

                move_positions.remove(position)

            #Remove positions containing a Player
            if position == self.player_position:

                move_positions.remove(position)

            #Remove positions that is non-blocking
            if self._tiles[position[0]][position[1]].is_blocking() == True:

                move_positions.remove(position)

        move_positions.insert(0, slug_position)

        return move_positions
        

    def perform_attack(self, entity: Entity, position: Position) -> None:

        #If entity doesn't have a weapon, return None
        if not entity.get_weapon():

            return

        else:

            if entity._symbol == PLAYER_SYMBOL: #Entity is Player
                
                for slugs_pos, slug in self.slugs.items():
                    
                    if slugs_pos in entity.get_weapon_targets(position):
                        
                        slug.apply_effects(entity.get_weapon_effect())

            elif self.player_position in entity.get_weapon_targets(position): #Entity is a Slug

                self._player.apply_effects(entity.get_weapon_effect())

       
    def end_turn(self) -> None:

        self._player.apply_poison()

        for slug in self.slugs.values():

           slug.apply_poison()

        slugs_copy = self.slugs.copy() #For iteration in loop
        new_slugs_dict = self.slugs.copy() #For updating with new state of slugs

        for slugs_pos, slugs in slugs_copy.items():

            if not slugs.is_alive():

                new_slugs_dict.pop(slugs_pos)
                self.slugs = new_slugs_dict.copy()
                self._tiles[slugs_pos[0]][slugs_pos[1]].set_weapon(slugs.get_weapon())
                
            else:
                
                if slugs.can_move():
                    
                    new_slugs_dict.pop(slugs_pos)
                    new_slug_pos = slugs.choose_move(self.get_valid_slug_positions(slugs), slugs_pos, self._old_player_position)
                    new_slugs_dict[new_slug_pos] = slugs
                    self.slugs = new_slugs_dict.copy()

        for slugs_pos, slugs in self.slugs.items():

            self.perform_attack(slugs, slugs_pos)
            slugs.end_turn()

    def handle_player_move(self, position_delta: Position) -> None:

        self._old_player_position = self.player_position
        self._new_position = (self.player_position[0] + position_delta[0], self.player_position[1] + position_delta[1])

        #Check if player moves out of bound (out of the dimension of the board)
        if self._new_position in range(0, self.get_dimensions()[0]) and self._new_position[1] in range(0, self.get_dimensions()[1]):

            return

        #Player can move only when there is no wall or another entitity
        if  self.get_tile(self._new_position)._symbol != '#' and not self.get_slugs().get(self._new_position):

            self.player_position = self._new_position

            if self.get_tile(self.player_position).get_weapon():
                
                self._player.equip(self.get_tile(self.player_position).get_weapon())
                self.get_tile(self.player_position).remove_weapon()
     
            self.perform_attack(self._player, self.player_position)
            self.end_turn()
                                               
    def has_won(self) -> bool:

        #Finding the position of the goal tile
        for col in self._tiles:

            for row in col:

                if str(row) == GOAL_TILE:

                    G_position = self._tiles.index(col), col.index(row)

        #If every slug has died and player at goal            
        if not self.slugs and self.player_position == G_position:

            return True

        else:

            return False

    def has_lost(self) -> bool:

        return not self._player.is_alive()

def load_level(filename: str) -> SlugDungeonModel:
    """Loads a new level from a new file, updating the Slugs dictionary, player position and Tiles list.

    Args:
        filename (str): The name of the file of the new level to load

    Returns:
        A SlugDungeonModel object containing the loaded level Slugs ditionary, player position and Tiles list.

    """
    
    level = open(filename, "r")
    player = Player(int(level.readline().replace('\n', '')))
    tile_list = []
    slugs_dict = {}
    init_player_position = ()

    for row in level:

        tile_list.append(list(row.replace('\n', '')))

    level.close()

    tiles = []

    for row_index, row in enumerate(tile_list):

        tiles_column = []

        #Creating tiles according to the symbol in the text file
        for col_index, tile in enumerate(row):

            if tile in [NICE_SLUG_SYMBOL, ANGRY_SLUG_SYMBOL, SCARED_SLUG_SYMBOL]:

                slugs_dict[(row_index, col_index)] = create_slug(tile)

            elif tile == PLAYER_SYMBOL:

                init_player_position = (row_index, col_index)

            tiles_column.append(create_tile(tile))

        tiles.append(tiles_column)

    return SlugDungeonModel(tiles, slugs_dict, player, init_player_position)

##################################################################################################

class DungeonMap(AbstractGrid):

    def __init__(self, master, dimensions, size) -> None:

        super().__init__(master, dimensions, size)
        self.pack(side=tk.LEFT, anchor=tk.W, expand=True)

    def redraw(self, tiles: list[list[Tile]], player_position: Position, slugs: dict[Position, Slug]) -> None:

        self.clear()
        self._dimensions = (len(tiles), len(tiles[0]))
        self.config(bg=FLOOR_COLOUR, width=self._size[0], height=self._size[1])

        #Creatin grid and assigning color according to the symbol in the tiles list
        for x, row in enumerate(tiles):
            
            for y, col in enumerate(row):
                
                bbox = self.get_bbox((x, y))

                if str(col) == '#':
                    
                    self.create_rectangle(bbox[0], bbox[1], bbox[2], bbox[3], fill=WALL_COLOUR, outline='black')

                elif str(col) == 'G':
                    
                    self.create_rectangle(bbox[0], bbox[1], bbox[2], bbox[3], fill=GOAL_COLOUR, outline='black')

                elif col.get_weapon() != None:
                    
                    self.create_text(self.get_midpoint((x, y)), text=col.get_weapon().get_symbol(), font=REGULAR_FONT)

                else:
                    
                    self.create_rectangle(bbox[0], bbox[1], bbox[2], bbox[3], outline='black')

        #Creating circles in the grid according to the type of slugs
        for position, slug in slugs.items():

            bbox = self.get_bbox(position)
            self.create_oval(bbox[0], bbox[1], bbox[2], bbox[3], fill=SLUG_COLOUR, outline="black", width=1)

            if str(slug) == 'AngrySlug':
                
                text = 'Angry\nSlug'

            elif str(slug) == 'NiceSlug':
                
                text = 'Nice\nSlug'

            elif str(slug) == 'ScaredSlug':
                
                text = 'Scared\nSlug'
                
            self.create_text(self.get_midpoint(position), text=text, font=REGULAR_FONT)

        if player_position: #Player does exist

            bbox = self.get_bbox(player_position)
            self.create_oval(bbox[0], bbox[1], bbox[2], bbox[3], fill=PLAYER_COLOUR, outline="black", width=1)
            self.create_text(self.get_midpoint(player_position), text='Player', font=REGULAR_FONT)

class DungeonInfo(AbstractGrid):

    def __init__(self, master, dimensions, size) -> None:

        super().__init__(master, dimensions, size)
        self.pack()  

    def redraw(self, entities: dict[Position, Entity]) -> None:

        self.clear()

        #Creating labeles for each attributes
        self.create_text(self.get_midpoint((0,0)), text='Name', font=TITLE_FONT)
        self.create_text(self.get_midpoint((0,1)), text='Position', font=TITLE_FONT)
        self.create_text(self.get_midpoint((0,2)), text='Weapon', font=TITLE_FONT)
        self.create_text(self.get_midpoint((0,3)), text='Health', font=TITLE_FONT)
        self.create_text(self.get_midpoint((0,4)), text='Poison', font=TITLE_FONT)
        
        if type(entities) == dict: #Entity is Slugs

            x = 1
            for slug in entities.values():

                #Name
                self.create_text(self.get_midpoint((x,0)), text=slug, font=REGULAR_FONT)
                x += 1

            x = 1
            for slug_pos, slug in entities.items():

                #Position
                self.create_text(self.get_midpoint((x,1)), text=f"{slug_pos}", font=REGULAR_FONT)
                x += 1

            x = 1
            for slug in entities.values():

                #Weapon
                self.create_text(self.get_midpoint((x,2)), text=slug.get_weapon(), font=REGULAR_FONT)
                x += 1

            x = 1
            for slug in entities.values():

                #Health
                self.create_text(self.get_midpoint((x,3)), text=slug.get_health(), font=REGULAR_FONT)
                x += 1

            x = 1
            for slug in entities.values():

                #Poison
                self.create_text(self.get_midpoint((x,4)), text=slug.get_poison(), font=REGULAR_FONT)
                x += 1

        else: #Entity is a SlugDungeonModel

            self.create_text(self.get_midpoint((1,0)), text='Player', font=REGULAR_FONT)

            if entities.get_player(): #Player exists
                
                self.create_text(self.get_midpoint((1,1)), text=f"({entities.get_player_position()[0]}, {entities.get_player_position()[1]})", font=REGULAR_FONT)

            else: #Player does not exist
                
                self.create_text(self.get_midpoint((1,1)), text="None", font=REGULAR_FONT)

            weapon = entities.get_player().get_weapon()

            #If player dont have a weapon
            if not weapon:
                
                weapon = 'None'
                
            self.create_text(self.get_midpoint((1,2)), text=weapon, font=REGULAR_FONT)
            self.create_text(self.get_midpoint((1,3)), text=entities.get_player().get_health(), font=REGULAR_FONT)
            self.create_text(self.get_midpoint((1,4)), text=entities.get_player().get_poison(), font=REGULAR_FONT)
            
class ButtonPanel(tk.Frame):

    def __init__(self, root: tk.Tk, on_load: Callable, on_quit: Callable) -> None:

        super().__init__()

        self.config(width=900, height=100)
        self.pack(side=tk.TOP, fill=tk.X) 

        load_button = tk.Button(self, text="Load Game", command=on_load)
        load_button.pack(side=tk.LEFT, expand=True, ipady=10)

        quit_button = tk.Button(self, text="Quit", command=on_quit)
        quit_button.pack(side=tk.RIGHT, expand=True, ipady=10) 

class SlugDungeon():

    def __init__(self, root: tk.Tk, filename: str) -> None:

        root.title("Slug Dungeon")
        self._model = load_level(filename)
        self._old_model = self._model
        self._master = root
        self._filename = filename
        self._master.bind("<KeyPress>", self.handle_key_press)

        self._top_frame = tk.Frame(self._master)

        self.dungeon_map = DungeonMap(self._top_frame, self._model.get_dimensions(), DUNGEON_MAP_SIZE)
        self.dungeon_map.redraw(self._model.get_tiles(), self._model.get_player_position(), self._model.get_slugs())

        self.slugs_info = DungeonInfo(self._top_frame, (7, 5), SLUG_INFO_SIZE)
        self.slugs_info.redraw(self._model.get_slugs())

        self._top_frame.pack()

        self.player_info = DungeonInfo(self._master, (2, 5), PLAYER_INFO_SIZE)
        self.player_info.redraw(self._model)

        self._buttons = ButtonPanel(self._master, self.on_load, self.on_quit)
        
    def redraw(self) -> None:

        self._master.update()
        
        self.dungeon_map.redraw(self._model.get_tiles(), self._model.get_player_position(), self._model.get_slugs())
        self.slugs_info.redraw(self._model.get_slugs())
        self.player_info.redraw(self._model)
        
    def handle_key_press(self, event: tk.Event) -> None:

        self._master.update()

        if event.keysym == "a": #Move left

            self._model.handle_player_move((0, -1))
            
        elif event.keysym == "d": #Move right

            self._model.handle_player_move((0, 1))
            
        elif event.keysym == "w": #Move up

            self._model.handle_player_move((-1, 0))
            
        elif event.keysym == "s": #Move down

            self._model.handle_player_move((1, 0))

        elif event.keysym == "space": #Stay

            self._model.handle_player_move((0, 0))

        self.redraw()

        if self._model.has_won():

            self._master.update_idletasks()
            answer = messagebox.askyesno(WIN_TITLE, WIN_MESSAGE)
    
            if answer: #If 'play again
                
                self.load_level()
                
            else: #If not play again
                
                self.on_quit()

        if self._model.has_lost():

            self._master.update_idletasks()
            answer = messagebox.askyesno(LOSE_TITLE, LOSE_MESSAGE)
    
            if answer: #If play again

                self.load_level()
                
            else: #If not play again
                
                self.on_quit()

        self._master.update_idletasks()
            
    def load_level(self) -> None:

        #Replace current model with the new level's model
        self._model = load_level(self._filename)
        self.redraw()

    def on_load(self) -> None:

        #Prompt the user to insert a new level file
        self._filename = filedialog.askopenfilename(title="Select a File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        self.load_level()

    def on_quit(self) -> None:

        #Close the window
        self._master.destroy()
    
def play_game(root: tk.Tk, file_path: str) -> None:
    """Creates a new GUI according to the information of the model in the loaded level.

    """

    SlugDungeon(root, file_path)

def main() -> None:
    """Load a new level from a file then creates a new window with a GUI of the given level layout. 

    """
    
    # Implement your main function here
    root = tk.Tk()
    filename = "levels\\level1.txt"
    play_game(root, filename)
    root.mainloop()

if __name__ == "__main__":
    main()
