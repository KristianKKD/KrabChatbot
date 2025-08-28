import asyncio

async def capture_input(model, bot, tts):
    from main import receive_message  # Still here if needed to avoid circular import

    model_input_keyword = "input:"
    model_raw_input_keyword = "raw:"

    async def handle_exit():
        return False

    async def handle_resetai():
        await model.disable_model()
        await model.load_model()
        return True

    async def handle_enableai():
        model.enabled = True
        return True

    async def handle_disableai():
        model.enabled = False
        return True

    async def handle_enabletts():
        await bot.enable_tts()
        return True

    commands = {
        "exit": handle_exit,
        "resetai": handle_resetai,
        "enableai": handle_enableai,
        "disableai": handle_disableai,
        "enabletts": handle_enabletts,
    }

    while True:
        user_input = await asyncio.to_thread(input, "Enter input:")
        content = user_input.strip()

        # Check for command
        cmd = content.lower()
        if cmd in commands:
            should_continue = await commands[cmd]()
            if should_continue is False:
                break
            continue

        # Check for model input keyword
        if content.lower().startswith(model_input_keyword):
            message = content[len(model_input_keyword):].strip()
            await receive_message(bot, model, tts, ('krabgor', message))
        elif content.lower().startswith(model_raw_input_keyword):
            message = content[len(model_raw_input_keyword):].strip()
            await receive_message(bot, model, tts, ('krabgor', message), raw=True)
        else:
            print("Invalid input.")
