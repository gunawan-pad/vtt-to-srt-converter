from __future__ import print_function, unicode_literals, division, absolute_import

import re
from io import open
import timeit

from six.moves.html_parser import HTMLParser
import argparse

# Download subtitle
# youtube-dl --write-sub --sub-lang en --skip-download https://www.youtube.com/watch?v=ws5aWK5Wci8

# convert vtt to srt:
# https://toolslick.com/conversion/subtitle/vtt-to-srt

# text = "Can you notice? <i>can't you notice?</i>\n<a.coto>link</a> <b .nganu>ggg</b>"

_ghp = HTMLParser()
_rec_tag_remove = re.compile(r'</?([^ibu]|(?!font))\s*(\.[^>]+)?>', re.I | re.S)
_rec_tag_clean_class = re.compile(r'<(\w+)\s*\.[^>]+>', re.I | re.S)
_rec_tag_timestamp = re.compile(r'<\s*[\d:.]+\s*>', re.I | re.S)


def html_unescape(s):
    return _ghp.unescape(s)


def clean_tags(s):
    # remove illegal srt tags, <a> etc
    # classes eg: <i.nganu>
    # timestamp tag <00:17.500>

    # allowed_srt_tags = ['i', 'b', 'u', 'font']

    s = _rec_tag_timestamp.sub('', s)
    s = _rec_tag_remove.sub('', s)
    # remove tag'class
    s = _rec_tag_clean_class.sub('<\\1>', s)
    return s


def convert_vtt_to_srt_v3(vtt_file, out_file):
    with open(vtt_file, 'r', encoding="utf8") as fvtt:
        file_content = fvtt.read()  # + '\n\n'

    # fndall = re.search(r'^.*?(?=\n\n)', strall, re.S)
    # headers = dict([l.split(': ') for l in fndall.group().splitlines() if ': ' in l])

    blocks = re.split(r'\n\n', file_content, flags=re.S | re.U)

    counter = 0
    block_index = -1
    rec_cue = re.compile(r'([^\n]+\n)?([\d:.]+ --> [\d:.]+)( [^\n]+)?\n(.*?)$',
                         flags=re.S)

    with open(out_file, 'w', encoding="utf8") as fo:
        for block in blocks:
            block_index += 1

            fnd = rec_cue.search(block)
            if not fnd:
                # TODO: parse header, NOTE, STYLE etc
                continue

            cue_id, cue_timing, cue_settings, cue_text = fnd.groups()  # [0]
            # TODO: parse start time, end time
            # cue settings: positions, size, align
            fo.write(
                '%i\n%s\n%s\n\n' % (
                    counter,
                    cue_timing.replace('.', ','),
                    html_unescape(clean_tags(cue_text))
                )
            )
            counter += 1


def main():
    # python3 -m cProfile  vtt2srt.py
    parser = argparse.ArgumentParser(description="Vtt to srt file converter")
    parser.add_argument('in_vtt', help='in vtt file path')
    parser.add_argument('out_srt', help='out srt file path')

    args = parser.parse_args()
    in_vtt = args.in_vtt
    out_srt = args.out_srt

    convert_vtt_to_srt_v3(in_vtt, out_srt)


if __name__ == '__main__':
    main()
    # import cProfile
    # cProfile.run("main()", sort='time')

    # r = timeit.timeit(stmt=main, number=50)
    # print(r)
