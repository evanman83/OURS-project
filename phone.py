# config variables
screen_lock_rpi_pin = 26
audio_changeover_rpi_pin = 21
testing = False
serial_port = '/dev/ttyUSB2'

if (testing):
    # if running on your PC, these imports might be what you need
    from PySide2.QtWidgets import QMainWindow,QWidget,QAction,QPushButton,QApplication,QListWidget,QGridLayout,QLabel,QDesktopWidget,QTextEdit,QTabWidget,QVBoxLayout,QFormLayout,QLineEdit,QMessageBox,QPlainTextEdit
    from PySide2.QtCore import QTimer,QDateTime,Qt
    from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
else:
    # if running on your Raspberry Pi, these imports, and actions, might be what you need
    from PyQt5.QtWidgets import QMainWindow,QWidget,QAction,QPushButton,QApplication,QListWidget,QGridLayout,QLabel,QDesktopWidget,QTextEdit,QTabWidget,QVBoxLayout,QFormLayout,QLineEdit,QMessageBox,QPlainTextEdit
    from PyQt5.QtCore import QTimer,QDateTime,Qt
    from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
    import serial
    ser = serial.Serial(serial_port, 9600, timeout = 2)
    import pigpio
    pi = pigpio.pi()
    pi.set_mode(screen_lock_rpi_pin, pigpio.INPUT)
    pi.set_pull_up_down(screen_lock_rpi_pin, pigpio.PUD_UP)

# imports
import sys
import time
import os
import re

# setup database
db = QSqlDatabase("QSQLITE")
db.setDatabaseName("test.sqlite")
db.open()
db.exec_("CREATE TABLE IF NOT EXISTS contact (name STRING, mobile NUMBER);")
db.exec_("CREATE TABLE IF NOT EXISTS sms (mobile NUMBER, message STRING, received_at DATETIME);")


class WinForm(QWidget):
    def __init__(self,parent=None):

        super(WinForm, self).__init__(parent)
        self.setWindowTitle('Phone')
        self.resize(400, 600)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        layout=QVBoxLayout()

        # global variables
        self.dialling = ""
        self.gps_active = False
        self.counter = 0
        self.network = ""
        self.signal = ""
        self.call_state = ""

        # initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        #self.tabs.resize(300, 500)

        # add tabs
        self.tabs.addTab(self.tab1, "Call")
        self.tabs.addTab(self.tab2, "SMS")
        self.tabs.addTab(self.tab3, "Contacts")
        self.tabs.addTab(self.tab4, "Cmd")

        # create tab #1 - Calling
        self.tab1.layout = QGridLayout(self)
        self.tab1.label = QLabel('Starting...')
        self.tab1.label.setAlignment(Qt.AlignCenter);
        self.tab1.btnGreenPhone = QPushButton('Answer')
        self.tab1.btnRedPhone = QPushButton('Hang up')
        self.tab1.btnDial1 = QPushButton('1')
        self.tab1.btnDial2 = QPushButton('2')
        self.tab1.btnDial3 = QPushButton('3')
        self.tab1.btnDial4 = QPushButton('4')
        self.tab1.btnDial5 = QPushButton('5')
        self.tab1.btnDial6 = QPushButton('6')
        self.tab1.btnDial7 = QPushButton('7')
        self.tab1.btnDial8 = QPushButton('8')
        self.tab1.btnDial9 = QPushButton('9')
        self.tab1.btnDial0 = QPushButton('0')
        self.tab1.layout.addWidget(self.tab1.label,0,0,1,3)
        self.tab1.layout.addWidget(self.tab1.btnGreenPhone,1,0)
        self.tab1.layout.addWidget(self.tab1.btnRedPhone,1,2)
        self.tab1.layout.addWidget(self.tab1.btnDial1,2,0)
        self.tab1.layout.addWidget(self.tab1.btnDial2,2,1)
        self.tab1.layout.addWidget(self.tab1.btnDial3,2,2)
        self.tab1.layout.addWidget(self.tab1.btnDial4,3,0)
        self.tab1.layout.addWidget(self.tab1.btnDial5,3,1)
        self.tab1.layout.addWidget(self.tab1.btnDial6,3,2)
        self.tab1.layout.addWidget(self.tab1.btnDial7,4,0)
        self.tab1.layout.addWidget(self.tab1.btnDial8,4,1)
        self.tab1.layout.addWidget(self.tab1.btnDial9,4,2)
        self.tab1.layout.addWidget(self.tab1.btnDial0,5,1)
        self.tab1.setLayout(self.tab1.layout)
        self.tab1.btnDial0.clicked.connect(lambda: self.dialNumber("0"))
        self.tab1.btnDial1.clicked.connect(lambda: self.dialNumber("1"))
        self.tab1.btnDial2.clicked.connect(lambda: self.dialNumber("2"))
        self.tab1.btnDial3.clicked.connect(lambda: self.dialNumber("3"))
        self.tab1.btnDial4.clicked.connect(lambda: self.dialNumber("4"))
        self.tab1.btnDial5.clicked.connect(lambda: self.dialNumber("5"))
        self.tab1.btnDial6.clicked.connect(lambda: self.dialNumber("6"))
        self.tab1.btnDial7.clicked.connect(lambda: self.dialNumber("7"))
        self.tab1.btnDial8.clicked.connect(lambda: self.dialNumber("8"))
        self.tab1.btnDial9.clicked.connect(lambda: self.dialNumber("9"))
        self.tab1.btnGreenPhone.clicked.connect(self.greenPhone)
        self.tab1.btnRedPhone.clicked.connect(self.redPhone)
        self.tab1.btnGreenPhone.setEnabled(False)
        self.tab1.btnRedPhone.setEnabled(False)

        # create tab #2 - SMS
        self.tab2.layout = QGridLayout(self)
        self.tab2.smsMobile = QLineEdit()
        self.tab2.smsText = QPlainTextEdit()
        self.tab2.layout.addWidget(QLabel("Mobile:"),0,0,1,1)
        self.tab2.layout.addWidget(self.tab2.smsMobile,0,1,1,3)
        self.tab2.layout.addWidget(self.tab2.smsText,1,0,2,4)
        self.tab2.btnCall = QPushButton('Call')
        self.tab2.btnReply = QPushButton('Reply')
        self.tab2.btnDelete = QPushButton('Del')
        self.tab2.btnSend = QPushButton('Send')
        self.tab2.layout.addWidget(self.tab2.btnCall,3,0)
        self.tab2.layout.addWidget(self.tab2.btnReply,3,1)
        self.tab2.layout.addWidget(self.tab2.btnDelete,3,2)
        self.tab2.layout.addWidget(self.tab2.btnSend,3,3)
        self.tab2.listwidget = QListWidget()
        self.tab2.listwidget.setWordWrap(True)
        self.tab2.listwidget.setStyleSheet("QListWidget::item { border-bottom: 1px solid grey; padding: 10 0; } QListWidget::item:selected { color: black; background: rgb(210,210,210); }")
        self.listSMSs()
        self.tab2.listwidget.clicked.connect(self.selectSMS)
        self.tab2.layout.addWidget(self.tab2.listwidget,4,0,4,4)
        self.tab2.btnCall.setEnabled(False)
        self.tab2.btnReply.setEnabled(False)
        self.tab2.btnDelete.setEnabled(False)
        self.tab2.setLayout(self.tab2.layout)
        self.tab2.btnCall.clicked.connect(self.callSelectedContact)
        self.tab2.btnReply.clicked.connect(self.smsSelectedContact)
        self.tab2.btnDelete.clicked.connect(self.deleteSMS)
        self.tab2.btnSend.clicked.connect(self.sendSMS)

        # create tab #3 - People / address book / contacts
        self.tab3.layout = QGridLayout(self)
        self.tab3.newContactName = QLineEdit()
        self.tab3.newContactMobile = QLineEdit()
        self.tab3.layout.addWidget(QLabel("Name:"),0,0,1,1)
        self.tab3.layout.addWidget(self.tab3.newContactName,0,1,1,3)
        self.tab3.layout.addWidget(QLabel("Mobile:"),1,0,1,1)
        self.tab3.layout.addWidget(self.tab3.newContactMobile,1,1,1,3)
        self.tab3.btnCall = QPushButton('Call')
        self.tab3.btnSMS = QPushButton('SMS')
        self.tab3.btnDelete = QPushButton('Del')
        self.tab3.btnSave = QPushButton('Save')
        self.tab3.layout.addWidget(self.tab3.btnCall,2,0)
        self.tab3.layout.addWidget(self.tab3.btnSMS,2,1)
        self.tab3.layout.addWidget(self.tab3.btnDelete,2,2)
        self.tab3.layout.addWidget(self.tab3.btnSave,2,3)
        self.tab3.listwidget = QListWidget()
        self.tab3.listwidget.setStyleSheet("QListWidget::item { border-bottom: 1px solid grey; padding: 10 0; } QListWidget::item:selected { color: black; background: rgb(210,210,210); }")
        self.listContacts()
        self.tab3.listwidget.clicked.connect(self.selectContact)
        self.tab3.layout.addWidget(self.tab3.listwidget,3,0,1,4)
        self.tab3.btnCall.setEnabled(False)
        self.tab3.btnSMS.setEnabled(False)
        self.tab3.btnDelete.setEnabled(False)
        self.tab3.setLayout(self.tab3.layout)
        self.tab3.btnCall.clicked.connect(self.callSelectedContact)
        self.tab3.btnSMS.clicked.connect(self.smsSelectedContact)
        self.tab3.btnDelete.clicked.connect(self.deleteContact)
        self.tab3.btnSave.clicked.connect(self.saveNewContact)

        # create tab #4 - Commands / debug / console
        self.tab4.layout = QGridLayout(self)
        self.tab4.log = QTextEdit()
        self.tab4.btnPhoto = QPushButton('Photo')
        self.tab4.btnGPSOn = QPushButton('GPS On')
        self.tab4.btnGPSOff = QPushButton('GPS Off')
        self.tab4.btnNetwork = QPushButton('Network')
        self.tab4.btnSignal = QPushButton('Signal')
        self.tab4.layout.addWidget(self.tab4.log,0,0,1,3)
        self.tab4.layout.addWidget(self.tab4.btnPhoto,2,0)
        self.tab4.layout.addWidget(self.tab4.btnGPSOn,2,1)
        self.tab4.layout.addWidget(self.tab4.btnGPSOff,2,2)
        self.tab4.layout.addWidget(self.tab4.btnNetwork,3,0)
        self.tab4.layout.addWidget(self.tab4.btnSignal,3,1)
        self.tab4.setLayout(self.tab4.layout)
        self.tab4.btnPhoto.clicked.connect(lambda: self.takePhoto())
        self.tab4.btnGPSOn.clicked.connect(lambda: self.toggleGPS(True))
        self.tab4.btnGPSOff.clicked.connect(lambda: self.toggleGPS(False))
        self.tab4.btnNetwork.clicked.connect(lambda: self.writeToSerial("AT+COPS?"))
        self.tab4.btnSignal.clicked.connect(lambda: self.writeToSerial("AT+CSQ"))

        # add tabs to widget
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # start the timer thread
        self.timer = QTimer()
        self.timer.timeout.connect(self.refreshScreen)
        self.timer.start(1000)


    def refreshScreen(self):

        # increment the counter
        self.counter = self.counter + 1
        if (self.counter == 1000):
            self.counter = 0

        # get the network name
        if (self.counter == 1):
            self.writeToSerial("AT+COPS?")

        # get the network signal strength, every 50 seconds
        if (self.counter % 50 == 5):
            self.writeToSerial("AT+CSQ")

        # get GPS position, every 25 seconds
        if (self.gps_active):
            if (self.counter % 25 == 0):
                self.writeToSerial("AT+CGPSINFO")

        # scan for new SMS messages, every 100 seconds
        if (self.counter % 100 == 20):
            self.downloadSMSs()

        # play ringtone if incoming call, every 2 seconds
        if (self.call_state == "incoming"):
            if (self.counter % 2 == 0):
                os.system("aplay ringtone.wav > /dev/null 2>&1")

        # update the screen
        if (self.call_state == ""):
            if (self.dialling == ""):
                thetime = QDateTime.currentDateTime()
                time_display = thetime.toString('hh:mm:ss')
                if (self.network != "" and self.signal != ""):
                    time_display = self.network + " " + str(int(int(self.signal)/31*100)) + "%\n" + time_display
                self.tab1.label.setText(time_display)
            else:
                self.tab1.label.setText("Dial "+self.dialling)
                self.tab1.btnRedPhone.setEnabled(True)
                self.tab1.btnRedPhone.setText("Cancel")
                self.tab1.btnGreenPhone.setText("Call")
                if (len(self.dialling) > 10):
                    self.tab1.btnGreenPhone.setEnabled(True)
        else:
            if (self.call_state == "incoming"):
                self.tab1.label.setText("Incoming call!")
                self.tab1.btnRedPhone.setEnabled(True)
                self.tab1.btnGreenPhone.setEnabled(True)
                self.tab1.btnRedPhone.setText("Reject")
                self.tab1.btnGreenPhone.setText("Answer")
            if (self.call_state == "outgoing"):
                self.tab1.label.setText("Making call...")
                self.tab1.btnGreenPhone.setEnabled(False)
                self.tab1.btnRedPhone.setEnabled(True)
                self.tab1.btnRedPhone.setText("Hang up")
            if (self.call_state == "busy"):
                self.tab1.label.setText("On phone call")
                self.tab1.btnGreenPhone.setEnabled(False)
                self.tab1.btnRedPhone.setEnabled(True)
                self.tab1.btnGreenPhone.setText("Answer")
                self.tab1.btnRedPhone.setText("Hang up")


        # read from serial port
        read_str = self.readFromSerial()


        # take action on responses
        if "CGPSINFO" in read_str:
            bits = read_str.split("CGPSINFO: ")
            f = open("location.txt", "w")
            f.write(bits[1])
            f.close

        if "COPS:" in read_str:
            bits = read_str.split(",")
            self.network = bits[2].strip('\"')

        if "CSQ:" in read_str:
            bits = read_str.split("CSQ: ")
            temp = bits[1].split(",")
            self.signal = temp[0]

        if "RING" in read_str:
            self.call_state = "incoming"

        if "MISSED_CALL" in read_str:
            self.call_state = ""
            self.hearPhoneAudio(False)

        if "BUSY" in read_str:
            self.call_state = ""
            self.hearPhoneAudio(False)

        if "NO CARRIER" in read_str:
            self.call_state = ""
            self.hearPhoneAudio(False)

        if "VOICE CALL: BEGIN" in read_str:
            self.call_state = "busy"
            self.writeToSerial("AT+CMICGAIN=5")
            self.hearPhoneAudio(True)

        if "VOICE CALL: END" in read_str:
            self.call_state = ""
            self.hearPhoneAudio(False)

        if "+CMTI:" in read_str:
            self.downloadSMSs()
            self.alert("New SMS received!")


        # turn on / off screen lock
        if (not testing):
            screen_lock = pi.read(screen_lock_rpi_pin)
            if (screen_lock == 1):
                os.system("xset dpms force on")
                os.system("xinput enable 6")
            else:
                os.system("xset dpms force off")
                os.system("xinput disable 6")


    def writeToSerial(self,cmd):
        self.tab4.log.append("> "+cmd)
        if (not testing):
            cmd = cmd + "\r"
            ser.close()
            ser.open()
            ser.write(cmd.encode())
        else:
            print("> "+cmd)


    def readFromSerial(self, buffer = 64):
        if (not testing):
            read_val = ser.read(size=buffer)
            read_str = bytearray(read_val).decode()
            if (len(read_str) > 1):
                temp = read_str.strip()
                temp = temp.replace("\r\n\r\n", "\n")
                temp = temp.replace("\r\r\n", "\n")
                self.tab4.log.append(temp)
            return read_str
        else:
            return "-"


    def downloadSMSs(self):
        self.writeToSerial('AT+CMGL="ALL"')
        message_dump = self.readFromSerial(5000)
        messages = message_dump.split("+CMGL:")
        count = 0
        for message in messages:
            lines = message.split("\r\n")
            if (len(lines) > 1):
                message = lines[1]
                temp = lines[0].split(",")
                if (len(temp) > 5):
                    mobile = temp[2].strip('\"')
                    if (len(mobile) > 20):
                        mobile = bytes.fromhex(mobile).decode('ascii').replace(chr(0),"")
                        message = bytes.fromhex(message).decode('ascii').replace(chr(0),"")
                    if (mobile[0] == "+"):
                        mobile = mobile[1:]
                    date = temp[4].strip('\"')
                    time = temp[5].strip('\"')
                    date = "20" + date
                    date = date.replace('/', "-")
                    temp = time.split("+")
                    time = temp[0]
                    timestamp = date + " " + time
                    query = QSqlQuery(db)
                    query.prepare("INSERT INTO sms (mobile,message,received_at) VALUES (:mobile,:message,:received_at)")
                    query.bindValue(":mobile", mobile)
                    query.bindValue(":message", message)
                    query.bindValue(":received_at", timestamp)
                    query.exec()
                    count = count + 1
        if (count > 0):
            self.writeToSerial("AT+CMGD=,4")
            self.listSMSs()


    def listSMSs(self):
        query = QSqlQuery(db)
        query.exec_("SELECT mobile,name FROM contact")
        saved_contacts = {}
        while query.next():
            saved_contacts[query.value(0)] = query.value(1)
        query = QSqlQuery(db)
        query.exec_("SELECT mobile,message,received_at FROM sms ORDER BY received_at DESC")
        row = 0
        self.tab2.listwidget.clear()
        while query.next():
            person = '+' + str(query.value(0))
            if (query.value(0) in saved_contacts):
                person = person + '\n' + saved_contacts[query.value(0)]
            self.tab2.listwidget.insertItem(row, str(query.value(2)) + ': ' + person + '\n' + str(query.value(1)))
            row = row + 1


    def listContacts(self):
        query = QSqlQuery(db)
        query.exec_("SELECT name,mobile FROM contact ORDER BY name DESC")
        row = 0
        self.tab3.listwidget.clear()
        while query.next():
            self.tab3.listwidget.insertItem(row, query.value(0) + ' +' + str(query.value(1)))
            row = row + 1


    def selectSMS(self, qmodelindex):
        sms = self.tab2.listwidget.currentItem().text()
        temp = sms.split(": +")
        self.current_sms_timestamp = temp[0]
        temp = temp[1].split('\n')
        self.current_contact_number = temp[0]
        self.tab2.btnCall.setEnabled(True)
        self.tab2.btnReply.setEnabled(True)
        self.tab2.btnDelete.setEnabled(True)


    def selectContact(self, qmodelindex):
        contact = self.tab3.listwidget.currentItem().text()
        temp = contact.split("+")
        self.current_contact_number = temp[1]
        self.tab3.btnCall.setEnabled(True)
        self.tab3.btnSMS.setEnabled(True)
        self.tab3.btnDelete.setEnabled(True)


    def callSelectedContact(self):
        self.dialling = self.current_contact_number
        self.tabs.setCurrentIndex(0)


    def smsSelectedContact(self):
        self.tab2.smsMobile.setText(self.current_contact_number)
        self.tab2.smsText.setFocus()
        self.tabs.setCurrentIndex(1)


    def deleteContact(self):
        query = QSqlQuery(db)
        query.exec_("DELETE FROM contact WHERE mobile LIKE \""+self.current_contact_number+"\"")
        self.listContacts()


    def deleteSMS(self):
        query = QSqlQuery(db)
        query.exec_("DELETE FROM sms WHERE received_at LIKE \""+self.current_sms_timestamp+"\"")
        self.listSMSs()


    def saveNewContact(self):
        name = self.tab3.newContactName.text().title()
        nameClean = re.sub(r'[^A-Za-z ]', '', name)
        mobile = self.tab3.newContactMobile.text()
        mobileClean = re.sub(r'[^0-9]', '', mobile)
        if (len(nameClean) < 1):
            self.alert("Name to short")
        else:
            if (len(mobileClean) < 11):
                self.alert("Number to short")
            else:
                query = QSqlQuery(db)
                query.exec_("INSERT INTO contact (name,mobile) VALUES (\""+nameClean+"\",\""+mobileClean+"\")")
                self.listContacts()
                self.tab3.newContactName.setText("")
                self.tab3.newContactMobile.setText("")
                self.alert("Contact saved")


    def dialNumber(self,num):
        self.dialling = self.dialling + num;
        self.refreshScreen;


    def greenPhone(self):
        if (self.call_state == "incoming"):
            self.writeToSerial("ATA")
        if (len(self.dialling) > 10):
            self.tab1.label.setText("Dialling "+self.dialling+"...")
            self.writeToSerial("ATD+"+self.dialling+";")
            self.hearPhoneAudio(True)
            self.call_state = "outgoing"


    def redPhone(self):
        self.dialling = ""
        self.call_state = ""
        self.tab1.btnGreenPhone.setEnabled(False)
        self.tab1.btnRedPhone.setEnabled(False)
        self.tab1.btnRedPhone.setText("Hang up")
        self.tab1.btnGreenPhone.setText("Answer")
        self.writeToSerial("AT+CHUP")


    def hearPhoneAudio(self,on):
        if (not testing):
            if (on):
                pi.write(audio_changeover_rpi_pin,1)
            else:
                pi.write(audio_changeover_rpi_pin,0)


    def takePhoto(self):
        thetime = QDateTime.currentDateTime()
        time_stamp = thetime.toString('yyyyMMdd-hhmmss')
        os.system("libcamera-still -o photo-"+time_stamp+".jpg --qt-preview")


    def toggleGPS(self,on):
        if (on):
            self.writeToSerial("AT+CGPS=1")
            self.gps_active = True
        else:
            self.writeToSerial("AT+CGPS=0")
            self.gps_active = False


    def sendSMS(self):
        message = self.tab2.smsText.toPlainText()
        mobile = self.tab2.smsMobile.text()
        if (len(message) < 1):
            self.alert("Message is too short")
        else:
            if (len(mobile) < 11):
                self.alert("Number to short")
            else:
                #query = QSqlQuery(db)
                #query.exec_("INSERT INTO contact (name,mobile) VALUES (\""+nameClean+"\",\""+mobileClean+"\")")
                time.sleep(0.5)
                mobile = "+" + mobile
                self.writeToSerial('ATZ')
                time.sleep(0.5)
                self.writeToSerial('AT+CMGF=1')
                time.sleep(0.5)
                self.writeToSerial('AT+CMGS="' + mobile + '"')
                time.sleep(0.5)
                self.writeToSerial(message)
                time.sleep(0.5)
                #self.writeToSerial(str(bytes([26])))
                ser.write(bytes([26]))
                time.sleep(0.5)
                self.tab2.smsMobile.setText("")
                self.tab2.smsText.setPlainText("")
                self.alert("SMS sent")

    def alert(self,msgText):
        msgBox = QMessageBox()
        msgBox.setText(msgText)
        msgBox.exec()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=WinForm()
    #form.adjustSize();
    #form.move(QApplication::desktop()->screen()->rect().center() - widget.rect().center());
    form.show()
    sys.exit(app.exec_())
