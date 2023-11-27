from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import Word, Synonym, Addition, Type, BuildWord
import simplejson
from threading import Thread
import requests

API_URL = "https://api-inference.huggingface.co/models/Mokhiya/syn-roberta"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


allowed_chars = ['\'', ' ']


def createWord(word, add):
    if add == '':
        return word
    else:

        s = add.exeption
        arr = s.split('|')

        for w in arr:
            v = w.split('-')

            if word.endswith(v[0]):
                return word[:len(word) - len(v[1])] + v[2]
        if len(arr) > 0:
            v = w.split('-')
            if len(v) == 3:
                return word + v[2]
        return word


def createBuildWord(word, adds):
    for add in adds:
        word = createWord(word, add)
    return word


def createBuildWord2(word, cnt, additions):
    adds = Addition.objects.all();

    for add in adds:
        bword = createWordAdds(word, add)
        model = BuildWord.objects.create(word=bword, root=word, additions='')
        model.save()


def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator


@start_new_thread
def build_words(max_additions):
    words = Word.objects.get(pk=110)

    for w in [words]:
        adds = w.additions.all()
        # model = BuildWord.objects.create(word=w.s, root = w, additions = '')
        # model.save()
        for add in adds:
            bword = createWord(w.s, add)
            model = BuildWord.objects.create(word=bword, root=w, additions=add.add)
            model.save()
            adds2 = add.additions.all()
            for add2 in adds2:
                model = BuildWord.objects.create(word=createWord(bword, add2), root=w,
                                                 additions=add.add + '|' + add2.add)
                model.save()


def index(request):
    # BuildWord.objects.all().delete()
    # build_words(3)

    return render(request, 'index.html', {'from': '', 'to': ''})


def getWordIds(word):
    models = Word.objects.filter(s=word)
    arr = []
    for v in models:
        arr.append(v.id)
    return arr


def getAdditions(model):
    text = model.exeption
    arr = text.split('|')
    ret = []
    for s in arr:
        v = s.split('-')
        ret.append(v[0][:len(v[0]) - len(v[1])] + v[2])
    return ret


def getSynonyms(word, brr):
    adds = Addition.objects.all()

    for model in adds:

        s = model.exeption
        arr = s.split('|')
        for t in arr:
            wrr = [val for val in brr]
            v = t.split('-')
            txt = v[0][:len(v[0]) - len(v[1])] + v[2]
            if word.endswith(txt):
                ww = word[:len(word) - len(v[2])] + v[1]
                word_ids = getWordIds(ww)
                models = Synonym.objects.filter(Q(w1__in=word_ids) | Q(w2__in=word_ids))

                vrr = []
                for vc in models:
                    if vc.w1 in word_ids:
                        vrr.append(vc.w2.id)
                    else:
                        vrr.append(vc.w1.id)

                res = Word.objects.filter(id__in=vrr)
                if len(res) > 0:
                    wrr.append(model)
                    return res, wrr
                else:
                    wrr.append(model)
                    models, adds = getSynonyms(ww, wrr)
                    if len(models) > 0:
                        return models, adds

    word_ids = getWordIds(word)
    models = Synonym.objects.filter(Q(w1__in=word_ids) | Q(w2__in=word_ids))

    vrr = []
    for v in models:
        if v.w1 in word_ids:
            vrr.append(v.w2.id)
        else:
            vrr.append(v.w1.id)

    res = Word.objects.filter(id__in=vrr)
    if len(res) > 0:
        return res, []
    else:
        return Word.objects.filter(id__in=[]), []


def getWordsFromModels(models):
    arr = []
    for model in models:
        arr.append(model.s)
    return arr


def isSpaceable(str):
    return str == ' '


def createWordAdds(word, adds):
    adds = adds[::-1]
    for add in adds:
        word = createWord(word, add)
    return word


def getUnderlinedText(id, word, words, add):
    for i in range(len(words)):
        words[i] = '"' + createWordAdds(words[i], add) + '"'
        words[i] = words[i].replace("'", "&apos;")

    words = list(set(words))

    arr = '[' + ','.join(words) + ']'
    return '<span class = "marked-underlined" data-id = "' + str(id) + '" id = "mark-' + str(
        id) + '" data-words = \'' + arr + '\' onclick = "getWords(' + str(id) + ');">' + word + '</span>'


def removeFirstSpaces(text):
    for i in range(len(text)):
        if text[i] != ' ':
            return text[i:]
    return text


def getArrByText(text):
    arr = []
    text = removeFirstSpaces(text) + ' '
    word = ''
    chars = ''

    cur = 0
    for c in text:
        if c.isalpha() or c.isdigit() or c == '\'':
            if cur == 0:
                arr.append(chars)
            word += c
            chars = ''
            cur = 1
        else:
            if cur == 1:
                arr.append(word)
            cur = 0
            chars += c
            word = ''

    arr.append(chars)
    if len(arr) > 1:
        arr[-1] = arr[-1][:-1]
    return arr


def getSynonymText(id, text):
    arr = getArrByText(text)
    res = arr[0]

    i = 1
    while i < len(arr):
        find2 = False
        if i + 2 < len(arr):
            w = arr[i] + ' ' + arr[i + 2]
            models, add = getSynonyms(w, [])

            if len(models) > 0 and isSpaceable(arr[i + 1]):
                find2 = True
                res += getUnderlinedText(id * 100 + i, arr[i] + arr[i + 1] + arr[i + 2], getWordsFromModels(models),
                                         add)
                i += 3
        if find2 == False:
            w = arr[i]
            models, add = getSynonyms(w, [])
            if len(models) > 0:
                res += getUnderlinedText(id * 100 + i, arr[i], getWordsFromModels(models), add)
                i += 1
            else:
                res += arr[i]
                i += 1

        if i < len(arr):
            res += arr[i]
        i += 1

    return res


def view_words(request):
    words = Word.objects.all()
    return render(request, 'words.html', {'words': words})


@csrf_exempt
def check(request):
    # print(request)
    isGet = False
    text = ''
    if request.method == 'POST':
        text = request.POST['text']
    elif request.method == 'GET':
        if 'text' in request.GET:
            text = request.GET['text']
        isGet = True
    res = ''
    tmp = ''
    id = 1
    for c in text:
        if c.isalpha() or c.isdigit() or (c in allowed_chars):
            tmp += c
        else:
            res += getSynonymText(id, tmp)
            id += 1
            res += c
            tmp = ''

    res += getSynonymText(id, tmp)
    id += 1

    res = res.replace('< /', '</')

    data = ''
    result = simplejson.dumps({'html': res, 'data': data})
    if isGet:
        return render(request, 'index.html', {'from': text})
    else:
        return HttpResponse(result)
