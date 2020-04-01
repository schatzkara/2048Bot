from graphics import Graphics
import constants as c
import keyboard

bot = True
heuristic = c.HIGHSCORE
look_ahead = 5
trials = 20
log = True

if __name__ == "__main__":
    Graphics(bot=bot, heuristic=heuristic, look_ahead=look_ahead, trials=trials, log=log)
    #
    # heuristics = [c.HIGHSCORE, c.MOSTMERGES, c.MOSTMERGESAVAIL]
    # look_aheads = [1,2,3,4,5]
    #
    # for l in look_aheads:
    #     for h in heuristics:
    #         g = Graphics(bot=bot, heuristic=h, look_ahead=l, trials=trials, log=log)
    #         keyboard.press("enter")
    #         keyboard.release("enter")
    #         del g
