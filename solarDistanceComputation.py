#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CS Systèmes d'Information (CS SI)
#
# This file is part of the "Calceph Earth-Sun distance" project
#
#     https://github.com/CS-SI/calceph_earth-sun_distance
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import math
import argparse

from calcephpy import CalcephBin, Constants


def to_julian_date(year, month, day, hour, minute, second):
    a = (14 - month) / 12
    y = year + 4800 - a
    m = month + 12 * a - 3

    julian_date = day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045

    # float division
    julian_date += (hour - 12) / 24. + minute / 1440. + second / 86400.

    return julian_date


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''solarDistanceComputation script help section. ''')
    parser.add_argument('ephemeris_files', type=str, nargs='+', help='Paths to the ephemeris files to use. They must '
                                                                     'be compatible with the calceph library. (see '
                                                                     'https://www.imcce.fr/content/medias/recherche/'
                                                                     'equipes/asd/calceph/html/python/calceph.multiple.'
                                                                     'html#menu-calceph-open)')
    parser.add_argument('year', type=int, help='Year at the moment of the acquisition.')
    parser.add_argument('month', type=int, help='Month at the moment of the acquisition.')
    parser.add_argument('day', type=int, help='Day at the moment of the acquisition.')
    parser.add_argument('hour', type=int, help='Hour at the moment of the acquisition.')
    parser.add_argument('minute', type=int, help='Minute at the moment of the acquisition.')
    parser.add_argument('second', type=int, help='Second at the moment of the acquisition.')
    args = parser.parse_args()

    if (args.month < 1) or (args.month > 12):
        raise Exception('month must be between 1 and 12.')

    if (args.day < 1) or (args.day > 31):
        raise Exception('day must be between 1 and 31.')

    if (args.hour < 0) or (args.hour > 23):
        raise Exception('hour must be between 0 and 23.')

    if (args.minute < 0) or (args.minute > 59):
        raise Exception('minute must be between 0 and 59.')

    if (args.second < 0) or (args.second > 59):
        raise Exception('second must be between 0 and 59.')

    print('Computing Earth/Sun distance the {y}/{m}/{d} at {h} h {mn} mn {s} s.'
          .format(y=args.year, m=args.month, d=args.day, h=args.hour, mn=args.minute, s=args.second))

    # compute julian date
    cur_julian_date = to_julian_date(args.year, args.month, args.day, args.hour, args.minute, args.second)
    julian_date_ent = int(cur_julian_date)
    julian_date_dec = cur_julian_date - julian_date_ent

    print('Corresponding julian date is {}.'.format(cur_julian_date))

    # open ephemeris file
    try:
        peph = CalcephBin.open(args.ephemeris_files)
    except RuntimeError:
        raise Exception('Cannot open ephemeris files')

    # compute the cartesian position of the sun (target 11) in the geocentric (center 3) referential
    try:
        out = peph.compute_unit(julian_date_ent, julian_date_dec, 11, 3, Constants.UNIT_AU + Constants.UNIT_SEC)
    except RuntimeError:
        raise Exception('Cannot compute earth/sun distance')

    # compute the distance (norm)
    norm = math.sqrt(pow(out[0], 2.) + pow(out[1], 2.) + pow(out[2], 2.))
    print('Earth/Sun distance is {var}.'.format(var=norm))

    # close ephemeris file
    peph.close()
