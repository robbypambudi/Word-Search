import yaml


def readConfigFile():
    with open(r'config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config


def writeConfigFile(data):
    with open(r'config.yaml', 'w') as file:
        yaml.dump(data, file)


def gameLavel(level: str, name: str):
    print(level + " " + name)

    config = readConfigFile()

    currLevel = 0

    if (level == 'Easy'):
        currLevel = 1
    elif (level == 'Medium'):
        currLevel = 2
    elif (level == 'Hard'):
        currLevel = 3

    word_count = config['levels'][currLevel]['words']

    config['player']['level'] = currLevel
    config['player']['name'] = name
    config['player']['score'] = 0
    config['word_count'] = int(word_count)

    writeConfigFile(config)

    return config
