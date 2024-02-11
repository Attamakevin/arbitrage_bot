import os
import re
import fnmatch
import copy


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {'*': ''})
    dic[keys[-1]] = value


def dir_metatree(
        _ROOT_='.',
        ignore_dot_files=False,
        listen_gitignore=True):

    _LEAF_ = {'*': ''}

    data = copy.copy(_LEAF_)

    for dirName, subdirList, fileList in os.walk(_ROOT_):
        dirPath = dirName.split('/')[1:]

        if ignore_dot_files:

            if any([name.startswith('.') for name in dirPath]):
                continue

        for fname in fileList:

            if ignore_dot_files:
                if fname.startswith('.'):
                    continue

            if listen_gitignore:
                if os.path.exists('.gitignore'):
                    pass

                    path = os.path.join(dirName, fname)

                    patterns = [line[:-1] for line in
                               open('.gitignore').readlines()
                                if not line.startswith('#') and line[:-1]]

                    any_matched = False

                    for pattern in patterns:
                        result = re.search(fnmatch.translate(pattern), path)
                        if result:
                            any_matched = True

                    if any_matched:
                        continue



            if dirPath:
                nested_set(data, dirPath+[fname], copy.copy(_LEAF_))
            else:
                data[fname] = copy.copy(_LEAF_)

    return data


