import requests
import urllib
from pprint import pprint
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
APP_ACCESS_TOKEN = response['access_token']
BASE_URL = 'https://api.instagram.com/v1/'

def owner_info():
    r = requests.get('%susers/self/?access_token=%s' %(BASE_URL , APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        print "Username is %s" % (r['data']['username'])
        print "No of followers are %s"  %( r['data'] ['counts'] ['followed_by'])
        print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
        print 'No. of posts: %s' % (r['data']['counts']['media'])

    else:
        print " Status code other than 200 received"




def owner_post():
    r = requests.get('%susers/self/media/recent/?access_token=%s' %(BASE_URL , APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        url = r['data'][1]['images']['standard_resolution']['url']
        name = r['data'][1]['id'] + '.jpg'
        urllib.urlretrieve(url,name)
        print "Your image is downloaded"

    else:
        print " Status code other than 200 received"
def get_user_id(uname):
    r=requests.get('%susers/search?q=%s&access_token=%s'%(BASE_URL, uname,APP_ACCESS_TOKEN)).json()
    pprint(r)
    return r['data'][0]['id']


def user_info(uname):
    user_id=get_user_id(uname)
    r = requests.get('%susers/%s/?access_token=%s' % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        print "Username is %s" % (r['data']['username'])
        print "No of followers are %s" % (r['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
        print 'No. of posts: %s' % (r['data']['counts']['media'])

    else:
        print " Status code other than 200 received"

def user_post(username):
    user_id = get_user_id(username)
    r = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        print r['data'][0]['images']['standard_resolution']['url']
        url = r['data'][0]['images']['standard_resolution']['url']
        name = r['data'][0]['id'] + '.jpg'
        urllib.urlretrieve(url, name)
        print "Your image is downloaded"

    else:
        print " Status code other than 200 received"

def get_media_id(uname):
    user_id = get_user_id(uname)
    r = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        return r['data'][1]['id']

    else:
        print " Status code other than 200 received"


def like_post(uname):
    media_id = get_media_id(uname)
    payload = {"access_token": APP_ACCESS_TOKEN}
    url = BASE_URL + 'media/%s/likes' %(media_id)
    r= requests.post(url,payload).json
    if r['meta']['code']==200:
        print 'Like hogya hai'
    else:
        print 'Like ni hua'


def comment_post(uname):
    media_id = get_media_id(uname)
    payload = {"access_token": APP_ACCESS_TOKEN,"text":comment}
    comment = raw_input('What is your comment ? ')
    url = BASE_URL + 'media/%s/comments' % (media_id)
    r = requests.post(url, payload).json
    if r['meta']['code'] == 200:
        print 'Comment hogya hai'
    else:
        print 'Comment ni hua'


def delete_comment(uname):
    media_id = get_media_id(uname)
    r = requests.get('%smedia/%s/comments?access_token=%s'  %(BASE_URL,media_id,APP_ACCESS_TOKEN)).json
    if r ['meta'] ['code']==200:
        if len (r['data']) > 0 :
            for index in range(0,len(r['data'])):
                comment_id = r['data'][index]['id']
                comment_text = r['data'][index]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print 'Negative comment : %s' % comment_text
                    r = requests.delete('%smedia/%s/comments/%s/?access_token=%s' % (
                    BASE_URL, media_id, comment_id, APP_ACCESS_TOKEN)).json()
                    if r['meta']['code'] == 200:
                        print 'Comment successfully deleted!'
                    else:
                        print 'Could not delete the comment'
                else:
                    print comment_text + 'is a positive comment'
        else:
            print 'No Comments found'
    else:
        print "Error"


def start_bot():
    show_menu = True
    while show_menu:
        query = input('What do you want to do? \n 1. Get Owner Info \n 2. Get owner post \n 3. Get User Info \n 4. Get User Post \n 5. Like a post \n 6. Comment on a post \n 7. Delete negative comments \n  0. Exit ')
        if query==1:
            owner_info()
        elif query==2:
            owner_post()
        elif query==3:
            user_name=raw_input('What is the username of that user? ')
            user_info(user_name)
        elif query==4:
            user_name = raw_input('What is the username of that user? ')
            user_post(user_name)
        elif query==5:
            user_name=raw_input('What is the username of that user? ')
            like_post(user_name)
        elif query==6:
            user_name = raw_input('What is the username of that user? ')
            comment_post(user_name)
        elif query==7:
            user_name = raw_input('What is the username of that user? ')
            del_comment(user_name)
        elif query==0:
            show_menu = False
        else:
            print'Please fill the valid choice'


start_bot()