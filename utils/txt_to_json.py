#!/usr/bin/env python3
import os
import re
import json
import sys

def list_to_json(lst, level):
    curlst = lst
    sublst = []
    children = None
    for i in range(0,len(curlst)):
        j = i
        levelact = curlst[i].replace(curlst[i].lstrip(),'').count('\t')
        if level == levelact:
            if i < len(curlst):
                children = list_to_json(curlst[i+1:], level + 1)
            else:
                children = None
            object = curlst[i][levelact:]
            obs = re.split(',|\.', object)
            name = obs[0]
            pages=[]
            note=[]
            for t in obs[1:]:
                 s = t.strip()
                 nums = re.findall(r'\d+', s)
                 if nums:
                     if nums == s or '-'.join(nums) == s:
                         pages.append(s)
                 if s[:4].lower() == 'see ':
                     note.append(s)
            dic = {}
            if name:
                dic['name'] = name
            if pages:
                dic['pages'] = pages
            if note:
                dic['note'] = note
            if children:
                dic['children'] = children
            print(dic)
            sublst.append(dic)
        elif level > levelact:
            return sublst
    return sublst

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isfile(path):
            with open(path) as f:
                idx = f.read().strip().split('\n')
            mainlst = list_to_json(idx, 0)
            if len(sys.argv) > 2:
                outpath = sys.argv[2]
            else:
                outpath = '.'.join((os.path.splitext(path)[0], 'json'))
            with open(outpath, 'w') as outfile:
                json.dump(mainlst, outfile, indent=3)
