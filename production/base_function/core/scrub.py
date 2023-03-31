import copy


def all_url_mutate_closure(client_url_file):
    def add_url_mutate(obj, key, index):
        file_id = obj[key]

        part_of_key = key.replace('file_id', '')
        if part_of_key != "":
            new_key = "url_file" + part_of_key
        else:
            new_key = "url_file"
        obj[new_key] = client_url_file.replace("{id}", file_id)
        del obj[key]
    return add_url_mutate


def scrub_internal(obj, func, good_key="file_id", index=0):
    if isinstance(obj, dict):
        # the call to `list` is useless for py2 but makes
        # the code py2/py3 compatible
        for key in list(obj.keys()):
            if key.startswith(good_key):
                func(obj, key, index)
                index = index + 1
            elif key in obj:
                scrub_internal(obj[key], func, good_key, index)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            current = obj[i]
            if type(current) == str and current.startswith(good_key):
                func(obj, good_key, index)
                index = index + 1
            else:
                scrub_internal(current, func, good_key, index)
    else:
        # neither a dict nor a list, do nothing
        pass
    return obj


def add_url(obj, client_url_file, good_key="file_id"):
    return scrub_internal(copy.deepcopy(obj), all_url_mutate_closure(client_url_file), good_key)


def del_mutate(obj, key, index):
    del obj[key]


def scrub(data, bad_key="file_id"):
    return scrub_internal(copy.deepcopy(data), del_mutate, bad_key)
