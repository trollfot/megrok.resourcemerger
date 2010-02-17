import martian


class merge(martian.MarkerDirective):
    scope = martian.CLASS
    store = martian.ONCE_NOBASE

 
class slim(martian.MarkerDirective):
    scope = martian.CLASS
    store = martian.ONCE_NOBASE
    
