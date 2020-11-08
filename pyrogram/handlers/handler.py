#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import inspect
from typing import Callable

import pyrogram
from pyrogram.filters import Filter
from pyrogram.types import Update


class Handler:
    def __init__(self, callback: Callable, filters: Filter = None):
        self.callback = callback
        self.filters = filters

    async def __call__(self, client: "pyrogram.Client", *args, **kwargs):
        if callable(self.callback):
            if inspect.iscoroutinefunction(self.callback):
                return await self.callback(client, *args, **kwargs)
            else:
                return await client.run_in_executor(self.callback, client, *args)

        return None

    async def check(self, client: "pyrogram.Client", update: Update):
        if callable(self.filters):
            if inspect.iscoroutinefunction(self.filters.__call__):
                return await self.filters(client, update)
            else:
                return await client.run_in_executor(self.filters, client, update)

        return True
