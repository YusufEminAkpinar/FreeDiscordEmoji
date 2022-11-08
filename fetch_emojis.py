def get_emojis():
    import requests
    import json
    token = input('Please enter your Discord Token: ')

    base_url = 'https://discord.com/api/v8' # Discord API base URL
    headers = { 
        'Content-Type': 'application/json',
        'Authorization': token, 
    }
    response = requests.get(base_url+'/users/@me/guilds', headers=headers) 
    if response.status_code != 200:
        print('Incorrect Discord Token. Please try again.')
        return -1
    servers = json.loads(response.text) 

    ids = []
    emoji_list = []

    for server in servers: 
        ids.append(server['id']) # get server ids

    for id in ids:
        emojis = []
        response = requests.get(base_url+'/guilds/'+str(id)+'/emojis', headers=headers) # get emojis from each server
        server_emojis = json.loads(response.text)
        for emoji in server_emojis:
            emoji_name = emoji['name']
            emoji_id = emoji['id']
            animated = emoji['animated']
            if animated: # Save emoji as gif if animated
                emoji_url = 'https://cdn.discordapp.com/emojis/'+str(emoji_id)+'.gif?size=40&quality=lossless'
            else: # and as png if not
                emoji_url = 'https://cdn.discordapp.com/emojis/'+str(emoji_id)+'.png?size=40&quality=lossless'
            emojis.append({'name': emoji_name, 'emoji_url': emoji_url}) # add emoji name and url to list
        emoji_list.append({"server_id": id, "emojis": emojis}) # add server id and list of emojis to list
    return emoji_list


def download_emoji_thumbnails(emoji_list, path):
    import requests
    import os
    for emojis in emoji_list:
        for emoji in emojis['emojis']:
            emoji_name = emoji['name']
            emoji_url = emoji['emoji_url']
            animated_flag = emoji_url.split('.')[3].split('?')[0] # get animated flag from url
            response = requests.get(emoji_url)
            if response.status_code == 200: 
                if animated_flag == 'gif':
                    file_name = emoji_name + '.gif'
                else:
                    file_name = emoji_name + '.png'
                if os.path.isfile(path + file_name):
                    print(f'Skipped {emoji_name}, existed emoji with same name.')
                else:   
                    with open(path+'/'+file_name, 'wb') as f: 
                        f.write(response.content) # write emoji to file
                        print('Downloaded: '+file_name) 


# Stole it like a boss from PySimpleGUI's Demo Programs :)
def display_notification(title, message, icon, display_duration_in_ms=1000, use_fade_in=True, alpha=0.9, location=None):
    """
    Function that will create, fade in and out, a small window that displays a message with an icon
    The graphic design is similar to other system/program notification windows seen in Windows / Linux
    :param title: (str) Title displayed at top of notification
    :param message: (str) Main body of the noficiation
    :param icon: (str) Base64 icon to use. 2 are supplied by default
    :param display_duration_in_ms: (int) duration for the window to be shown
    :param use_fade_in: (bool) if True, the window will fade in and fade out
    :param alpha: (float) Amount of Alpha Channel to use.  0 = invisible, 1 = fully visible
    :param location: Tuple[int, int] location of the upper left corner of window. Default is lower right corner of screen
    """
    import textwrap
    import PySimpleGUI as sg
    
    WIN_MARGIN = 60
    WIN_COLOR = "#282828"
    TEXT_COLOR = "#ffffff"

    # Compute location and size of the window
    message = textwrap.fill(message, 50)
    win_msg_lines = message.count("\n") + 1

    screen_res_x, screen_res_y = sg.Window.get_screen_size()
    win_margin = WIN_MARGIN  # distance from screen edges
    win_width, win_height = 430, 70 + (14.8 * win_msg_lines)
    win_location = location if location is not None else (screen_res_x - win_width - win_margin, screen_res_y - win_height - win_margin)

    layout = [[sg.Graph(canvas_size=(win_width, win_height), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH-",
                        background_color=WIN_COLOR, enable_events=True)]]

    window = sg.Window(title, layout, background_color=WIN_COLOR, no_titlebar=True,
                    location=win_location, keep_on_top=True, alpha_channel=0, margins=(0, 0), element_padding=(0, 0),
                    finalize=True)

    window["-GRAPH-"].draw_rectangle((win_width, win_height), (-win_width, -win_height), fill_color=WIN_COLOR, line_color=WIN_COLOR)
    window["-GRAPH-"].draw_image(data=icon, location=(20, 20))
    window["-GRAPH-"].draw_text(title, location=(64, 20), color=TEXT_COLOR, font=("Arial", 12, "bold"), text_location=sg.TEXT_LOCATION_TOP_LEFT)
    window["-GRAPH-"].draw_text(message, location=(64, 44), color=TEXT_COLOR, font=("Arial", 9), text_location=sg.TEXT_LOCATION_TOP_LEFT)

    # change the cursor into a "hand" when hovering over the window to give user hint that clicking does something
    window['-GRAPH-'].set_cursor('hand2')

    if use_fade_in == True:
        for i in range(1,int(alpha*100)):               # fade in
            window.set_alpha(i/100)
            event, values = window.read(timeout=20)
            if event != sg.TIMEOUT_KEY:
                window.set_alpha(1)
                break
        event, values = window(timeout=display_duration_in_ms)
        if event == sg.TIMEOUT_KEY:
            for i in range(int(alpha*100),1,-1):       # fade out
                window.set_alpha(i/100)
                event, values = window.read(timeout=20)
                if event != sg.TIMEOUT_KEY:
                    break
    else:
        window.set_alpha(alpha)
        event, values = window(timeout=display_duration_in_ms)

    window.close()