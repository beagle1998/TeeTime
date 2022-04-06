

from re import T
import easygui as eg



def time_inputs():
    #return mwf, and time frames
    q = "Enter the days you wish to book"
    t = "Tee_Book"
    o = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    days = eg.multchoicebox(q,t,o)
 
    times = eg.enterbox("What times to book(ex. 11:00am-1:00pm)")

    return days,times.split("-")

def time_convert(t):
    total = []
    for i in t:
        if ":" in i:
            total.append(i)
        total.append(i[:-2]+":00"+i[-2:])
    return total
a,b = time_inputs()
print(a,b)
print(time_convert(b))










but1 = driver.find_element(by = By.ID, value = "page")
    but1 = but1.find_element(by = By.ID, value = "content")
    but1 = but1.find_element(by = By.CLASS_NAME, value = "btn")
    but1.click()
    time.sleep(2)

    bk = driver.find_element(by = By.ID, value = "page")
    bk = bk.find_element(by = By.ID, value = "content")
    bk = bk.find_element(by = By.ID, value = "times")

