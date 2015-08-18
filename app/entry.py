from tornado.web import UIModule


class EntryModule(UIModule):
    def render(self, entry):
        return self.render_string('modules/wrap.html', entry=entry)
