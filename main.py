import PySimpleGUI as sg
from pyperclip import copy
from fetch_emojis import *
import os

# ===========================================================================================================================
if not os.path.exists(f'/home/{os.getlogin()}/.config/dc-emoji/'): os.mkdir(f'/home/{os.getlogin()}/.config/dc-emoji/')
BASE_PATH = f'/home/{os.getlogin()}/.config/dc-emoji/'
if not os.path.exists(BASE_PATH + 'thumbnails/'): os.mkdir(BASE_PATH + 'thumbnails/')
THUMBNAIL_PATH = BASE_PATH + 'thumbnails/'
# ===========================================================================================================================


def saving_to_file(emoji_list, path=THUMBNAIL_PATH):
    import json
    download_emoji_thumbnails(emoji_list, path)
    with open(BASE_PATH+'emojis.json', 'w') as f:
        json.dump(emoji_list, f, indent=4)


def img_to_base64(img):
    import base64
    with open(img, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def main():
    from json import load
    names = []
    names_and_urls = {}
    if not os.path.isfile(BASE_PATH+'emojis.json'):
        saving_to_file(get_emojis())
    with open(BASE_PATH+'emojis.json', 'r') as json_file:
        lst = load(json_file)
        for server in lst:
            for emojis in server['emojis']:
                e_name = emojis['name']
                url = emojis['emoji_url']
                names.append(e_name)
                names_and_urls[e_name] = url
    names = [*set(names)]
    layout = [  [sg.Input(do_not_clear=True, size=(60, 1),enable_events=True, key='_INPUT_')],
                [sg.Listbox(names, size=(60, 10), enable_events=True, key='_LIST_', background_color='#241f1c', text_color='white', font=("Times New Roman", 12))],
                [sg.Button('Exit')]]
    
    sg.theme('DarkAmber')   # Add a touch of color

    window = sg.Window('Emoji Picker', layout, size=(400, 270))
    # Event Loop
    while True:
        event, values = window.Read()
        if event is None or event == 'Exit':
            break
        if values['_INPUT_'] != '':
            search = values['_INPUT_'].lower() # convert to lowercase
            new_values = [x for x in names if x.startswith(search)] # filtering
            window.Element('_LIST_').Update(new_values)
        else:
            window.Element('_LIST_').Update(names) # resetting list
        if event == '_LIST_':
            name = values['_LIST_'][0] 
            url = names_and_urls[name] # get url from name
            copy(url) # copy url to clipboard
            title = f"{name} has been copied to your clipboard." 
            message = 'Press Ctrl+V to paste it into Discord.' 
            try: 
                os.path.isfile(THUMBNAIL_PATH + name + '.png') 
                name = name + '.png'
            except FileNotFoundError: 
                name = name + '.gif'
            display_notification(title, message, img_to_base64(THUMBNAIL_PATH + name)) 

    window.Close()


if __name__ == '__main__':
    main()