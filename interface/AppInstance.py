from interface.App import App
# singleton wrapper, do not touch
# any methods declared in App can be used in AppInstance safely anyway, so infrastructure still works.

class AppInstance(App):
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(AppInstance, cls).__new__(cls)
        return cls.instance
