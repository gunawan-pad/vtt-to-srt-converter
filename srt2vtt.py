from __future__ import print_function, unicode_literals, division, absolute_import

# import os
import re
from io import open
import argparse


def convert_srt_to_vtt(in_file, out_file):
    with open(in_file, 'r', encoding="utf8") as fvtt:
        strall = fvtt.read() + '\n\n'

    fndall = re.findall(r'(?:\d+\n)[\d:,]+ --> [\d:,]+\n.*?(?=\n\n)',
                        strall, re.S)

    with open(out_file, 'w', encoding="utf8") as fo:
        for fnd in fndall:
            line_number, time_stamp, text = fnd.split('\n', 2)
            fo.write('%s\n%s\n\n' % (time_stamp.replace(',', '.'), text))


def main():
    # python3 -m cProfile  vtt2srt.py
    # import cProfile

    parser = argparse.ArgumentParser(description="Srt to vtt file converter")
    parser.add_argument('in_srt', help='in srt file path')
    parser.add_argument('out_vtt', help='out vtt file path')

    args = parser.parse_args()
    out_vtt = args.out_vtt
    in_srt = args.in_srt

    convert_srt_to_vtt(in_srt, out_vtt)


if __name__ == '__main__':
    main()
