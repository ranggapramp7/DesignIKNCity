from PIL import Image, ImageTk
import tkinter as tk
import random

# Ukuran peta
MAP_SIZE = 150
CELL_SIZE = 32  # Ukuran gambar per cell

# Konstanta berbagai jenis jalan
EMPTY = 0
ROAD = 'road'
CROSSROAD = 'crossroad'
SIMPANG = 'simpang'
TIKUNGAN = 'tikungan'

# Jumlah jenis jalan
CROSSROAD_LIMIT = 9
SIMPANG_LIMIT = 24
TIKUNGAN_LIMIT = 32

# Jarak minimal antar jalan
MIN_DISTANCE = 5

# Konstanta ukuran bangunan
BIG_BUILDING = 'big_building'
MEDIUM_BUILDING = 'medium_building'
SMALL_BUILDING = 'small_building'
HOUSE = 'house'
TREE = 'tree'

# Ukuran bangunan
BUILDING_SIZES = {
    BIG_BUILDING: (10, 5),
    MEDIUM_BUILDING: (5, 3),
    SMALL_BUILDING: (2, 2),
    HOUSE: (1, 2),
    TREE: (1, 1)
}

# Source images
building_images = {
    BIG_BUILDING: 'big_building.png',
    MEDIUM_BUILDING: 'medium_building.png',
    SMALL_BUILDING: 'small_building.png',
    HOUSE: 'house.png',
    TREE: 'tree.png'
}

# Jumlah Bangunan
BUILDING_MINIMUMS = {
    BIG_BUILDING: 50,
    MEDIUM_BUILDING: 120,
    SMALL_BUILDING: 270,
    HOUSE: 530,
    TREE: 600
}

class MapGenerator:
    def __init__(self, size):
        self.size = size
        self.map = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.generate_map()
    
    def generate_map(self):
        # Clear the map
        self.map = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        crossroad_count = 0
        simpang_count = 0
        tikungan_count = 0

        while crossroad_count < CROSSROAD_LIMIT or simpang_count < SIMPANG_LIMIT or tikungan_count < TIKUNGAN_LIMIT:
            x = random.randint(1, self.size - 2)
            y = random.randint(1, self.size - 2)
            if self.map[x][y] == EMPTY and self.is_location_valid(x, y):
                if crossroad_count < CROSSROAD_LIMIT:
                    self.map[x][y] = CROSSROAD
                    self.extend_road(x, y, 'up')
                    self.extend_road(x, y, 'down')
                    self.extend_road(x, y, 'left')
                    self.extend_road(x, y, 'right')
                    crossroad_count += 1
                elif simpang_count < SIMPANG_LIMIT:
                    direction = random.choice(['up', 'down', 'left', 'right'])
                    if direction == 'up':
                        self.map[x][y] = 'simpang_bawah'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'right')
                    elif direction == 'down':
                        self.map[x][y] = 'simpang_atas'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'right')
                    elif direction == 'left':
                        self.map[x][y] = 'simpang_kanan'
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'down')
                    elif direction == 'right':
                        self.map[x][y] = 'simpang_kiri'
                        self.extend_road(x, y, 'right')
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'down')
                    simpang_count += 1
                elif tikungan_count < TIKUNGAN_LIMIT:
                    direction = random.choice(['up-right', 'up-left', 'down-right', 'down-left'])
                    if direction == 'up-right':
                        self.map[x][y] = 'kiri_bawah'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'right')
                    elif direction == 'up-left':
                        self.map[x][y] = 'kanan_bawah'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'left')
                    elif direction == 'down-right':
                        self.map[x][y] = 'kiri_atas'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'right')
                    elif direction == 'down-left':
                        self.map[x][y] = 'kanan_atas'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'left')
                    tikungan_count += 1

        self.place_buildings()
        self.place_trees()

    def is_location_valid(self, x, y, width=1, height=1):
        for i in range(max(0, x - MIN_DISTANCE), min(self.size, x + width + MIN_DISTANCE)):
            for j in range(max(0, y - MIN_DISTANCE), min(self.size, y + height + MIN_DISTANCE)):
                if self.map[i][j] != EMPTY:
                    return False
        return True

    def extend_road(self, x, y, direction):
        if direction == 'up':
            for i in range(x-1, -1, -1):
                if self.map[i][y] != EMPTY:
                    break
                self.map[i][y] = 'vertical_road'
        elif direction == 'down':
            for i in range(x+1, self.size):
                if self.map[i][y] != EMPTY:
                    break
                self.map[i][y] = 'vertical_road'
        elif direction == 'left':
            for j in range(y-1, -1, -1):
                if self.map[x][j] != EMPTY:
                    break
                self.map[x][j] = 'horizontal_road'
        elif direction == 'right':
            for j in range(y+1, self.size):
                if self.map[x][j] != EMPTY:
                    break
                self.map[x][j] = 'horizontal_road'

    def place_buildings(self):
        for building, minimum in BUILDING_MINIMUMS.items():
            if building == TREE:
                continue
            count = 0
            while count < minimum:
                x = random.randint(0, self.size - BUILDING_SIZES[building][0])
                y = random.randint(0, self.size - BUILDING_SIZES[building][1])
                if self.is_location_valid_for_building(x, y, BUILDING_SIZES[building][0], BUILDING_SIZES[building][1]):
                    for i in range(x, x + BUILDING_SIZES[building][0]):
                        for j in range(y, y + BUILDING_SIZES[building][1]):
                            self.map[i][j] = building
                    count += 1

    def place_trees(self):
        count = 0
        while count < BUILDING_MINIMUMS[TREE]:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.map[x][y] == EMPTY:
                self.map[x][y] = TREE
                count += 1

    def is_location_valid_for_building(self, x, y, width, height):
        # Check if any cell in the proposed area is a road or another building
        for i in range(x, x + width):
            for j in range(y, y + height):
                if i >= 0 and i < self.size and j >= 0 and j < self.size:
                    if self.map[i][j] != EMPTY:
                        return False
        # Check the surrounding cells for roads within 1 cell distance
        road_found = False
        for i in range(max(0, x - 1), min(self.size, x + width + 1)):
            for j in range(max(0, y - 1), min(self.size, y + height + 1)):
                if self.map[i][j] in ['vertical_road', 'horizontal_road', 'crossroad', 'simpang_bawah', 'simpang_atas', 'simpang_kanan', 'simpang_kiri', 'kiri_bawah', 'kanan_bawah', 'kiri_atas', 'kanan_atas']:
                    road_found = True
                # Ensure a minimum distance of 2 cells from other buildings
                if i in range(x, x + width) and j in range(y, y + height):
                    continue
                if self.map[i][j] in BUILDING_SIZES:
                    return False
        return road_found

    def get_map(self):
        return self.map

class MapDisplay(tk.Frame):
    def __init__(self, parent, map_data):
        super().__init__(parent)
        self.parent = parent
        self.map_data = map_data

        # Load images
        self.images = {
            'vertical_road': ImageTk.PhotoImage(Image.open("Source/vertical_road.png")),
            'horizontal_road': ImageTk.PhotoImage(Image.open("Source/horizontal_road.png")),
            'crossroad': ImageTk.PhotoImage(Image.open("Source/crossroad.png")),
            'simpang_bawah': ImageTk.PhotoImage(Image.open("Source/simpang_bawah.png")),
            'simpang_atas': ImageTk.PhotoImage(Image.open("Source/simpang_atas.png")),
            'simpang_kanan': ImageTk.PhotoImage(Image.open("Source/simpang_kanan.png")),
            'simpang_kiri': ImageTk.PhotoImage(Image.open("Source/simpang_kiri.png")),
            'kanan_atas': ImageTk.PhotoImage(Image.open("Source/kanan_atas.png")),
            'kanan_bawah': ImageTk.PhotoImage(Image.open("Source/kanan_bawah.png")),
            'kiri_bawah': ImageTk.PhotoImage(Image.open("Source/kiri_bawah.png")),
            'kiri_atas': ImageTk.PhotoImage(Image.open("Source/kiri_atas.png")),
            BIG_BUILDING: ImageTk.PhotoImage(Image.open(f"Source/building_images/{building_images[BIG_BUILDING]}")),
            MEDIUM_BUILDING: ImageTk.PhotoImage(Image.open(f"Source/building_images/{building_images[MEDIUM_BUILDING]}")),
            SMALL_BUILDING: ImageTk.PhotoImage(Image.open(f"Source/building_images/{building_images[SMALL_BUILDING]}")),
            HOUSE: ImageTk.PhotoImage(Image.open(f"Source/building_images/{building_images[HOUSE]}")),
            TREE: ImageTk.PhotoImage(Image.open(f"Source/decor/{building_images[TREE]}")),
            'grass': ImageTk.PhotoImage(Image.open("Source/grass.png"))  
        }

        # Frame untuk kanvas peta dan tombol
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Kanvas untuk menampilkan peta dengan scrollbars
        self.canvas = tk.Canvas(self.main_frame, bg="white", scrollregion=(0, 0, MAP_SIZE * CELL_SIZE, MAP_SIZE * CELL_SIZE))
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        
        self.hbar = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky=tk.EW)
        self.vbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky=tk.NS)
        
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.draw_map()

        # Frame untuk tombol
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=2, padx=10, pady=10, sticky=tk.N)
        self.redesign_button = tk.Button(self.button_frame, text="Re-design", command=self.redesign_map)
        self.redesign_button.pack()

    def draw_map(self):
        self.canvas.delete("all")
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                cell_type = self.map_data[i][j]
                if cell_type in self.images:
                    if cell_type in BUILDING_SIZES:
                        building_size = BUILDING_SIZES[cell_type]
                        if self.is_top_left_of_building(i, j, building_size):
                            self.canvas.create_image(j * CELL_SIZE, i * CELL_SIZE, anchor=tk.NW, image=self.images[cell_type])
                    else:
                        self.canvas.create_image(j * CELL_SIZE, i * CELL_SIZE, anchor=tk.NW, image=self.images[cell_type])
                else:
                    self.canvas.create_image(j * CELL_SIZE, i * CELL_SIZE, anchor=tk.NW, image=self.images['grass'])

    def is_top_left_of_building(self, i, j, building_size):
        if i + building_size[0] <= MAP_SIZE and j + building_size[1] <= MAP_SIZE:
            for x in range(building_size[0]):
                for y in range(building_size[1]):
                    if self.map_data[i + x][j + y] != self.map_data[i][j]:
                        return False
            return True
        return False

    def redesign_map(self):
        # Generate new map data
        map_generator = MapGenerator(MAP_SIZE)
        self.map_data = map_generator.get_map()
        # Redraw map
        self.draw_map()

def main():
    root = tk.Tk()
    root.title("Random Map Generator")

    map_generator = MapGenerator(MAP_SIZE)
    map_data = map_generator.get_map()
    map_display = MapDisplay(root, map_data)
    map_display.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
