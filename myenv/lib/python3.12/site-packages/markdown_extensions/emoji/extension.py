from markdown import Extension
from markdown.inlinepatterns import InlineProcessor
from emojidb import emojis as emoji_map, aliases as emoji_aliases

RE_EMOJI = r'(:[+\-\w]+:)'


def get_code_points(s):
    return [c for c in s]


class EmojiPattern(InlineProcessor):
    """Return element of type `tag` with a text attribute of group(2) of an `InlineProcessor`."""

    def __init__(self, pattern, config, md):
        InlineProcessor.__init__(self, pattern, md)
        self.options = config['options']

    def _get_unicode_char(self, value):
        return ''.join([chr(int(c, 16)) for c in value.split('-')])

    def _get_unicode(self, emoji):
        uc = emoji.get('unicode')
        uc_alt = emoji.get('unicode_alt', uc)
        return uc, uc_alt

    def _get_alt(self, shortname, uc_alt):
        if uc_alt is None:
            alt = shortname
        else:
            alt = self._get_unicode_char(uc_alt)
        return alt

    def handleMatch(self, m, data):
        el = m.group(1)
        shortname = emoji_aliases.get(el, el)
        emoji = emoji_map.get(shortname, None)
        if emoji:
            uc, uc_alt = self._get_unicode(emoji)
            alt = self._get_alt(el, uc_alt)
            el = self.md.htmlStash.store(alt)
        return el, m.start(0), m.end(0)


class EmojiExtension(Extension):
    """Add emoji extension to Markdown class."""

    def __init__(self, **kwargs):
        """Initialize."""

        self.config = {
            'options': [
                {},
                "Emoji options see documentation for options for github and emojione."
            ]
        }
        super(EmojiExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        config = self.getConfigs()
        md.inlinePatterns.register(EmojiPattern(RE_EMOJI, config, md), "emoji", 75)


def makeExtension(**kwargs):
    return EmojiExtension(**kwargs)
