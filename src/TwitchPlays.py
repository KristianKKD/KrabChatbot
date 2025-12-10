import keyboard
import mouse
import asyncio    

async def process_twitch_input(content):
    commands = [c.strip().lower() for c in content.split(' ') if c.strip()]
    results = []

    default_time = 2000
    time = default_time
    count = 1

    for command in commands:
        keyboard_inputs = {
            "up": "w",
            "down": "s",
            "left": "a",
            "right": "d",

            "lookleft": "left",
            "lookright": "right",
            "lookup": "up",
            "lookdown": "down",

            "jump": "space",
        }

        mouse_inputs = {
            "crank" : "right",
            "krabgo1crank" : "right",
            "kill"  : "left"
        }

        #translate text into relevant key/mouse input
        if ':' in command:
            cmd, time_part = command.split(':', 1)
            cmd = cmd.strip()
            try:
                time = int(time_part.strip())
            except ValueError:
                time = default_time
        else:
            cmd = command.strip()

        if 'x' in cmd:
            cmd, count_str = cmd.split('x', 1)
            cmd = cmd.strip()
            try:
                count = int(count_str.strip())
            except ValueError:
                count = 1

        #error handling
        if time <= 0:
            time = default_time

        if cmd not in keyboard_inputs and cmd not in mouse_inputs:
            results.append(False)
            continue

        #translate the key/mouse into action
        action_type = ""
        target_key = ""

        if cmd in keyboard_inputs:
            action_type = "keyboard"
            target_key = keyboard_inputs[cmd]
        elif cmd in mouse_inputs:
            action_type = "mouse"
            target_key = mouse_inputs[cmd]

        print("PRESSING " + target_key + " for " + str(time) + "ms x" + str(count))
        asyncio.create_task(input(action_type, target_key, time, count))
            
        results.append(True)

    return all(results)

async def input(action_type, key, time, count):
    for _ in range(count):
        if action_type == "keyboard":
            keyboard.release(key)
            keyboard.press(key)
            await asyncio.sleep(time/1000)
            keyboard.release(key)
        elif action_type == "mouse":
            mouse.release(button=key)
            mouse.press(button=key)
            await asyncio.sleep(time/1000)
            mouse.release(button=key)
    # await asyncio.sleep(0.2)