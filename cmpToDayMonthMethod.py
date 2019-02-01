import numpy as np
import math
import argparse
import matplotlib.pyplot as plt

from calcephpy import CalcephBin, Constants


def to_julian_date(year, month, day, hour, minute, second):
    a = (14 - month) / 12
    y = year + 4800 - a
    m = month + 12 * a - 3

    julian_date = day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045

    # float division
    julian_date += (hour-12) / 24. + minute / 1440. + second / 86400.

    return julian_date


def get_solar_distance_from_day_month(day, month):
    if month <= 2:
        j = (month - 1) * 31 + day
    elif month > 8:
        j = (month - 1) * 31 - (month - 2) / 2 - 2 + day
    else:
        j = (month - 1) * 31 - (month - 1) / 2 - 2 + day

    om = (j - 4) * .9856 * math.pi/180
    d__1 = 1. - math.cos(om) * .01673

    return d__1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''cmpToMonthDayMethod script help section. ''')
    parser.add_argument('ephemeris_files', type=str, nargs='+', help='Paths to the ephemeris files to use. They must '
                                                                     'be compatible with the calceph library. (see '
                                                                     'https://www.imcce.fr/content/medias/recherche/'
                                                                     'equipes/asd/calceph/html/python/calceph.multiple.'
                                                                     'html#menu-calceph-open)')
    parser.add_argument('year', type=int, help='Year at the moment of the acquisition.')
    args = parser.parse_args()

    # open ephemeris file
    try:
        peph = CalcephBin.open(args.ephemeris_files)
    except RuntimeError:
        raise Exception('Cannot open ephemeris files')

    solar_dist_eph = []
    solar_dist_day_month = []
    diff = []
    rel_diff = []

    for cur_month in range(12):
        nb_days = 31
        if cur_month == 1:
            nb_days = 28
        elif cur_month % 2 == 1:
            nb_days = 30

        for cur_day in range(nb_days):
            # compute julian date
            cur_julian_date = to_julian_date(args.year, cur_month+1, cur_day+1, 0, 0, 0)
            julian_date_ent = int(cur_julian_date)
            julian_date_dec = cur_julian_date - julian_date_ent

            # compute earth/sun distance using the calceph library
            out = peph.compute_unit(julian_date_ent, julian_date_dec, 11, 3, Constants.UNIT_AU + Constants.UNIT_SEC)
            norm_eph = math.sqrt(pow(out[0], 2.) + pow(out[1], 2.) + pow(out[2], 2.))

            # compute earth/sun distance using the elliptical model
            norm_day_month = get_solar_distance_from_day_month(cur_day+1, cur_month+1)

            solar_dist_eph.append(norm_eph)
            solar_dist_day_month.append(norm_day_month)
            diff.append(norm_eph-norm_day_month)
            rel_diff.append(abs(norm_eph-norm_day_month)/norm_day_month*100.)

    # plot the results
    plt.plot(solar_dist_eph, 'r', label='using ephemeris')
    plt.plot(solar_dist_day_month, 'b', label='using day/month')
    plt.ylabel('solar distance (in AU)')
    plt.legend(loc='upper right')
    plt.show()

    # print the errors statistics
    print('difference max : {}'.format(np.max(np.abs(diff))))
    print('difference mean : {}'.format(np.mean(diff)))
    print('difference standard deviation : {}'.format(np.std(diff)))
    print('relative difference max (in %): {}'.format(np.max(rel_diff)))
    print('relative difference mean (in %): {}'.format(np.mean(rel_diff)))
    print('relative difference standard deviation (in %): {}'.format(np.std(rel_diff)))

    # close ephemeris file
    peph.close()
