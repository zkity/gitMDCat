#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import copy

comment = '[^_^]: # (zk)\n'


def genCat():
    """生成指定目录下的.md文件的git目录
    :returns: [[filePath, fileCategory], ...]

    """
    arg = sys.argv
    if len(arg) == 1:
        dirPath = './'
    elif len(arg) == 2:
        dirPath = arg[1]
        if not os.path.exists(dirPath):
            print('输入路径: {} 不存在'.foramt(dirPath))
            exit()
    else:
        print('参数个数有误')
        exit()

    mdFilePath = []
    for fPath, ds, fs in os.walk(dirPath):
        for f in fs:
            if f.endswith('.md'):
                mdFilePath.append(os.path.join(fPath, f))

    allSet = []
    for md in mdFilePath:
        with open(md, 'r') as mdFile:
            lines = mdFile.readlines()
        cat = [x for x in lines if re.match(r'^\s*#+\s+', x)]
        catSet = []
        for catLine in cat:
            s4num = catLine.strip().split(' ')[0].count('#') - 1
            nos4 = catLine.replace('#', '').replace('\n', '').strip()
            ah = '* [{}]'.format(nos4)
            nosy = nos4.replace('.', '').replace(' ', '-').replace(',', '').replace('(', '').replace(')', '')
            be = '(#{})'.format(nosy)
            catLineResult = '  '*s4num + ah + be + '\n'
            catLineResult = catLineResult.lower()
            catSet.append(catLineResult)
        catSet.append('\n')
        catSet.append(comment)
        allSet.append([md, copy.deepcopy(catSet)])
    return allSet


def newFile(catSet):
    """将跟新后的目录写入相应的文件

    :catSet: 目录记录
    :returns: TODO

    """
    for cat in catSet:
        if len(cat[1]) > 0:
            with open(cat[0], 'r+') as f:
                old = f.readlines()
                i = 0
                for i in range(len(old)):
                    if old[i] == comment:
                        i += 1
                        break
                if i == len(old)-1:
                    i = 0
                oldNew = old[i:len(old)]
                f.seek(0)
                f.write(''.join(cat[1]))
                f.write(''.join(oldNew))


def main():
    """为指定目录下的.md文件添加git目录
    :returns: None

    """
    cat = genCat()
    newFile(cat)


if __name__ == "__main__":
    main()
