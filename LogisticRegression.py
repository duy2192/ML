from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from sklearn.metrics import accuracy_score
from tkinter import Menu
from tkinter import filedialog as fd
from MyLogisticRegression import MyLogisticRegression

dataTrain = pd.read_csv('data_train.csv')
yTrain = dataTrain['ketqua'].to_numpy()
xTrain = dataTrain.drop(['ketqua'], axis=1).to_numpy()
LR = LogisticRegression(max_iter=1000,fit_intercept=TRUE) ##Dùng Thư Viện sklearn
# LR = MyLogisticRegression() ##Tự code thuật toán
LR.fit(xTrain, yTrain)
print("w=", LR.coef_)
print("bias=", LR.intercept_)

def predictY(xTest):
    return LR.predict(xTest)


def validateEntry(inp):
    try:
        if(inp != ""):
            data = float(inp)
            if(data > 10 or data < 0):
                return False
    except:
        return False
    return True


def handleBtnClearClick():
    txtX1.delete(0, END)
    txtX2.delete(0, END)
    txtX3.delete(0, END)
    txtX4.delete(0, END)
    txtX5.delete(0, END)
    txtX6.delete(0, END)
    txtX7.delete(0, END)
    txtX8.delete(0, END)
    txtX9.delete(0, END)
    labelPred.configure(text='', background="#273c75")

    return


def handleBtnPredictClick():
    try:
        x1 = txtX1.get()
        x2 = txtX2.get()
        x3 = txtX3.get()
        x4 = txtX4.get()
        x5 = txtX5.get()
        x6 = txtX6.get()
        x7 = txtX7.get()
        x8 = txtX8.get()
        x9 = txtX9.get()
        x1 = -1 if x1 == '' else float(x1)
        x2 = -1 if x2 == '' else float(x2)
        x3 = -1 if x3 == '' else float(x3)
        x4 = -1 if x4 == '' else float(x4)
        x5 = -1 if x5 == '' else float(x5)
        x6 = -1 if x6 == '' else float(x6)
        x7 = -1 if x7 == '' else float(x7)
        x8 = -1 if x8 == '' else float(x8)
        x9 = -1 if x9 == '' else float(x9)
        xTest = np.array([[x1, x2, x3, x4, x5, x6, x7, x8, x9]])
        predict = predictY(xTest)
        if(x1 == -1 and x2 == -1 and x3 == -1 and x4 == -1 and x5 == -1 and x6 == -1 and x7 == -1 and x8 == -1 and x9 == -1):
            handleBtnClearClick()
            messagebox.showwarning("Warning!", "Chưa nhập dữ liệu!")
        else:
            if(predict == 1):
                predict = "Đỗ!"
                labelPred.configure(background="#20bf6b")
            else:
                predict = "Trượt!"
                labelPred.configure(background="#eb3b5a")
            labelPred.configure(text="Kết quả: " + str(predict))
    except Exception as e:
        print(e)
        messagebox.showerror("Error!", "Lỗi!")
    return


def handleCloseTestWindow():
    root.deiconify()
    testWindow.withdraw()


def btnHandleTest():
    try:

        filename = fd.askopenfilename()
        if(filename == ''):
            return
        if(filename.split(".")[-1] == "csv"):

            dataTest = pd.read_csv(filename)
            yTest = dataTest['ketqua'].to_numpy()
            xTest = dataTest.drop(['ketqua'], axis=1).to_numpy()
            
            yPredict = LR.predict(xTest)

            result = np.concatenate(
                (xTest, np.array([yTest]).T, np.array([yPredict]).T), axis=1)
            style.configure('Treeview', rowheight=30, height=result.shape[1])
            tbl.tag_configure('styleRow', font=("Arial", 12))
            tbl.delete(*tbl.get_children())

            for i, value in enumerate(result):
                tbl.insert('', 'end', values=np.append(
                    i+1, value).tolist(), tags=('styleRow'))

            count = 0
            for i in range(len(yPredict)):
                if(yPredict[i] == yTest[i]):
                    count = count + 1
            rate = accuracy_score(yTest, yPredict) * 100

            labelRes.configure(text="Số dự đoán đúng : " + str(count) + " trên tổng " + str(len(
                yPredict)) + ' --- Đạt tỷ lệ chính xác : ' + str(rate) + '%', fg="#2ecc71")
            labelRes.pack(fill=X, pady=10)
            root.withdraw()
            testWindow.deiconify()

        else:
            messagebox.showwarning("ALert!", "Cần đúng định dạng file .csv!")

    except Exception as e:
        messagebox.showerror("Error!", "Lỗi!")
        print(e)
        return


root = Tk()

root.title("Logistic_Regression")
root.minsize(920, 800)
root.geometry('%dx%d+%d+%d' % (950, 800, (root.winfo_screenwidth()/2) -
                               (425), (root.winfo_screenheight()/2) - (400)))
root.configure(background="#273c75")
menubar = Menu(root)
root.config(menu=menubar)
mode_menu = Menu(menubar, tearoff=0)

mode_menu.add_command(
    label='Test',
    command=btnHandleTest,
)

mode_menu.add_command(
    label='Exit',
    command=root.destroy,
)

menubar.add_cascade(
    label="Mode",
    menu=mode_menu
)

header = Label(root, text="Hồi Quy Logistic", fg="#9c88ff",
               font=("Helvetica  ", 25, "bold"), bg="#273c75")
header.pack(pady=40)

frame1 = Frame(root, background="#273c75")
frame1.pack(fill=X, padx=50, pady=30)

labelX1 = Label(frame1, text="Toán", fg="#9c88ff",
                font=("Arial  ", 15), bg="#273c75")
labelX1.pack(side=LEFT, padx=0, pady=0, anchor=NE)

txtX1 = Entry(frame1, width=5, font=("Arial  ", 15), validate='key', vcmd=(
    root.register(validateEntry), '%P'), background="#f1f2f6")
txtX1.pack(side=LEFT, padx=102, pady=0, anchor=NE)

txtX2 = Entry(frame1, width=5, font=("Arial  ", 15), validate='key', vcmd=(
    root.register(validateEntry), '%P'), background="#f1f2f6")
txtX2.pack(side=RIGHT, padx=0, pady=0, anchor=NE)

labelX2 = Label(frame1, text="Ngữ Văn", fg="#9c88ff",
                font=("Arial  ", 15), bg="#273c75")
labelX2.pack(side=RIGHT, padx=50, pady=0, anchor=NE)

frame2 = Frame(root, background="#273c75")
frame2.pack(fill=X, padx=50, pady=30)

labelX3 = Label(frame2, text="Ngoại Ngữ", fg="#9c88ff",
                font=("Arial  ", 15), bg="#273c75")
labelX3.pack(side=LEFT, padx=0, pady=0, anchor=NE)

txtX3 = Entry(frame2, width=5, font=("Arial  ", 15), validate='key', vcmd=(
    root.register(validateEntry), '%P'), background="#f1f2f6")
txtX3.pack(side=LEFT, padx=40, pady=0, anchor=NE)


txtX4 = Entry(frame2, width=5, font=("Arial  ", 15), validate='key', vcmd=(
    root.register(validateEntry), '%P'), background="#f1f2f6")
txtX4.pack(side=RIGHT, padx=0, pady=0, anchor=NE)

labelX4 = Label(frame2, text="Vật Lý", fg="#9c88ff",
                font=("Arial  ", 15), bg="#273c75")
labelX4.pack(side=RIGHT, padx=50, pady=0, anchor=NE)


frame3 = Frame(root, background="#273c75")
frame3.pack(fill=X, padx=50, pady=30)

labelX5 = Label(frame3, text="Hóa Học", fg="#9c88ff",
                font=("Arial  ", 15), bg="#273c75")
labelX5.pack(side=LEFT, padx=0, pady=0, anchor=NE)

txtX5 = Entry(frame3, width=5, font=("Arial  ", 15), validate='key', vcmd=(
    root.register(validateEntry), '%P'), background="#f1f2f6")
txtX5.pack(side=LEFT, padx=65, pady=0, anchor=NE)

txtX6 = Entry(frame3, width=5, font=("Arial  ", 15), validate='key', vcmd=(
    root.register(validateEntry), '%P'), background="#f1f2f6")
txtX6.pack(side=RIGHT, padx=0, pady=0, anchor=NE)

labelX6 = Label(frame3, text="Sinh Học", fg="#9c88ff",
                font=("Arial  ", 15), bg="#273c75")
labelX6.pack(side=RIGHT, padx=50, pady=0, anchor=NE)


frame4 = Frame(root, background="#273c75")
frame4.pack(fill=X, padx=50, pady=30)

labelX7 = Label(frame4, text="Lịch Sử", fg="#9c88ff",
                font=("Arial  ", 15), bg="#273c75")
labelX7.pack(side=LEFT, padx=0, pady=0, anchor=NE)

txtX7 = Entry(frame4, width=5, font=("Arial  ", 15), validate='key', vcmd=(
    root.register(validateEntry), '%P'), background="#f1f2f6")
txtX7.pack(side=LEFT, padx=75, pady=0, anchor=NE)

txtX8 = Entry(frame4, width=5, font=("Arial  ", 15), validate='key', vcmd=(
    root.register(validateEntry), '%P'), background="#f1f2f6")
txtX8.pack(side=RIGHT, padx=0, pady=0, anchor=NE)

labelX8 = Label(frame4, text="Địa Lý", fg="#9c88ff",
                font=("Arial  ", 15), bg="#273c75")
labelX8.pack(side=RIGHT, padx=50, pady=0, anchor=NE)

frame5 = Frame(root, background="#273c75")
frame5.pack(fill=X, padx=50, pady=30)


txtX9 = Entry(frame5, width=5, font=("Arial  ", 15), validate='key', vcmd=(
    root.register(validateEntry), '%P'), background="#f1f2f6")
txtX9.pack(side=RIGHT, padx=0, pady=0, anchor=NE)

# labelScore=Label(frame5,text="Độ chính xác: "+str(round(LR.score(xTrain, yTrain)*100))+"%", font=("Arial  ", 15), background="#273c75",fg="#2ecc71")
# labelScore.pack(side=LEFT, padx=0, pady=0, anchor=NE)


labelX9 = Label(frame5, text="GDCD", fg="#9c88ff",
                font=("Arial  ", 15), bg="#273c75")
labelX9.pack(side=RIGHT, padx=50, pady=0, anchor=NE)


frame6 = Frame(root, background="#273c75")
frame6.pack(fill=X, padx=50, pady=30)

btnClear = Button(frame6, text="Xóa", borderwidth=5, font=('Arial', 15, 'bold'),
                  foreground='#ecf0f1', background="#b2bec3", relief="solid", command=handleBtnClearClick)
btnClear.pack(side=LEFT, padx=0, pady=20)

btnPred = Button(frame6, text="Dự đoán", borderwidth=5, font=('Arial', 15, 'bold'),
                 foreground='#ecf0f1', background="#3498db", relief="solid", command=handleBtnPredictClick)
btnPred.pack(side=LEFT, padx=20, pady=20)

labelPred = Label(frame6, text="", fg="#ecf0f1",
                  font=("Arial", 20, 'bold'), bg="#273c75")
labelPred.pack(side=RIGHT, padx=0, pady=20)

#-------------------------------------------------------------------------------------------------------------#
testWindow = Toplevel(root)
testWindow.geometry("1000x800")
testWindow.title("Test")
testWindow.minsize(1000, 700)
testWindow.geometry('%dx%d+%d+%d' % (1200, 800, (testWindow.winfo_screenwidth()/2) -
                                     (600), (testWindow.winfo_screenheight()/2) - (400)))
testWindow.configure(background="#273c75")
testWindow.withdraw()
testWindow.protocol("WM_DELETE_WINDOW", handleCloseTestWindow)

framehead = Frame(testWindow, background="#273c75")
framehead.pack(fill=X)
frameTbl = Frame(testWindow, background="#273c75")
frameTbl.pack(fill=X)
style = ttk.Style(testWindow)
frameResult = Frame(testWindow, background="#273c75")
frameResult.pack(fill=X)
labelTest = Label(framehead, text="Kiểm tra",  fg="#9c88ff", font=(
    "Helvetica  ", 25, "bold"), background="#273c75")
labelTest.pack(pady=40)
btnChangeFile = Button(framehead, text="Chọn File", borderwidth=5, font=('Arial', 10, 'bold'),
                       foreground='#ecf0f1', background="#34495e", relief="solid", command=btnHandleTest)
btnChangeFile.pack(padx=0, pady=30, anchor=N)
tbl = ttk.Treeview(frameTbl, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9,
                                      10, 11, 12, 13), show="headings")
labelTestRes = Label(frameResult, text="Kết quả",  fg="#9c88ff", font=(
    "Helvetica  ", 20, "bold"), background="#273c75")
labelTestRes.pack(fill=X, pady=20)
labelRes = Label(frameResult,  fg="#9c88ff", font=(
    "Helvetica  ", 15), background="#273c75")
style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
tbl.pack(anchor=N)
tbl["displaycolumns"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)


tbl.column(1, width=90, minwidth=80, stretch=YES)
tbl.column(2, width=90, minwidth=80, stretch=YES)
tbl.column(3, width=90, minwidth=80, stretch=YES)
tbl.column(4, width=90, minwidth=80, stretch=YES)
tbl.column(5, width=90, minwidth=80, stretch=YES)
tbl.column(6, width=90, minwidth=80, stretch=YES)
tbl.column(7, width=90, minwidth=80, stretch=YES)
tbl.column(8, width=90, minwidth=80, stretch=YES)
tbl.column(9, width=90, minwidth=80, stretch=YES)
tbl.column(10, width=90, minwidth=80, stretch=YES)
tbl.column(11, width=90, minwidth=80, stretch=YES)
tbl.column(12, width=90, minwidth=80, stretch=YES)
tbl.heading(1, text="STT")
tbl.heading(2, text="Toán")
tbl.heading(3, text="Ngữ Văn")
tbl.heading(4, text="Ngoại Ngữ")
tbl.heading(5, text="Vật Lý")
tbl.heading(6, text="Hóa Học")
tbl.heading(7, text="Sinh Học")
tbl.heading(8, text="Lịch Sử")
tbl.heading(9, text="Địa Lý")
tbl.heading(10, text="GDCD")
tbl.heading(11, text="Kết Quả")
tbl.heading(12, text="Dự Đoán")


root.mainloop()
