import re
from googletrans import Translator
import pandas as pd
import os

cwd = os.getcwd()
root_dir = cwd + r'\translations'
if not os.path.exists(root_dir):
    os.mkdir(root_dir)

properties_file = "{0}\i18n.properties".format(cwd)

f = open(properties_file,"r", encoding="utf-8")
data_org = f.read()
f.close()

matchinglines = re.findall(".*=.*", data_org)

entrytag, entrytext = [], []

for line in matchinglines:
    splitline = line.split("=")
    entrytag.append(splitline[0])
    entrytext.append(splitline[-1])

print("default i18n file scanned\n")

#langs = ['es']#,'nl', 'pl', 'no', 'sk', 'fi', 'sv', 'pt', 'ja', 'zh-cn', 'ko','it', 'tr', 'ru','th','zh-tw','hr', 'cs', 'de','fr', 'da', 'hu',]
langs = ['hr', 'cs', 'de','fr', 'da', 'hu','es','nl', 'pl', 'no', 'sk', 'fi', 'sv', 'pt', 'ja', 'zh-cn', 'ko','it', 'tr', 'ru','th','zh-tw']

for lang in langs:
    if not os.path.exists(root_dir+r'\{0}'.format(lang)):
        os.mkdir(root_dir+r'\{0}'.format(lang))
    os.chdir(root_dir+r'\{0}'.format(lang))
    src_lang = "en"
    dest_lang = lang
    output_file = r"i18_{0}.properties".format(dest_lang)
    unicode_file = r"unicode_{0}.txt".format(dest_lang)
    excel_file = r"i18_details_{0}.xlsx".format(dest_lang)
    
    print("{0} lang started".format(lang))
    data = data_org
    
    trans = Translator()
    translatedtext = []
    
    translations = trans.translate(entrytext, src=src_lang, dest=dest_lang)
    
    for translation in translations:
    	translatedtext.append(translation.text)

    entryuni = []
    count = 0
    for line in translatedtext:
        lineunicode=''
        words = re.findall(r'{[^}]*}|\：|\:|[\w]+', line)
        linewords=''
        for word in words:
            if '{' not in word or '}' not in word:
                characters = list(word)
                linechars=''
                for char in characters:
                    if re.search('[^A-Za-z\:\?]', char):
                        unic = str(hex(ord(char)))
                        unic = unic[2:].zfill(4)
                        unic = r'\u' + unic
                    else:
                        unic = char
                    linechars = linechars + unic
                linewords = linewords + ' ' + linechars
            else:
                linewords = linewords + ' ' + word 
        lineunicode = lineunicode + linewords 
        entryuni.append(lineunicode)
        count = count +1

    f2 = open(unicode_file,'w') 
    for index, item in enumerate(entryuni):
        f2.write(u"{0}     {1}".format(entrytag[index], entryuni[index]))
        f2.write("\n")
    f2.close()
    print("\tunicode file created")
    
    f3 = open(output_file, 'w', encoding="utf-8")
    for index, item in enumerate(entrytext[1:]):
        repl_str = r"={0}".format(entryuni[index+1])
        data = re.sub("=("+re.escape(item)+")\\n", repl_str.replace('\\u', r'\\u')+"\n", data)
    f3.write(data)
    f3.close()
    print("\tiproperties file created")
    
    # finalarray = [entrytag, entrytext, translatedtext]
    # df = pd.DataFrame(finalarray)
    # df.T.to_excel(excel_file)
    # print("\texcel file created")
    print("{0} lang completed".format(lang))
