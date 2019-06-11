# Interactive python 2 client for fizzbot

import json
import urllib2

domain = 'http://api.noopschallenge.com'

def print_sep(): print('----------------------------------------------------------------------')

# print server response
def print_response(dict):
    print('')
    print('message:')
    print(dict.get('message'))
    print('')
    for key in dict:
        if key != 'message':
            print('%s: %s' % (key, json.dumps(dict.get(key))))
    print('')

# try an answer and see what fizzbot thinks of it
def try_answer(question_url, answer):
    print_sep()
    body = json.dumps({ 'answer': answer })
    print('*** POST %s %s' % (question_url, body))
    try:
        req = urllib2.Request(domain + question_url, body, {'Content-Type': 'application/json'})
        res = urllib2.urlopen(req)
        response = json.load(res)
        print_response(response)
        print_sep()
        return response

    except urllib2.HTTPError as e:
        response = json.load(e)
        print_response(response)
        return response

# keep trying answers until a correct one is given
def get_correct_answer(question_url, ans):
    while True:
        response = try_answer(question_url, ans)

        if (response.get('result') == 'interview complete'):
            print('congratulations!')
            exit()

        if (response.get('result') == 'correct'):
            return response.get('nextQuestion')

def matchRule(p):
    if p[1]%p[0]['number'] == 0:
        return p[0]['response']
    else:
        return ''

def go(rules, l):
    ans = []
    for i in l:
        res = ''.join(map(matchRule,zip(rules,[i]*len(rules))))
        if len(res)>0:
            ans.append(res)
        else:
            ans.append(str(i))
    return ' '.join(ans)

# do the next question
def do_question(domain, question_url):
    print_sep()
    print('*** GET %s' % question_url)

    question_data = json.load(urllib2.urlopen( ('%s%s' % (domain, question_url)) ))
    print('*'*20)
    print(question_data)
    print('*'*20)
    print_response(question_data)
    print_sep()

    next_question = question_data.get('nextQuestion')

    if next_question: return next_question
    if 'rules' in question_data.keys():
        return get_correct_answer(question_url, go(question_data['rules'], question_data['numbers']))
    else:
        return get_correct_answer(question_url, '{"answer":"COBOL"}')


def main():
    question_url = '/fizzbot'
    question_url = do_question(domain, question_url)
    while question_url:
        question_url = do_question(domain, question_url)

if __name__ == '__main__': main()
