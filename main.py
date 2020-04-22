from graphics import Graphics
from bot import Bot
import constants as c
import keyboard

bot = True
heuristic = c.MULTIATTRIBUTE
look_ahead = 3
trials = 8
log = True

if __name__ == "__main__":
    Graphics(bot=bot, heuristic=heuristic, look_ahead=look_ahead, trials=trials, log=log)


    '''heuristics = [
    #     c.HIGHSCORE,
    #     c.MOSTMERGES,
    #     c.MOSTMERGESAVAIL,
    #     c.HIGHCORNER,
    #     c.MONOTONIC,
        c.TWONEAREMPTY,
        c.MULTIATTRIBUTE,
        c.MULTIATTRIBUTE_TURN]
    # heuristics = [c.MULTIATTRIBUTE_TURN]
    # look_aheads = [1,2,3,4]
    trials = [6, 8]  # [2, 4, 6, 8]
    #
    for h in heuristics:
    #     for l in look_aheads:
        for t in trials:
            for x in range(4):
                b = Bot(size=c.BOARD_SIZE, start_tiles=c.INIT_TILES,
                        look_ahead=3, trials=t, heuristic=h,
                        log=True)
                b.play()'''
