class ElementNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

def apply_config_builder(config_builder, config):
    for expectation in config_builder.expectations:
        expectation(config, config_builder.complete_key)

    for transformer in config_builder.transformers:
        transformer(config, config_builder.complete_key)

    try:
        if not isinstance(get_node(config, config_builder.complete_key), dict):
            return
    except ElementNotFoundException:
        return

    for partial_key, children in config_builder.children.items():
        apply_config_builder(children, config)

def get_node(data, key):
    key_list = [] if key is None else key.split('.')

    try:
        return reduce(lambda d, k: d[k], key_list, data)
    except KeyError:
        raise ElementNotFoundException("Element \"%s\" not found." % key)

def get_parent(data, key):
    if "." not in key:
        return data

    key_list = key.split('.')
    del key_list[-1]

    try:
        return reduce(lambda d, k: d[k], key_list, data)
    except KeyError:
        raise ElementNotFoundException("Element \"%s\" not found." % ".".join(key_list))
