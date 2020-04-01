BOARD_SIZE = 4
INIT_TILES = 2
LOOK_AHEAD = 1

RANDOM = 0
HIGHSCORE = 1
MOSTMERGES = 2
MOSTMERGESAVAIL = 3
HIGHCORNER = 4
MONOTONIC = 5
TWONEAREMPTY = 6
MULTIATTRIBUTE = 7

HIGH_TILE_IN_CORNER = 0
MONOTONIC_ROW = 1
TWO_NEAR_EMPTY_SPACE = 2

ATTRIBUTE_SCORES = {HIGH_TILE_IN_CORNER: 10,
                    MONOTONIC_ROW: 5,
                    TWO_NEAR_EMPTY_SPACE: 5}

LOG_FILES = {RANDOM: "log_random.txt",
             HIGHSCORE: "log_highscore.txt",
             MOSTMERGES: "log_mostmerges.txt",
             MOSTMERGESAVAIL: "log_mostmergesavail.txt",
             HIGHCORNER: "log_highcorner.txt",
             MONOTONIC: "log_monotonic.txt",
             TWONEAREMPTY: "log_twonearempty.txt",
             MULTIATTRIBUTE: "log_multiattribute.txt"}

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
TITLE_FONT = ("Arial", 30)
TILE_FONT = ("Arial", 40)
BOARD_COLOR = '#776e65'

TILE_WIDTH = 4
TILE_HEIGHT = 2
TILE_PADX = 5
TILE_PADY = 5

text_color_dict = {0: '#BDAD9E',
                   2: '#BDAD9E',
                   4: '#ede0c8',
                   8: '#f9f6f2',
                   16: '#f9f6f2',
                   32: '#f9f6f2',
                   64: '#f9f6f2',
                   128: '#f9f6f2',
                   256: '#f9f6f2',
                   512: '#f9f6f2',
                   1024: '#f9f6f2',
                   2048: '#f9f6f2'
                   }

tile_color_dict = {0: '#BDAD9E',
                   2: '#eee4da',
                   4: '#ede0c8',
                   8: '#f2b179',
                   16: '#f59563',
                   32: '#f67c5f',
                   64: '#f65e3b',
                   128: '#edcf72',
                   256: '#edcc61',
                   512: '#edc850',
                   1024: '#edc53f',
                   2048: '#edc22e'
                   }