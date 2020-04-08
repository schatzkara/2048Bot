from graphics import Graphics
from bot import Bot
import constants as c
import keyboard

bot = True
heuristic = c.MULTIATTRIBUTE
look_ahead = 4
trials = 1
log = True

if __name__ == "__main__":
    # Graphics(bot=bot, heuristic=heuristic, look_ahead=look_ahead, trials=trials, log=log)

    heuristics = [c.TWONEAREMPTY, c.MOSTMERGES, c.MOSTMERGESAVAIL,
                  c.HIGHCORNER, c.MONOTONIC, c.TWONEAREMPTY]

    for h in heuristics:
        for x in range(5):
            b = Bot(size=c.BOARD_SIZE, start_tiles=c.INIT_TILES,
                    look_ahead=1, trials=trials, heuristic=c.RANDOM,
                    log=log)
            b.play()
