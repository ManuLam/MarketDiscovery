import asyncio
from random import randint

import cv2
from win32gui import FindWindow, GetWindowRect
import pyautogui
from PIL import Image, ImageChops
import time
import winsound
import win32api, win32con

from analyze_images import image_compute_numbers
from human_click import move_mouse

from src.discord_hook import ping_discord

main_path = "C:\\Users\\Manu\\PycharmProjects\\ItemDiscovery\\"
path = main_path + "images\\{0}." + time.strftime("%Y%m%d-%H%M%S") + ".png"
trophy_path = main_path + "trophy\\{0}." + time.strftime("%Y%m%d-%H%M%S") + ".png"
found_path = main_path + "found\\{0}." + time.strftime("%Y%m%d-%H%M%S") + ".png"
game_title = "LOST ARK (64-bit, DX11) v.2.0.2.1"

window_handle = FindWindow(None, game_title)
x1, y1, width, height = GetWindowRect(window_handle)
width -= 3

# Auction gui
auction_tab_width = 1376
auction_tab_height = 861
auction_gui_x_shift = width - auction_tab_width
auction_gui_y_shift = auction_tab_height - y1
auction_gui_coords = (auction_gui_x_shift, y1, width, auction_gui_y_shift)

# Buy Now price column gui
auction_buy_now_price_col_width = 155
auction_buy_now_price_col_height = 775
auction_buy_now_price_col_height_add_top = 206
auction_buy_now_price_col_x_shift = width - auction_buy_now_price_col_width
auction_buy_now_price_col_y_shift = auction_buy_now_price_col_height - y1
auction_buy_now_price_col_coords = (auction_buy_now_price_col_x_shift, y1 + auction_buy_now_price_col_height_add_top, width, auction_buy_now_price_col_y_shift)

# Buy Now price column gui
market_buy_now_price_col_width = 155
market_buy_now_price_col_height = 775
market_buy_now_price_col_height_add_top = 206
market_buy_now_price_col_x_shift = 1512
market_buy_now_price_col_width_shift = 1665
market_buy_now_price_col_y_shift = market_buy_now_price_col_height - y1
market_buy_now_price_col_coords = (market_buy_now_price_col_x_shift, y1 + market_buy_now_price_col_height_add_top, market_buy_now_price_col_width_shift, market_buy_now_price_col_y_shift)


def screen_capture(coords, title, trophy=False, save=False):
    save_location = path.format(title)

    if trophy:
        save_location = trophy_path.format(title)

    return crop_save(coords, save_location, save), save_location


def crop_save(coords, save_location, save=False):
    pyautogui.screenshot(save_location)
    im = Image.open(save_location)
    im = im.crop(coords)

    if save:
        im.save(save_location)

    return im


def image_save(image_name, image_location, save_folder, replace):
    im = Image.open(image_location + image_name)
    image_name = image_name.replace("cache", replace)
    im.save(image_location + save_folder + "\\" + image_name)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def ping_sound():
    duration = 200  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)


def randomize_sleep(x, y):
    sleep_time = randint(x, y)
    print("Sleeping for {0} seconds!".format(sleep_time))
    time.sleep(sleep_time)


searchbox_x1, searchbox_y1, searchbox_x2, searchbox_y2 = 1512, 138, 1705, 151


def randomize_searchbox_location():
    return randint(searchbox_x1, searchbox_x2), randint(searchbox_y1, searchbox_y2)


def within_searchbox():
    x, y = pyautogui.position()
    return (searchbox_x2 >= x >= searchbox_x1) and (searchbox_y2 >= y >= searchbox_y1)


def move_and_leftclick(x, y, speed=.144):
    move_mouse(x, y, speed)
    pyautogui.leftClick()


def moveToTier(tier):
    button_helper = AuctionButtons()
    tier_coords = {"T2": button_helper.T2_coords(), "T3": button_helper.T3_coords()}
    time.sleep(.11)
    move_and_leftclick(*button_helper.search_filter_button_coords(), speed=.088)
    time.sleep(.11)
    move_and_leftclick(*tier_coords[tier], speed=.088)
    time.sleep(.11)
    move_and_leftclick(*button_helper.accept_button_coords(), speed=.088)
    time.sleep(.11)
    move_and_leftclick(*button_helper.search_button_coords(), speed=.088)
    time.sleep(.11)


AUCTION_BUY_COL = "AuctionBuyCol"
AUCTION_GUI = "AuctionGUI"


CACHE_IMAGE_NAME = "{0}.cache.png".format(AUCTION_BUY_COL)
AUCTION_GUI_IMAGE_NAME = "{0}.cache.png".format(AUCTION_GUI)

CACHE_IMAGE = main_path + CACHE_IMAGE_NAME
AUCTION_GUI_IMAGE = main_path + AUCTION_GUI_IMAGE_NAME


import time

from AuctionButtons import AuctionButtons

def auto_buy():
    buttons = AuctionButtons()
    move_and_leftclick(*buttons.item_one(), speed=.077)
    time.sleep(.05)
    move_and_leftclick(*buttons.bid_buy(), speed=.077)
    time.sleep(.05)
    move_and_leftclick(*buttons.confirm_buy(), speed=.077)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)


def find_low_price(prices, threshold, diff, discord_image, PING_NOTIFICATION=True):
    try:
        # todo lets compare before...
        if len(prices) > 0 and threshold >= prices[0]:
            print("Found {0}: ".format(threshold), prices)

            if PING_NOTIFICATION and diff.getbbox():
                ping_discord(prices[0], discord_image, threshold)

            auto_buy()
            # ping_sound()

            # image_save(discord_image, main_path, "found", time.strftime("%Y%m%d-%H%M%S"))
            return True

        print("Not found: ", prices)
    except Exception as e:
        print("ERROR: ", prices, e)


def autoMoveTier(tier):
    if tier == "T2": moveToTier("T2")
    if tier == "T3": moveToTier("T3")


# from pynput import keyboard
#
# def listener():
#     # The event listener will be running in this block
#     with keyboard.Events() as events:
#         for event in events:
#             if event.key == keyboard.Key.esc:
#                 exit()
#
# qq = asyncio.Queue()
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(listener())


from src.GemStorage import T2
from src.GemStorage import T3

def main(gem_set):
    print("System started!")
    rotate_speed = (0, 1)

    if len(gem_set) == 1:
        rotate_speed = (2, 3)

    # gem_set =  t3gems

    iterations_map = {T2.Level6Gem: 1, T2.Level7Gem: 1, T2.Level5Gem: 1, T3.Level2Gem: 1, T3.Level3Gem: 1, T3.Level4Gem: 1, T3.Level5Gem: 1}
    coords = {"Auction": auction_buy_now_price_col_coords, "Market": market_buy_now_price_col_coords}

    if len(gem_set) > 0:
        prev_tier = gem_set[0]().get_tier()
        moveToTier(prev_tier)
    else:
        print("empty set!")
        return

    while True:
        start_remove_iteration = True
        for g in gem_set:
            iterations = 0

            gem = g()
            if prev_tier != gem.get_tier():
                autoMoveTier(gem.get_tier())

            prev_tier = gem.get_tier()

            if not within_searchbox():
                move_and_leftclick(*randomize_searchbox_location())

            threshold = gem.threshold

            # start with replacing the search field
            for command in gem.get_commands():
                time.sleep(.22)
                pyautogui.press(command)
                time.sleep(.22)

            if g not in iterations_map:
                iter_range = 1
            else:
                iter_range = iterations_map[g]

            for step in range(iter_range):
                # TODO, simple for now
                if (iterations != 0 and iterations % 2 == 0 and not within_searchbox()):
                    move_and_leftclick(*randomize_searchbox_location())

                if within_searchbox():
                    time.sleep(.22)
                    pyautogui.press("enter")
                    time.sleep(1)

                auction_buy_col_save = screen_capture(coords[gem.get_selling_type()], AUCTION_BUY_COL, trophy=False, save=False)
                discord_image = screen_capture(auction_gui_coords, AUCTION_GUI, trophy=False, save=False)

                diff = ImageChops.difference(auction_buy_col_save[0], Image.open(CACHE_IMAGE))
                auction_buy_col_save[0].save(CACHE_IMAGE)

                prices = list(map(int, image_compute_numbers(CACHE_IMAGE)))
                found = find_low_price(prices, threshold, diff, discord_image[1])

                cv2.waitKey(3)

                if found:
                    randomize_sleep(4, 6)
                else:
                    randomize_sleep(*rotate_speed)

                iterations += 1

        randomize_sleep(2, 3)


if __name__ == "__main__":
    t2gems = [T2.Level6Gem, T2.Level7Gem]
    t3gems = [T3.Level2Gem, T3.Level3Gem, T3.Level4Gem, T3.Level5Gem]
    gem_set = t3gems

    main(gem_set)
    # print(pyautogui.position())
