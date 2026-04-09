import curses
import time

_instance = None

def get():
    return _instance


class Terminal:
    def __init__(self, typewriter_speed=0.02):
        self.stdscr = None
        self.text_win = None
        self.input_win = None
        self.typewriter_speed = typewriter_speed
        self._height = 0
        self._width = 0

    def setup(self, stdscr):
        global _instance
        _instance = self

        self.stdscr = stdscr
        self._height, self._width = stdscr.getmaxyx()

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)

        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        curses.curs_set(0)

        stdscr.clear()
        stdscr.refresh()

        text_height = self._height - 2
        self.text_win = curses.newwin(text_height, self._width, 0, 0)
        self.text_win.scrollok(True)
        self.text_win.idlok(True)

        self.input_win = curses.newwin(2, self._width, text_height, 0)

        self._draw_separator()
        self.text_win.refresh()
        self.input_win.refresh()

    def _draw_separator(self):
        try:
            self.input_win.addstr(0, 0, '─' * (self._width - 1), curses.color_pair(1))
        except curses.error:
            pass
        self.input_win.refresh()

    def game_print(self, *args, **kwargs):
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        text = sep.join(str(a) for a in args) + end

        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line:
                self._write_wrapped(line)
            if i < len(lines) - 1:
                self._newline()

    def _newline(self):
        try:
            self.text_win.addstr('\n', curses.color_pair(1))
        except curses.error:
            pass
        self.text_win.refresh()

    def _write_wrapped(self, text):
        max_w = self._width - 1
        while len(text) > max_w:
            split_at = text.rfind(' ', 0, max_w)
            if split_at <= 0:
                split_at = max_w
            self._write_chunk(text[:split_at])
            self._newline()
            text = text[split_at:].lstrip()
        if text:
            self._write_chunk(text)

    def _write_chunk(self, text):
        if self.typewriter_speed > 0:
            for char in text:
                try:
                    self.text_win.addstr(char, curses.color_pair(1))
                except curses.error:
                    pass
                self.text_win.refresh()
                time.sleep(self.typewriter_speed)
        else:
            try:
                self.text_win.addstr(text, curses.color_pair(1))
            except curses.error:
                pass
            self.text_win.refresh()

    def game_input(self, prompt=''):
        if prompt:
            self.game_print(prompt, end=' ')

        self.input_win.clear()
        self._draw_separator()
        try:
            self.input_win.addstr(1, 0, '> ', curses.color_pair(1))
        except curses.error:
            pass
        self.input_win.refresh()

        curses.echo()
        curses.curs_set(1)
        try:
            raw = self.input_win.getstr(1, 2, self._width - 4)
        except curses.error:
            raw = b''
        curses.noecho()
        curses.curs_set(0)

        result = raw.decode('utf-8', errors='replace')

        try:
            self.text_win.addstr(f'\n\n> {result}\n\n', curses.color_pair(1))
        except curses.error:
            pass
        self.text_win.refresh()

        self.input_win.clear()
        self._draw_separator()
        self.input_win.refresh()

        return result
