import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from instagram.items import InstagramItem



class InstaSpider(scrapy.Spider):
    name = 'Insta'
    download_delay = 1
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = 'https://www.instagram.com/api/v1/web/accounts/login/ajax/'
    insta_login = 'voyage_and_more'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1703501314:AahQAE7upkaU24GQOWXcHxwusCXZ9Q01hnFs0YDyG0rIYvoFvd/CUuqG7o+QIkRYyAb7PqL3k/NpDGimkF4wVMLxfvfi4a0SJKeMhQ4+zW4Mx4GdAiJtwh3hAn/D0XAECAZ/WLcH2TAHgRsysrpDqIX1oQ=='
    parse_user = 'dima_protasevich92'
    query_hash_posts = 'CsgoxJnIB8S'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    uagent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    proxy = '45.146.88.162:8000'
    # proxy = '195.154.184.80:8080'

    def parse(self, response: HtmlResponse):
        csrf_token = self.csrf_token(response.text)
        proxy = 'https://45.146.88.162:8000'
        yield scrapy.FormRequest(
            self.login_url,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login,
                      'enc_password': self.insta_pass,
                      'optIntoOneTap': "false",
                      'queryParams': "{}",
                      'trustedDeviceRecords': "{}",
                      },
            headers={'X-CSRFToken': csrf_token,
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'},
            meta={'proxy': proxy}
        )

    def user_parse(self, response: HtmlResponse):
        print(response.text)
        print(1)
        # proxy = 'https://45.146.88.162:8000'
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.parse_user},
                # meta={'proxy': proxy}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.id_user(response.text)
        print(1)
        variables = {'id': user_id, 'first': 12}
        url_posts = f'{self.graphql_url}query_hash={self.query_hash_posts}&{urlencode(variables)}'
        yield response.follow(
            url_posts,
            callback= self.user_posts_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        print(1)
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
                user_id=user_id,
                photo=post.get('node').get('display_url'),
                likes=post.get('node').get('edge_media_preview_like').get('count'),
                post_data=post['node']
            )
            yield item

    def csrf_token(self, text):
        token = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return token.split(':').pop().replace(r'"', '')

    def id_user(self, text):
        Uid = re.search(f'"user_id":"(\\d+)"', text).group()
        return Uid.split('"user_id":"')[-1].rstrip('"')
