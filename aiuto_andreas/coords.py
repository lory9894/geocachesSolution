from gpx_converter import Converter
import gpx_converter

Converter(input_file='coordinates.csv').csv_to_gpx(lats_colname='lat',
                                                 longs_colname='lon',
                                                 output_file='output.gpx')