# Robin - Assistente Virtuale

Robin è un assistente virtuale progettato per aiutare gli utenti a svolgere compiti specifici, fornire informazioni e intrattenere. Robin è stato creato con l'obiettivo di essere un assistente virtuale divertente e sarcastico, ma anche gentile e disponibile.


## Tecnologie utilizzate

Robin è stato sviluppato utilizzando diverse tecnologie, tra cui:

- Python
- API di OpenAI e Google
- Text to Speech (pyttsx3) ed espeak
- Speech Recognition di Google

## Come utilizzare Robin

- in ambiente Linux installare i requisiti con pip da requirements.txt
- installare espeak e una voce a tua scelta qui https://github.com/espeak-ng/espeak-ng/blob/master/docs/mbrola.md#linux-installation altrimenti usare la voce 'italian' di default
- nella cartella config aggiungere il file config.json fatto così:

        {
            "OPEN_AI_API_KEY" : "la tua api",
            "ascolta" : 0,
            "parla" : 1, 
            "voce" : {
                "nome" : "mb-it3",      // nome della voce espeak
                "rate-delta" : -60      // velocità del parlato
            },
            "model-gpt" : "gpt-3.5-turbo"
        }
        
- personalizza il file sopracitato e il file config/contesto.md
- lanciare l'assistente:
        python3 main.py

