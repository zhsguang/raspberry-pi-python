import keyboard
# while True:
#     if keyboard.read_key() == 'a':
#         print("You pressed 'a'.")
#         break
# def func_keydown(event):
#     print('key down')
# keyboard.on_press(func_keydown)
# keyboard.add_hotkey('space', print, args=['space was pressed'])
while True:
    # Wait for the next event.
    event = keyboard.read_event()
    # if event.event_type == keyboard.KEY_DOWN and event.name == 'up':
    #     print('up was pressed')
    # if event.event_type == keyboard.KEY_UP and event.name == 'up':
    #     print('up was released')
    if event.name == 'up':
        if event.event_type == keyboard.KEY_DOWN:
            print('up was pressed')
        if event.event_type == keyboard.KEY_UP:
            print('up was released')
# print("Press ESC to stop.")
# keyboard.wait('esc')