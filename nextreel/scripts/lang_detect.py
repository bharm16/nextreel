import logging

from langdetect import detect
import pymysql

from nextreel.scripts.mysql_query_builder import execute_query

# Setup logging
logging.basicConfig(level=logging.INFO)


# Function to identify the language of a title
def identify_language(title):
    try:
        return detect(title)
    except:
        return None  # Unknown


# Map langdetect's language codes to your specific set of language codes
# Map langdetect's language codes to your specific set of language codes
# This is a partial mapping; you should complete it based on your needs.
lang_map = {
    'en': 'en',  # English
    'ja': 'ja',  # Japanese
    'sv': 'sv',  # Swedish
    'tr': 'tr',  # Turkish
    'es': 'es',  # Spanish
    'sr': 'sr',  # Serbian
    'cs': 'cs',  # Czech
    'ru': 'ru',  # Russian
    'fr': 'fr',  # French
    'hi': 'hi',  # Hindi
    'sk': 'sk',  # Slovak
    'zh-cn': 'cmn',  # Mandarin (Simplified Chinese)
    'fa': 'fa',  # Persian
    'bg': 'bg',  # Bulgarian
    'ca': 'ca',  # Catalan
    # 'qbn': '',  # Not sure about this one
    'nl': 'nl',  # Dutch
    'pt': 'pt',  # Portuguese
    'uz': 'uz',  # Uzbek
    'uk': 'uk',  # Ukrainian
    # 'qbp': '',  # Not sure about this one
    'ar': 'ar',  # Arabic
    # 'rn': '',   # Rundi (not supported by langdetect)
    'bs': 'bs',  # Bosnian
    'ga': 'ga',  # Irish
    'de': 'de',  # German
    'zh-yue': 'yue',  # Cantonese (Traditional Chinese)
    'th': 'th',  # Thai
    'yi': 'yi',  # Yiddish
    'ka': 'ka',  # Georgian
    'sl': 'sl',  # Slovenian
    'hr': 'hr',  # Croatian
    'he': 'he',  # Hebrew
    'it': 'it',  # Italian
    'tg': 'tg',  # Tajik
    'kk': 'kk',  # Kazakh
    'bn': 'bn',  # Bengali
    'da': 'da',  # Danish
    'el': 'el',  # Greek
    'fi': 'fi',  # Finnish
    'be': 'be',  # Belarusian
    # 'gsw': '',  # Swiss German (not supported by langdetect)
    'gl': 'gl',  # Galician
    'eu': 'eu',  # Basque
    'az': 'az',  # Azerbaijani
    'ms': 'ms',  # Malay
    'pl': 'pl',  # Polish
    'id': 'id',  # Indonesian
    'mr': 'mr',  # Marathi
    # 'qbo': '',  # Not sure about this one
    'mi': 'mi',  # Maori
    'la': 'la',  # Latin
    'ta': 'ta',  # Tamil
    'lt': 'lt',  # Lithuanian
    'lv': 'lv',  # Latvian
    'af': 'af',  # Afrikaans
    'hy': 'hy',  # Armenian
    'ur': 'ur',  # Urdu
    'te': 'te',  # Telugu
    'ro': 'ro',  # Romanian
    'ml': 'ml',  # Malayalam
    'tl': 'tl',  # Tagalog
    'mk': 'mk',  # Macedonian
    'et': 'et',  # Estonian
    'gd': 'gd',  # Scottish Gaelic
    'cy': 'cy',  # Welsh
    # 'qal': '',  # Not sure about this one
    'xh': 'xh',  # Xhosa
    'gu': 'gu',  # Gujarati
    'kn': 'kn',  # Kannada
    # 'eka': '',  # Ekajuk (not supported by langdetect)
    'ko': 'ko',  # Korean
    'tk': 'tk',  # Turkmen
    'lb': 'lb',  # Luxembourgish
    'ky': 'ky',  # Kyrgyz
    'wo': 'wo',  # Wolof
    'zh': 'zh',  # Chinese
    'no': 'no',  # Norwegian
    'is': 'is',  # Icelandic
    'hu': 'hu',  # Hungarian
    'sq': 'sq',  # Albanian
    'vi': 'vi',  # Vietnamese
    'pa': 'pa',  # Punjabi
    'sd': 'sd',  # Sindhi
    'ps': 'ps',  # Pashto
    'zu': 'zu',  # Zulu
    'ku': 'ku',  # Kurdish
    # 'roa': '',  # Romance languages (not supported by langdetect)
    'tn': 'tn',  # Tswana
    'rm': 'rm',  # Romansh
    'su': 'su',  # Sundanese
    'jv': 'jv',  # Javanese
    'st': 'st',  # Sotho
    # 'prs': '',  # Dari (not supported by langdetect)
    # 'jsl': '',  # Yugoslavian Sign Language (not supported by langdetect)
    # 'fro': '',  # Old French (not supported by langdetect)
    'haw': 'haw',  # Hawaiian
    'mn': 'mn',  # Mongolian
    'lo': 'lo',  # Lao
    'my': 'my',  # Burmese
    'am': 'am',  # Amharic
    # 'qac': '',  # Not sure about this one
    'ne': 'ne',  # Nepali
    # 'myv': '',  # Erzya (not supported by langdetect)
    'br': 'br',  # Breton
    # 'iu': '',  # Inuktitut (not supported by langdetect)
    # 'cr': ''   # Cree (not supported by langdetect)
}

# Note: Some languages are not supported by langdetect and have been commented out.


# Database connection setup
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}


# Method to get DB connection (from get_movie_from_imdb.py)
def get_db_connection(db_config):
    """Establish a connection to the database."""
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        autocommit=True  # Auto-commit changes after each query
    )


# Establish a connection to the database
connection = get_db_connection(db_config)

# try:
#     with connection.cursor() as cursor:
#         fetch_sql = "SELECT titleId, title FROM `title.akastest` WHERE isOriginalTitle = '1'"
#         cursor.execute(fetch_sql)
#
#         for row in cursor.fetchall():
#             titleId, title = row
#             detected_lang = identify_language(title)
#             if detected_lang is not None:
#                 logging.info(f"Detected language for titleId {titleId}: {detected_lang}")
#                 mapped_lang = lang_map.get(detected_lang, None)
#                 update_sql = """
#                 UPDATE `title.basics`
#                 SET language = %s
#                 WHERE tconst = %s AND tconst IN (SELECT titleId FROM `title.akastest` WHERE titleId = %s);
#                 """
#                 execute_query(db_config, update_sql, (mapped_lang, titleId, titleId))
#                 logging.info(f"Updated language for titleId {titleId} in title.basics")
#
#             else:
#                 logging.warning(f"Could not detect language for titleId {titleId}. Skipping update.")
#
# finally:
#     connection.close()
#     logging.info("Database connection closed.")


def update_language_in_title_basics(db_config):
        print("Entered update_language_in_title_basics function.")  # Debugging line

        # SQL query to fetch titleId and title from title.akastest where isOriginalTitle = '1'
        fetch_sql = "SELECT titleId, title FROM `title.akastest` WHERE isOriginalTitle = '1'"

        # Execute the query and fetch all results
        rows = execute_query(db_config, fetch_sql, fetch='all')

        for row in rows:
            titleId = row['titleId']
            title = row['title']

            # Assuming you have a function identify_language that takes a title and returns its language
            detected_lang = identify_language(title)

            if detected_lang:
                print(f"Detected language for titleId {titleId}: {detected_lang}")  # Debugging line

                # SQL query to update language in title.basics table
                update_sql = """
                UPDATE `title.basics`
                SET language = %s
                WHERE tconst = %s AND tconst IN (SELECT titleId FROM `title.akastest` WHERE titleId = %s)
                """

                # Execute the update query
                execute_query(db_config, update_sql, params=(detected_lang, titleId, titleId), fetch='none')
                print(f"Updated language for titleId {titleId} in title.basics")  # Debugging line

            else:
                print(f"Could not detect language for titleId {titleId}. Skipping update.")  # Debugging line


# Example usage
if __name__ == "__main__":
    print("Script started.")  # Debugging line

    # Assuming db_config is defined somewhere
    update_language_in_title_basics(db_config)