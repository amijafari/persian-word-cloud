# Author: Andreas Christian Mueller <t3kcit@gmail.com>
#
# (c) 2012
# Modified by: Paul Nechifor <paul@nechifor.net>
#
# License: MIT

from __future__ import division
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
import warnings
from random import Random
import os
from operator import itemgetter

from wordcloud import WordCloud
from wordcloud.wordcloud import colormap_color_func


class PersianWordCloud(WordCloud):
    def __init__(self, font_path=None, width=400, height=200, margin=2,
                 ranks_only=None, prefer_horizontal=.9, mask=None, scale=1,
                 color_func=None, max_words=200, min_font_size=4,
                 stopwords=None, random_state=None, background_color='black',
                 max_font_size=None, font_step=1, mode="RGB",
                 relative_scaling=.5, regexp=None, collocations=True,
                 colormap=None, normalize_plurals=True):
        super(PersianWordCloud, self).__init__(font_path, width, height, margin,
                                               ranks_only, prefer_horizontal, mask, scale,
                                               color_func, max_words, min_font_size,
                                               stopwords, random_state, background_color,
                                               max_font_size, font_step, mode,
                                               relative_scaling, regexp, collocations,
                                               colormap, normalize_plurals)
        if font_path is None:
            font_path = FONT_PATH
        if color_func is None and colormap is None:
            # we need a color map
            import matplotlib
            version = matplotlib.__version__
            if version[0] < "2" and version[2] < "5":
                colormap = "hsv"
            else:
                colormap = "viridis"
        self.colormap = colormap
        self.collocations = collocations
        self.font_path = font_path
        self.width = width
        self.height = height
        self.margin = margin
        self.prefer_horizontal = prefer_horizontal
        self.mask = mask
        self.scale = scale
        self.color_func = color_func or colormap_color_func(colormap)
        self.max_words = max_words
        self.stopwords = stopwords if stopwords is not None else STOPWORDS
        self.min_font_size = min_font_size
        self.font_step = font_step
        self.regexp = regexp
        if isinstance(random_state, int):
            random_state = Random(random_state)
        self.random_state = random_state
        self.background_color = background_color
        self.max_font_size = max_font_size
        self.mode = mode
        if relative_scaling < 0 or relative_scaling > 1:
            raise ValueError("relative_scaling needs to be "
                             "between 0 and 1, got %f." % relative_scaling)
        self.relative_scaling = relative_scaling
        if ranks_only is not None:
            warnings.warn("ranks_only is deprecated and will be removed as"
                          " it had no effect. Look into relative_scaling.",
                          DeprecationWarning)
        self.normalize_plurals = normalize_plurals

    def generate(self, text):
        text_ = arabic_reshaper.reshape(text)
        bidi_text = get_display(text_)

        return self.generate_from_text(bidi_text)


item1 = itemgetter(1)

FONT_PATH = os.environ.get("FONT_PATH", os.path.join(os.path.dirname(__file__),
                                                     "fonts/Vazir-Light.ttf"))


STOPWORDS = set([get_display(arabic_reshaper.reshape(x.strip())) for x in
                 open((os.path.join(os.path.dirname(__file__), 'stopwords')), encoding='utf-8').read().split('\n')])
