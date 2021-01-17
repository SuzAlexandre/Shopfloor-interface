import sys
import pyodbc
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from updateLists import *

# To check to go faster typing: https://www.keybr.com/

# Create some default setup
Ok_char = '✔'
Nok_char = "✘"
Ok_color = 'color: green'
Nok_color = 'color: red'
Default_font = 'Arial' #'Hind'

class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Production interface")
        self.setGeometry(350,150,600,600)
        self.UI()

    def UI(self):
        # Setting up menu bar
        menuBar=QMenuBar()
        
        # Main menu
        menuFile=menuBar.addMenu('Main')
        actionExit=QAction('Exit',self)
        menuFile.addAction(actionExit)

        # Option menu
        menuOption=menuBar.addMenu('Options')
        actionDatabase=QAction('Database connection',self)
        actionLanguage=QAction('Language',self)
        menuOption.addAction(actionDatabase)
        menuOption.addAction(actionLanguage)

        # Help menu
        menuHelp=menuBar.addMenu('Help')
        actionAbout=QAction('About',self)
        menuHelp.addAction(actionAbout)

        # Setting up main layout
        mainLayout=QVBoxLayout()
        mainLayout.addWidget(menuBar)
        self.tabs=QTabWidget()

        tab_names=["Quality check","Packing station","Add scrap", "Downtime event", "Cutting tools change"]

        ## Creating all different tab widgets
        for i in range(1,len(tab_names)+1):
            cmd_str="self.tab" + str(i) + "=QWidget()"    
            exec(cmd_str)
            cmd_str="self.tabs.addTab(self.tab" + str(i) + ',"' + tab_names[i-1] + '")'
            exec(cmd_str)
        
        # Arranging Quality tab layout

        # Adding an horizontal layout that will include vertical layout
        tab1GridLayout=QGridLayout()
        
        # Adding barcode box and status
        self.DMC_text=QLabel("Barcode:")
        self.DMC_text.setAlignment(Qt.AlignRight)
        self.DMC_input=QLineEdit()
        self.DMC_input.editingFinished.connect(self.messageBox)

        self.Status_text=QLabel(Nok_char)
        self.Status_text.setFont(QFont(Default_font,100))
        self.Status_text.setAlignment(Qt.AlignCenter)
        self.Status_text.setStyleSheet(Nok_color)

        self.Info_text=QLabel("Information")
        self.Info_text.setAlignment(Qt.AlignCenter)
        self.Info_output=QLabel("Part status to be displayed here")
        self.Info_output.setWordWrap(True)
        self.Info_output.setStyleSheet("background-color: lightgrey;""border : 2px solid black;")
        self.Info_output.setAlignment(Qt.AlignTop)

        # Adding elements to quality layout
        tab1GridLayout.addWidget(self.DMC_text,1,0)
        tab1GridLayout.addWidget(self.DMC_input,1,1)
        tab1GridLayout.addWidget(self.Status_text,2,1)
        tab1GridLayout.addWidget(self.Info_text,0,2)
        tab1GridLayout.addWidget(self.Info_output,1,2,2,1)

        # setup grid layout size
        tab1GridLayout.setRowStretch(2,1)
        tab1GridLayout.setColumnStretch(0,1)
        tab1GridLayout.setColumnStretch(1,2)
        tab1GridLayout.setColumnStretch(2,3)

        # Arranging Scrap description tab layout
        # Layout description for me first
        # We will need a scan area and one in case no readable marking
        # if laser marked, no need to write produciton date, otherwise, need
        # define part type, found center, scrap center, scrap type, position of defect and type
        # Adding an horizontal layout that will include vertical layout
        tab2GridLayout=QGridLayout()
        
         # Adding barcode box and status
        self.scrap_tab_DMC_text=QLabel("Barcode:")
        self.scrap_tab_DMC_text.setAlignment(Qt.AlignRight)
        self.scrap_tab_DMC_input=QLineEdit()
        self.scrap_tab_DMC_input.editingFinished.connect(self.messageBox)

        # Adding part type selection
        self.scrap_001_Hbox=QHBoxLayout()
        self.part_type_text=QLabel("Select part type:")
        self.part_type_text.setAlignment(Qt.AlignRight)
        self.part_type_list=QComboBox(self)
        for cmt in range(10):
            self.part_type_list.addItem("Part type "+str(cmt))
        self.part_type_list_hand=QComboBox(self)
        self.part_type_list_hand.addItems(['LH','RH'])
        self.scrap_001_Hbox.addWidget(self.part_type_list)
        self.scrap_001_Hbox.addWidget(self.part_type_list_hand)

        # Adding cavity selection
        self.cavity_list_text=QLabel("Select cavity number:")
        self.cavity_list_text.setAlignment(Qt.AlignRight)
        self.cavity_list=QComboBox(self)
        for cmt in range(10):
            self.cavity_list.addItem("Cavity "+str(cmt))

        # Adding station selection (where scrap found)
        self.eq_select_list_text=QLabel("Select station:")
        self.eq_select_list_text.setAlignment(Qt.AlignRight)
        self.eq_select_list=QComboBox(self)
        for cmt in range(10):
            self.eq_select_list.addItem("Machine "+str(cmt)) 

        # Adding production date pick
        self.scrap_tab_production_date_text=QLabel("Select production date:")
        self.scrap_tab_production_date_text.setAlignment(Qt.AlignRight)
        self.scrap_tab_production_date=QDateEdit(calendarPopup=True)
        self.scrap_tab_production_date.setDateTime(QDateTime.currentDateTime())

        # Adding layout for area selection
        area_select_layout=QGridLayout()
        self.area_select_text=QLabel("Select defect area")
        self.area_select_text.setAlignment(Qt.AlignCenter)

        # Adding background image
        self.img_label = QLabel(self)
        self.img_label.mousePressEvent = self.getPos
        self.updateScrapPic(0)
        
        # Adding selection button for scraps
        scrap_view_selector_layout=QGridLayout()
        self.scrap_view_00=QPushButton('●')
        self.scrap_view_00.clicked.connect(lambda: self.updateScrapPic(0))
        self.scrap_view_01=QPushButton('◀ ')
        self.scrap_view_01.clicked.connect(lambda: self.updateScrapPic(1))
        self.scrap_view_02=QPushButton('▲')
        self.scrap_view_02.clicked.connect(lambda: self.updateScrapPic(2))
        self.scrap_view_03=QPushButton('▶')
        self.scrap_view_03.clicked.connect(lambda: self.updateScrapPic(3))
        self.scrap_view_04=QPushButton('▼')
        self.scrap_view_04.clicked.connect(lambda: self.updateScrapPic(4))        
        self.scrap_view_05=QPushButton('◎')
        self.scrap_view_05.clicked.connect(lambda: self.updateScrapPic(5)) 

        # Assign buttons in the grid
        scrap_view_selector_layout.addWidget(self.area_select_text,0,0,1,3)
        scrap_view_selector_layout.addWidget(self.scrap_view_00,2,1) # button / row / col
        scrap_view_selector_layout.addWidget(self.scrap_view_01,2,0)
        scrap_view_selector_layout.addWidget(self.scrap_view_02,1,1)
        scrap_view_selector_layout.addWidget(self.scrap_view_03,2,2)
        scrap_view_selector_layout.addWidget(self.scrap_view_04,3,1)
        scrap_view_selector_layout.addWidget(self.scrap_view_05,4,1)
        
        # Setting up grid 2 map
        tab2GridLayout.addWidget(self.scrap_tab_DMC_text,1,0)
        tab2GridLayout.addWidget(self.scrap_tab_DMC_input,1,1)
        tab2GridLayout.addWidget(self.eq_select_list_text,2,0)
        tab2GridLayout.addWidget(self.eq_select_list,2,1)
        tab2GridLayout.addWidget(self.scrap_tab_production_date_text,3,0)
        tab2GridLayout.addWidget(self.scrap_tab_production_date,3,1)
        tab2GridLayout.addWidget(self.part_type_text,4,0)
        tab2GridLayout.addLayout(self.scrap_001_Hbox,4,1)
        tab2GridLayout.addWidget(self.cavity_list_text,6,0)
        tab2GridLayout.addWidget(self.cavity_list,6,1)
        tab2GridLayout.addWidget(self.img_label,7,1,2,1)
        tab2GridLayout.addLayout(scrap_view_selector_layout,7,0)

        # Creating the maintenance event tab
        # What to add?? 
        # So will put: a start button for the event
        # Selection type
        # A stop time
        # Some later edit possibilities
        # What kind of fix at the end and any potential root cause identification
        # Any to identify what machine?
        # Anything to 





        self.tab1.setLayout(tab1GridLayout)
        self.tab3.setLayout(tab2GridLayout)
        #self.tab3.setLayout(gbox)

        mainLayout.addWidget(self.tabs)
        self.setLayout(mainLayout)

        self.show()

    def scrapTabLayout(self):
        # Function to define the scrap tab layout
        print('From scrapTabLayout function')

    def btnFunc(self):
        self.text.setText("Button is active")
        sys.exit()

    def DMCFunc(self):
        button.clicked.connect(self.messageBox)

    def messageBox(self):
        BarcodeInput = self.DMC_input.text()
        
        # Cleanup text input
        BarcodeInput = BarcodeInput.strip()

        self.DMC_input.text = BarcodeInput
        
        if len(BarcodeInput) > 5:
            res = check_part(conn,BarcodeInput)
            self.Info_output.setText(str(res[0]))
            self.Info_output.setText('Part results')

            self.Status_text.setText('✔')
            self.Status_text.setStyleSheet('color: green')

            # if res != Null:
            #     self.Status_text.setText('✔')
            #     self.Status_text.setStyleSheet('color: green')

    def getPos(self,event):
        x = event.pos().x()
        y = event.pos().y() 
        print('Button pressed at x: ' + str(x) + ' y:' + str(y))
    
    def updateScrapPic(self,view):
        # setting up the picture path
        picture_path= 'img/part_view_' + str(view) + '.png'
        print(picture_path)

        self.pixmap=QPixmap(picture_path)
        self.pixmap_scaled=self.pixmap.scaledToHeight(300)
        self.img_label.setPixmap(self.pixmap_scaled)
        self.img_label.setGeometry(0,0,100,300)

# Setting up database connection
def check_part(conn,search_val):
    cursor = conn.cursor()
    cursor.execute('select caster_name from caster_list')#,search_val)
    
    # Checking cursor size
    #results=cursor.fetchone()
    results=''

    for row in cursor:
        #results.append(row)
        print(row)
    
    results.append('end')

    conn.commit()
    return results

def main():
    App=QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

conn = pyodbc.connect(
"Driver={SQL Server Native Client 11.0};"
"Server=10.41.32.4;"
"Database=SZ_001;"
"Trusted_Connection=yes;")

if __name__=='__main__':
    main()

conn.close()