import tkinter as tk  # import tkinter as tk
import yaml  # import yaml

# Fungsi untuk membaca file config.yaml


def readConfigFile():
    with open(r'config.yaml') as file:  # membuka file config.yaml
        # membaca file config.yaml
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config  # mengembalikan nilai config

# Fungsi untuk menulis file config.yaml


def writeConfigFile(data):
    with open(r'config.yaml', 'w') as file:  # membuka file config.yaml dengan mode write
        # menulis data ke file config.yaml dengan format yaml
        yaml.dump(data, file)

# Fungsi untuk mengatur level game dan nama pemain


def gameLavel(level: str, name: str):
    config = readConfigFile()  # membaca file config.yaml

    currLevel = 0  # mendefinisikan variabel currLevel dengan nilai 0

    if (level == 'Easy'):  # jika level adalah Easy
        currLevel = 1  # currLevel diisi dengan nilai 1
    elif (level == 'Medium'):  # jika level adalah Medium
        currLevel = 2  # currLevel diisi dengan nilai 2
    elif (level == 'Hard'):  # jika level adalah Hard
        currLevel = 3  # currLevel diisi dengan nilai 3

    # mendefinisikan variabel word_count dengan nilai words pada level yang dipilih
    word_count = config['levels'][currLevel]['words']

    # mengisi nilai level pada config dengan nilai currLevel
    config['player']['level'] = currLevel
    # mengisi nilai name pada config dengan nilai name
    config['player']['name'] = name
    # mengisi nilai score pada config dengan nilai 0
    config['player']['score'] = 0
    config['word_count'] = int(word_count)

    writeConfigFile(config)  # menulis file config.yaml

    return config  # mengembalikan nilai config

# Fungsi untuk mengatur level game dan nama pemain


def labelGame(root, config, levelDetails, currScore):
    labelWelcome = tk.Label(master=root,  # mendefinisikan labelWelcome
                            text="Welcome",  # teks labelWelcome
                            fg='#2c334a',  # warna teks labelWelcome
                            font=('Helvetica', 12, 'bold')).grid(row=0, column=0)  # font labelWelcome

    labelWName = tk.Label(master=root,  # mendefinisikan labelWName
                          text=config['player']['name'],  # teks labelWName
                          fg='#2c334a',  # warna teks labelWName
                          font=('Helvetica', 12, 'bold')).grid(row=0, column=1)  # font labelWName

    labelLevelLbl = tk.Label(master=root,  # mendefinisikan labelLevelLbl
                             text="Level",  # teks labelLevelLbl
                             fg='#2c334a',  # warna teks labelLevelLbl
                             font=('Helvetica', 12)).grid(row=1, column=0)  # font labelLevelLbl

    labelLevel = tk.Label(master=root,  # mendefinisikan labelLevel
                          text=levelDetails[0],  # teks labelLevel
                          fg='#2c334a',  # warna teks labelLevel
                          font=('Helvetica', 12, 'bold')).grid(row=1, column=1)  # font labelLevel

    labelLevelLbl = tk.Label(master=root,  # mendefinisikan labelLevelLbl
                             text="Words",  # teks labelLevelLbl
                             fg='#2c334a',  # warna teks labelLevelLbl
                             font=('Helvetica', 12)).grid(row=2, column=0)  # font labelLevelLbl

    labelLevel = tk.Label(master=root,  # mendefinisikan labelLevel
                          text=levelDetails[1],  # teks labelLevel
                          fg='#2c334a',  # warna teks labelLevel
                          font=('Helvetica', 12, 'bold')).grid(row=2, column=1)  # font labelLevel

    labelLevelLbl = tk.Label(master=root,  # mendefinisikan labelLevelLbl
                             text="Score",  # teks labelLevelLbl
                             fg='#2c334a',  # warna teks labelLevelLbl
                             font=('Helvetica', 12)).grid(row=3, column=0)  # font labelLevelLbl

    labelLevel = tk.Label(master=root,  # mendefinisikan labelLevel
                          textvariable=currScore,  # teks labelLevel
                          fg='#2c334a',  # warna teks labelLevel
                          font=('Helvetica', 12, 'bold')).grid(row=3, column=1)  # font labelLevel
