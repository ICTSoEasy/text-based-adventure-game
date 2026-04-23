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
        self.use_uppercase = False
        self._height = 0
        self._width = 0
        self._line_buffer = []   # all committed display lines
        self._current_line = ''  # line currently being written (not yet committed)
        self._scroll_offset = 0  # lines scrolled up from bottom (0 = live view)
        self._after_input = False

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

        self.status_win = curses.newwin(2, self._width, 0, 0)

        text_height = self._height - 4
        self.text_win = curses.newwin(text_height, self._width, 2, 0)
        self.text_win.scrollok(True)
        self.text_win.idlok(True)

        self.input_win = curses.newwin(2, self._width, text_height + 2, 0)
        self.input_win.keypad(True)

        self._draw_separator()
        self.text_win.refresh()
        self.input_win.refresh()

    def update_status(self, game_name='', score=None, turns=None, lives=None):
        try:
            parts = [game_name] if game_name else []
            if score is not None:
                parts.append(f'Score: {score}')
            if turns is not None:
                parts.append(f'Turns: {turns}')
            if lives is not None:
                parts.append(f'Lives: {lives}')
            text = '  >  '.join(parts)
            self.status_win.erase()
            self.status_win.addstr(0, 0, text[:self._width - 1], curses.color_pair(1))
            self.status_win.addstr(1, 0, '─' * (self._width - 1), curses.color_pair(1))
            self.status_win.refresh()
        except curses.error:
            pass

    def _draw_separator(self):
        try:
            self.input_win.addstr(0, 0, '─' * (self._width - 1), curses.color_pair(1))
        except curses.error:
            pass
        self.input_win.refresh()

    def _sentence_case(self, text):
        import re
        text = text.lower()
        text = re.sub(r'(?<=[.!?])\s+([a-z])', lambda m: m.group(0)[:-1] + m.group(1).upper(), text)
        text = re.sub(r'(^|\n)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
        return text

    def game_print(self, *args, **kwargs):
        import re
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        text = sep.join(str(a) for a in args) + end
        if self._after_input:
            text = '\n' + text
            self._after_input = False

        # Extract {^}...{/^} forced-uppercase sections before case conversion
        forced = []
        def _extract(m):
            forced.append(m.group(1).upper())
            return f'\x00{len(forced)-1}\x00'
        text = re.sub(r'\{\^\}(.*?)\{/\^\}', _extract, text, flags=re.DOTALL)

        if self.use_uppercase:
            text = text.upper()
        else:
            text = self._sentence_case(text)

        # Restore forced-uppercase sections
        for i, section in enumerate(forced):
            text = text.replace(f'\x00{i}\x00', section)

        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line:
                self._write_wrapped(line)
            if i < len(lines) - 1:
                self._newline()

    def _commit_line(self):
        self._line_buffer.append(self._current_line)
        self._current_line = ''

    def _newline(self):
        self._commit_line()
        try:
            self.text_win.addstr('\n', curses.color_pair(1))
        except curses.error:
            pass
        self.text_win.refresh()

    def _write_wrapped(self, text):
        max_w = min(80, self._width - 1)
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
        self._current_line += text
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

    def _scroll_up(self):
        text_h = self.text_win.getmaxyx()[0]
        step = max(1, text_h // 2)
        max_offset = max(0, len(self._line_buffer) - text_h)
        self._scroll_offset = min(self._scroll_offset + step, max_offset)
        self._redraw_text_win()

    def _scroll_down(self):
        text_h = self.text_win.getmaxyx()[0]
        step = max(1, text_h // 2)
        self._scroll_offset = max(0, self._scroll_offset - step)
        self._redraw_text_win()

    def _redraw_text_win(self):
        # Include any uncommitted current line in the view
        buffer = self._line_buffer[:]
        if self._current_line:
            buffer.append(self._current_line)

        text_h = self.text_win.getmaxyx()[0]
        total = len(buffer)
        if self._scroll_offset == 0:
            start = max(0, total - text_h)
            lines = buffer[start:]
        else:
            end = total - self._scroll_offset
            start = max(0, end - text_h)
            lines = buffer[start:end]

        self.text_win.clear()
        for line in lines:
            try:
                self.text_win.addstr(line + '\n', curses.color_pair(1))
            except curses.error:
                pass
        self.text_win.refresh()

    def game_input(self, prompt=''):
        if prompt:
            self.game_print(prompt, end=' ')

        # Always return to live view when awaiting input
        if self._scroll_offset != 0:
            self._scroll_offset = 0
            self._redraw_text_win()

        curses.curs_set(1)
        input_str = ''

        def _refresh_input():
            self.input_win.clear()
            self._draw_separator()
            try:
                self.input_win.addstr(1, 0, '> ', curses.color_pair(1))
                display = input_str[:self._width - 4]
                self.input_win.addstr(1, 2, display, curses.color_pair(1))
                self.input_win.move(1, 2 + len(display))
            except curses.error:
                pass
            self.input_win.refresh()

        _refresh_input()

        while True:
            ch = self.input_win.getch()

            if ch == curses.KEY_PPAGE:
                self._scroll_up()
                _refresh_input()
            elif ch == curses.KEY_NPAGE:
                self._scroll_down()
                _refresh_input()
            elif ch in (curses.KEY_ENTER, ord('\n'), ord('\r'), 10, 13):
                break
            elif ch in (curses.KEY_BACKSPACE, 127, 8):
                input_str = input_str[:-1]
                _refresh_input()
            elif 32 <= ch < 256:
                if len(input_str) < self._width - 4:
                    input_str += chr(ch)
                    _refresh_input()

        curses.curs_set(0)
        result = input_str

        # Echo input into text window and buffer
        self._commit_line()  # commit any pending partial line
        echo = f'> {result}'
        self._line_buffer.append(echo)
        self._after_input = True
        try:
            self.text_win.addstr(f'\n{echo}\n', curses.color_pair(1))
        except curses.error:
            pass
        self.text_win.refresh()

        self.input_win.clear()
        self._draw_separator()
        self.input_win.refresh()

        return result
