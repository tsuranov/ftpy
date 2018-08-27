#!/usr/bin/env python3
import ftplib
import os
import asyncio
import aiofiles
# 

urlFTP = 'mirror.yandex.ru'
pathFTP = 'knoppix/DVD'
#
print ("Start FTP downloader!")
#
ftp = ftplib.FTP( urlFTP )
ftp.login()
ftp.cwd( pathFTP )

#Получаем список файлов
filenames = []
def handleDownload (strFileName):
    #отсекаем каталоги
    if strFileName[0] != 'd':
        #оставляем только имя файла из:
        #-rw-r--r--    1 ftp      ftp            65 Aug 17 11:26 orel-2.12-14.08.2018_15.12.md5
        filenames.append(strFileName[strFileName.rfind(" ") + 1 : ])

ftp.retrlines('LIST', handleDownload)
print("Count files: ", len(filenames) )
ftp.quit()

#Асихронное закачка
async def download_ftp(strFileName):
    print("Download: ", strFileName)
    ftp = ftplib.FTP( urlFTP )
    ftp.login()
    ftp.cwd( pathFTP )

    #не работает асихронная закачка или запись???

    #with open(strFileName, 'wb') as local_file:
    #        ftp.retrbinary('RETR ' + strFileName, local_file.write)
    
    #async with aiofiles.open(strFileName, mode='wb') as local_file:
    #    ftp.retrbinary('RETR ' + strFileName,  await local_file.write())
    print("End download: ", strFileName)
    ftp.quit()

    
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future( download_ftp( filenames[i] )) for i in range(0, len(filenames))]
async_download = asyncio.wait(tasks)
loop.run_until_complete(async_download)
loop.close()
#ftp.quit()
print ("End FTP downloader!")



