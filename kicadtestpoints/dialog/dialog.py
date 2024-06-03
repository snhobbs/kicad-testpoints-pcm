import wx
import wx.aui
import os
import wx.lib.buttons as buttons
from pathlib import Path


version = "0.1.4"
body = "Choose test points by setting the desired pads 'Fabrication Property' to 'Test Point Pad'."
frame_title = "Test Point Report Export"

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(400, 300))

        self.panel = wx.Panel(self)

        # Get current working directory
        default_file_path = os.path.join(os.getcwd(), "kicad-testpoint-report.csv")

        # File output selector
        file_output_label = wx.StaticText(self.panel, label="File Output:")
        self.file_output_selector = wx.FilePickerCtrl(self.panel, style=wx.FLP_SAVE | wx.FLP_USE_TEXTCTRL, wildcard="CSV files (*.csv)|*.csv", path=default_file_path)

        # Lorem Ipsum text
        lorem_text = wx.StaticText(self.panel, label=body)

        # Buttons
        self.submit_button = buttons.GenButton(self.panel, label="Submit")
        self.cancel_button = buttons.GenButton(self.panel, label="Cancel")
        self.submit_button.SetBackgroundColour(wx.Colour(150, 225, 150))
        self.cancel_button.SetBackgroundColour(wx.Colour(225, 150, 150))
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        # Menu
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        about_menu_item = file_menu.Append(wx.ID_ANY, "&About", "About this application")
        self.Bind(wx.EVT_MENU, self.on_about, about_menu_item)
        menubar.Append(file_menu, "&Menu")
        self.SetMenuBar(menubar)

        # Horizontal box sizer for buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.submit_button, 0, wx.ALL, 5)
        button_sizer.Add(self.cancel_button, 0, wx.ALL, 5)

        # Sizer for layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(file_output_label, 0, wx.ALL, 5)
        sizer.Add(self.file_output_selector, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(lorem_text, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.panel.SetSizer(sizer)
        self.SetMinSize((400, 200))  # Set a minimum width and height for the frame
        self.Layout()

    def on_submit(self, event):
        file_path = self.file_output_selector.GetPath()
        if file_path:
            print("Submitting...")
            print("File Path:", file_path)
            success_dialog = SuccessDialog(self)
            success_dialog.ShowModal()
            success_dialog.Destroy()
            self.Close()
        else:
            failure_dialog = FailureDialog(self)
            failure_dialog.ShowModal()
            failure_dialog.Destroy()

    def on_cancel(self, event):
        print("Canceling...")
        self.Close()

    def on_about(self, event):
        about_dialog = AboutDialog(self)
        about_dialog.ShowModal()
        about_dialog.Destroy()

class AboutDialog(wx.Dialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent, title="About", size=(300, 200))

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        version_text = wx.StaticText(panel, label=f"Version: {version}")
        version_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        message_text = wx.StaticText(panel, label="This application is powered by TheJigsApp.")
        link = wx.StaticText(panel, label="Visit www.thejigsapp.com for more information.")

        message_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        link.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        link.SetForegroundColour(wx.BLUE)
        link.Bind(wx.EVT_LEFT_UP, self.on_url_click)

        sizer.Add(version_text, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(message_text, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(link, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer)

    def on_url_click(self, event):
        wx.LaunchDefaultBrowser("https://www.thejigsapp.com")

class SuccessDialog(wx.Dialog):
    def __init__(self, parent):
        super(SuccessDialog, self).__init__(parent, title="Success", size=(300, 150))

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        success_text = wx.StaticText(panel, label="File created successfully!")
        success_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        sizer.Add(success_text, 0, wx.ALL, 10)

        panel.SetSizer(sizer)

class FailureDialog(wx.Dialog):
    def __init__(self, parent):
        super(FailureDialog, self).__init__(parent, title="Failure", size=(300, 150))

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        failure_text = wx.StaticText(panel, label="Please select a file output path.")
        failure_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        sizer.Add(failure_text, 0, wx.ALL, 10)

        panel.SetSizer(sizer)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, frame_title)
        frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
