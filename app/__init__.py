from flask import Flask
import os

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






from app import routes