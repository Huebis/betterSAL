import database

import os


uploadFolder = "user_documents"








def saveNewFile(file):
    oldFileName = file.filename
    fileId, newFileName = database.addNewFile(oldFileName)
    file.save(os.path.join(uploadFolder, newFileName))
    return fileId

def lookUpFile(fileId)
    nameBefor,nameAfter = database.getNamesOfFile(FileId)

    path = os.path.join(uploadFolder, nameAfter)
    if not os.path.exists(file_path):
        return False
    
    return 

