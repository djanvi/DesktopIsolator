#!/usr/bin/python

import gtk
import os,pwd
import sys,string,subprocess,getpass

#get user login name
username = pwd.getpwuid( os.getuid() )[ 0 ]

class PyApp(gtk.Window):


    def __init__(self):
        super(PyApp, self).__init__()

        self.set_title("SSH File System Mounter:")
        self.set_size_request(400, 380)
        self.set_position(gtk.WIN_POS_CENTER)
	self.set_border_width(8)
	self.set_icon_from_file("/usr/share/pixmaps/seahorse/48x48/seahorse-key.png")

        vbox = gtk.VBox(False, 2)
 
	#create table for keeping the icons     
        table = gtk.Table(8, 3, True)
	table.attach(gtk.Label("Which file system, you want to mount ?"),0,3,0,1)
	
	TempButton=gtk.Button("Temp-user")
	TempButton.connect("clicked",self.mount_tempuser)
	table.attach(TempButton,1,2,1,2)
	#open file for reading role names
	passwd = open('/etc/passwd')
	roles=[]
 	i=1
        j=2
	
	#read from a password file and copy roles into roles list
	for line in passwd.readlines():
      		rec = string.splitfields(line, ':')
      		if rec[0].startswith(username+"-"):
			roles.append(rec[0])
	# create buttons and register their events
        for role in roles:
	     rolename=role
             role=gtk.Button(role)
	     role.connect("clicked",self.mount_role,rolename)
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
         gtk.BUTTONS_CLOSE, "Select the role name you want to mount")
 	md.run()
 	md.destroy()
    
    def about_info(self,widget):
	about = gtk.AboutDialog()
        about.set_program_name("Secure It Mounter")
        about.set_version("0.1")
        about.set_copyright("(c) TCS Innovation labs")
        about.set_comments("GUI for mounting  sshfs filesystems ")
        about.set_website("http://www.tcs.com")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("/usr/share/pixmaps/seahorse/48x48/seahorse-key.png"))
        about.set_icon_from_file("/usr/share/pixmaps/seahorse/48x48/seahorse-key.png")
        about.run()
        about.destroy()
    
    def mount_role(self,widget,data):
	username=data+"@localhost"+":"
        mountpoint="/home/"+os.getlogin()+"/Role-"+data.lstrip(os.getlogin()+"-")
	
	if os.path.exists(mountpoint):
		pass
	else:   
		os.mkdir(mountpoint)

	try:
    		retcode = subprocess.call(["sshfs",username,mountpoint])
    	except OSError, e:
    		print >>sys.stderr, "Execution failed:", e
	sys.exit()
       
	    
    def mount_tempuser(self,widget):
	mountpoint="/home/"+os.getlogin()+"/Role-temp-user"

	if os.path.exists(mountpoint):
		pass
	else:
		os.mkdir(mountpoint) # see permissions over here 	
	try:
		retcode = subprocess.call(["sshfs","temp-user@localhost:",mountpoint])
		
	except OSError, e:
  		print >>sys.stderr, "Execution failed:", e
	
	self.destroy()
	
PyApp()
gtk.main()
