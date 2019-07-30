import os, getpass, time, re, csv, kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

# try:
#     os.path.getfilsize("")
# except Exception as e:
#     raise
print(getpass.getuser())
Window.size = (350, 325)
start_day = 0
stop_day = 0

class MyGrid(Widget):

    # Default Settings
    def default(self):

        self.startbtn.disabled = False
        self.stopbtn.disabled = True
        self.startentry.text = ""
        self.startentry.disabled = False
        self.stopentry.disabled = False
        self.stopentry.text = ""
        self.activity_dropdown.text = "Choose Activity"
        self.activity_input.text = ""

    # Start Button Event
    def start(self):

        # time tuple
        current_time = get_time()
        global start_day
        start_day = current_time[0]
        hr = current_time[1]
        min = current_time[2]
        sec = current_time[3]
        time_to_str = str(hr).zfill(2) + ":" + str(min).zfill(2) + ":" + str(sec).zfill(2)

        # Validate that hours and minutes are 2-digit numbers
        if re.match("\d{1,2}[\./,`=*+:;\"'\\\-]\d{2}$", self.startentry.text):

            # if hr is 1 or 2 digits
            if len(self.startentry.text) == 4:
                start_entry_hr = self.startentry.text[0]
                start_entry_min = self.startentry.text[2:]
            else:
                start_entry_hr = self.startentry.text[0:2]
                start_entry_min = self.startentry.text[3:]

            # Validate that hours are from 00 to 23
            # Popup error message if not
            if int(start_entry_hr) < 0 or int(start_entry_hr) > 23:
                validate(2)

            # Validate that minutes are from 00 to 59
            # Popup error message if not
            elif int(start_entry_min) < 0 or int(start_entry_min) > 59:
                    validate(3)

            # Add ".00" to end if manually entered and diasable start button and
            #   entry, and enable stop button
            else:

                # if time is between midnight and 1am
                if hr == 0 and int(start_entry_hr) == 12:
                    self.startentry.text = "00." + start_entry_min + ".00"

                # Convert to military time if pm
                elif hr > 12 and int(start_entry_hr) < 12:
                    add12 = int(start_entry_hr) + 12
                    self.startentry.text = str(add12) + "." + start_entry_min + ".00"
                    self.startbtn.disabled = True
                    self.stopbtn.disabled = False
                    self.startentry.disabled = True

                else:
                    self.startentry.text = start_entry_hr.zfill(2) + "." + start_entry_min + ".00"
                    self.startbtn.disabled = True
                    self.stopbtn.disabled = False
                    self.startentry.disabled = True

        # If not manually entered, get current time
        # Disable start button & entrybox
        # Enable stop button
        elif self.startentry.text == "":
            self.startentry.text = time_to_str
            self.startbtn.disabled = True
            self.stopbtn.disabled = False
            self.startentry.disabled = True

        # If validation isn't met, popup error message
        else:
            validate(1)

    # Stop Button Event
    def stop(self):

        # time tuple
        current_time = get_time()
        global stop_day
        stop_day = current_time[0]
        hr = current_time[1]
        min = current_time[2]
        sec = current_time[3]
        time_to_str = str(hr).zfill(2) + ":" + str(min).zfill(2) + ":" + str(sec).zfill(2)

        # Validate that hours and minutes are 2-digit numbers
        if re.match("\d{1,2}[\./,`=*+:;\"'\\\-]\d{2}$", self.stopentry.text):
            if len(self.stopentry.text) == 4:
                stop_entry_hr = self.stopentry.text[0]
                stop_entry_min = self.stopentry.text[2:]
            else:
                stop_entry_hr = self.stopentry.text[0:2]
                stop_entry_min = self.stopentry.text[3:]

            # Validate that hours are from 00 to 23
            # Popup error message if not
            if int(stop_entry_hr) < 0 or int(stop_entry_hr) > 23:
                validate(2)

            # Validate that minutes are from 00 to 59
            # Popup error message if not
            elif int(stop_entry_min) < 0 or int(stop_entry_min) > 59:
                    validate(3)

            # Add ".00" to end if manually entered and diasable start button and
            #   entry, and enable stop button
            else:
                if hr > 12 and int(stop_entry_hr) < 12:
                    add12 = int(stop_entry_hr) + 12
                    self.stopentry.text = str(add12) + "." + stop_entry_min + ".00"
                    self.stopbtn.disabled = True
                    self.stopentry.disabled = True
                else:
                    self.stopentry.text = stop_entry_hr.zfill(2) + "." + stop_entry_min + ".00"
                    self.stopbtn.disabled = True
                    self.stopentry.disabled = True

        # If not manually entered, get current time
        # Disable start button & entrybox
        # Enable stop button
        elif self.stopentry.text == "":
            self.stopentry.text = time_to_str
            self.stopbtn.disabled = True
            self.stopentry.disabled = True

        # If validation isn't met, popup error message
        else:
            validate(1)

    # Submit Button Event
    def submit(self):

        # Checks that start/stop times were entered correctly
        if self.startbtn.disabled != True or self.stopbtn.disabled != True:
            validate(4)

        # Checks if an activity is chosen
        elif (self.activity_dropdown.text == "Choose Activity" and
            self.activity_input.text == ""):
            validate(5)

        else:

            start_hr = self.startentry.text[0:2]
            start_min = self.startentry.text[3:5]
            start_sec = self.startentry.text[6:]

            stop_hr = self.stopentry.text[0:2]
            stop_min = self.stopentry.text[3:5]
            stop_sec = self.stopentry.text[6:]

            # if stop time is in the next day
            if stop_day > start_day:
                stop_hr = str(int(stop_hr) + 24)

            start_tot = ((int(start_hr) * 3600)
                        + (int(start_min) * 60)
                        + int(start_sec))

            stop_tot = ((int(stop_hr) * 3600)
                        + (int(stop_min) * 60)
                        + int(stop_sec))

            tot_sec = stop_tot - start_tot
            tot_hr = tot_sec / 3600

            if tot_sec < 0:
                self.startentry.disabled = False
                self.stopentry.disabled = False
                validate(6)

            else:

                # activity is manually entered, add it to the front of the activities list
                if self.activity_input.text != "":
                    self.activity_dropdown.values.insert(0, self.activity_input.text)
                    print(self.activity_input.text)

                # If chosen from activity dropdown munu
                else:
                    print(self.activity_dropdown.text)

                print("Start:", self.startentry.text)
                print("Stop:", self.stopentry.text)
                print(start_tot, stop_tot, tot_sec, tot_hr, "\n")

                # Resets everthing back to default
                MyGrid.default(self)

class MyApp(App):
    def build(self):
        return MyGrid()

def validate(id):

    # 1: Wrong Format
    # 2: Out of Range - Hours
    # 3: Out of Range - Minutes
    # 4: Start/Stop
    # 5: Activity Empty
    # 6: Negative Time
    if id == 1:
        popup = Popup(title = "Wrong Format",
            content = Label(text = "Please use hh.mm format"),
            size_hint = (None, None),
            size = (250, 100))
        popup.open()

    if id == 2:
        popup = Popup(title = "Out of Range",
            content = Label(text = "Hours must be from 00 to 23"),
            size_hint = (None, None),
            size = (250, 100))
        popup.open()

    if id == 3:
        popup = Popup(title = "Out of Range",
            content = Label(text = "Minutes must be from 00 to 59"),
            size_hint = (None, None),
            size = (250, 100))
        popup.open()

    if id == 4:
        popup = Popup(title = "Start/Stop",
            content = Label(text = "Start/Stop times not entered correctly"),
            size_hint = (None, None),
            size = (300, 100))
        popup.open()

    if id == 5:
        popup = Popup(title = "Activity Empty",
            content = Label(text = "Please choose/enter activity"),
            size_hint = (None, None),
            size = (250, 100))
        popup.open()

    if id == 6:
        popup = Popup(title = "Negative Time",
            content = Label(text = "Total time cannot be negative"),
            size_hint = (None, None),
            size = (250, 100))
        popup.open()

def get_time():
    time_tup = time.localtime(time.time())
    day = time_tup[2]
    hr = time_tup[3]
    min = time_tup[4]
    sec = time_tup[5]
    return (day, hr, min, sec)

if __name__ == "__main__":
    MyApp().run()
