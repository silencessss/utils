from google_trans_new import google_translator

SRC = '膚質'
Langcodes={'Filipino': 'fil','Hebrew': 'he','afrikaans': 'af','albanian': 'sq','amharic': 'am','arabic': 'ar','armenian': 'hy','azerbaijani': 'az','basque': 'eu','belarusian': 'be','bengali': 'bn','bosnian': 'bs','bulgarian': 'bg','catalan': 'ca','cebuano': 'ceb','chichewa': 'ny','chinese (simplified)': 'zh-cn','chinese (traditional)': 'zh-tw','corsican': 'co','croatian': 'hr','czech': 'cs','danish': 'da','dutch': 'nl','english': 'en','esperanto': 'eo','estonian': 'et','filipino': 'tl','finnish': 'fi','french': 'fr','frisian': 'fy','galician': 'gl','georgian': 'ka','german': 'de','greek': 'el','gujarati': 'gu','haitian creole': 'ht','hausa': 'ha','hawaiian': 'haw','hebrew': 'iw','hindi': 'hi','hmong': 'hmn','hungarian': 'hu','icelandic': 'is','igbo': 'ig','indonesian': 'id','irish': 'ga','italian': 'it','japanese': 'ja','javanese': 'jw','kannada': 'kn','kazakh': 'kk','khmer': 'km','korean': 'ko','kurdish (kurmanji)': 'ku','kyrgyz': 'ky','lao': 'lo','latin': 'la','latvian': 'lv','lithuanian': 'lt','luxembourgish': 'lb','macedonian': 'mk','malagasy': 'mg','malay': 'ms','malayalam': 'ml','maltese': 'mt','maori': 'mi','marathi': 'mr','mongolian': 'mn','myanmar (burmese)': 'my','nepali': 'ne','norwegian': 'no','pashto': 'ps','persian': 'fa','polish': 'pl','portuguese': 'pt','punjabi': 'pa','romanian': 'ro','russian': 'ru','samoan': 'sm','scots gaelic': 'gd','serbian': 'sr','sesotho': 'st','shona': 'sn','sindhi': 'sd','sinhala': 'si','slovak': 'sk','slovenian': 'sl','somali': 'so','spanish': 'es','sundanese': 'su','swahili': 'sw','swedish': 'sv','tajik': 'tg','tamil': 'ta','telugu': 'te','thai': 'th','turkish': 'tr','ukrainian': 'uk','urdu': 'ur','uzbek': 'uz','vietnamese': 'vi','welsh': 'cy','xhosa': 'xh','yiddish': 'yi','yoruba': 'yo','zulu': 'zu'}
Langcodes_value=[]
for k,v in Langcodes.items():
    Langcodes_value.append(v)

trans_arr=[]
# Translation
for i in range(len(Langcodes_value)):
    translator = google_translator()
    try:
        trans_text = translator.translate(SRC,lang_tgt=Langcodes_value[i])
        print(trans_text)
        trans_arr.append(trans_text)
    except:
        print('::|INFO|:: Start error with..',Langcodes_value[i])
print('::|INFO|:: All language have ..',len(trans_arr))
