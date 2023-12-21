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
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    insta_login = 'Onliskill_udm'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1597686026:AXZQAGiE2YwFIBtTijGNQylo1GUOPqJbcfHriZaRui08ZO828NQRP4IbD4yU+l8V1oKYSYbRSCtYmfsJwgRwi83oSqyHz64mqjl0mBaaVGQSHOgBUNuekvx8dIXEN1BNRo8O+t90zqCUaacE/g=='
    parse_user = 'ai_machine_learning'
    query_hash_posts = 'bfa387b2992c3a52dcbe447467b4b771'
    graphql_url = 'https://www.instagram.com/graphql/query/?'

    def parse(self, response:HtmlResponse):
        csrf_token = self.csrf_token(response.text)
        yield scrapy.FormRequest(
            self.login_url,
            method='POST',
            callback= self.user_parse,
            formdata={'username':self.insta_login,
                      'enc_password':self.insta_pass},
            headers={'X-CSRFToken':csrf_token}
        )

    def user_parse(self,response:HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username':self.parse_user}
            )


    def user_data_parse(self,response:HtmlResponse,username):
        user_id = self.id_user(response.text, username)
        variables={'id':user_id,'first':12}
        url_posts = f'{self.graphql_url}query_hash={self.query_hash_posts}&{urlencode(variables)}'

        yield response.follow(
            url_posts,
            callback= self.user_posts_parse,
            cb_kwargs={'username':username,
                       'user_id':user_id,
                       'variables':deepcopy(variables)}
        )
    


    def user_posts_parse(self,response:HtmlResponse,username,user_id,variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.graphql_url}query_hash={self.query_hash_posts}&{urlencode(variables)}'

            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            item = InstagramItem(
                user_id = user_id,
                photo = post.get('node').get('display_url'),
                likes = post.get('node').get('edge_media_preview_like').get('count'),
                post_data = post['node']
            )
            yield item

    def csrf_token(self, text):
        token = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return token.split(':').pop().replace(r'"', '')

    def id_user(self, text, username):
        Uid = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(Uid).get('id', username)