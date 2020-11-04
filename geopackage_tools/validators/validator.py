import os
import logging
from geopackage_tools.infra import db_conn as db
from geopackage_tools.config import *

_logger = logging.getLogger('gp_validator.validator')


def validate_tables(file_name, cursor):
    tables_names = db.get_tables(cursor)
    expected_tables = TABLES_LIST
    expected_tables.append(file_name)
    expected_tables = set(expected_tables)
    tables_names = set(tables_names)

    if expected_tables.issubset(tables_names):
        return True, tables_names
    else:
        return False, tables_names


def validate_index(cursor):
    indices_names = db.get_indices(cursor)

    if TILES_INDEX in indices_names:
        return True, indices_names
    else:
        return False, indices_names


def validate_tile_matrix(cursor):
    """
    validate if all tile matrix table contain all relevant fields and data according standard
    """
    state = False
    VAL_START_ZOOM_LEVEL
    max_level = VAL_MAX_ZOOM_LEVEL

    res = db.list_tile_matrix_data(cursor)
    expected_row_dict = {
        'zoom_level': VAL_START_ZOOM_LEVEL,
        'matrix_width': VAL_MAT_W,
        'matrix_height': VAL_MAT_H,
        'tile_width': VAL_TILE_W,
        'tile_height': VAL_TILE_H,
        'pixel_x_size': VAL_PIXEL_X_SIZE,
        'pixel_y_size': VAL_PIXEL_Y_SIZE
    }
    try:
        while expected_row_dict['zoom_level'] <= max_level:
            mat = res[expected_row_dict['zoom_level']]

            try:
                actual_row_dict = {
                    'zoom_level': mat[1],
                    'matrix_width': mat[2],
                    'matrix_height': mat[3],
                    'tile_width': mat[4],
                    'tile_height': mat[5],
                    'pixel_x_size': mat[6],
                    'pixel_y_size': mat[7]
                }
            except Exception as e:
                _logger.error('Error of some missed fields on tile matrix row, current raw are %s with message' % mat, str(e))
                return state, res

            if expected_row_dict == actual_row_dict:
                _update_dicts(expected_row_dict)
            else:
                _logger.error('wrong values of matrix, should be %s but actual %s' % (expected_row_dict, actual_row_dict))
                return state, res



    except Exception as e:
        _logger.error("Not valid gpkg_tile_matrix data, failed on iteration")
        return state, res
    return state, res


def _update_dicts(expected_row_dict):
    expected_row_dict['zoom_level'] += 1
    expected_row_dict['matrix_width'] *= 2
    expected_row_dict['matrix_height'] *= 2
    expected_row_dict['pixel_x_size'] /= 2
    expected_row_dict['pixel_y_size'] /= 2

    pass
