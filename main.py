import pyttsx3
import os
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import customtkinter
import pdfplumber
from pygame import mixer

mixer.init()

def pdf_to_text(book):
    text = ""
    reader = pdfplumber.open(book)
    pages = len(reader.pages)
    for i in range(pages):
        page = reader.pages[i]
        text += page.extract_text()

    return text

engine = pyttsx3.init()
engine.setProperty("rate", 150)

voices = engine.getProperty("voices")

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class SideFrame(customtkinter.CTkFrame):
    def __init__(self, master,  module, **kwargs):
        super().__init__(master, **kwargs)

        self.logo_label = customtkinter.CTkLabel(self, text=module, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        #self.start_reading_button = customtkinter.CTkButton(self, text="Stop Reading", command=self.stop_reading)
        #self.start_reading_button.grid(row=1, column=0, padx=0, pady=10)

        self.gender_buttons = customtkinter.CTkSegmentedButton(self, values=["Male", "Female"], command=self.change_voice)
        self.gender_buttons.set("Male")
        self.gender_buttons.grid(row=2, column=0, padx=0, pady=10)

        self.slider_frame = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.slider_frame.grid_columnconfigure(2, weight=1)
        self.slider_frame.grid(row=4, column=0, padx=0, pady=10)

        self.speed_slider = customtkinter.CTkSlider(self.slider_frame, orientation="vertical", from_=0.25, to=2, number_of_steps=7, command=self.speed_slider_event)
        self.speed_slider.grid(row=0, column=0, padx=(10, 20), pady=20)

        self.speed_label = customtkinter.CTkLabel(self.slider_frame, text="Speed")
        self.speed_label.grid(row=1, column=0, padx=(10, 10), pady=20)

        self.volume_slider = customtkinter.CTkSlider(self.slider_frame, orientation="vertical", from_=0, to=1, command=self.volume_slider_event)
        self.volume_slider.grid(row=0, column=1, padx=(20, 10), pady=(10, 10))

        self.volume_label = customtkinter.CTkLabel(self.slider_frame, text="Volume")
        self.volume_label.grid(row=1, column=1, padx=(10, 10), pady=20)

        if module == "Audio Book":
            self.controls = customtkinter.CTkFrame(master=self, fg_color="transparent")
            self.controls.grid_columnconfigure(2, weight=1)
            self.controls.grid(row=5, column=0, padx=0, pady=10)

            def pause_reading():
                if mixer.music.get_busy() == True:
                    self.controls.pause_button.configure(text="Resume", command=resume_reading)
                    mixer.music.pause()
                else:
                    pass

            def resume_reading():
                if mixer.music.get_busy() == False:
                    self.controls.pause_button.configure(text="Pause", command=pause_reading)
                    mixer.music.unpause()
                else:
                    pass

            def stop_reading():
                mixer.music.unload()
                mixer.music.stop()
                try:
                    os.remove("temp/audio.wav")
                except:
                    pass

            self.controls.pause_button = customtkinter.CTkButton(self.controls, text="Pause", command=pause_reading)
            self.controls.pause_button.grid(row=0, column=0, padx=0, pady=10)

            self.controls.stop_button = customtkinter.CTkButton(self.controls, text="Stop", command=stop_reading)
            self.controls.stop_button.grid(row=1, column=0, padx=0, pady=10)

    def change_voice(self, value):
        engine.setProperty("voice", voices[1].id if value == "Female" else voices[0].id)

    def speed_slider_event(self, value):
        freq = int(44100 * value)
        mixer.init(freq)
        
    def volume_slider_event(self, value):
        mixer.music.set_volume(value)

class BuiltIn(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        books = {"aib": "Alice in Borderland", "aofad": "All of us are Dead", "sg": "Squid Games", "bb": "Breaking Bad", "mh": "Money Heist", "l": "Lucifer", "m": "Manifest", "got": "Game of Thrones", "st": "Stranger Things", "mm": "Mismatched"}

        def text_to_audio(pdf):
            text = pdf_to_text("books/" + pdf + ".pdf")
            engine.save_to_file(text, "temp/audio.wav")
            engine.runAndWait()

            mixer.init()
            mixer.music.load("temp/audio.wav")
            mixer.music.play()

        i = 1
        for pdf, name in books.items():
            e = customtkinter.CTkButton(self, width=850, height=50, text="  ▶️" + name, font=customtkinter.CTkFont(size=15), anchor="w", command=lambda: text_to_audio(pdf))
            e.grid(row=i, column=1, padx=(35, 0), pady=10, sticky="w")
            i += 1
            
        self.available = customtkinter.CTkLabel(self, text="Available Books", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.available.grid(row=0, column=1, padx=(400, 400), pady=10, sticky="n")

class PDFReaderGUI(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.open_pdf_button = customtkinter.CTkButton(master=self, text="Open PDF", command=self.open_pdf_file, width=150, height=75, font=customtkinter.CTkFont(size=17))
        self.open_pdf_button.grid(row=0, column=1, padx=500, pady=20)


    def open_pdf_file(self):
        self.book = askopenfilename(title="Open PDF", filetype=(("PDF Files","*.pdf"),("All Files","*.*")))
        if self.book:
            self.now_reading = customtkinter.CTkLabel(self, text="Now Reading: ", font=customtkinter.CTkFont(size=20, weight="bold"))
            self.now_reading.grid(row=1, column=0, padx=20, pady=10)
            self.book_name = customtkinter.CTkLabel(self, text=self.book.split("/")[-1], font=customtkinter.CTkFont(size=15))
            self.book_name.grid(row=2, column=0, padx=20, pady=10)

            self.controls = customtkinter.CTkFrame(self)
            self.controls.grid_columnconfigure(3, weight=1)
            self.controls.grid(row=3, column=0, padx=20, pady=10)
            self.controls.start_button = customtkinter.CTkButton(self.controls, text="Start", command=self.generate_audio)
            self.controls.start_button.grid(row=0, column=0, padx=(10, 5), pady=10)
            self.controls.pause_button = customtkinter.CTkButton(self.controls, text="Pause", command=self.pause_reading, state="disabled")
            self.controls.pause_button.grid(row=0, column=1, padx=(5, 5), pady=10)
            self.controls.stop_button = customtkinter.CTkButton(self.controls, text="Stop", command=self.stop_reading, state="disabled")
            self.controls.stop_button.grid(row=0, column=2, padx=(5, 10), pady=10)
        else:
            pass

    def generate_audio(self):
        self.controls.start_button.configure(state="disabled")
        self.controls.pause_button.configure(state="normal")
        self.controls.stop_button.configure(state="normal")
        text = pdf_to_text(self.book)
        mixer.music.unload()
        try:
            os.remove("temp/audio.wav")
        except:
            pass
        engine.save_to_file(text, "temp/audio.wav")
        engine.runAndWait()

        mixer.music.load("temp/audio.wav")
        mixer.music.play()

    def pause_reading(self):
        mixer.music.pause()
        self.controls.pause_button.configure(text="Resume", command=self.resume_reading)

    def resume_reading(self):
        mixer.music.unpause()
        self.controls.pause_button.configure(text="Pause", command=self.pause_reading)

    def stop_reading(self):
        self.controls.stop_button.configure(state="disabled")
        self.controls.pause_button.configure(state="disabled")
        self.controls.start_button.configure(state="normal")
        mixer.music.unload()
        mixer.music.stop()
        try:
            os.remove("temp/audio.wav")
        except:
            pass

class ConverterGUI(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(3, weight=1)

        self.text_box = customtkinter.CTkTextbox(self, width=1000, height=500, font=customtkinter.CTkFont(size=20))
        self.text_box.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))

        self.convert_button = customtkinter.CTkButton(self, text="Convert", command=self.convert_text)
        self.convert_button.grid(row=1, column=0, padx=10, pady=20)

    def convert_text(self):
        text = self.text_box.get("0.0", "end")
        filename = asksaveasfilename(filetype=(("MP3 Files","*.mp3"),("WAV Files","*.wav")))
        engine.save_to_file(text, filename)
        engine.runAndWait()

class AudioBook(customtkinter.CTkToplevel):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1280x720")
        self.title("Audio Book")
        self.state("zoomed")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.audio_book_interface = SideFrame(master=self, module="Audio Book", width=140, corner_radius=10)
        self.audio_book_interface.grid(row=0, column=0, padx=(15, 0), pady=15, rowspan=3, sticky="nsew")
        self.audio_book_interface.grid_columnconfigure(3, weight=1)

        self.built_in_interface = BuiltIn(master=self)
        self.built_in_interface.grid(row=0, column=1, padx=15, pady=15, rowspan=3, sticky="nsew")
        self.built_in_interface.grid_columnconfigure(3, weight=1)

        def on_closing():
            self.destroy()
            root.state("zoomed")
            mixer.music.unload()
            mixer.music.stop()
            try:
                os.remove("temp/audio.wav")
            except:
                pass

        self.protocol("WM_DELETE_WINDOW", on_closing)

class PDFReader(customtkinter.CTkToplevel):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1280x720")
        self.title("PDF Reader")
        self.state("zoomed")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.pdf_reader_interface = SideFrame(master=self, module="PDF Reader", width=140, corner_radius=10)
        self.pdf_reader_interface.grid(row=0, column=0, padx=(15, 0), pady=15, rowspan=3, sticky="nsew")
        self.pdf_reader_interface.grid_columnconfigure(3, weight=1)

        self.pdf_reader_gui = PDFReaderGUI(master=self)
        self.pdf_reader_gui.grid(row=0, column=1, padx=15, pady=15, rowspan=3, sticky="nsew")
        self.pdf_reader_gui.grid_columnconfigure(3, weight=1)

        def on_closing():
            self.destroy()
            root.state("zoomed")
            mixer.music.unload()
            mixer.music.stop()
            try:
                os.remove("temp/audio.wav")
            except:
                pass

        self.protocol("WM_DELETE_WINDOW", on_closing)

class Converter(customtkinter.CTkToplevel):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1280x720")
        self.title("Text to MP3 Converter")
        self.state("zoomed")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.pdf_reader_interface = SideFrame(master=self, module="Text to MP3", width=140, corner_radius=10)
        self.pdf_reader_interface.grid(row=0, column=0, padx=(15, 0), pady=15, rowspan=3, sticky="nsew")
        self.pdf_reader_interface.grid_columnconfigure(3, weight=1)

        self.pdf_reader_gui = ConverterGUI(master=self)
        self.pdf_reader_gui.grid(row=0, column=1, padx=15, pady=15, rowspan=3, sticky="nsew")
        self.pdf_reader_gui.grid_columnconfigure(3, weight=1)

        def on_closing():
            self.destroy()
            root.state("zoomed")

        self.protocol("WM_DELETE_WINDOW", on_closing)

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Nova")
        self.geometry("500x1000")
        
        self.ab = customtkinter.CTkButton(self, corner_radius=6, command=self.open_audio_book, text="Audio Book")
        self.ab.place(relx=0.5, rely=0.43, anchor="center")

        self.pr = customtkinter.CTkButton(self, corner_radius=6, command=self.open_pdf_reader, text="PDF Reader")
        self.pr.place(relx=0.5, rely=0.5, anchor="center")

        self.pr = customtkinter.CTkButton(self, corner_radius=6, command=self.open_text_to_mp3, text="Text to MP3")
        self.pr.place(relx=0.5, rely=0.57, anchor="center")

        self.audio_book_window = None
        self.pdf_reader_window = None
        self.text_to_mp3_window = None

    def open_audio_book(self):
        if self.audio_book_window is None or not self.audio_book_window.winfo_exists():
            self.state("iconic")
            self.audio_book_window = AudioBook(self)
        else:
            self.audio_book_window.focus()

    def open_pdf_reader(self):
        if self.pdf_reader_window is None or not self.pdf_reader_window.winfo_exists():
            self.state("iconic")
            self.pdf_reader_window = PDFReader(self)
        else:
            self.pdf_reader_window.focus()

    def open_text_to_mp3(self):
        if self.text_to_mp3_window is None or not self.text_to_mp3_window.winfo_exists():
            self.state("iconic")
            self.text_to_mp3_window = Converter(self)
        else:
            self.text_to_mp3_window.focus()

app = App()
app.mainloop()
