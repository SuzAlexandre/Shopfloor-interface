import sys
#import pyodbc
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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
        mainLayout=QVBoxLayout()
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
        #self.Info_output.setMinimumHeight(20)

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
        self.part_type_list=QComboBox(self)
        for cmt in range(10):
            self.part_type_list.addItem("Part type "+str(cmt))
        self.part_type_list_hand=QComboBox(self)
        self.part_type_list_hand.addItems(['LH','RH'])
        self.scrap_001_Hbox.addWidget(self.part_type_list)
        self.scrap_001_Hbox.addWidget(self.part_type_list_hand)

        # Adding cavity selection
        self.cavity_list_text=QLabel("Select cavity number:")
        self.cavity_list=QComboBox(self)
        for cmt in range(10):
            self.cavity_list.addItem("Cavity "+str(cmt))

        # Adding equipment selection (where scrap found)
        self.eq_select_list_text=QLabel("Select equipment:")
        self.eq_select_list=QComboBox(self)
        for cmt in range(10):
            self.eq_select_list.addItem("Machine "+str(cmt)) 

        # Adding production date pick
        self.scrap_tab_production_date_text=QLabel("Select production date:")
        self.scrap_tab_production_date=QDateEdit(calendarPopup=True)
        self.scrap_tab_production_date.setDateTime(QDateTime.currentDateTime())

        # Adding layout for area selection
        area_select_layout=QGridLayout()
        self.area_select_text=QLabel("Select defect area")

        # adding background image
        test_frame=QFrame()
        test_frame.resize(500,800)
        #test_frame.setStyleSheet('background-color: rgb(200, 255, 255)')
        test_frame.setStyleSheet('background-image: url(test_bg.jpg);')
        
        test_frame.mousePressEvent = self.getPos
        area_select_layout.addWidget(test_frame,0,0,5,5)

        # declare array of buttons
        #scrap_area_buttons={}

        # adding selection buttons
        #for i_row in range(5):
        #    for i_col in range(5):
                
                # keep a reference to the buttons
                #scrap_area_buttons[(i_row, i_col)] = QPushButton('%d / %d' % (i_row, i_col))
                # add to the layout
                #area_select_layout.addWidget(scrap_area_buttons[(i_row, i_col)], i_row, i_col)
                
                #scrap_area_buttons[(i_row, i_col)].setStyleSheet("background-color: rgba(33,33,33,10)")

                # scrap_area_buttons[(i_row, i_col)].mousePressEvent.connect(self.getPos)

                # link to button function
                #cmd_str='self.Butt_'+ str(i_row) + str(i_col)+'.clicked.connect(lambda: self.scrapArea(' + str(i_row)+',' + str(i_col) +'))'
                #cmd_str='self.Butt_'+ str(i_row) + str(i_col)+'.clicked.connect(self.scrapArea(' + str(i_row)+',' + str(i_col) +'))'
                #exec(cmd_str)

        #self.Butt_00.clicked.connect(lambda: self.scrapArea(0,0))
        #self.Butt_44.clicked.connect(lambda: self.scrapArea(4,4))
        self.test_label = QLabel(self)
        self.pixmap=QPixmap('img/test_bg.jpeg')
        self.test_label.setPixmap(self.pixmap)

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
        tab2GridLayout.addWidget(self.area_select_text,7,0)
        tab2GridLayout.addLayout(area_select_layout,7,1)
        tab2GridLayout.addWidget(self.test_label,8,1)

        self.tab1.setLayout(tab1GridLayout)
        self.tab3.setLayout(tab2GridLayout)
        #self.tab3.setLayout(gbox)

        mainLayout.addWidget(self.tabs)
        self.setLayout(mainLayout)

        self.show()

    def scrapTabLayout(self):
        # Function to define the scrap tab layout
        print('Test function')


    def btnFunc(self):
        self.text.setText("Button is active")
        sys.exit()

    def DMCFunc(self):
        button.clicked.connect(self.messageBox)


    def messageBox(self):
        # mbox=QMessageBox.question(self,"Warning!!!","Are you sure to exit?",QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,QMessageBox.No)
        # if mbox==QMessageBox.Yes:
        #     sys.exit()
        # elif mbox==QMessageBox.No:
        #     print("You Clicked No Button")
        BarcodeInput = self.DMC_input.text()
        
        # Cleanup text input
        # BarcodeInput = BarcodeInput.strip()

        # self.DMC_input.text = BarcodeInput
        
        if len(BarcodeInput) > 5:
            #res = check_part(conn,BarcodeInput)
            #self.Info_output.setText(str(res[0]))
            self.Info_output.setText('Part results')

            self.Status_text.setText('✔')
            self.Status_text.setStyleSheet('color: green')

            # if res != Null:
            #     self.Status_text.setText('✔')
            #     self.Status_text.setStyleSheet('color: green')

            # print(len(BarcodeInput))
        # mbox=QMessageBox.information(self,"Information","You Logged Out!")

    def getPos(self,event):
        x = event.pos().x()
        y = event.pos().y() 
        print('Button pressed at x: ' + str(x) + ' y:' + str(x))

# Setting up database connection
# def check_part(conn,search_val):
    #cursor = conn.cursor()
    #cursor.execute('select Insert_Time from Laser_marker_printed_PN where DM_Content = ?',search_val)
    
    # Checking cursors sise
    #results=cursor.fetchone()

    # for row in cursor:
    #     results.append(row)
    
    # results.append('end')
#    result = 'Part status'

    #conn.commit()
 #   return results

def main():
    App=QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

#conn = pyodbc.connect(
#"Driver={SQL Server Native Client 11.0};"
#"Server=10.41.32.2;"
#"Database=SZ_001;"
#"Trusted_Connection=yes;"
#)  

if __name__=='__main__':
    main()

# conn.close()