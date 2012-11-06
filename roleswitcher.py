#!/usr/bin/python

import gtk
import os,pwd
import sys,string,subprocess,getpass

#get user login name
username=pwd.getpwuid( os.getuid() )[ 0 ]

class PyApp(gtk.Window):


    def __init__(self):
        super(PyApp, self).__init__()

        self.set_title("Role Chooser: "+sys.argv[1])
        self.set_size_request(400, 380)
        self.set_position(gtk.WIN_POS_CENTER)
	self.set_border_width(8)
	self.set_icon_from_file("/usr/share/pixmaps/seahorse/48x48/seahorse-key.png")

        vbox = gtk.VBox(False, 2)
 
	#create table for keeping the icons     
        table = gtk.Table(8, 3, True)
	table.attach(gtk.Label("Which role you want to use ?"),0,3,0,1)
	
	TempButton=gtk.Button("Temp-user")
	TempButton.connect("clicked",self.create_newuser_and_run)
	table.attach(TempButton,1,2,1,2)
	#open file for reading role names
	passwd = open('/etc/passwd')
	roles=[]
 	i=1
        j=2
	
	#read from a password file and copy roles into roles list
	for line in passwd.readlines():
      		rec = string.splitfields(line, ':')
      		if rec[0].startswith(username):
			roles.append(rec[0])
	# create buttons and register their events
        for role in roles:
	     rolename=role
             role=gtk.Button(role)
	     role.connect("clicked",self.run_in_role,rolename)
	     i +=1
	     j +=1
             table.attach(role, 1, 2, i, j)
      
               
	#code to add roles to the table with button method 
       # for role in roles:
        #        i +=1
	#	j +=1
        #	table.attach(gtk.Button(role), 1, 2, i, j)
        
	table.attach(gtk.HSeparator(),0,3,i+1,j+1)
	AboutButton=gtk.Button("About")
	HelpButton=gtk.Button("Help")
	CancelButton=gtk.Button("Cancel")
	

	AboutButton.connect("clicked",self.about_info)		
	HelpButton.connect("clicked",self.Help_needed)
	CancelButton.connect("clicked",gtk.main_quit)	
	
	
	#table.attach(TempButton,	
	table.attach(AboutButton,0,1,i+2,j+2)	
	table.attach(HelpButton,1,2,i+2,j+2)
	table.attach(CancelButton,2,3,i+2,j+2)
   	
        vbox.pack_start(table, True, True, 3)

        self.add(vbox)
        self.connect("destroy", gtk.main_quit)
        self.show_all()
        
    def Help_needed(self,widget):
	md = gtk.MessageDialog(self, 
         gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
         gtk.BUTTONS_CLOSE, "Select the role you want to use to run the application")
 	md.run()
 	md.destroy()
    
    def about_info(self,widget):
	about = gtk.AboutDialog()
        about.set_program_name("Secure It")
        about.set_version("0.1")
        about.set_copyright("(c) TCS Innovation labs")
        about.set_comments("Secure It is a tool to run application with minimum privileges")
        about.set_website("http://www.tcs.com")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("/usr/share/pixmaps/seahorse/48x48/seahorse-key.png"))
        about.set_icon_from_file("/usr/share/pixmaps/seahorse/48x48/seahorse-key.png")
        about.run()
        about.destroy()
    
    def run_in_role(self,widget,data):
	username=data+"@localhost"
	passedargs=""
        if len(sys.argv) >= 2 :
		arguements=sys.argv[1:]
		for arg in arguements :
			passedargs=passedargs+arg+" "

		try:
			#retcode = subprocess.call(["ssh","-tX", username,passedargs])
			retcode = os.system("ssh -ttfX "+username+" "+passedargs)
		except OSError, e:
			print >>sys.stderr, "Execution failed:", e
		self.destroy()
		sys.exit()
        else:
		md =gtk.MessageDialog(self,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                                     gtk.BUTTONS_CLOSE, "\n No Arguements are passed !! \n Exiting ...")
		md.run()
		md.destroy()
		sys.exit()
    
    def create_newuser_and_run(self,widget):
	
	if len(sys.argv) >= 2 :
		try:
			passedargs=""
			arguements=sys.argv[1:]		
			for arg in arguements :
				passedargs=passedargs+arg+" "

    			os.system("gksudo /bin/myuseradd.sh")
			retcode = os.system("ssh -ttfX temp-user@localhost"+passedargs)
			os.system("gksudo userdel --force --remove temp-user") 	
		except OSError, e:
  			print >>sys.stderr, "Execution failed:", e
		
		self.destroy()
	else:
		md =gtk.MessageDialog(self,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                                     gtk.BUTTONS_CLOSE, "\n No Arguements are passed !!\n Exiting ...")
		md.run()
		md.destroy()
		sys.exit()
	
PyApp()
gtk.main()
