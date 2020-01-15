from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from translate import Translator

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    dict = {'Afrikaans':'af', 'Albanian':'sq', 'Amharic':'am', 'Arabic':'ar', 'Armenian':'hy', 'Azerbaijani':'az', 'Basque':'eu', 'Belarusian':'be', 'Bengali':'bn', 'Bosnian':'bs', 'Bulgarian':'bg', 'Catalan':'ca','Cebuano':'ceb', 'Chinese':'CN', 'Chinese':'zh', 'Corsican':'co', 'Croatian':'hr', 'Czech':'cs', 'Danish':'da', 'Dutch':'nl', 'English':'en', 'Esperanto':'eo', 'Estonian':'et', 'Finnish':'fi', 'French':'fr', 'Frisian':'fy', 'Galician':'gl', 'Georgian':'ka', 'German':'de', 'Greek':'el', 'Gujarati':'gu', 'Haitian Creole':'ht', 'Hausa': 'ha', 'Hawaiian':'haw', 'Hebrew':'he', 'Hindi':'hi', 'Hmong':'hmn', 'Hungarian':'hu', 'Icelandic':'is', 'Igbo':'ig', 'Indonesian':'id', 'Irish':'ga', 'Italian':'it', 'Japanese':'ja', 'Javanese':'jv', 'Kannada':'kn', 'Kazakh':'kk', 'Khmer':'km', 'Korean':'ko', 'Kurdish':'ku', 'Kyrgyz':'ky', 'Lao':'lo', 'Latin':'la', 'Latvian':'lv', 'Lithuanian':'lt', 'Luxembourgish':'lb', 'Macedonian':'mk', 'Malagasy':'mg', 'Malay':'ms', 'Malayalam':'ml', 'Maltese':'mt', 'Maori':'mi', 'Marathi':'mr', 'Mongolian':'mn', 'Myanmar':'my', 'Nepali':'ne', 'Norwegian':'no', 'Nyanja':'ny', 'Pashto':'ps', 'Persian':'fa', 'Polish':'pl', 'Portuguese':'pt', 'Punjabi':'pa', 'Romanian':'ro', 'Russian':'ru', 'Samoan':'sm', 'Scots Gaelic':'gd', 'Serbian':'sr', 'Sesotho':'st', 'Shona':'sn', 'Sindhi':'sd', 'Sinhala':'si', 'Slovak':'sk', 'Slovenian':'sl', 'Somali':'so', 'Spanish':'es', 'Sundanese':'su', 'Swahili':'sw', 'Swedish':'sv', 'Tagalog':'tl', 'Tajik':'tg', 'Tamil':'ta', 'Telugu':'te', 'Thai':'th', 'Turkish':'tr', 'Ukrainian':'uk', 'Urdu':'ur', 'Uzbek':'uz', 'Vietnamese':'vi', 'Welsh':'cy', 'Xhosa':'xh', 'Yiddish':'yi', 'Yoruba':'yo', 'Zulu':'zu'}
    incoming_message = request.values.get('Body', '')
    incoming_msg = incoming_message.lower()
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            print(data)
            quote = f'{data["content"]} ({data["author"]})'
            print(quote)
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    # if responded == False:

    if 'translate' in incoming_msg:
        message = incoming_message.split(' from ')
        trans_lang = dict[message[1].split(' to ')[1].capitalize()]
        trans_text = message[0][10:]
        translator = Translator(to_lang=trans_lang, from_lang='autodetect')
        translation = translator.translate(trans_text)
        msg.body(translation)
        responded = True

    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)