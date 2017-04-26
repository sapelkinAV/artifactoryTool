import os, zipfile, shutil, glob
from pathlib import Path

import sys


def unzipFolders(path):
    extension = ".zip"
    for item in os.listdir(path):  # loop through items in dir
        if item.endswith(extension):  # check for ".zip" extension
            file_name = os.path.abspath(item)  # get full path of files
            zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
            zip_ref.extractall(path)  # extract file to dir
            zip_ref.close()  # close file
            os.remove(file_name)  # delete zipped file


def zipdir(dirPath=None, zipFilePath=None, includeDirInZip=True):
    if not zipFilePath:
        zipFilePath = dirPath + ".zip"
    if not os.path.isdir(dirPath):
        raise OSError("dirPath argument must point to a directory. "
                      "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)

    # Little nested function to prepare the proper archive path
    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return os.path.normcase(archivePath)

    outFile = zipfile.ZipFile(zipFilePath, "w",
                              compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        # Make sure we get empty directories as well
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            # some web sites suggest doing
            # zipInfo.external_attr = 16
            # or
            # zipInfo.external_attr = 48
            # Here to allow for inserting an empty directory.  Still TBD/TODO.
            outFile.writestr(zipInfo, "")
    outFile.close()


def zipFolders(path):
    for item in os.listdir(path):
        if os.path.isdir(item):
            file_name = os.path.abspath(item)
            zipdir(file_name)

    # delete folders
    for item in os.listdir(path):
        if os.path.isdir(item):
            shutil.rmtree(item)


def modifyBuildGradle(pathToBuildGradle):
    stringsToDelete = ['classpath \"jt400:jt400:1.0.0\"', 'classpath \"ccas400:ccas400:1.0.0\"']

    with open(pathToBuildGradle, "r") as file:
        lines = file.readlines()

    with open(pathToBuildGradle, "w") as file:
        for line in lines:
            if not any(filter_word in line for filter_word in stringsToDelete):
                file.write(
                    line.replace("url \"http://mvn/artifactory/releases\"", "url \"http://mvn/artifactory/public\""))


def findFileByName(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def editFolders(path):
    listdirs = [x[0] for x in os.walk(path)]
    listdirs.pop(0)
    for folder in listdirs:
        if os.path.isdir(folder):
            build_gradle = findFileByName('build.gradle',folder)
            if build_gradle is not None and os.path.isfile(build_gradle):
                modifyBuildGradle(build_gradle)








dir_name = os.path.realpath('./testArchieves/')

if __name__ == '__main__':
    dir_name = os.path.realpath(sys.argv[1])
    os.chdir(dir_name)
    unzipFolders(dir_name)
    editFolders(dir_name)
    zipFolders(dir_name)
