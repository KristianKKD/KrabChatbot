import keyboard
import asyncio    

async def process_twitch_input(content):
    # Allow multiple commands separated by commas
    commands = [c.strip() for c in content.split(' ') if c.strip()]
    results = []

    for command in commands:
        keyboard_inputs = {
            "up": "w",
            "down": "s",
            "left": "a",
            "right": "d",
            "jump": "space",
            "shoot": "e",
            "fire": "k",
            "switch": "q"
        }

        default_time = 2000
        time = default_time
        count = 1

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

        print(cmd, time, count)

        if time <= 0:
            time = default_time

        if cmd not in keyboard_inputs:
            results.append(False)
            continue

        asyncio.create_task(input(keyboard_inputs[cmd], time, count))
        results.append(True)

    return all(results)

async def input(key, time, count):
    for _ in range(count):
        keyboard.press(key)
        await asyncio.sleep(time/1000)
        keyboard.release(key)
    await asyncio.sleep(0.2)