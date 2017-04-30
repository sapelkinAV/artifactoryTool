import os, zipfile, shutil, glob, shutil
import re

import sys

dir_name = os.path.realpath(sys.argv[1])


path_to_archieve = []

def unzipStuff(workPath):
    for path, subdirs, files in os.walk(dir_name):
        for name in files:
            if name.endswith(".zip"):

                path_to_archieve.append((os.path.join(path, name).replace('.zip', '')))

                unzippingFile = zipfile.ZipFile(os.path.join(path, name))
                unzippingFile.extractall(os.path.join(path, name).replace('.zip', ''))
                os.remove(os.path.join(path, name))


def zipFiles():
    for element in path_to_archieve:
        print(element)
        shutil.make_archive(element,'zip',element)
        shutil.rmtree(element)

def modifyBuildGradle(pathToBuildGradle):
    stringsToDelete = ['classpath \"jt400:jt400:1.0.0\"', 'classpath \"ccas400:ccas400:1.0.0\"']
    lines = []
    with open(pathToBuildGradle, "r") as file:
        lines = file.readlines()

    with open(pathToBuildGradle, "w") as file:
        for line in lines:
            if not any(filter_word in line for filter_word in stringsToDelete):
                line = re.sub(r'url \"http://mvn/artifactory/releases\"','url \"http://mvn/artifactory/public\"',line)
                line = re.sub(r'classpath \"ru.alfabank.gradle:as400plugin:1.0...\"','classpath \"ru.alfabank.gradle:as400plugin:1.0.49\"',line)
                file.write(line)

def editFiles():
    for path, subdirs, files in os.walk(dir_name):
        for name in files:
            if name == 'build.gradle':
                modifyBuildGradle(os.path.join(path,name))



unzipStuff(dir_name)
editFiles()
zipFiles()
