from graphics import Graphics
from bot import Bot
import constants as c
import keyboard

bot = True
heuristic = c.RANDOM
look_ahead = 1
trials = 1
log = True

if __name__ == "__main__":
    Graphics(bot=bot, heuristic=heuristic, look_ahead=look_ahead, trials=trials, log=log)


    '''heuristics = [
        c.HIGHSCORE,
        c.MOSTMERGES,
        c.MOSTMERGESAVAIL,
        c.HIGHCORNER,
        c.MONOTONIC,
        c.TWONEAREMPTY,
        c.MULTIATTRIBUTE,
        c.MULTIATTRIBUTE_TURN]
    look_aheads = [1,2,3,4]
    trials = [2, 4, 6, 8, 10]
    
    for h in heuristics:
    #     for l in look_aheads:
        for t in trials:
            for x in range(5):
                b = Bot(size=c.BOARD_SIZE, start_tiles=c.INIT_TILES,
                        look_ahead=3, trials=t, heuristic=h,
                        log=True)
                b.play()'''
