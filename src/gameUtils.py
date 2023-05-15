import tkinter as tk
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


def labelGame(root, config, levelDetails, currScore):
    abelWelcome = tk.Label(master=root,
                           text="Welcome",
                           fg='#2c334a',
                           font=('Helvetica', 12, 'bold')).grid(row=0,
                                                                column=0)

    labelWName = tk.Label(master=root,
                          text=config['player']['name'],
                          fg='#2c334a',
                          font=('Helvetica', 12, 'bold')).grid(row=0, column=1)

    labelLevelLbl = tk.Label(master=root,
                             text="Level",
                             fg='#2c334a',
                             font=('Helvetica', 12)).grid(row=1, column=0)

    labelLevel = tk.Label(master=root,
                          text=levelDetails[0],
                          fg='#2c334a',
                          font=('Helvetica', 12, 'bold')).grid(row=1, column=1)

    labelLevelLbl = tk.Label(master=root,
                             text="Words",
                             fg='#2c334a',
                             font=('Helvetica', 12)).grid(row=2, column=0)

    labelLevel = tk.Label(master=root,
                          text=levelDetails[1],
                          fg='#2c334a',
                          font=('Helvetica', 12, 'bold')).grid(row=2, column=1)

    labelLevelLbl = tk.Label(master=root,
                             text="Score",
                             fg='#2c334a',
                             font=('Helvetica', 12)).grid(row=3, column=0)

    labelLevel = tk.Label(master=root,
                          textvariable=currScore,
                          fg='#2c334a',
                          font=('Helvetica', 12, 'bold')).grid(row=3, column=1)
