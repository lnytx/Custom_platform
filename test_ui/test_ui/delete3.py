import os


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

print("PROJECT_DIR",PROJECT_DIR)
print("os.path.dirname(__file__)",os.path.dirname(__file__))
UPLOADFILES = os.path.join(PROJECT_DIR, 'uploadfiles')
# PROJECT_DIR D:\Program Files\Python_Workspace
# os.path.dirname(__file__) D:\Program Files\Python_Workspace\test_ui
