# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""
import cyrtranslit

from .mapping_ru_eng_config import RU_CYR_TO_LAT_DICT, RU_LAT_TO_CYR_DICT


class Translator:
    """Переводчик русских слов в кириллицу и обратно"""

    def __init__(self):
        self._cyrtranslit = self._updated_cyrtranslit()

    @staticmethod
    def _updated_cyrtranslit():
        """Обновление словарей cyrtranslit новой буквенной конфигурацией"""

        cyrtranslit.TRANSLIT_DICT.update({
            'ru': {  # Russian
                'tolatin': RU_CYR_TO_LAT_DICT,
                'tocyrillic': RU_LAT_TO_CYR_DICT
            }
        })
        return cyrtranslit

    def ru_cyr_to_lat(self, text):
        """Перевод с кириллицы в латиницу"""

        return self._cyrtranslit.to_latin(string_to_transliterate=text, lang_code='ru')

    def ru_lat_to_cyr(self, text):
        """Перевод с латиницы в кириллицу"""

        return self._cyrtranslit.to_cyrillic(string_to_transliterate=text, lang_code='ru')
