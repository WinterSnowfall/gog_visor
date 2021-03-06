#!/usr/bin/env python3
'''
@author: Winter Snowfall
@version: 2.30
@date: 23/12/2020

Warning: Built for use with python 3.6+
'''

import sqlite3
import logging
import argparse
from os import path

##logging configuration block
log_file_full_path = path.join('..', 'logs', 'gog_create_db.log')
logger_file_handler = logging.FileHandler(log_file_full_path, mode='w', encoding='utf-8')
logger_format = '%(asctime)s %(levelname)s >>> %(message)s'
logger_file_handler.setFormatter(logging.Formatter(logger_format))
logging.basicConfig(format=logger_format, level=logging.INFO) #DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger(__name__)
logger.addHandler(logger_file_handler)

##db configuration block
db_file_full_path = path.join('..', 'output_db', 'gog_visor.db')

##CONSTANTS
CREATE_GOG_COMPANIES_QUERY = ('CREATE TABLE gog_companies (gc_int_nr INTEGER PRIMARY KEY AUTOINCREMENT, '
                              'gc_int_added TEXT NOT NULL, '
                              'gc_int_delisted TEXT, '
                              'gc_name TEXT UNIQUE NOT NULL)')

CREATE_GOG_FILES_QUERY = ('CREATE TABLE gog_files (gf_int_nr INTEGER PRIMARY KEY AUTOINCREMENT, '
                          'gf_int_added TEXT NOT NULL, '
                          'gf_int_removed TEXT, '
                          'gf_int_id INTEGER NOT NULL, '
                          'gf_int_download_type TEXT NOT NULL, '
                          'gf_id INTEGER NOT NULL, '
                          'gf_name TEXT NOT NULL, '
                          'gf_os TEXT, '
                          'gf_language TEXT, '
                          'gf_version TEXT, '
                          'gf_type TEXT, '
                          'gf_count INTEGER, '
                          'gf_total_size INTEGER NOT NULL, '
                          'gf_file_id TEXT NOT NULL, '
                          'gf_file_size INTEGER NOT NULL)')

CREATE_GOG_PRICES_QUERY = ('CREATE TABLE gog_prices (gpr_int_nr INTEGER PRIMARY KEY AUTOINCREMENT, '
                           'gpr_int_added TEXT NOT NULL, '
                           'gpr_int_outdated TEXT, '
                           'gpr_int_id INTEGER NOT NULL, '
                           'gpr_int_title TEXT, '
                           'gpr_int_country_code TEXT NOT NULL, '
                           'gpr_currency TEXT NOT NULL, '
                           'gpr_base_price REAL NOT NULL, '
                           'gpr_final_price REAL NOT NULL)')

CREATE_GOG_PRODUCTS_QUERY = ('CREATE TABLE gog_products (gp_int_nr INTEGER PRIMARY KEY AUTOINCREMENT, '
                             'gp_int_added TEXT NOT NULL, '
                             'gp_int_delisted TEXT, '
                             'gp_int_updated TEXT, '
                             'gp_int_json_payload TEXT NOT NULL, '
                             'gp_int_json_diff TEXT, '
                             'gp_int_v2_updated TEXT, '
                             'gp_int_v2_json_payload TEXT, '
                             'gp_int_v2_json_diff TEXT, '
                             'gp_int_is_movie INTEGER NOT NULL, '
                             'gp_v2_developer TEXT, '
                             'gp_v2_publisher TEXT, '
                             'gp_v2_tags TEXT, '
                             'gp_v2_series TEXT, '
                             'gp_v2_features TEXT, '
                             'gp_v2_is_using_dosbox INTEGER, '
                             'gp_id INTEGER UNIQUE NOT NULL, '
                             'gp_title TEXT, '
                             'gp_slug TEXT NOT NULL, '
                             'gp_cs_compat_windows INTEGER NOT NULL, '
                             'gp_cs_compat_osx INTEGER NOT NULL, '
                             'gp_cs_compat_linux INTEGER NOT NULL, '
                             'gp_languages TEXT, '
                             'gp_links_forum TEXT, '
                             'gp_links_product_card TEXT, '
                             'gp_links_support TEXT, '
                             'gp_in_development INTEGER NOT NULL, '
                             'gp_is_installable INTEGER NOT NULL, '
                             'gp_game_type TEXT NOT NULL, '
                             'gp_is_pre_order INTEGER NOT NULL, '
                             'gp_release_date TEXT, '
                             'gp_description_lead TEXT, '
                             'gp_description_full TEXT, '
                             'gp_description_cool TEXT, '
                             'gp_changelog TEXT)')

##main thread start

#added support for optional command-line parameter mode switching
parser = argparse.ArgumentParser(description=('GOG DB create (part of gog_visor) - a script to create the sqlite DB structure '
                                              'for the other gog_visor utilities.'))

args = parser.parse_args()

#db file check/creation section
if not path.exists(db_file_full_path):
    logger.info('No DB file detected. Creating new SQLite DB...')
    
    with sqlite3.connect(db_file_full_path) as db_connection:
        db_cursor = db_connection.cursor()
        db_cursor.execute(CREATE_GOG_COMPANIES_QUERY)
        db_cursor.execute(CREATE_GOG_FILES_QUERY)
        db_cursor.execute('CREATE INDEX gf_int_id_index ON gog_files (gf_int_id)')
        db_cursor.execute(CREATE_GOG_PRICES_QUERY)
        db_cursor.execute('CREATE INDEX gpr_int_id_index ON gog_prices (gpr_int_id)')
        db_cursor.execute(CREATE_GOG_PRODUCTS_QUERY)
        db_connection.commit()
    
    logger.info('DB created successfully.')
else:
    logger.error('Existing DB file detected. Please delete the existing file if you are attempting to recreate the DB!')

##main thread end
