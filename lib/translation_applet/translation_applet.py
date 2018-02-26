import gtk
import gobject

from translation_client import translation_client


class TranslationApplet(object):
    def __init__(self):
        self._translation_client = translation_client.TranslationClient('http://localhost:8080/')
        self._sid = None
        self._uuid = None

    def run(self):
        json = self._translation_client.login('user1', 'passwd1')
        assert 'sid' in json
        self._sid = json['sid']
        
        clipboard = gtk.clipboard_get(selection='PRIMARY')
        clipboard.connect('owner-change', self._on_clipboard_owner_change)
        
        gobject.timeout_add(200, self._on_timeout)
        
        gtk.main()

    def _on_clipboard_owner_change(self, clipboard, event):
        text = clipboard.wait_for_text()
        if text is None:
            return
        
        if self._uuid:
            json = self._translation_client.cancel(self._sid, self._uuid)
            assert json is None
            self._uuid = None
        
        text = text.strip()
        if not text:
            return
        
        json = self._translation_client.translate(self._sid, text, 'en', 'es')
        assert 'uuid' in json
        self._uuid = json['uuid']
    
    def _on_timeout(self):
        if self._uuid:
            json = self._translation_client.poll(self._sid, self._uuid)
            assert 'result' in json
            result = json['result']
            
            if result is not None:
                print result
                self._uuid = None
        return True
