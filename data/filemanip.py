# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 14:52:28 2019

@author: Carlos
"""

import os
import sys
from pathlib import Path
import numpy as np
import datetime

def query_yes_no(question, default="yes"):
    '''
    Ask a yes/no question via raw_input() and return their answer.

    :param question: is a string that is presented to the user.
    :param default: is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    :return: True for "yes" or False for "no".
    '''
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def check_overwrite(directory):
    '''
        Checks if file exists:
            If yes, asks user for overwriting privileges.
                If user alow overwriting: proceed execution
                If user deny overwriting: exit program
            If not, proceed execution.

        :param directory: string with folder directory path
    '''
    if os.path.isfile(str(Path(directory))):
        if query_yes_no('File already exists!! Do you wish to ovewrite it?', 'no'):
            pass
        else:
            print('Exiting.......')
            sys.exit(1)


def saveDict(dictObj, dirpath, filename='foo.dat', obs=''):

    '''
        Saves a dictionary in a txt file. Cannot be recovered. If the dict values are
        arrays, consider using saveDataDict.

        :param dictObj: dict name
        :param dirpath: directory to save file as str or Path object from pathlib.
        :param filename: name of the txt file to save.
        :param obs: string to add to the header.

        :return: nothing
    '''

    dirpath = Path(dirpath)

    file = open(str(Path(dirpath) / filename), 'w')
    file.write('# ===File generated by filemanip.saveDict()===\n')
    file.write('# Date: ' + str(datetime.datetime.now()) +'\n')
    file.write('# Obs.: ' + str(obs) + '\n')

    try:
        for i in dictObj:
            line = ''
            line += '{0} : {1} \n'.format(i, dictObj[i])
            file.write(line)
    except: print('save failed.')
    file.close()


def saveDataDict(data, dirpath, filename='foo.dat', obs='', header=''):
    '''
        Saves a dict in a txt file. With a header based on the dict keys.

        :param data: dictionary with data. All dict values must have the save length.
        :param dirpath: directory to save file as str or Path object from pathlib.
        :param filename: name of the txt file to save.
        :param obs: string to add to the header.
        :param header: string to be used as header. Overwrites auto header generation based on dict keys.

        :return: nothing
    '''

    dirpath = Path(dirpath)
    check_overwrite(str(dirpath / filename))

    file = open(str(Path(dirpath) / filename), 'w')
    file.write('# ===File generated by myModules.saveDict===\n')
    file.write('# Date: ' + str(datetime.datetime.now()) +'\n')
    file.write('# Obs.: ' + str(obs) + '\n')

    if header=='':
        header = '#H '
        for i in list(data.keys()):
            if i == list(data.keys())[-1]:
                header +=  str(i) + '\n'
            else:
                header +=  str(i) + ', '
    file.write(str(header))


    for j in range(0, len(data[max(data, key=len)])):
        line = ''
        for i in list(data.keys()):
            if i == list(data.keys())[-1]:
                try: line += str(data[i][j]) + '\n'
                except IndexError: line += '\n'
            else:
                try: line += str(data[i][j]) + ', '
                except IndexError: line += ', '
        file.write(line)
    file.close()

def getDataDict(fullpath):
    '''
        Extract data from file saved by myModules.saveDict.

        :param fullpath: directory path of the file to read.

        :return: dictionary with the data (values are numpy arrays).
    '''

    # Get Header
    file = open(str(Path(fullpath)), 'r')
    header = file.readline()
    while header[0:2] != '#H':
        header = file.readline()
    header = header[3:-1]  # Removes #H and \n
    header = header.split(', ')
    
#    file = open(str(Path(fullpath)), 'r')
#    line = file.readline()
#    while line[0] == '#':
#        line = file.readline()
#    line = line[:-1]
#    line.split(', ')

    # get data
    data = np.genfromtxt(str(Path(fullpath)), delimiter=',')

#    return {n:data[:, header.index(n)] for n in header}

    datadict = dict()
    for name in header:
        if np.isin('nan', data[:, header.index(name)]):
            first_nan = np.where(np.isnan(data[: ,header.index(name)]))[0][0]
            datadict[name] = data[:first_nan, header.index(name)]
        else:
            datadict[name] = data[:, header.index(name)]
        
    return datadict

def changeFilesName(fileList, separator, values2keep, ask=True):
    '''
    '''
    for filePath in fileList:
        try:
            a = filePath.name.split('.')
            ext = a[-1]
            name = ''.join(a[0:-1])
        except: name = filePath.name
    
        a = name.split(separator)
        
        nameNew =''
        for idx in values2keep:
            nameNew = nameNew + a[idx] + '_'
        nameNew = nameNew[:-1] + '.' + ext
        
        print('OLD NAME = ' + filePath.name)
        print('NEW NAME = ' + nameNew)
        print('\n')
    
        if not ask:
            filePath.rename(filePath.parent / nameNew)
    
    if ask:
        y = query_yes_no('Change names?', default="yes")
    else:
        print('Files renamed!')
        return
    if y or not ask:
        changeFilesName(fileList, separator, values2keep, ask=False)