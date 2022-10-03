# -*- coding: utf-8 -*-
import tensorflow as tf
import pandas as pd
import sys
from urllib.parse import urlparse
import os.path
import re
import numpy as np

# URLをstringでうけとって、0か1を返す
# 0なら正常、1ならフィッシング


def urldet(url):
    # url https://example.com^^^

    urldata = pd.DataFrame()
    urldata['url'] = pd.DataFrame([url])

    # feature engineering
    #urldata['url_length'] = urldata['url'].apply(lambda i: len(str(i)))
    urldata['hostname_length'] = urldata['url'].apply(lambda i: len(urlparse(i).netloc))
    urldata['path_length'] = urldata['url'].apply(lambda i: len(urlparse(i).path))
    def fd_length(url):
        urlpath= urlparse(url).path
        try:
            return len(urlpath.split('/')[1])
        except:
            return 0

    urldata['fd_length'] = urldata['url'].apply(lambda i: fd_length(i))
    urldata['count-'] = urldata['url'].apply(lambda i: i.count('-'))
    urldata['count@'] = urldata['url'].apply(lambda i: i.count('@'))
    urldata['count?'] = urldata['url'].apply(lambda i: i.count('?'))
    urldata['count%'] = urldata['url'].apply(lambda i: i.count('%'))
    urldata['count.'] = urldata['url'].apply(lambda i: i.count('.'))
    urldata['count='] = urldata['url'].apply(lambda i: i.count('='))
    urldata['count-http'] = urldata['url'].apply(lambda i : i.count('http'))
    urldata['count-https'] = urldata['url'].apply(lambda i : i.count('https'))
    urldata['count-www'] = urldata['url'].apply(lambda i: i.count('www'))
    def digit_count(url):
        digits = 0
        for i in url:
            if i.isnumeric():
                digits = digits + 1
        return digits
    urldata['count-digits']= urldata['url'].apply(lambda i: digit_count(i))
    def letter_count(url):
        letters = 0
        for i in url:
            if i.isalpha():
                letters = letters + 1
        return letters
    urldata['count-letters']= urldata['url'].apply(lambda i: letter_count(i))
    def no_of_dir(url):
        urldir = urlparse(url).path
        return urldir.count('/')
    urldata['count_dir'] = urldata['url'].apply(lambda i: no_of_dir(i))
    #Use of IP or not in domain
    def having_ip_address(url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
        if match:
            # print match.group()
            return -1
        else:
            # print 'No matching pattern found'
            return 1
    urldata['use_of_ip'] = urldata['url'].apply(lambda i: having_ip_address(i))

    model = tf.keras.models.load_model('./deturl_model.h5')
    #model = tf.model.load_weights('./deturl_model.h5')

    data = np.expand_dims(urldata.values[0, 1:], 0).astype(np.float32)

    out = model.predict([data])
    out = out[0][0]

    # 0 Non Malicious, 1 Mallicious

    if out < 0.5:
        return 0 
    else:
        return 1