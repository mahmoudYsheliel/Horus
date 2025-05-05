import yaml


filters_conf = {}
stream_sources_conf = {}
zmq_conf = {}
settings = {}


def load_conf_files():
    global filters_conf, stream_sources_conf, zmq_conf, settings

    with open('conf/filters.yml', 'r') as f:
        filters_conf = yaml.safe_load(f.read())

    with open('conf/stream_sources.yml', 'r') as f:
        stream_sources_conf = yaml.safe_load(f.read())

    with open('conf/zmq.yml', 'r') as f:
        zmq_conf = yaml.safe_load(f.read())

    with open('conf/settings.yml', 'r') as f:
        settings = yaml.safe_load(f.read())


def get_filters_conf() -> dict:
    return filters_conf


def get_stream_sources_conf() -> dict:
    return stream_sources_conf


def get_zmq_conf() -> dict:
    return zmq_conf


def get_settings() -> dict:
    return settings


load_conf_files()
