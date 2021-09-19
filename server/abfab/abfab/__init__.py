from guillotina import configure

app_settings = {
    # provide custom application settings here...
}


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan('abfab.api')
    configure.scan('abfab.install')
    configure.scan('abfab.content')
