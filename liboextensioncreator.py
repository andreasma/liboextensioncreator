#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import os
import shutil
import ntpath
from xml.dom import minidom
from zipfile import ZipFile
import validators
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel, QLineEdit, QFormLayout, QVBoxLayout, QHBoxLayout, QComboBox, QDialogButtonBox, QCheckBox, QFileDialog


cwd = os.getcwd()
description_filename = ''
icon_filename = ''
extensionname = ''


class CreatorApp(QMainWindow):
    
    def __init__(self): 
        super().__init__() 
        self.title = 'LibreOffice Extension Creator Dialog'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 700
        self.setWindowTitle(self.title) 
        self.setGeometry(self.left, self.top, self.width, self.height) 
  
        self.tab_widget = MyTabWidget(self) 
        self.setCentralWidget(self.tab_widget) 
  
        self.show()



        
        
class MyTabWidget(QWidget): 
    def __init__(self, parent): 
        super(QWidget, self).__init__(parent) 
        self.layout = QFormLayout(self) 
  
        # Initialize tab screen 
        self.tabs = QTabWidget() 
        self.tab1 = QWidget() 
        self.tab2 = QWidget() 
        self.tab3 = QWidget() 
        self.tabs.resize(600, 500) 
  
        # Add tabs 
        self.tabs.addTab(self.tab1, "General") 
        self.tabs.addTab(self.tab2, "Registration / License") 
        self.tabs.addTab(self.tab3, "Extension Content") 
  
        # Create first tab 
        self.tab1.layout = QFormLayout(self)
        self.nameliboext = QLineEdit()
        self.tab1.layout.addRow("Name of your LibreOffice Extension",self.nameliboext)
        self.nameextauthor = QLineEdit()
        self.tab1.layout.addRow("Name of the extension author / publisher",self.nameextauthor)
        self.authorwebsite = QLineEdit()
        self.tab1.layout.addRow("URL of the author's / publisher's  website or blog", self.authorwebsite)      
        self.extversion = QLineEdit()
        self.tab1.layout.addRow("Version number of the extension (e.gl 0.1)", self.extversion)
        self.extidentifier = QLineEdit()
        self.tab1.layout.addRow("Identifier", self.extidentifier)
        self.showedname = QLineEdit()
        self.tab1.layout.addRow("Displayed Name", self.showedname)
        self.platform = QLabel()
        self.platform.setText('Platform')
        self.platf = QComboBox()
        self.tab1.layout.addRow(self.platform, self.platf)
        self.platf.addItem('all')
        self.platf.addItem('linux_x86')
        self.platf.addItem('linux_x86_64')
        self.platf.addItem('windows_x86')
        self.platf.addItem('macosx_x86')
        self.platf.addItem('macosx_x86_64')
        self.platf.addItem('free_bsd_x86')
        self.platf.addItem('free_bsd_x86_x64')
        self.platf.addItem('linux_arm_eabi')
        self.platf.addItem('linux_arm_oabi')
        self.platf.addItem('linux_ia64')
        self.platf.addItem('linux_mips_eb')
        self.platf.addItem('linux_mips_el')
        self.platf.addItem('linux_powerpc')
        self.platf.addItem('linux_powerpc64')
        self.platf.addItem('linux_s390')
        self.platf.addItem('linux_s390x')
        self.platf.addItem('linux_sparc')
        self.platf.addItem('macosx_powerpc')
        self.platf.addItem('os2_x86')
        self.platf.addItem('solaris_sparc')
        self.platf.addItem('solaris_x86')
        self.liboversion = QLabel()
        self.liboversion.setText('Minimal LibreOffice version')
        self.libv = QComboBox()
        self.tab1.layout.addRow(self.liboversion,self.libv)
        self.libv.addItem('4.2')
        self.libv.addItem('4.3')
        self.libv.addItem('4.4')
        self.libv.addItem('5.0')
        self.libv.addItem('5.1')
        self.libv.addItem('5.2')
        self.libv.addItem('5.3')
        self.libv.addItem('5.4')
        self.libv.addItem('6.0')
        self.libv.addItem('6.1')
        self.libv.addItem('6.2')
        self.libv.addItem('6.3')
        self.libv.addItem('6.4')
        self.libv.addItem('7.0')
        self.libv.addItem('7.1')
        self.descr = QLabel()
        self.descr.setText('Description / Documentation of the Extension (*.txt) (English Language)')
        self.descrbutton = QPushButton()
        self.descrbutton.setText('Choose File')
        self.descrbutton.setGeometry(QtCore.QRect(200, 150, 93, 28)) 
        self.tab1.layout.addRow(self.descr, self.descrbutton)
        self.descrbutton.clicked.connect(self.copy_description_file)
        self.exticon = QLabel()
        self.exticon.setText('Choose an Icon for your extension, if you already created one.')
        self.exticonbutton = QPushButton()
        self.exticonbutton.setText('Choose an Icon')
        self.exticonbutton.setGeometry(QtCore.QRect(200,150,93,28))
        self.tab1.layout.addRow(self.exticon, self.exticonbutton)
        self.exticonbutton.clicked.connect(self.copy_icon_file)
        self.button_label = QLabel()
        self.button_label.setText('Once you are finished with the data fields, you could create the extension by clicking the OK button.')
        self.tab1.layout.addRow(self.button_label)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.tab1.layout.addRow(self.button_label, self.buttonBox)
        self.tab1.setLayout(self.tab1.layout)
        
        
        # Create second tab 
        self.tab2.layout = QFormLayout(self)
        self.acceptedby = QLabel()
        self.acceptedby.setText('Accepted by')
        self.ack = QComboBox()
        self.tab2.layout.addRow(self.acceptedby, self.ack)
        self.ack.addItem('admin')
        self.ack.addItem('user')
        self.extlicense = QLabel()
        self.extlicense.setText('Choose a license for your extension')
        self.extlicense.setGeometry(QtCore.QRect(500, 150, 93, 28))
        self.eli = QComboBox()
        self.eli.setGeometry(QtCore.QRect(200, 150, 93, 28))
        self.tab2.layout.addRow(self.extlicense, self.eli)
        self.eli.addItem('GPL-2.0 (General Public License Version 2.0)')
        self.eli.addItem('GPL-3.0 (General Public License Version 3.0)')
        self.eli.addItem('LGPL-3.0 (Lesser General Public License Version 3.0)')
        self.eli.addItem('LGPL-2.1 (Lesser General Public License Version 2.1)')
        self.soupd = QLabel()
        self.soupd.setText('suppress-on-update')
        self.soupdbox = QCheckBox()
        self.sifreq = QLabel()
        self.sifreq.setText('suppress-if-required')
        self.sifreqbox = QCheckBox()
        self.tab2.layout.addRow(self.soupdbox, self.soupd)
        self.tab2.layout.addRow(self.sifreqbox, self.sifreq)
        self.tab2.setLayout(self.tab2.layout)
  
        # Add tabs to widget 
        self.layout.addWidget(self.tabs) 
        self.setLayout(self.layout) 
        
    def accept(self):
        # create the extension
        global extensionname
        extensionname = self.nameliboext.text().replace(' ', '')
        identifier = self.extidentifier.text().strip()
        author = self.nameextauthor.text().strip()
        extensionversion = self.extversion.text().strip()
        displayedname = self.showedname.text().strip()
        platform = self.platf.currentText()
        libreofficeversion = self.libv.currentText()
        wb = self.authorwebsite.text().strip()
        if validators.url(wb):
            website = wb
        else:
            website = None
        accepted_by = self.ack.currentText()
        extension_license = self.eli.currentText().lower().split(' (')[0]
        licensefilename = extension_license + '.' + 'txt'
        licenserellink = os.path.join('registration', licensefilename)
        
        
        # building manifest.xml
        manifestfile = minidom.Document()
        manifest_manifest = manifestfile.createElement('manifest:manifest')
        manifest_manifest.setAttribute('xmlns:manifest', 'http://openoffice.org/2001/manifest')
        manifest_file_entry = manifestfile.createElement('manifest:file-entry')
        manifest_file_entry.setAttribute('manifest:media-type', 'application/vnd.sun.star.configuration-data')
        manifest_file_entry.setAttribute('manifest:full-path', 'paths.xcu')
        manifest_manifest.appendChild(manifest_file_entry)
        manifestfile.appendChild(manifest_manifest)
        
        # building path.xcu
        path_xcu_file = minidom.Document()
        odc = path_xcu_file.createElement('oor:component-data')
        odc.setAttribute('oor:package', 'org.openoffice.Office')
        odc.setAttribute('oor:name', 'Paths')
        odc.setAttribute('xmlns:install', 'http://openoffice.org/2004/installation')
        odc.setAttribute('xmlns:oor', 'http://openoffice.org/2001/registry')
        odc.setAttribute('xmlns:xs', 'http://www.w3.org/2001/XMLSchema')
        odc.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        path_xcu_file.appendChild(odc)
        
                
        # building the description.xml file
        descriptionfile = minidom.Document()
        tag_description = descriptionfile.createElement('description')
        tag_description.setAttribute('xmlns', 'http://openoffice.org/extensions/description/2006')
        tag_description.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        tag_identifier = descriptionfile.createElement('identifier')
        tag_identifier.setAttribute('value', identifier)
        tag_version = descriptionfile.createElement('version')
        tag_version.setAttribute('value', extensionversion)
        tag_platform = descriptionfile.createElement('platform')
        tag_platform.setAttribute('value', platform)
        tag_display_name = descriptionfile.createElement('display-name')
        tag_dp_name = descriptionfile.createElement('name')
        tag_dp_name.setAttribute('lang', 'en')
        tag_dp_name_data = descriptionfile.createTextNode(displayedname)
        tag_publisher = descriptionfile.createElement('publisher')
        tag_name = descriptionfile.createElement('name')
        if website != None:
            tag_name.setAttribute('xlink:href', website)
        tag_author = descriptionfile.createTextNode(author)
        if icon_filename != '':
            iconname = ntpath.basename(icon_filename)
            iconrellink = os.path.join('images', iconname)
            tag_icon = descriptionfile.createElement('icon')
            tag_icon_default = descriptionfile.createElement('default')
            tag_icon_default.setAttribute('xlink:href', iconrellink)
        tag_dependencies = descriptionfile.createElement('dependencies')
        tag_dependencies.setAttribute('xmlns:lo', 'http://libreoffice.org/extensions/description/2011')
        tag_minimal_version = descriptionfile.createElement('lo:LibreOffice-minimal-version')
        tag_minimal_version.setAttribute('name', 'LibreOffice ' + libreofficeversion)
        tag_minimal_version.setAttribute('value', libreofficeversion)
        if description_filename != '':
            name = ntpath.basename(description_filename)
            rellink = os.path.join('description', name)
            tag_extension_description = descriptionfile.createElement('extension-description')
            tag_src = descriptionfile.createElement('src')
            tag_src.setAttribute('xlink:href', rellink)
            tag_src.setAttribute('lang', 'en')
        tag_registration = descriptionfile.createElement('registration')
        tag_simple_license = descriptionfile.createElement('simple-license')
        tag_simple_license.setAttribute('accept-by', accepted_by)
        if self.soupdbox.isChecked() == True:
            tag_simple_license.setAttribute('suppress-on-update', 'True')
        if self.sifreqbox.isChecked() == True:
            tag_simple_license.setAttribute('suppress-if-required', 'True')
        tag_license_text = descriptionfile.createElement('license-text')
        tag_license_text.setAttribute('lang', 'en')
        tag_license_text.setAttribute('xlink:href', licenserellink)
        tag_description.appendChild(tag_identifier)
        tag_description.appendChild(tag_version)
        tag_description.appendChild(tag_platform)
        tag_dp_name.appendChild(tag_dp_name_data)
        tag_display_name.appendChild(tag_dp_name)
        tag_description.appendChild(tag_display_name)
        tag_name.appendChild(tag_author)
        tag_publisher.appendChild(tag_name)
        tag_description.appendChild(tag_publisher)
        if icon_filename != '':
            tag_icon.appendChild(tag_icon_default)
            tag_description.appendChild(tag_icon)
        tag_dependencies.appendChild(tag_minimal_version)
        tag_description.appendChild(tag_dependencies)
        if description_filename != '':
            tag_extension_description.appendChild(tag_src)
            tag_description.appendChild(tag_extension_description)
        tag_simple_license.appendChild(tag_license_text)
        tag_registration.appendChild(tag_simple_license)
        tag_description.appendChild(tag_registration)
        descriptionfile.appendChild(tag_description)
        
        
        os.makedirs(os.path.join(cwd, 'working_directory', extensionname, 'META-INF'), exist_ok=True)
        os.makedirs(os.path.join(cwd, 'working_directory', extensionname, 'registration'), exist_ok=True)
        path = os.path.join(cwd, 'working_directory', extensionname)
        licenseinputpath = os.path.join(cwd, 'license_files', licensefilename)
        licenseoutputpath = os.path.join(cwd, 'working_directory', extensionname, 'registration', licensefilename)
              
        shutil.copy(licenseinputpath, licenseoutputpath)
        
        with open(os.path.join(path, 'description.xml'), 'w') as f:
            descriptionfile.writexml(f, "", "\t", "\n")
            
        with open(os.path.join(path, 'META-INF', 'manifest.xml'), 'w') as f:
            manifestfile.writexml(f, "", "\t", "\n")
            
        with open(os.path.join(path, 'path.xcu'), 'w') as f:
            path_xcu_file.writexml(f, "", "\t", "\n")
            
        
        with ZipFile(extensionname + '.' + 'oxt', 'w') as liboextensionzip:
            os.chdir(path)
            for root, dirs, files in os.walk('.'):
                for name in files:
                    if not name == extensionname:
                        liboextensionzip.write(os.path.join(root, name)) 
          
     
            
    def reject(self):
        pass
        
        
           
    def copy_description_file(self):
        global description_filename
        description_filename, _ = QFileDialog.getOpenFileName(
            caption="Choose description / documenation file", filter="Plain text (*.txt)"
            )
        if description_filename:
            os.makedirs(os.path.join(cwd, 'working_directory', extensionname, 'description'), exist_ok=True)
            path = os.path.join(cwd, 'working_directory', extensionname, 'description')
            shutil.copy(description_filename, path)
        
               
    def copy_icon_file(self):
        global icon_filename
        icon_filename, _ = QFileDialog.getOpenFileName(
            caption='Choose an icon file for your extension', filter='Image (*.png)'
            )
        if icon_filename:
            os.makedirs(os.path.join(cwd, 'working_directory', extensionname, 'images'), exist_ok=True)
            path = os.path.join(cwd, 'working_directory', extensionname, 'images')
            shutil.copy(icon_filename, path)
        

  
if __name__ == '__main__': 
    app = QApplication(sys.argv) 
    ex = CreatorApp() 
    sys.exit(app.exec_()) 
