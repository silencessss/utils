## Introduction
While I using a [google translate API](https://pypi.org/project/googletrans/) on PyPI, a problem still appear that "AttributeError: 'NoneType' object has no attribute 'group'". I trying to deal with the problem, not sucessed. Fortunately, I found another API: [google-trans-new](https://pypi.org/project/google-trans-new/).


## Problem
Problem 1. `json.decoder.JSONDecodeError: Extra data: line 1 column 340 (char 339)`

Solution: Open `google_trans_new.py` in line 151. Modified `response = (decoded_line + ']')` to `response = decoded_line`.

## Note
1. ::input:: '範例' → ::output:: 'example '. 注意字串末尾有空白符。

## language code
{'Filipino': 'fil','Hebrew': 'he','afrikaans': 'af','albanian': 'sq','amharic': 'am','arabic': 'ar','armenian': 'hy','azerbaijani': 'az','basque': 'eu','belarusian': 'be','bengali': 'bn','bosnian': 'bs','bulgarian': 'bg','catalan': 'ca','cebuano': 'ceb','chichewa': 'ny','chinese (simplified)': 'zh-cn','chinese (traditional)': 'zh-tw','corsican': 'co','croatian': 'hr','czech': 'cs','danish': 'da','dutch': 'nl','english': 'en','esperanto': 'eo','estonian': 'et','filipino': 'tl','finnish': 'fi','french': 'fr','frisian': 'fy','galician': 'gl','georgian': 'ka','german': 'de','greek': 'el','gujarati': 'gu','haitian creole': 'ht','hausa': 'ha','hawaiian': 'haw','hebrew': 'iw','hindi': 'hi','hmong': 'hmn','hungarian': 'hu','icelandic': 'is','igbo': 'ig','indonesian': 'id','irish': 'ga','italian': 'it','japanese': 'ja','javanese': 'jw','kannada': 'kn','kazakh': 'kk','khmer': 'km','korean': 'ko','kurdish (kurmanji)': 'ku','kyrgyz': 'ky','lao': 'lo','latin': 'la','latvian': 'lv','lithuanian': 'lt','luxembourgish': 'lb','macedonian': 'mk','malagasy': 'mg','malay': 'ms','malayalam': 'ml','maltese': 'mt','maori': 'mi','marathi': 'mr','mongolian': 'mn','myanmar (burmese)': 'my','nepali': 'ne','norwegian': 'no','pashto': 'ps','persian': 'fa','polish': 'pl','portuguese': 'pt','punjabi': 'pa','romanian': 'ro','russian': 'ru','samoan': 'sm','scots gaelic': 'gd','serbian': 'sr','sesotho': 'st','shona': 'sn','sindhi': 'sd','sinhala': 'si','slovak': 'sk','slovenian': 'sl','somali': 'so','spanish': 'es','sundanese': 'su','swahili': 'sw','swedish': 'sv','tajik': 'tg','tamil': 'ta','telugu': 'te','thai': 'th','turkish': 'tr','ukrainian': 'uk','urdu': 'ur','uzbek': 'uz','vietnamese': 'vi','welsh': 'cy','xhosa': 'xh','yiddish': 'yi','yoruba': 'yo','zulu': 'zu'}
