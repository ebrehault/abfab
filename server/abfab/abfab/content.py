from guillotina import configure, content, schema
from guillotina.interfaces import IFolder, IItem
from guillotina.events import IObjectAddedEvent
from mimetypes import guess_type
from zope.interface import implementer, Interface

class IAbFabEditable(Interface):
    pass

class IDirectory(IFolder):
    main = schema.Text()
    module = schema.Text()
    data = schema.JSONField()

@configure.contenttype(
    type_name='Directory',
    schema=IDirectory,
    globally_addable=True,
    allowed_types=['File', 'Directory', 'Content'])
@implementer(IAbFabEditable)
class Directory(content.Folder):
    pass

class IFile(IItem):
    content_type = schema.Text()

@configure.contenttype(
    type_name='File',
    schema=IFile,
    globally_addable=False,
    behaviors=["guillotina.behaviors.attachment.IAttachment"],
)
@implementer(IAbFabEditable)
class File(content.Item):
    pass

@configure.subscriber(for_=(IFile, IObjectAddedEvent))
async def on_create_file(obj, evnt):
    if getattr(obj, 'content_type', None) is None:
        content_type = guess_type(obj.id)[0] or 'text/plain'
        obj.content_type = content_type
        obj.register()
    
class IContent(IItem):
    view = schema.Text()
    data = schema.JSONField()

@configure.contenttype(
    type_name='Content',
    schema=IContent,
    globally_addable=True,
)
@implementer(IAbFabEditable)
class Content(content.Item):
    pass
