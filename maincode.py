import tkinter as tk 
from tkinter import ttk,messagebox,filedialog
from tkinter.messagebox import showinfo
from PIL import ImageFont,Image,ImageDraw,ImageTk
import pytesseract
import numpy as np
import textwrap




#global variable 
param_inputs = []

#list will be appended with all the necessary parameters(file type,file address/text,handwriting font,pdf output response)
def set_variables_filename(inputs:str):
    param_inputs.append(inputs)





#---------------------------
#all functions regarding gui
#---------------------------



#creating class for all gui created by tkinter 
#class takes argument to initialize root window
class App(tk.Tk):
    def __init__(self):

        #avoids referring to base class
        super().__init__()

        #creating first window where user will be asked to select input form
        self.title('SELECT INPUT FORM')
        self.geometry('600x400')
        self.label = ttk.Label(self, text="\n\nSelect Your Input Form\n\n",width=20,font=("bold", 20))
        self.label.pack()

        #variable v will store user's input
        self.v=tk.StringVar(value=' ')
        self.rbutton1 = tk.Radiobutton(self, text='  TEXT', variable=self.v, value='text').pack(anchor='w')
        self.rbutton2=tk.Radiobutton(self, text='  TEXTFILE', variable=self.v, value='textfile').pack(anchor='w')
        self.rbutton3=tk.Radiobutton(self, text='  IMAGE', variable=self.v, value='image').pack(anchor='w')

        #command will call function button_clicked
        self.button1=tk.Button(self, text='Submit',width=20,bg='brown',fg='white',command=self.button_clicked).pack()




    def button_clicked(self):

        #ans will extract the user input from variable v and will be appended to global variable
        ans=(self.v.get())

        #if the input is appropriate the function will procide
        if ans=='text' or ans=='image' or ans=='textfile':
            set_variables_filename(str(ans))

            #the window closes
            self.destroy()

            #depending on user's input different window is creating asking to enter text/select the file
            if ans=='textfile' or ans=='image':
                super().__init__()
                self.title('Tkinter Open File Dialog')
                self.geometry('600x400')

                #command will call button_clicked2_img_file function
                self.button2 = ttk.Button(self,text='Open a File',command=self.button_clicked2_img_file).pack(expand=True)
            
        
            else:
                super().__init__()
                self.title('Tkinter Enter Text')
                self.geometry('600x400')
                l1 = ttk.Label(self, text="\n\n  ENTER YOUR TEXT HERE:\n\n\n", width=15,font=("bold", 15))
                l1.pack(fill='x')
                self.entry=tk.StringVar()
                self.entry = ttk.Entry(self,width=40)
                self.entry.pack()

                #command will call button_clicked2_txt function
                self.button3 = ttk.Button(self,text='Submit',command=self.button_clicked2_txt).pack(expand=True)


        #errormessage function will be called if wrong input is given  
        else:
            self.errormessage()

            

    

    #will store the file address in a variable and will append that value to param_inputs(global variable)
    def button_clicked2_img_file(self):
        filetypes = (('text files', '*.txt'),('All files', '*.*'),('image' , '.jpg .png .jpeg .pjp'))
        filename = filedialog.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
        showinfo(title='Selected File',message=filename)
        filename_input = filename
        set_variables_filename(filename)

        #calls function handwriting_input
        self.handwriting_input()




    #will append the text entered by user into gloabal variable param_inputs       
    def button_clicked2_txt(self):
        text=self.entry.get()

        #check if input provided is valid or not
        if bool(text)==False or text.isspace():
            self.errormessage()
        
        else:
            txt_input = text
            set_variables_filename(str(text))

            #calls function handwriting_input
            self.handwriting_input()




    #closes the previous window and creates a new window asking for handwriting style while displaying all the options and font style
    def handwriting_input(self):
        self.destroy()
        super().__init__()
        self.title('Choose handwriting style')
        self.geometry('900x700')

        #displays the image showing all font stlyes
        img = Image.open('hwsample.jpg')
        img = img.resize((1400, 500), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        panel = ttk.Label(self, image=img)
        panel.image = img
        panel.pack()

        #creates a drop down menu for user to select handwriting style
        hw_options_list = ["Handwriting 1", "Handwriting 2", "Handwriting 3", "Handwriting 4","Handwriting 5"]
        self.handwriting_no = tk.StringVar()
        dropdown = ttk.OptionMenu(self,self.handwriting_no,"Select an option",*hw_options_list)
        dropdown.config(width=25)
        dropdown.pack()

        #command calls button_clicked3 function
        self.button3=tk.Button(self, text='Submit',width=20,bg='brown',fg='white',command=self.button_clicked3).pack()




    #appends the users input of handwriting style in param_inputs and asks user if they want output in pdf and store the reply in the list
    def button_clicked3(self):
        hw=self.handwriting_no.get()

        #checks if handwrirting option is selected or not
        if hw=='Select an option':
            self.errormessage()

        else:
            handwriting_input=hw
            set_variables_filename(str(hw))
            pdforwhatinput=tk.StringVar()
            pdforwhat=messagebox.askyesno("askyesno", "Do you want the output in pdf?")
            messagebox.showinfo('OUTPUT', 'Your output is stored in output folder')
            set_variables_filename(pdforwhat)
            self.destroy()
        
        
    

    #function to declare warning when input is not appropriate
    def errormessage(self):
        message_respond=messagebox.showwarning("WARNING!!!", "You didn't provided any valid input")

        




#-------------------------------------------------------
#all function used to convert text into handwritten font 
#-------------------------------------------------------




#function converts the output images into pdf
#function takes the list of address of output images as argument
def img2pdf(addresslist):
    
    #open each output image and converts it into rgb
    openl=[Image.open(i) for i in addresslist]
    imagelist=[im.convert('RGB') for im in openl]
    im=imagelist[0]
    
    #appending the list of images into the pdf
    im.save('output\HWoutput.pdf',save_all=True,append_images=imagelist[1:])



#function extracts text from an input image
#takes the filelocation as input
def img2text(filename):
    img1 = np.array(Image.open(filename))
    
    #using tesseract tool to extract text with the help of numpy array
    #enter the location of tesseract below on your system
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(img1)
    return text



#function extracts text from a textfile
#takes filelocation as input
def textfile2text(filename):
    file=open(filename,encoding="utf-8")
    text=file.readlines()
    return text



    

#-------------------------------------------------------                             
#main program body where all the function calling occurs    
#-------------------------------------------------------
    

        


if __name__ == "__main__":
    print('hello')

    #the class is called and therefore the gui gets displayed
    app = App()
    app.mainloop()

    #using the values stores in global variable accordingly
    ans=param_inputs[0]
    if ans=='image':
        filename=param_inputs[1]
        text=img2text(filename)
        
    elif ans=='text':
        text=param_inputs[1]

    elif ans=='textfile':
        filename=param_inputs[1]
        
        text=textfile2text(filename)

    #empty list that will later store output image address
    adlst=[]

    while text:
        
        hs=param_inputs[2]

        #storing font into variable according to useres choice
        #storing data related to font into a list
        if hs=='Handwriting 1':
            a='handwritings\HW1.ttf'

            #contains 4 values as [handwriting_no,font_size,maxchar_in_single_line,max_no_of_lines]
            hwinpt=[1,35,153,24]
        elif hs=='Handwriting 2':
            a='handwritings\HW2.ttf'
            hwinpt=[2,40,154,25]                                                    
        elif hs=='Handwriting 3':                                                                 
            a='handwritings\HW3.ttf' 
            hwinpt=[3,37,178,25]                                                   
        elif hs=='Handwriting 4':                                                                 
            a='handwritings\HW4.ttf'                                                
            hwinpt=[4,30,149,31]
        elif hs=='Handwriting 5':
            a='handwritings\HW5.ttf'
            hwinpt=[5,55,120,27]
        
        
        #creating blank img to write on with user picked font
        image = Image.new(mode='RGB', size=(1920,1080), color='#ffffff')
        print(a)
        font = ImageFont.truetype(font=a, size=hwinpt[1])

        
        #string that will store modified format style so that text could fit on img
        txt=""      
        for i in text:

            #breaking lines accordingly to fit text on img
            if len(i)>hwinpt[2]:
                txt+=textwrap.fill(text=i, width=hwinpt[2])
                txt+='\n'
            else:
                txt+=i
        
        
        #var that will store total number of output img
        imgno=0

        #will store no of lines printed on 1 img
        linecounter=0

        #will store text printed of 1 img
        text1page=""
        txtlst=txt.split("\n")
        for i in txtlst:
            text1page+=i
            text1page+='\n'
            linecounter+=1

            #check max no of lines in 1 img and creates new img acoordingly
            if linecounter>=hwinpt[3] :
                imgno+=1
                image = Image.new(mode='RGB', size=(1920,1080), color='#ffffff')
                draw = ImageDraw.Draw(im=image)
                draw.text(xy=(10, 10), text=text1page, font=font, fill='black', align='left')

                #saving images in output folder and storing their address in adlst


                image.save('output\img'+str(imgno)+'.png')
                
                adlst.append('output\img'+str(imgno)+'.png')
                text1page=""
                linecounter=0
        
        #prints the remaing lines that were left. Works only if loop executed properly
        else:
            imgno+=1
            image = Image.new(mode='RGB', size=(1920,1080), color='#ffffff')
            draw = ImageDraw.Draw(im=image)
            draw.text(xy=(10, 10), text=text1page, font=font, fill='black', align='left')

            #saving images in output folder and storing their address in adlst
            image.save('output\img'+str(imgno)+'.png') 
            adlst.append('output\img'+str(imgno)+'.png')
            

        
        break


    #option to convert output into images
    pdforwhat=param_inputs[3]
    if pdforwhat==True:
        img2pdf(adlst)
