from bs4 import BeautifulSoup


def parse_message_text(request):
    text = request.data.get('text')

    if request.method == 'PUT' and not text:
        return
    if not text:
        raise ValueError('empty message text')

    clear_text = BeautifulSoup(text, features='html.parser').get_text()

    if not clear_text:
        raise ValueError('wrong message text')
    request.data['text'] = clear_text
