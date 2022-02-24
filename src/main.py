from random import randint

import cv2
import win32gui
from win32gui import FindWindow, GetWindowRect
import pyautogui
from PIL import Image, ImageChops
import time
import winsound
import win32api, win32con

from analyze_images import image_compare, cv2_show_image, image_compute_numbers
from human_click import move_mouse

path = "images\\{0}." + time.strftime("%Y%m%d-%H%M%S") + ".png"
trophy_path = "trophy\\{0}." + time.strftime("%Y%m%d-%H%M%S") + ".png"
found_path = "found\\{0}." + time.strftime("%Y%m%d-%H%M%S") + ".png"
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

def screen_capture(coords, title, trophy=False, display=False, save=False):
    if display:
        print(coords)

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


def image_save(save_location, replace, path):
    im = Image.open(save_location)
    save_location = save_location.replace("fresh", replace)
    im.save(path + "\\" + save_location)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


from discord import Webhook, RequestsWebhookAdapter
import discord


def ping_discord(price, threshold):
    with open(file='C:\\Users\\Manu\\PycharmProjects\\ItemDiscovery\\AuctionBuyCol.fresh.png', mode='rb') as f:
        my_file = discord.File(f)

    webhook = Webhook.from_url("https://discord.com/api/webhooks/946189381482463302/9svEN_y6TeHErHyhh52rOzro-M-cEsRuTT8LovcR8mTdaC1i6tjBBTH-hlyKgAdPlr7Q", adapter=RequestsWebhookAdapter())
    webhook.send(username="SHADY MERCHANT", avatar_url="https://i.imgur.com/a/jIokIO2", file=my_file, content="<@&946199864767836190> LOWEST PRICE FOUND @ {0} | THRESHOLD @ {1}".format(price, threshold))


def ping_sound():
    duration = 200  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)


def randomize_searchbox_location():
    return randint(1512, 1705), randint(138, 151)


def main():
    i = 0

    coords = auction_buy_now_price_col_coords
    # coords = market_buy_now_price_col_coords

    while True:
        searchbox_x, searchbox_y = randomize_searchbox_location()

        thresholdLv3 = 355
        thresholdLv4 = 800
        thresholdLv6 = 233
        thresholdLv7 = 633
        thresholdBook = 250
        threshold = thresholdLv6

        runLv7 = True
        runLv4 = False


        if i % 2 == 0:
            move_mouse(searchbox_x, searchbox_y)
            pyautogui.leftClick()


        i += 1
        time.sleep(.33)

        if runLv7 and i % 4 == 0:
            move_mouse(searchbox_x, searchbox_y)
            pyautogui.leftClick()

            #4th alteration, check level 7
            threshold = thresholdLv7
            pyautogui.press("backspace")
            pyautogui.press("7")

        if runLv4 and i % 4 == 0:
            move_mouse(searchbox_x, searchbox_y)
            pyautogui.leftClick()

            #3rd alteration, check level 3
            threshold = thresholdLv4
            pyautogui.press("backspace")
            pyautogui.press("4")

        time.sleep(.6)

        if pyautogui.position() == (searchbox_x, searchbox_y):
            pyautogui.press("enter")

            time.sleep(1.2)

        SAVE = False
        doShow = False
        PING_NOTIFICATION = True

        AUCTION_GUI = "AuctionGUI"
        AUCTION_BUY_COL = "AuctionBuyCol"

        #auction_gui_save = screen_capture(auction_gui_coords, AUCTION_GUI, trophy=SAVE)
        auction_buy_col_save = screen_capture(coords, AUCTION_BUY_COL, trophy=SAVE, save=False)

        # Computer vision check these coords to see difference in price
        # try:
        #     show_compare = image_compare("{0}.fresh.png".format(AUCTION_BUY_COL), auction_buy_col_save[1])
        # except Exception as e:
        #     doShow = False
        #     print(e)
        #
        diff = ImageChops.difference(auction_buy_col_save[0], Image.open("{0}.fresh.png".format(AUCTION_BUY_COL)))
        auction_buy_col_save[0].save("{0}.fresh.png".format(AUCTION_BUY_COL))
        #
        # if doShow:
        #     cv2_show_image(show_compare)
        #     cv2.waitKey(0)


        ar = list(image_compute_numbers("{0}.fresh.png".format(AUCTION_BUY_COL)))

        def find_low_price(diff):
            try:
                if len(ar) > 0 and int(ar[0]) <= threshold:
                    # print("Found {0}".format(element))
                    print("FOUND {0}: ".format(threshold), ar)

                    if diff.getbbox():
                        ping_discord(ar[0], threshold)

                    # ping_sound()

                    image_save("{0}.fresh.png".format(AUCTION_BUY_COL), time.strftime("%Y%m%d-%H%M%S"), "found")
                    return

                if len(ar) >= 2 and int(ar[0]) > int(ar[1]):
                    # print("Found {0}".format(element))
                    print("FOUND {0}: ".format(threshold), ar)

                    if diff.getbbox():
                        ping_discord(ar[0], threshold)

                    # ping_sound()

                    image_save("{0}.fresh.png".format(AUCTION_BUY_COL), time.strftime("%Y%m%d-%H%M%S"), "found")
                    return


                print("show: ", ar)
            except Exception as e:
                print("ERROR: ", ar, e)


        find_low_price(diff)

        cv2.waitKey(3)

        if runLv7 and i % 4 == 0:
            pyautogui.press("backspace")
            pyautogui.press("6")


        if runLv4 and i % 4 == 0:
            pyautogui.press("backspace")
            pyautogui.press("3")

        sleep_time = randint(5, 7)

        print("Sleeping for {0} seconds", sleep_time)
        time.sleep(sleep_time)



if __name__ == "__main__":
    main()
    # print(pyautogui.position())
