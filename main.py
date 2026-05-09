from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import OneLineListItem, TwoLineIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# নতুন লেয়ার (ContentScreen) সহ KV ডিজাইন
KV = '''
ScreenManager:
    LoginScreen:
    DashboardScreen:
    SemesterScreen:
    ContentScreen:

<LoginScreen>:
    name: 'login'
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "30dp"
        md_bg_color: 0.1, 0.1, 0.2, 1

        MDLabel:
            text: "BPI-COMMUNITY"
            halign: "center"
            font_style: "H3"
            bold: True
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDCard:
            size_hint: None, None
            size: "320dp", "300dp"
            pos_hint: {"center_x": .5}
            elevation: 15
            radius: [25, ]
            padding: "25dp"
            orientation: 'vertical'
            spacing: "20dp"

            MDLabel:
                text: "STUDENT LOGIN"
                bold: True
                halign: "center"
                font_style: "H6"

            MDTextField:
                id: login_id
                hint_text: "Admin/Student ID"
                mode: "rectangle"
                icon_right: "account-circle"

            MDRaisedButton:
                text: "LOGIN TO SYSTEM"
                pos_hint: {"center_x": .5}
                size_hint_x: 1
                md_bg_color: 0.1, 0.2, 0.6, 1
                on_release: app.check_login(login_id.text)

<DashboardScreen>:
    name: 'dashboard'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "BPI-COMMUNITY"
            md_bg_color: 0.1, 0.2, 0.6, 1
            left_action_items: [["menu", lambda x: None]]
        ScrollView:
            MDList:
                id: dept_list

<SemesterScreen>:
    name: 'semester_screen'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            id: sem_title
            title: "Semesters"
            md_bg_color: 0.1, 0.2, 0.6, 1
            left_action_items: [["arrow-left", lambda x: app.back_to_screen('dashboard')]]
        ScrollView:
            MDList:
                id: sem_list

<ContentScreen>:
    name: 'content_screen'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            id: content_title
            title: "Details"
            md_bg_color: 0.1, 0.2, 0.6, 1
            left_action_items: [["arrow-left", lambda x: app.back_to_screen('semester_screen')]]
        ScrollView:
            MDList:
                id: content_list
'''

class LoginScreen(Screen): pass
class DashboardScreen(Screen): pass
class SemesterScreen(Screen): pass
class ContentScreen(Screen): pass

class StudentApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def check_login(self, user_id):
        if user_id.lower() == "admin": 
            self.root.current = 'dashboard'
            self.load_departments()
        else:
            self.show_popup("Error", "Invalid ID. Use 'admin' to test.")

    def load_departments(self):
        container = self.root.get_screen('dashboard').ids.dept_list
        container.clear_widgets()
        
        # নোটিশ ও টিচার্স
        for n, i in [("Notice Board", "bell"), ("Teacher Details", "account-tie")]:
            item = TwoLineIconListItem(text=n, secondary_text="Click to see")
            item.add_widget(IconLeftWidget(icon=i))
            item.bind(on_release=lambda x, name=n: self.show_popup(name, "Coming Soon..."))
            container.add_widget(item)

        container.add_widget(OneLineListItem(text="--- Departments ---", divider=None))
        
        depts = [("Computer Technology", "laptop"), ("Civil Technology", "office-building"), 
                 ("Electrical Technology", "flash"), ("Mechanical Technology", "cog"), ("Marine Technology", "ferry")]
        
        for name, icon in depts:
            item = TwoLineIconListItem(text=name, secondary_text="Enter Department")
            item.add_widget(IconLeftWidget(icon=icon))
            item.bind(on_release=lambda x, n=name: self.open_semesters(n))
            container.add_widget(item)

    def open_semesters(self, dept_name):
        self.root.current = 'semester_screen'
        screen = self.root.get_screen('semester_screen')
        screen.ids.sem_title.title = f"BPI - {dept_name}"
        container = screen.ids.sem_list
        container.clear_widgets()
        
        for i in range(1, 9):
            sem_name = f"{i}th Semester"
            item = OneLineListItem(text=sem_name)
            item.bind(on_release=lambda x, s=sem_name, d=dept_name: self.open_details(d, s))
            container.add_widget(item)

    def open_details(self, dept, sem):
        # সেমিস্টারের ভেতরে ঢুকলে যা দেখাবে
        self.root.current = 'content_screen'
        screen = self.root.get_screen('content_screen')
        screen.ids.content_title.title = f"{dept} - {sem}"
        container = screen.ids.content_list
        container.clear_widgets()
        
        # ১. ক্লাস রুটিন অপশন
        routine_item = TwoLineIconListItem(text="Class Routine", secondary_text="Daily schedule")
        routine_item.add_widget(IconLeftWidget(icon="calendar-clock"))
        routine_item.bind(on_release=lambda x: self.show_popup("Routine", f"{dept} {sem} Routine loading..."))
        container.add_widget(routine_item)
        
        # ২. প্রতিদিনের পড়া (Lesson Update)
        lesson_item = TwoLineIconListItem(text="Daily Lessons", secondary_text="Today's topics by teachers")
        lesson_item.add_widget(IconLeftWidget(icon="book-open-variant"))
        lesson_item.bind(on_release=lambda x: self.show_popup("Daily Lessons", "Today's lesson details will be shown here."))
        container.add_widget(lesson_item)

    def back_to_screen(self, screen_name):
        self.root.current = screen_name

    def show_popup(self, title, text):
        if not self.dialog:
            self.dialog = MDDialog(title=title, text=text, buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        else:
            self.dialog.title = title
            self.dialog.text = text
        self.dialog.open()

if __name__ == '__main__':
    StudentApp().run()
