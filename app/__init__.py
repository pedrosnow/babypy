from app.model.taskmanager import taskmanager
from flask import Flask
import sqlite3
import os
import logging


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


logging.basicConfig(filename=f"{checkedFoldarRoot}\\log.txt", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


from app import routes