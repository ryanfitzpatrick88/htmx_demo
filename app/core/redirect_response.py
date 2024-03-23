from fastapi.responses import RedirectResponse

class HTTPResponseHXRedirect(RedirectResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers['HX-Redirect']=self.headers['Location']
        self.status_code = 200