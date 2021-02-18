import sys
import pyodbc
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
from itertools import groupby

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
        self.setGeometry(50,50,800,600)
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
        self.DMC_input.editingFinished.connect(self.analyseDMCInput)

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
        # if laser marked, no need to write production date, otherwise, need
        # define part type, found center, scrap center, scrap type, position of defect and type
        # Adding an horizontal layout that will include vertical layout
        tab2GridLayout=QGridLayout()
        
         # Adding barcode box and status
        self.scrap_tab_DMC_text=QLabel("Barcode:")
        self.scrap_tab_DMC_text.setAlignment(Qt.AlignRight)
        self.scrap_tab_DMC_input=QLineEdit()

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
        self.eq_select_list_text=QLabel("Detected station:")
        self.eq_select_list_text.setAlignment(Qt.AlignRight)
        self.eq_type_select_list=QComboBox(self)
        self.eq_select_list=QComboBox(self)

        equipment_list = get_equipment_list(conn_SCND_SZ)
        equipment_type_list = equipment_list['Equipment type']
        equipment_type_sorted = sorted(equipment_type_list)
        equipment_type_list=[]
 
        for k,g in groupby(equipment_type_sorted):
            equipment_type_list.append(k)

        # self.eq_type_select_list.addItem("")
        self.eq_type_select_list.addItems(equipment_type_list)
        self.eq_type_select_list.currentTextChanged.connect(lambda: self.updateEquipmentNamesList(equipment_list, self.eq_type_select_list.currentText()))
        self.eq_type_select_list.setCurrentIndex(2) #5 is value for casters

        # add an horizontal layout for equipment selection
        scrap_tab_equipment_selection_layout=QHBoxLayout()
        scrap_tab_equipment_selection_layout.addWidget(self.eq_type_select_list)
        scrap_tab_equipment_selection_layout.addWidget(self.eq_select_list)

        # Adding production date pick
        self.scrap_tab_production_date_text=QLabel("Select production date:")
        self.scrap_tab_production_date_text.setAlignment(Qt.AlignRight)
        self.scrap_tab_production_date=QDateEdit(calendarPopup=True)
        self.scrap_tab_production_date.setDateTime(QDateTime.currentDateTime())

        # Adding layout for area selection
        #area_select_layout=QGridLayout()
        self.area_select_text=QLabel("Select defect area")
        self.area_select_text.setAlignment(Qt.AlignCenter)

        # Adding background image
        self.img_label = QLabel(self)
        #self.img_label.mousePressEvent = self.getPos
        
        self.scrap_info_map=[]

        # Create a graphic scene to analyse defect position
        self.graph_scene = QGraphicsScene(self)
        self.graph_view = QGraphicsView(self.graph_scene)
        self.graph_view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.graph_scene.setSceneRect(0,0,200,200)
        self.graph_view.mousePressEvent = self.manageScrapPoints

        self.updateScrapPic(0)
        self.scrap_view=0
        
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

        # Adding remove or add scrap point radio button
        scrap_add_label=QLabel('Select action')
        radio_butt_layout=QVBoxLayout()
        self.scrap_add_dent=QRadioButton('Dent')
        self.scrap_add_porosity=QRadioButton('Porosity')
        self.scrap_add_crack=QRadioButton('Crack')
        self.scrap_add_miss_mach=QRadioButton('Missing machining')
        self.scrap_add_other=QRadioButton('Add defect')
        self.scrap_add_other.setChecked(True)
        self.scrap_radio_rmv=QRadioButton('Remove defect')
        
        # Adding buttons to layout
        radio_butt_layout.addWidget(scrap_add_label)
        # radio_butt_layout.addWidget(self.scrap_add_dent)
        # radio_butt_layout.addWidget(self.scrap_add_porosity)
        # radio_butt_layout.addWidget(self.scrap_add_crack)
        # radio_butt_layout.addWidget(self.scrap_add_miss_mach)
        radio_butt_layout.addWidget(self.scrap_add_other)

        radio_butt_layout.addWidget(self.scrap_radio_rmv)

        # Assign buttons in the grid
        scrap_view_selector_layout.addWidget(self.area_select_text,0,0,1,3)
        scrap_view_selector_layout.addWidget(self.scrap_view_00,2,1) # button / row / col
        scrap_view_selector_layout.addWidget(self.scrap_view_01,2,0)
        scrap_view_selector_layout.addWidget(self.scrap_view_02,1,1)
        scrap_view_selector_layout.addWidget(self.scrap_view_03,2,2)
        scrap_view_selector_layout.addWidget(self.scrap_view_04,3,1)
        scrap_view_selector_layout.addWidget(self.scrap_view_05,4,1)
        scrap_view_selector_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # Create buttons to save to database and reset 
        scrap_add_cancel = QHBoxLayout()
        self.save_scrap_button = QPushButton("Save to database")
        self.save_scrap_reset = QPushButton("Reset")
        self.save_scrap_reset.clicked.connect(self.resetScrapInfo)
        scrap_add_cancel.addWidget(self.save_scrap_reset)
        scrap_add_cancel.addWidget(self.save_scrap_button)
        
        # Setting up grid 2 map
        tab2GridLayout.addWidget(self.scrap_tab_DMC_text,1,0)
        tab2GridLayout.addWidget(self.scrap_tab_DMC_input,1,1)
        tab2GridLayout.addLayout(scrap_tab_equipment_selection_layout,2,1)
        tab2GridLayout.addWidget(self.eq_select_list_text,2,0)
        # tab2GridLayout.addWidget(self.eq_type_select_list,2,1)
        tab2GridLayout.addWidget(self.eq_select_list,2,3)
        tab2GridLayout.addWidget(self.scrap_tab_production_date_text,3,0)
        tab2GridLayout.addWidget(self.scrap_tab_production_date,3,1)
        tab2GridLayout.addWidget(self.part_type_text,4,0)
        tab2GridLayout.addLayout(self.scrap_001_Hbox,4,1)
        tab2GridLayout.addWidget(self.cavity_list_text,6,0)
        tab2GridLayout.addWidget(self.cavity_list,6,1)
        tab2GridLayout.addWidget(self.graph_view,7,1,2,1)
        tab2GridLayout.addLayout(scrap_view_selector_layout,7,2)
        tab2GridLayout.addLayout(radio_butt_layout,7,0)
        tab2GridLayout.addLayout(scrap_add_cancel,9,1)

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

    def analyseDMCInput(self):
        BarcodeInput_cursor = self.DMC_input.selectAll()
        BarcodeInput = self.DMC_input.selectedText()
        
        # Cleanup text input
        BarcodeInput = BarcodeInput.strip()

        # Some special cleanup for Aiways
        if BarcodeInput.find('AIWAYS'):
            BarcodeInput=BarcodeInput.replace(',','%044A')

        self.DMC_input.text = BarcodeInput
        
        if len(BarcodeInput) > 5:
            res = check_part(conn,BarcodeInput)

            if res!=0:
                # Data clean up and formatting
                marking_time = res['Insert Time']
                marking_time = marking_time - datetime.timedelta(microseconds=marking_time.microsecond)

                # Create part info string
                infos = ('Part information:' + '\n' +
                ' SO number: ' + res['SO number'] + '\n Part type: ' + res['Part type'] + ' ' + res['Hand sign'] + 
                '\n\nPart marked at : ' + str(marking_time) + 
                '\n\nCode information:' + '\n Visual content: ' + str(res['Visual content']) +'\n Code level: ' + str(res['Code level']) +'\n Matching level at laser marking: ' + str(res['Matching level']) + 
                '\n\nChemistry information:' + '\n Batch ID: ' + str(res['Batch ID']))
                
                # Reading chemistry results in case they are some
                if res['Chemistry results']!=0:
                    # Store chemisty results
                    chem_res = res['Chemistry results']

                    # Data cleanup and formatting
                    operator_name = str(chem_res['Operator name'])
                    inspector_name = str(chem_res['Inspector name'])

                    chem_infos = ('\n Check at station: ' + chem_res['Preparation line'] + str(chem_res['Preparation station']) +
                    ' at ' + str(chem_res['Insert time']) +
                    '\n Checked by inspector: ' + inspector_name + ' and operator: ' + operator_name +
                    '\n Crucible ID: ' + str(chem_res['Crucible ID']) +
                    '\n Used at caster ' + str(chem_res['Used station']) + ' at :' + str(chem_res['Used time']))
                else: chem_infos =' no batch ID recorded'

                # Reading xray results
                if res['Xray results']!=0:
                    # Store Xray results
                    xray_res = res['Xray results']

                    # Formatting about xray results and check type
                    if xray_res['Part inspection status']==1:
                        xray_validation_char=Ok_char
                    else:
                        xray_validation_char=Nok_char
                   
                    if xray_res['Part validation type']==0:
                        xray_validation_type_str = 'automated'
                    else:
                        xray_validation_type_str = 'manual'

                    # Setting up the info string
                    xray_infos = ('\n\nX-Ray check: \n Inspection done on station ' + str(xray_res['Machine number']) + ' at ' + str(xray_res['Inspection time']) +
                    '\n Inspection results ' + xray_validation_char + 
                    '\n Validation type: ' + xray_validation_type_str)
                else: xray_infos = '\n\nNo Xray information recorded'

                # Reading packing results
                if res['Pack results']!=0:
                    # Store Xray results
                    pack_res = res['Pack results']

                    # Formatting about xray results and check type 
                    process_status = pack_res['Last process status']
                    if process_status!='None':
                        process_status_dic = {0: 'Finished goods', 99: 'In process', 13: 'Blabla 13', 14:'Blabla 13', -1: 'Unknown reference value'}
                        process_status_str = process_status_dic.get(process_status,-1)
                    else: process_status_str = 'Unknown'

                    packing_time = pack_res['Packing time']
                    packing_time = packing_time - datetime.timedelta(microseconds=packing_time.microsecond) 

                    # Setting up the info string
                    pack_infos = ('\n\nPacking information: \n Last packing recorded at station ' + str(pack_res['Station reference']) +
                    '\n Packing time: ' + str(packing_time) +
                    '\n Lot number: ' + str(pack_res['Lot number']) +
                    '\n Most probable layer: ' + str(pack_res['Layer number'])+
                    '\n Last process status: ' + process_status_str)
                else: pack_infos = '\n\n No packing information recorded'

                infos = infos + chem_infos + xray_infos + pack_infos
                
                self.Info_output.setText(infos)

                self.Status_text.setText('✔')
                self.Status_text.setStyleSheet('color: green')
            else:
                self.Info_output.setText('Part not in database')
            # if res != Null:
            #     self.Status_text.setText('✔')
            #     self.Status_text.setStyleSheet('color: green')

    def updateEquipmentNamesList(self,equipment_list, reference_type):
        # Link update fonction to other content update
        equipment_name_list_full=equipment_list['Internal name']
        equipment_type_list_full=equipment_list['Equipment type']
        equipment_ID_list_full=equipment_list['Equipment ID']
        equipment_name_list=[]
            
        cmpt = 0
        for eq in equipment_type_list_full:
            if eq==reference_type:
                equipment_name_list.append(equipment_name_list_full[cmpt])
            cmpt = cmpt+1
        
        self.eq_select_list.clear()
        self.eq_select_list.addItems(equipment_name_list)

    def getPos(self,event):
        x = event.pos().x()
        y = event.pos().y() 
        print('Button pressed at x: ' + str(x) + ' y:' + str(y))

        # test add a red dot
        painter = QPainter(self.pixmap)
        point = QPoint(x,y)
        painter.setPen(QColor(255,0,0,200))
        painter.drawPixmap(point,self.pixmap)
        # painter.drawPoint(x,y)
        
    def updateScrapPic(self,view):
        # Update scrap view number
        self.scrap_view=view
        
        for item in self.graph_scene.items():
            self.graph_scene.removeItem(item)

        
        # setting up the picture path
        picture_path= 'img/part_view_' + str(view) + '.png'

        self.pixmap=QPixmap(picture_path)
        self.pixmap_scaled=self.pixmap.scaledToHeight(250)
        self.pixmap_rescaled=self.pixmap.scaledToHeight(int(self.graph_scene.height()))
        self.scene_backgroung=self.graph_scene.addPixmap(self.pixmap_scaled)
        self.graph_view.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Adding relative scrap points
        for scrap_point in self.scrap_info_map:
            if scrap_point['view']==view:
                ellipse = QGraphicsEllipseItem(0,0,5,5)
                ellipse.setPen(Qt.red)
                ellipse.setBrush(Qt.red)
                ellipse.setPos(scrap_point['x'],scrap_point['y'])
                self.graph_scene.addItem(ellipse)

        # self.img_label.setPixmap(self.pixmap_scaled)
        # self.img_label.setGeometry(0,0,100,300)

    def manageScrapPoints(self,event):
        x = event.x()
        y = event.y()
        
        # read actual view
        view=self.scrap_view

        # will create or delete items according to radio butt
        if not(self.scrap_radio_rmv.isChecked()):
            # Adding new element in the info map and reload the picture
            self.scrap_info_map.append({'view':view, 'x':x,'y':y})
            self.updateScrapPic(view)

        elif self.scrap_radio_rmv.isChecked():
            temp_scrap_map=[]
            for scrap_point in self.scrap_info_map:
                if scrap_point['view']!=view or abs(x-scrap_point['x'])>10 or abs(y-scrap_point['y'])>10:
                    temp_scrap_map.append({'view':scrap_point['view'], 'x':scrap_point['x'],'y':scrap_point['y']})
            self.scrap_info_map[:]=[]
            self.scrap_info_map=temp_scrap_map
            self.updateScrapPic(view)

    def resetScrapInfo(self):
        # Resetting scrap map
        self.scrap_info_map[:]=[]
        self.updateScrapPic(self.scrap_view)

# Checking part status
def check_part(conn,search_val):
    cursor = conn.cursor()
    
    # Searching for marking data
    cursor.execute("select Machine_NO, SO_Number, Hand_Sign ,Part_Type, Insert_Time, Code_Level, Matching_Level, VC_Content, Batch_ID from Laser_marker_printed_PN where DM_content=? ",search_val)

    # Checking cursor size
    row_count = cursor.rowcount

    # If the size is null, will skip the other checks and return results is null
    if row_count==0:
        results=0
    else:
        # Fetching data from cursor
        row = cursor.fetchone()

        # Saving data in local variables
        results = {'Machine number' : row[0], 'SO number' : row[1], 'Hand sign' : row[2], 'Part type' : row[3].strip(), 'Insert Time' : row[4],
        'Code level' : row[5], 'Matching level' : row[6], 'Visual content' : row[7], 'Batch ID' : row[8]}
        
        Batch_ID = row[8]
        # Retrieve batch ID information
        if Batch_ID!='':
            cursor.execute("select line, station, crucible_id, density, temperature, kmold, silicon, titanium, copper, iron, stronium, manganese, magnesium, zinc, insert_time, Used_Station, Used_Time, inspector_name, operator_name from Casting_Chemistry_use where batch_id=?",Batch_ID)
            
            # Checking cursor size
            row_count = cursor.rowcount

            # if no result, will send no information results
            if row_count==0:
                chemistry_results=0
            else:
                # Fetching data from cursor
                row = cursor.fetchone()

                # Putting together results as a dictionary
                chemistry_results = {'Preparation line': row[0], 'Preparation station': row[1],
                    'Crucible ID': row[2],
                    'Density': row[3],'Temperature' : row[4], 'Kmold' : row[5],
                    'Silicon' : row[6], 'Titanium' : row[7], 'Copper' : row[8], 'Stronium' : row[9],
                    'Manganese' : row[10], 'Magnesium' : row[11], 'Zinc' : row[13],
                    'Insert time' : row[14], 'Used station' : row[15], 'Used time' : row[16], 'Inspector name' : row[17], 'Operator name' : row[18]}
        else: # in case we cannot find any Batch ID, need to put chemistry results as 0 
            chemistry_results=0

        # Checking for any XRay information
        cursor.execute("select Inspection_Time, Part_Inspection_Status, Part_Validation_Type, Machine_NO, Program_Code from X_Ray_Inspection_Result where DM_Content = ?",search_val)
        
        # Checking cursor size
        row_count = cursor.rowcount

        # If the size is null, will skip the other checks and return results is null
        if row_count==0:
            xray_results=0
        else:
             # Fetching data from cursor
            row = cursor.fetchone()

            # Putting together results as a dictionary
            xray_results = {'Inspection time': row[0], 'Part inspection status': row[1], 'Part validation type': row[2], 'Machine number': row[3], 'Program code': row[4]}
        
        # Checking for Heat treat information


        # Checking for any packing information
        cursor.execute("select Updated_Time, Insert_Time, Data_Source, LOT_NO, Layer_NO, Last_Process_State from Packing_Station_and_CLPI where DM_Content = ?",search_val)
        
        # Checking cursor size
        row_count = cursor.rowcount

        # If the size is null, will skip the other checks and return results is null
        if row_count==0:
            pack_results=0
        else:
             # Fetching data from cursor
            row = cursor.fetchone()

            # Define the packing time
            if str(row[0])=='None':
                packing_time = row[1]
            else:
                packing_time = row[0]
            print(str(packing_time))

            # Putting together results as a dictionary
            pack_results = {'Packing time': packing_time, 'Station reference': row[2], 'Lot number': row[3], 'Layer number': row[4], 'Last process status': row[5]}

        # Putting together results as a dictionary
        results['Chemistry results'] = chemistry_results
        results['Xray results'] = xray_results
        results['Pack results'] = pack_results

    conn.commit()
    return results

# Get equipment list
def get_equipment_list(conn):
    cursor = conn.cursor()

    #create query string
    cursor.execute('select equipment_ID, description, equipment_type , internal_name from equipment_list')

    # Checking cursor size
    row_count = cursor.rowcount

    # If the size is null, will skip the other checks and return results is null
    if row_count==0:
        results=0
    else:
        
        # Initialize results dictionnary
        results={'Equipment ID':[], 'Description':[], 'Equipment type':[], 'Internal name':[]}

        # Loop in equipment list
        for row in cursor:
            # Saving data in local variables
            results['Equipment ID'].append(row[0])
            results['Description'].append(row[1])
            results['Equipment type'].append(row[2])
            results['Internal name'].append(row[3])
    
    conn.commit()
    return results

# Main application definition
def main():
    App=QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

conn = pyodbc.connect(
"Driver={SQL Server Native Client 11.0};"
"Server=10.41.32.2;"
"Database=SZ_001;"
"Trusted_Connection=yes;")

conn_SCND_SZ = pyodbc.connect(
"Driver={SQL Server Native Client 11.0};"
"Server=10.41.32.4;"
"Database=SZ_001;"
"Trusted_Connection=yes;")

if __name__=='__main__':
    main()

conn.close()