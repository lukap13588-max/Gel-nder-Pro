# Geländer PRO – V1
Python 3.10+ installieren, Terminal in diesem Ordner öffnen. Windows PowerShell:

```
python -m pip install -r requirements.txt
$env:ADMIN_PASSWORD='Eigenes-langes-Adminpasswort'
$env:TEAM_PASSWORD='Anderes-langes-TeamPasswort'
python app.py
```

PC: http://localhost:8000. Handy im selben WLAN: http://IP-DES-PC:8000 (IP via ipconfig, ggf. Windows-Firewall für privates Netz freigeben). Der PC muss laufen. Nur vertrauenswürdiges internes Netz für diesen Test nutzen. Kein öffentliches Portforwarding. Für produktiven Einsatz HTTPS, langlebigen SECRET_KEY, WSGI-Server, individuelle Benutzerkonten und Login-Ratenbegrenzung einrichten. HTTPS=1 erst bei funktionierendem TLS. Zwei gemeinsame Rollenpasswörter sind nur eine erste Lösung, keine individuelle Benutzerverwaltung.

SQLite-Datei gelaender.db enthält Daten und komprimierte Fotos. Für Backup Server stoppen und Datei kopieren. Keine Beispieldaten. Kein QR-Code. iPhone-Fotos in einem vom Browser lesbaren Format (JPEG/PNG); HEIC ggf. vorher konvertieren. Keine OCR, PDF-Anhänge, Offline-Synchronisierung oder native Installation in V1. Browser-Verknüpfung möglich (zum Home-Bildschirm). Für Zugriff außerhalb des WLAN ist ein sicherer Server erforderlich.
