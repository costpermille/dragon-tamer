#!/usr/bin/env python3.5
import os
import urllib
import requests
import json

headers = {
    'user-agent': 'dragon-tamer/0.1 (https://github.com/costpermille/dragon-tamer)'
}

cfg = {
    'wanted': ['summoner', 'champion', 'mastery', 'item', 'rune', 'profileicon'],
    'img_base': '/var/www/akamai/cdn-origin/img',
    'platform': 'euw',
    'language': 'en_GB',
    'host': 'ddragon.leagueoflegends.com'
}

cfg_versions = 'https://%s/realms/%s.json' % (cfg['host'], cfg['platform'])
versions = requests.get(cfg_versions, headers=headers).json()

for type in cfg['wanted']:
    ver = versions['n'][type]
    data_path = 'https://%s/cdn/%s/data/%s/%s.json' % (
        cfg['host'], ver, cfg['language'], type)
    print("{} (ver {}) @ {}".format(type, ver, data_path))

    data = requests.get(data_path, headers=headers).json()

    for (k, v) in data['data'].items():
        group = v['image']['group']

        key = k

        if group == "gray_mastery":
            group = "mastery"

        if not os.path.exists(cfg['img_base'] + "/" + group):
            os.makedirs(cfg['img_base'] + "/" + group)

        filename = "%s/%s/%s" % (cfg['img_base'], group, v['image']['full'])

        url = "https://%s/cdn/%s/img/%s/%s" % (cfg['host'], ver, group, v['image']['full'])

        urllib.request.urlretrieve(url, filename)

        print("Acquiring {} from {}".format(filename, url))
