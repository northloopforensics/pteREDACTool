#python3


import PySimpleGUI as sg
import os
import sys
import datetime
import time
import glob2
import hashlib
import zipfile
from PIL import Image, ImageFilter
import io
import fitz
from distutils.dir_util import copy_tree
from nudenet import NudeClassifier
from nudenet import NudeDetector

#global image file extensions
ImageExts = (".JPG", ".JPEG", ".PNG", ".BMP", ".HEIC", ".HEIF", ".jpg", ".jpeg", ".jpe", ".jif",
            ".jfif", ".heif", ".heic", ".gif", ".png", ".bmp")
#global video file extensions
VideoExts = (".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".mp4", ".m4v", ".m4p", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd", ".mkv",
            ".ogg", ".webm", ".MPG", ".MP2", ".MPEG", ".MPE", ".MPV", ".MP4", ".M4V", ".M4P", ".AVI", ".WMV", ".MOV", ".QT", ".FLV", ".SWF",
            ".AVCHD", ".MKV", ".OGG", ".WEBM")

pteraimg = (b'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')


def make_report():
    savePath = (values['OUTPUT'])
    global org_stdout
    org_stdout = sys.stdout
    reportName = ("REDACTION REPORT")
    global completeName
    completeName = os.path.join(savePath, reportName+".txt")
    
    now = datetime.datetime.now()
    org_stdout = sys.stdout
    with open(completeName, 'w') as report:
        sys.stdout = report
        print("**********************     Redaction Report - pteREDACTool     **********************", '\n',
              "       _      ______ ___________  ___  _____ _____           _                  $ + ",'\n',                               
              "      | |     | ___ \  ___|  _  \/ _ \/  __ \_   _|         | |                   $... ",'\n',                              
              " _ __ | |_ ___| |_/ / |__ | | | / /_\ \ /  \/ | | ___   ___ | |                    $=Z$7777I. ",'\n',                        
              "|  _ \| __/ _ \    /|  __|| | | |  _  | |     | |/ _ \ / _ \| |               ,$   $ZZ77$77777777",'\n',                    
              "| |_) | ||  __/ |\ \| |___| |/ /| | | | \__/\ | | (_) | (_) | |             77$.   777$777777777... ",'\n',                 
              "| .__/ \__\___\_| \_\____/|___/ \_| |_/\____/ \_/\___/ \___/|_|           777$     7$7$$7I7777  ",'\n',                     
              "| |                                                                    $7$?$I     +7$77$77777+ ",'\n',                      
              "|_|                                                                  I77I7II       7$$77$77. ",'\n',                        
              "                                                           Z        77?.I7$7I      $77$77$77   ",'\n',                       
              "                                                         .DD       7. ~7. ,+7?     7$$7777777  ",'\n',                        
              "                                                         ONZ.      7      :7Z$?,Z$$77$777$77  ",'\n',                        
              "                                                          I?OZ$$=         . 78Z8$$?IZ77$77.  ",'\n',                          
              "                                                         $O?Z7$777$7,.... 7$Z8I$7+ZZ77$7   ",'\n',                           
              "                                                        7I$7$77$$777777$$$77I+:O$$Z$$$7    ",'\n',                           
              "                                                        ?777$7$7$7$7777777$77$ON8Z$$7$     ",'\n',                           
              "                                                       777$7$7777$$777777777777Z77$7$7     ",'\n',                          
              "                                                     +7II77I7777$77$$7777$777I7777$77+     ",'\n',                           
              "                                                      77I?II7.   .7$7. ..??$777$77$ 77     ",'\n',                           
              "                                                      7.                    .I7  ~7= 77     ",'\n',                          
              "                                                                             .7    7, ?.    ",'\n',                          
              "                                                                             I.      $$$7  ",'\n',                           
              "                                                                             .7      . .   ",'\n',                          
              "                                                                             $$$.          ",'\n', 
              "Redaction Performed On:  ", now.strftime("%Y-%m-%d %H:%M:%S"), '\n',
              "Redaction Performed By User:  ", os.getlogin(), '\n',
              "Source Directory:  ", values['SOURCE'], '\n',
              "Output Directory:  ", values['OUTPUT'], '\n',
              "User Settings:", '\n',
              "\t", "Redact Image Files - ", values['IMAGES'], '\t\t\t\t', "Redact Video Files - ", values['VIDEOS'], '\n',
              "\t", "Redact Based on Nudity Level - ", values['NUDITY'], '\t\t\t', "Redact Based on MD5 Hash - ", values['HASH'], '\n',
              "\t", "Redact Images from PDFs - ", values['PDF'], '\t\t\t', "Redact Images from DOCXs - ", values['DOCX'], '\n\n',
              "#######################  FILES REDACTED   #######################")
             
    sys.stdout = org_stdout  
       

def run_fast_scandir(dir, ext):    #iterates over target folder. recursive thru all contents. makes list files based on ext provided
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)

        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)

    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)

    return subfolders, files

def nudity_filter():        #FILTER BY NUDITY LEVEL AND REMOVE FILES
    classifier = NudeClassifier()
    allList = (classifier.classify(files,  batch_size=1))
    if (values['NUDITYLEVEL']) != 'Normal Filter':
        nudlev = float('.1')
    else:
        nudlev = float('.5')
    badfiles = {k:v for k,v in allList.items() if v['unsafe'] >= nudlev}
    removefiles = list(badfiles.keys())  #FILES TO REMOVE
    
    for f in removefiles: ##DELETION OF BAD FILES
        sg.Print("Removing file based on nudity content: ", f)
        window.refresh()
        with open(completeName, 'a') as report:
            sys.stdout = report
            print(f)
            sys.stdout = org_stdout
        os.remove(f)

def copy_folder():   #COPIES THE SOURCE FOLDER
    try:
        copy_tree(values['SOURCE'], values['OUTPUT'])
        for root, dirs, files in os.walk(values['OUTPUT']):
            
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o777)
            for f in files:
                os.chmod(os.path.join(root, f), 0o777)
            sg.Print("Copying Files...")
    except Exception:
        sg.Print('Error Copying- verify user access to files and folders')
        pass            

def image_delete():            #delete image files by file extension
    dir_name = (values['OUTPUT'])
    ImageItems = os.walk(dir_name)
    ImageExts = (".JPG", ".JPEG", ".PNG", ".BMP", ".HEIC", ".HEIF", ".jpg", ".jpeg", ".jpe", ".jif",
                 ".jfif", ".heif", ".heic", ".gif", ".png", ".bmp")

    for root, dirs, files in ImageItems:
        for file in files:
            if file.endswith(ImageExts):
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print(os.path.join(root,file))
                sys.stdout = org_stdout
                sg.Print("Redacting Image File: ", os.path.join(root,file))
                window.refresh()
                os.remove(os.path.join(root, file))
                

def video_delete():             #delete video files by file extension
    dir_name = (values['OUTPUT'])
    VideoItems = os.walk(dir_name)
    VideoExts = (".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".mp4", ".m4v", ".m4p", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd", ".mkv",
            ".ogg", ".webm", ".MPG", ".MP2", ".MPEG", ".MPE", ".MPV", ".MP4", ".M4V", ".M4P", ".AVI", ".WMV", ".MOV", ".QT", ".FLV", ".SWF",
            ".AVCHD", ".MKV", ".OGG", ".WEBM")

    for root, dirs, files in VideoItems:
        for file in files:
            if file.endswith(VideoExts):
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print(os.path.join(root,file))
                sys.stdout = org_stdout
                sg.Print("Redacting Video File: ", os.path.join(root,file))
                window.refresh()
                os.remove(os.path.join(root, file))

def md5_remove():
    name = (values['OUTPUT'])

    with open(values['HASHLIST'], 'r') as f:   #opens file cont hash list
        HLvariableCase = f.read().splitlines()

    remove = [x.lower() for x in HLvariableCase]  #hashes moved to lower case to work with code below    

    for root, subfolder, files in os.walk(name):
        for items in files:
            filename = os.path.join(root, items)
            with open(filename, 'rb') as inputfile:
                data = inputfile.read()
            hash_list = ([filename, hashlib.md5(data).hexdigest()])
            inputfile.close()
            #print(hash_list)

            if hash_list[1] in remove:  #Compare file hashes with hashes in list file.
                remove_list = (hash_list[0])
                sg.Print("Removing File Based on MD5: ", remove_list)
                window.refresh()
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print(remove_list)
                sys.stdout = org_stdout
                os.remove(remove_list)


def redact_PDF():
    dir_name = (values['OUTPUT'])
    for root, subfolder, files in os.walk(dir_name):
        for items in files:
            try:
            #print(items)
                filename = os.path.join(root, items)
            #print(filename)
                if filename.endswith(".pdf"):     #Walks the directories and finds the PDFs
        
                    sg.Print("Redacting Images from PDF: ", filename)
                    window.refresh()
                    doc = fitz.open(filename)    #Opens PDF file

                    if values['FIRSTPAGE'] == True:
                        for pageNumber, page in enumerate(doc.pages(1, None)):  #get page numbers for pdf and skips 1st page 
                            for imgNumber, img in enumerate(page.getImageList(), start=1):#get image numbers for each page
                                #print(img[7])         
                                box = page.getImageBbox(img[7])  #img[7] provides the image name
        
                            # colors for redaction box
                                yellow = (1, 1, 0)
                                black = (0, 0, 0)
        
                                for line in box:    #Loop allows redaction for pages with more than 1 image
                                    #print(line)
                                    page.addRedactAnnot(box, "REDACTED",align=fitz.TEXT_ALIGN_CENTER, fill=black, text_color=yellow)

                            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)   #applies redactions per page, prevents image modification and forces replacement

                    else:
                        for pageNumber, page in enumerate(doc.pages()):  #get page numbers for pdf and skips 1st page 
                            for imgNumber, img in enumerate(page.getImageList(), start=1):#get image numbers for each page
                                #print(img[7])         
                                box = page.getImageBbox(img[7])  #img[7] provides the image name
        
                            # colors for redaction box
                                yellow = (1, 1, 0)
                                black = (0, 0, 0)
        
                                for line in box:    #Loop allows redaction for pages with more than 1 image
                                    #print(line)
                                    page.addRedactAnnot(box, "REDACTED",align=fitz.TEXT_ALIGN_CENTER, fill=black, text_color=yellow)

                            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)   #applies redactions per page, prevents image modification and forces replacement
                    with open(completeName, 'a') as report:
                        sys.stdout = report
                        print(filename)
                    sys.stdout = org_stdout  
                    redactedFile = os.path.join(root, "REDACTED-" + items)
                doc.save(redactedFile, garbage=3, deflate=True)  #saves the new redacted PDF with amended file name, deflate removes spare areas
            except ValueError:
                sg.Print('There was an error redacting ' + filename + ". Please review its status in the output folder.")
                window.refresh()
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print('There was an error redacting ' + filename + ". Please review its status in the output folder.")
                sys.stdout = org_stdout
                pass
            except Exception:
                sg.Print('There was an error redacting ' + filename)
                window.refresh()
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print('There was an error redacting ' + filename + ". Please review its status in the output folder.")
                sys.stdout = org_stdout
              
            

#breaking on other office files like pptx & xlsx
def redact_imagesDOCX():
    dir_name = (values['OUTPUT'])
    blur = ImageFilter.GaussianBlur(150)
    for root, subfolder, files in os.walk(dir_name):
        for items in files:
            filename = os.path.join(root, items)
            #print(filename)
            if filename.endswith(".docx"):
                sg.Print("Redacting Images from DOCX: ", filename)
                window.refresh()
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print(filename)
                sys.stdout = org_stdout
                
                outfile = os.path.join(root, 'REDACTED-' + items)
                #print(outfile)
                
                with zipfile.ZipFile(filename) as inzip:
                    with zipfile.ZipFile(outfile, "w") as outzip:
                        for info in inzip.infolist():
                            name = info.filename
                                #print(info)
                            content = inzip.read(info)
                            if name.endswith((".png", ".jpeg", ".jpg", ".jfif", ".bmp", ".gif")):
                                fmt = name.split(".")[-1]
                                img = Image.open(io.BytesIO(content))
                                img = img.convert().filter(blur)
                                outb = io.BytesIO()
                                img.save(outb, fmt)
                                content = outb.getvalue()
                                info.file_size = len(content)
                                info.CRC = zipfile.crc32(content)
                            outzip.writestr(info, content)

    

sg.theme('DarkGrey13')   # Add a touch of color
# All the stuff inside your window.
popup =  [sg.popup("This tool is intended to assist, not replace, a human being in producing documents and files for use in legal proceedings.",
                   "The user must click 'OK' to acknowledge any productions made with this tool should be manually reviewed.",
                   "Use this tool at your own risk.  No warranty or guarantee is offered in its use.", no_titlebar=True, grab_anywhere=True)]

layout = [  [sg.Text('pteREDACTool', size=(29, 1), font=('Arial Black', 20, 'bold underline')), sg.Image(data=pteraimg)],
            [sg.Text('Files in Source will be copied to Output. Unwanted files will then be removed from Output directory:')],
            [sg.Text('Source Directory:'),sg.Input(key='SOURCE'), sg.FolderBrowse(key='SOURCE')],
            [sg.Text('Output Directory:'),sg.Input(key='OUTPUT'), sg.FolderBrowse(key='OUTPUT')],
            [sg.Text('_'*100)],
            [sg.Text('SELECT ELEMENTS TO DELETE FROM OUTPUT DIRECTORY:')],
            [sg.Text('Delete Files by Image or Video File Extensions:')],
            [sg.Text(' '*5), sg.Checkbox('.jpg, .jpeg, .jpe, .jif, .jfif, .heif, .heic, .gif, .png, .bmp', default=False, disabled=False, key='IMAGES')],
            [sg.Text(' '*5), sg.Checkbox('.mpg,.mp2, .mpeg, .mpe, .mpv, .mp4, .m4v, .m4p, .avi, .wmv, .mov, .qt, .flv, .swf, .avchd, .mkv,.ogg, .webm', default=False, disabled=False, key='VIDEOS')],
            [sg.Text('_'*100)],
            [sg.Checkbox('Files Based on Nudity Level   |', default=False, key='NUDITY'),sg.Text('Select Nudity Filter Level: '), sg.Combo(['Normal Filter', 'Aggresive Filter'], key='NUDITYLEVEL')],
            [sg.Text('_'*100)],
            [sg.Checkbox('Files Based on MD5   |', default=False, key='HASH'), sg.Text("MD5 Hash List (.txt)"), sg.Input(key='HASHLIST'), sg.FileBrowse(key='HASHLIST')],
            [sg.Text('_'*100)],
            [sg.Text('REDACT IMAGES INSIDE DOCUMENTS:')],
            [sg.Checkbox('Redact Images from PDF   |', default=False, key='PDF'), sg.Checkbox('Do NOT Redact 1st Page of PDFs', default=False, key='FIRSTPAGE')],
            [sg.Checkbox('Redact Images from .DOCXs', default=False, key='DOCX')],
            [sg.Text('_'*100)],
            [sg.Button('Ok'), sg.Button('Exit'), sg.Text(' '*148), sg.Button('?', key='HELP')]]



# Create the Window
window = sg.Window('pteREDACTool - Image/Video Redaction Tool', layout, no_titlebar=False, alpha_channel=.95, grab_anywhere=True, icon='.\\NLC logo.ico')
# Event Loop to process "events" and get the "values" of the inputs


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    elif event == 'HELP':
        popup = [sg.popup("pteREDACTool is a redaction tool designed to help those working on CSAM investigations.",
                          "The tool is designed to copy the contents of a directory (Source) to a second location (Output) and then delete/redact files in the second directory. It does this in the following order:", 
                          "1. Copy evidence to new location.", 
                          "2. Remove files based on file extension, nudity level, or MD5 hash.", 
                          "3. Create Report.", '\n',
                          "If you find there are problems running the nudity filter, please navigate to 'C:/Users/*username*/.NudeNet/' (this is a Hidden folder). If any .onnx files are present with no data, delete the contents of the folder and restart pteREDACTool WITH A STRONG INTERNET CONNECTION and run the nudity filter against a data set.  This will cause the tool to download the needed filter data.",
                          "Document redaction for PDFs and DOCXs currently only supports images.  For PDFs you can elect to skip the first page of a document to preserve headers and letterheads.",
                          "**IMPORTANT** Document redaction will leave a copy of BOTH the redacted and unredacted document in the output folder.  The examiner will need to delete unwanted versions manually. pteREDECTool makes this easier by renaming redacted documents with the prefiX 'REDACTED-'.", "\n Copyright 2021 North Loop Consulting, LLC", no_titlebar=True, grab_anywhere=True)]
    elif event == 'Ok':
        
        if (values['SOURCE']) != 0:   #copies
            for i in range(100000):
                sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='COPYING...', font='Courier 20', text_color="White", background_color='Grey', transparent_color='Grey', time_between_frames=120)
            copy_folder()
            make_report()
            sg.PopupAnimated(None)
            if (values['IMAGES']) == True:  #deletes images in copy
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING IMAGE FILES...', font='Courier 20', text_color="White", background_color='Grey', transparent_color='Grey', time_between_frames=120)
                image_delete()
                window.refresh()
            if (values['VIDEOS']) == True: #deletes videos in copy
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING VIDEO FILES...', font='Courier 20', text_color="White",background_color='Grey', transparent_color='Grey', time_between_frames=120)
                video_delete()
                sg.PopupAnimated(None)      # close all Animated Popups
                window.refresh()
            if (values['NUDITY']) == True: #deletes based on nudity level in copy
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING NUDITY, THIS TAKES SOME TIME...', font='Courier 20', text_color="White", background_color='Grey', transparent_color='Grey', time_between_frames=120)
                subfolders, files = run_fast_scandir(values['OUTPUT'], ImageExts)
                run_fast_scandir(values['OUTPUT'], ImageExts)
                nudity_filter()
                sg.PopupAnimated(None)      # close all Animated Popups
                window.refresh()
            if (values['HASH']) == True: #deletes base on a list of provided md5 hashes
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING BASED ON MD5...', font='Courier 20', text_color="White", background_color='Grey', transparent_color='Grey', time_between_frames=120)
                md5_remove()
                sg.PopupAnimated(None)      # close all Animated Popups
                window.refresh()
            if (values['PDF']) == True:
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING PDF CONTENT...', font='Courier 20', text_color="White", background_color='Grey', transparent_color='Grey', time_between_frames=120)
                redact_PDF()
                sg.PopupAnimated(None)      # close all Animated Popups
                window.refresh()
            if (values['DOCX']) == True:
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING DOCUMENT CONTENT...', font='Courier 20', text_color="White", background_color='Grey', transparent_color='Grey', time_between_frames=120)
                redact_imagesDOCX()
                sg.PopupAnimated(None)      # close all Animated Popups
                window.refresh()
            sg.PopupAnimated(None)      # close all Animated Popups
        pop = [sg.popup("Looks like we're done. Here is the 'REDACTION REPORT.txt' now saved in your output directory.", no_titlebar=True, grab_anywhere=True)]
        time.sleep(1)
        os.startfile(completeName)
        window.refresh()

window.close()
