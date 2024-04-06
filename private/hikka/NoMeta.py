#  Copyright (c) 2023 Dmertixddd aka Tokyani
#  All rights reserved.
#  This code, including all of its parts, is the property of Dmertixddd aka Tokyani and is protected by copyright law.
#  Owner: Dmertixddd aka Tokyani
#  Contact: dmertixddd.t.me
#
#  Permission is granted to use, modify, and distribute this code only with explicit written permission from the owner.
#  Violation of copyright may result in legal consequences.

# meta developer: @dmertixddd

from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class NoMeta(loader.Module):
    """Simple NoMeta Module"""
    strings = {"name": "NoMeta", "nometa": "@neprivet"}
    strings_en = {"nometa": "Hello! Before you start a conversation, read this: @neprivet "}
    strings_ru = {"nometa": "Привет! Прежде чем начать разговор, прочтите это: @neprivet"}

    @loader.command(
        en_doc="Saying about NoMeta (@neprivet) on english",
        ru_doc="Говорит о NoMeta (@neprivet) на русском",
    )
    async def nometa(self, message: Message):
        """Gives the basics of NoMeta"""
        await utils.answer(message, self.strings("nometa"))
