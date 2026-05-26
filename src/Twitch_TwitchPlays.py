import keyboard
import mouse
import asyncio    

async def process_twitch_input(content:str) -> list[str]:
    commands:list[str] = [c.strip().lower() for c in content.split(' ') if c.strip()]
    results:list[str] = []

    DEFAULT_TIME_MS:int = 2000
    DEFAULT_COUNT:int = 1

    for command in commands:
        cmd:str = command
        time_ms:int = DEFAULT_TIME_MS
        count:int = DEFAULT_COUNT

        keyboard_inputs:dict[str] = {
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

        mouse_inputs:dict[str] = {
            "crank" : "right",
            "krabgo1crank" : "right",
            "kill"  : "left"
        }

        # Is it a valid command
        all_inputs:dict[str] = mouse_inputs + keyboard_inputs
        if cmd not in all_inputs:
            results.append(False)
            continue

        # Time
        if ':' in command:
            cmd, time_part = command.strip().split(':', 1)
            try:
                time_ms = int(time_part.strip())
            except ValueError:
                pass

        # Count
        if 'x' in cmd:
            cmd, count_str = cmd.split('x', 1)
            try:
                count = int(count_str.strip())
            except ValueError:
                pass

        # Error handling
        if time_ms <= 0 or time_ms >= 1000 : time_ms = DEFAULT_TIME_MS
        if count < 0 or count >= 1000 : count = DEFAULT_COUNT

        # Do the action
        action_type:str = ""
        target_key:str = ""

        if cmd in keyboard_inputs:
            action_type = "keyboard"
            target_key = keyboard_inputs[cmd]
        elif cmd in mouse_inputs:
            action_type = "mouse"
            target_key = mouse_inputs[cmd]
        else:
            print(f"Error deciding which action type for the input: {cmd}")
            return

        print(f"PRESSING {target_key} for {str(time_ms)}ms, {str(count)} times")
        asyncio.create_task(input(action_type, target_key, time_ms, count))
            
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