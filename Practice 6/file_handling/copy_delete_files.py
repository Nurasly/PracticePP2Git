import shutil, os

shutil.copy("data.txt", "data_backup.txt")
os.remove("data.txt") # Deletes the original