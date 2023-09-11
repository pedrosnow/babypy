from app.model.taskmanager import taskmanager
from flask import Flask
import sqlite3
import os
import json

app = Flask(__name__)

folder_root = 'streamdata'
disco_local = os.path.abspath(os.sep)

checkedFoldarRoot = os.path.join(disco_local, folder_root)

if not os.path.exists(checkedFoldarRoot):
    os.mkdir(checkedFoldarRoot)

folder_data = 'data'

checkedFoldarData = os.path.join(checkedFoldarRoot, folder_data)
if not os.path.exists(checkedFoldarData):
    os.mkdir(checkedFoldarData)

task_manager = os.path.join(checkedFoldarRoot, "task_manager.db")

if not os.path.exists(task_manager):
    conexao = sqlite3.connect(task_manager)

    instance_taskmanager = taskmanager()
    instance_taskmanager.setCaminho(task_manager)

try:
     configuracao = open(f'{checkedFoldarRoot}\config.json')
except FileNotFoundError as e:
    configuracao = f'{checkedFoldarRoot}\config.json'
    
    with open(configuracao, "w") as outfile:
        json.dump({}, outfile)

load_config = open(f'{checkedFoldarRoot}\\config.json')
load_config = json.load(load_config)



from app import routes