import textwrap
from typing import Tuple, List, Reversible

import tcod

import color


class Message:
    """
    plain_text: The actual message text.
    fg: The “foreground” color of the message.
    count: Bundles messages together so MessageLog won't have repeated messages
    """
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        """ if the message repeats then bundles them together """
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    """ Keeps a list of messages to display """
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
        self,
        text: str,
        fg: Tuple[int, int, int] = color.white,
        *,
        stack: bool = True,
    ) -> None:
        """
        Adds new message to log
        text: text of the message
        fg: is the foreground color of the message
        stack: true log should stack messages instead of having a fixed number of them
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
        self,
        console: tcod.Console,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        """ Renders the messages to the console """
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def render_messages(
        console: tcod.Console,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: Reversible[Message],
    ) -> None:
        y_offset = height - 1

        for message in reversed(messages):
            for line in reversed(textwrap.wrap(message.full_text, width)):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return