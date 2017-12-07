"""
Tasks done:

1) Show help.
2) Print the program's installed version
3) Basic statistics about merged/closed rate.
4) User who opened.
5) User who closed.
6) Attached labels.
7) Number of comments created.
8) Day of the week opened.
9) Day of the week closed.
10) Number of days opened.

"""
import base64
import ConfigParser
import datetime
import getopt
from getpass import getpass
import json
import requests
from requests.auth import HTTPBasicAuth
from sys import argv


def get_credentials():
    config = ConfigParser.ConfigParser()
    config.read("settings")
    if config.has_option('main', 'login'):
        user = config.get('main', 'login')
        password = config.get('main', 'password')
        return base64.b64decode(user), base64.b64decode(password)
    else:
        print "Yoy need valid credentials to access GutHub."
        user = raw_input("Please, input your github login: ")
        password = getpass("Please, input you password: ")
        settings = file("settings", "a")
        settings.write('\n'+'login = ' + base64.b64encode(user)+'\n')
        settings.write('password = ' + base64.b64encode(password)+'\n')
        settings.close()
        return user, password


def get_labels():
    link = 'https://api.github.com/repos/alenaPy/devops_lab/labels'
    user, password = get_credentials()
    r = requests.get(link, auth=HTTPBasicAuth(user, password))
    pars = json.loads(r.content)
    for name in pars:
        print name['name']
    r.close()

def count_merged_pr(big_json, what_to_count):
    json_parse = json.loads(big_json)
    count = 0
    for item in json_parse:
        if item[str(what_to_count)]:
            count += 1
    return count

def make_http_req(link):
    user, password = get_credentials()
    r = requests.get(link, auth=HTTPBasicAuth(user, password))
    return r


def go_through_pages(link, what_to_look):
    count = 0
    r = make_http_req(link)
    if r.links:
        last_link = r.links['last']['url']
        while True:
            r = make_http_req(r.links['next']['url'])
            count += count_merged_pr(r.content, what_to_look)
            if r.url == last_link:
                break
    else:
        count += count_merged_pr(r.content, what_to_look)
    return str(count)


def get_merged(link):
    return go_through_pages(link, 'merged_at')


def get_numbers_of_pr(link):
    parsed_answer = json.loads(make_http_req(link).content)
    return parsed_answer[0]['number']

def get_closed_pr(link):
    return go_through_pages(link, 'closed_at')

def check_user_repo(user, repo):
    r = make_http_req('https://api.github.com/users/'+str(user))
    my_flag = bool(True)
    if r.status_code != 200:
        print "Sorry, can't find user" + str(user)
        my_flag = False
    else:
        r = make_http_req('https://api.github.com/repos/'+str(user)+'/'+str(repo))
        if r.status_code != 200:
            print "Sorry, no such repository"
            my_flag = False
    return my_flag


def get_comments(link):
    return go_through_pages(link, 'body')


def get_label(link):
    r = json.loads(make_http_req(main_link).content)
    labels = ""
    for i in r['labels']:
        labels += i['name']+" "
    return labels


def get_version():
    config = ConfigParser.ConfigParser()
    config.read("settings")
    print config.get('main', 'version')


def user_in_pr(link, pr):
    resp = make_http_req(link+'/pulls/'+str(pr))
    json_parsed = json.loads(resp.content)
    if json_parsed.get('closed_at'):
        resp = make_http_req(link + '/issues/' + str(pr))
        json_parsed = json.loads(resp.content)
        message = "PR is closed. User who closed: " + (json_parsed.get('closed_by')).get('login')
    else:
        message = "PR is opened. User who opened: " + ((json_parsed.get('user')).get('login'))
    return message

def parse_date_param(link):
    resp = make_http_req(link)
    json_parsed = json.loads(resp.content)
    if json_parsed.get('closed_at'):
        print json_parsed.get('closed_at')
        closed_date = datetime.datetime.strptime(json_parsed.get('closed_at')[:10], "%Y-%m-%d").date()
        closed_day = datetime.datetime.strptime(json_parsed.get('closed_at')[:10], '%Y-%m-%d').strftime('%A')
        message = "Sorry, PR is closed at " + str(closed_day) + "," + str(closed_date)
    else:
        pr_date = datetime.datetime.strptime(json_parsed.get('created_at')[:-1], "%Y-%m-%dT%H:%M:%f").date()
        message = "PR is opened " + str(datetime.datetime.now().day-pr_date.day) + " days ago."
        day = datetime.datetime.strptime(json_parsed.get('created_at')[:10], '%Y-%m-%d').strftime('%A')
        message += "It was "+str(day)+"."
    return message

def print_help():
    print """

      Usage: task5.py username repository [-s all|merged|closed][-c PR_NUMB][-l PR_NUMB][-u PR_NUMB][-d PR_NUMB]

      username - name of user you want to look in github
      repository - name of repo you want to look in github
      PR_NUMB - number of pull request

      [-s all|merged|closed]: shows stats for repository:
          all - all stats
          merged - only merged
          closed - only closed
      [-c PR_NUMB]: shows number of comments in pull request
      [-l PR_NUMB]: shows labels in pull request
      [-u PR_NUMB]: shows info about users who opened/closed pull request
      [-d PR_NUMB]: shows date info about pull request
      """


if len(argv) == 1:
    print "Usage: "+argv[0]+" username repository [options]"
elif argv[1] == '-h' or argv[1] == '--help':
    print_help()
elif argv[1] == '-v' or argv[1] == '--version':
    get_version()
elif len(argv) >= 3:
    can_go = check_user_repo(argv[1], argv[2])
    if can_go:
        main_link = 'https://api.github.com/repos/' + str(argv[1]) + '/' + str(argv[2])
        print "USERNAME: "+argv[1]+" REPOSITORY: " + argv[2]
        myopts, args = getopt.getopt(argv[3:], "s:c:l:u:d:")
        for s, v in myopts:
            if s == '-s':
                main_link += '/pulls?state'
                merged = get_merged(main_link + '=all')
                closed_pr = get_closed_pr(main_link + '=closed')
                all_pr = get_numbers_of_pr(main_link + '=all')
                if v == 'all':
                    print "Total PR="+str(all_pr)+". Merged - " + str(merged) + ", closed - " + str(closed_pr)
                if v == 'merged':
                    print "merged - " + str(merged)
                if v == "closed":
                    print "closed - " + str(closed_pr)
            elif s == '-c':
               main_link += '/pulls/'+str(v)+'/comments'
               comments = get_comments(main_link)
               if int(comments) == 0:
                    print "Sorry, this PR seems to be closed."
               else:
                    print "Total comments for PR #" + str(v) + " - "+str(comments)
            elif s == '-l':
                main_link += '/issues/' + str(v)
                print main_link
                label = get_label(main_link)
                if label:
                    print "Labels for PR #" + str(v) + ": " + str(label)
                else:
                    print "No labels found"
            elif s == '-u':
                print user_in_pr(main_link, str(v))
            elif s == '-d':
                print "here!"
                main_link += '/pulls/' + str(v)
                print parse_date_param(main_link)
else:
    print_help()
