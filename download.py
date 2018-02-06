#!/usr/bin/env python3.6
import os
import urllib
import requests
import json

headers = {
    'user-agent': 'dragon-tamer/0.1 (https://github.com/costpermille/dragon-tamer)'
}

cfg = {
    'wanted': ['summoner', 'champion', 'mastery', 'item', 'rune', 'profileicon'],
    'img_base': './data',
    'platform': 'euw',
    'language': 'en_GB',
    'host': 'ddragon.leagueoflegends.com'
}

if not os.path.exists(cfg['img_base']):
    print("[!] Created {} for you, since it doesn't exist.".format(cfg['img_base']))
    os.makedirs(cfg['img_base'])


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

        try:
            key = v['key']
        except KeyError:
            key = k

        if group == "gray_mastery":
            group = "mastery"

        if not os.path.exists("{}/{}/{}".format(cfg['img_base'], ver, group)):
            os.makedirs("{}/{}/{}".format(cfg['img_base'], ver, group))

        filename = "{}/{}/{}/{}.png".format(cfg['img_base'],
                                        ver, group, key)
        url = "https://%s/cdn/%s/img/%s/%s" % (
            cfg['host'], ver, group, v['image']['full'])

        print("Acquiring {} from {}".format(filename, url))
        urllib.request.urlretrieve(url, filename)

    if not os.path.exists("{}/{}".format(cfg['img_base'], "latest")):
        os.makedirs("{}/{}".format(cfg['img_base'], "latest"))

    v_base = "{}/{}/{}".format("..", ver, group)
    v_latest = "{}/{}/{}".format(cfg['img_base'], "latest", group)
    print("[!] Linked {} to {}.".format(v_latest, v_base))
    os.symlink(v_base, v_latest)
