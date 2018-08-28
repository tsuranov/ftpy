#!/usr/bin/env python3
import ftplib
import os
import asyncio
import aiofiles
import aioftp
# 

urlFTP = 'mirror.yandex.ru'
pathFTP = 'knoppix/DVD'
filenames = []

print ("Start FTP downloader!")
#####################################################################
#Однопоточный вариант
#####################################################################
#ftp = ftplib.FTP( urlFTP )
#ftp.login()
#ftp.cwd( pathFTP )

#Получаем список файлов
#filenames = []
#def handleDownload (strFileName):
#    print (strFileName)
#    #отсекаем каталоги
#    if strFileName[0] == '-':
#        #оставляем только имя файла из:
#        #-rw-r--r--    1 ftp      ftp            65 Aug 17 11:26 orel-2.12-14.08.2018_15.12.md5
#        filenames.append(strFileName[strFileName.rfind(" ") + 1 : ])
#ftp.retrlines('LIST', handleDownload)
#print("Count files: ", len(filenames) )
#ftp.quit()

#####################################################################
#Многопоточность
#####################################################################

async def get_list(urlFTP, pathFTP, filenames):
    async with aioftp.ClientSession( urlFTP ) as client:
        await client.change_directory( pathFTP )
        for path, info in (await client.list(recursive=False)):
            if info["type"] == "file":
                filenames.append( path.name )

loop = asyncio.get_event_loop()
task = [asyncio.ensure_future(get_list(urlFTP, pathFTP, filenames) ), ]
loop.run_until_complete(asyncio.wait( task ))

#Асихронное закачка
async def download_ftp(urlFTP, pathFTP, listFileName):
    async with aioftp.ClientSession( urlFTP ) as client:
        for strFileName in listFileName:
            if await client.is_file(pathFTP + '/' + strFileName):
                print ("Download: " + pathFTP + '/' + strFileName)
                await client.download(pathFTP + '/' + strFileName)
                print("End download: " + pathFTP + '/' + strFileName)

#Разбитие на потоки
def chunks(lst, chunk_size):
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

del filenames[0]
lst_flnms = chunks(filenames, (len(filenames)//2 + 1) )

async def async_download():
    tasks = [asyncio.ensure_future(
        download_ftp( urlFTP, pathFTP, lst_flnms[i] )) for i in range(0, 2)]
    await asyncio.wait(tasks)

loop.run_until_complete(async_download())
loop.close()
print ("End FTP downloader!")



