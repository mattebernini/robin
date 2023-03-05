import sys
import speech_recognition as sr
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Impostazioni finestra principale
        self.setWindowTitle("Assistente vocale")
        self.setGeometry(100, 100, 500, 500)

        # Etichetta per l'input vocale
        self.input_label = QLabel(self)
        self.input_label.setText("Input vocale:")
        self.input_label.move(50, 50)

        # Pulsante per l'input vocale
        self.input_button = QPushButton(self)
        self.input_button.setText("Ascolta")
        self.input_button.move(150, 50)
        self.input_button.clicked.connect(self.get_audio_input)

        # Etichetta per l'input scritto
        self.input_text_label = QLabel(self)
        self.input_text_label.setText("Input scritto:")
        self.input_text_label.move(50, 100)

        # Casella di testo per l'input scritto
        self.input_text = QLineEdit(self)
        self.input_text.move(150, 100)

        # Etichetta per l'output vocale
        self.output_label = QLabel(self)
        self.output_label.setText("Output vocale:")
        self.output_label.move(50, 150)

        # Pulsante per l'output vocale
        self.output_button = QPushButton(self)
        self.output_button.setText("Riproduci")
        self.output_button.move(150, 150)
        self.output_button.clicked.connect(self.play_audio_output)

        # Etichetta per l'output scritto
        self.output_text_label = QLabel(self)
        self.output_text_label.setText("Output scritto:")
        self.output_text_label.move(50, 200)

        # Casella di testo per l'output scritto
        self.output_text = QTextEdit(self)
        self.output_text.move(150, 200)

    def get_audio_input(self):
        # Inizializza il recognizer
        r = sr.Recognizer()

        # Utilizza il microfono come sorgente audio
        with sr.Microphone() as source:
            print("Ascolto...")
            audio = r.listen(source)

        # Trascrivi l'audio in testo
        try:
            text = r.recognize_google(audio, language='it-IT')
            self.input_text.setText(text)
        except sr.UnknownValueError:
            print("Non ho capito")
        except sr.RequestError as e:
            print("Errore nella richiesta: {0}".format(e))

    def play_audio_output(self):
        # Riproduci l'audio
        pass # Inserisci qui il codice per la riproduzione dell'audio

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
