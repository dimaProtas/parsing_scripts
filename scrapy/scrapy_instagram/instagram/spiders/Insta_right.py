import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from instagram.items import InstagramItem


class InstaSpider(scrapy.Spider):
    name = 'Insta'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    login = 'oandreeva88@mail.ru'
    password ='#PWD_INSTAGRAM_BROWSER:9:1597045909:AVdQANMTHh3/b/aRVQieSeaUSCBi8n/DeW1KqbFNsFcj92J+j16LT98SbAkIo11CEF5LLrN2VHknjK5e9WhJpt6uvNWm6rtX57YiiXEcVItKcElQPqYExGK55JjmE4Cwidpm6pQ5vMlKOtqx'
    start_link ='https://www.instagram.com/accounts/login/ajax/'
    users = ['svetlanagureva_art', 'inmary']
    graphQLurl = 'https://www.instagram.com/graphql/query/?'
    hash_followIN = 'c76146de99bb02f6415203be841dd25a'
    hash_followOut = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response):
        token = self.csrf_token(response.text)
        yield scrapy.FormRequest(self.start_link, method='POST', 
                                 formdata={'username':self.login, 'enc_password':self.password},
                                 callback = self.parse_user,
                                 headers = {'X-CSRFToken':token})
        
    def parse_user(self, response:HtmlResponse):
        answer = json.loads(response.text)
        if answer['authenticated']:
            for login in self.users:
                yield response.follow(f'/{login}', callback = self.followNext, cb_kwargs = {'username':login})

    
    def followNext(self, response:HtmlResponse, username):
        userID = self.id_user(response.text, username)
        variables = {'id':userID, "include_reel":'true',
                        "fetch_mutual":'true',"first":50}

        urlIn = f'{self.graphQLurl}query_hash={self.hash_followIN}&{urlencode(variables)}'
        urlOut = f'{self.graphQLurl}query_hash={self.hash_followOut}&{urlencode(variables)}'


        yield response.follow(urlIn, callback = self.inafter,
                              cb_kwargs={'username':username, 
                                         'userID':userID, 
                                         'variables':deepcopy(variables)})

        yield response.follow(urlOut, callback=self.outafter,
                              cb_kwargs={'username': username,
                                         'userID': userID,
                                         'variables': deepcopy(variables)})

            
    def inafter(self, response:HtmlResponse, username, userID, variables):
        j_data = json.loads(response.text)
        data = j_data.get('data').get('user').get('edge_followed_by')
        isNext = data.get('page_info').get('has_next_page')
        
        if isNext:
            variables['after'] = data.get('page_info').get('end_cursor')
            
            urlIn = f'{self.graphQLurl}query_hash={self.hash_followIN}&{urlencode(variables)}'
            yield response.follow(urlIn, callback = self.inafter,
                                  cb_kwargs={'username':username,
                                             'userID':userID,
                                             'variables':deepcopy(variables)})
        followers = data.get('edges')
        for f in followers:
            item = InstagramItem(
                    user_id = userID,
                    user = username,
                    how = 'in',
                    data = f,
                    ava = f['node']['profile_pic_url'], 
                    name = f['node']['full_name']
                    )
            yield item

    def outafter(self, response:HtmlResponse, username, userID, variables):
        j_data = json.loads(response.text)
        data = j_data.get('data').get('user').get('edge_follow')
        isNext = data.get('page_info').get('has_next_page')
        if isNext:
            variables['after'] = data.get('page_info').get('end_cursor')

            urlOut = f'{self.graphQLurl}query_hash={self.hash_followOut}&{urlencode(variables)}'
            yield response.follow(urlOut, callback = self.outafter,
                                  cb_kwargs={'username':username,
                                             'userID':userID,
                                             'variables':deepcopy(variables)})
        followings = data.get('edges')
        for f in followings:
            item = InstagramItem(
                    user_id = userID,
                    user = username,
                    how = 'out',
                    data = f,
                    ava = f['node']['profile_pic_url'],
                    name = f['node']['full_name']
                    )
            yield item


    def csrf_token(self, text):
        token = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return token.split(':').pop().replace(r'"', '')

    def id_user(self, text, username):
        Uid = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(Uid).get('id', username)
    