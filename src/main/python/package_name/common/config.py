# -*- coding: utf-8 -*-
import os
import yaml

LOG_LEVEL = 'LOG_LEVEL'

PACKAGE_HOST = 'PACKAGE_HOST'
PACKAGE_PORT = 'PACKAGE_PORT'
TIME_INTERVAL = 'TIME_INTERVAL'
EMAIL_CONF_PATH = 'EMAIL_CONF_PATH'
CAFE_CONF_PATH = 'CAFE_CONF_PATH'
LOG_PROPERTIES_PATH = 'LOG_PROPERTIES_PATH'

CONFIG_FIELDS = (
    LOG_LEVEL,
    PACKAGE_HOST,
    PACKAGE_PORT,
    TIME_INTERVAL,
    EMAIL_CONF_PATH,
    CAFE_CONF_PATH,
    LOG_PROPERTIES_PATH
)

# 기본적으로 설정되는 Config 내용
DEFAULT_CONFIG = {
    LOG_LEVEL: 'INFO',
    PACKAGE_HOST: "localhost",
    PACKAGE_PORT: 7474,
    TIME_INTERVAL: '1h',
    EMAIL_CONF_PATH: "${PACKAGE_HOME}/etc/email.conf",
    CAFE_CONF_PATH: "${PACKAGE_HOME}/etc/cafe.conf",
    LOG_PROPERTIES_PATH: "${PACKAGE_HOME}/etc/log-properties.conf"
}

# 1s, 1m, 1h와 같이 표현되는 시간 필드. 최종적으로 초단위로 변환된다.
TIME_FIELDS = (
    TIME_INTERVAL,
)

# ${PACKAGE_HOME}과 같이 환경변수가 포함된 Path를 절대경로로 바꾸어 줘야 하는 필드들.
PATH_FIELDS = (
    EMAIL_CONF_PATH,
    CAFE_CONF_PATH,
)

config = None


def _time_parse(timeStr):
    length = len(timeStr)
    num = long(timeStr[:length-1])
    unit = timeStr[length-1]

    if unit == 's':
        return num
    elif unit == 'm':
        return num*60
    elif unit == 'h':
        return num*3600
    elif unit == 'd':
        return num*86400
    elif unit == 'y':
        return num*86400*365
    else:
        return num


def get_config_path():
    if 'PACKAGE_CONFIG' in os.environ:
        path = os.environ['PACKAGE_CONFIG']
        if os.path.exists(path):
            return path
    if 'PACKAGE_HOME' in os.environ:
        path = os.environ['PACKAGE_HOME'] + '/etc/package.conf'
        if os.path.exists(path):
            return path
    if 'HOME' in os.environ:
        path = os.environ['HOME'] + '/etc/package.conf'
        if os.path.exists(path):
            return path

    return None


def read_configuration(path=get_config_path()):
    try:
        stream = open(path, 'r')
    except TypeError:
        return DEFAULT_CONFIG
    cfg = yaml.load(stream)
    if cfg is None:
        return {}
    else:
        return cfg


def get_configuration():
    global config
    if config:
        return config

    _config = DEFAULT_CONFIG

    try:
        package_home = os.environ['PACKAGE_HOME']
        _config['PACKAGE_HOME'] = package_home
    except KeyError:
        pass

    try:
        path = os.environ['PACKAGE_CONFIG']
        _config.update(read_configuration(path))
    except KeyError:
        _config.update(read_configuration())
    config = _config

    # Time Field들을 모두 파싱하여 저장
    for field in TIME_FIELDS:
        config[field] = _time_parse(config[field])

    # Path Field들을 모두 변환하여 저장
    for field in PATH_FIELDS:
        if type(config[field]) == list:
            for i in xrange(0, len(config[field])):
                config[field][i] = os.path.expandvars(config[field][i])
        else:
            config[field] = os.path.expandvars(config[field])

    return config


def get_preference(field):
    global config
    if field not in CONFIG_FIELDS:
        raise Exception('%s is invalid field name' % field)
    if not config:
        config = get_configuration()
    return config[field]


def test():
    for field in CONFIG_FIELDS:
        print field, ':', get_preference(field)

if __name__ == '__main__':
    test()
