import os
import sha
import shutil
import tempfile
from cStringIO import StringIO
from megrok import resource
from hurry.resource import ResourceInclusion
from slimmer import css_slimmer, js_slimmer

SLIMMERS = {'.css': css_slimmer,
            '.js': js_slimmer,
            '.kss': css_slimmer}

TEMPDIR = tempfile.gettempdir()
PREFIX = "merged-library-"


class MergeLibrary(resource.Library):
    resource.use_hash(False)
    resource.path(TEMPDIR)


def slimmer(ext, content):
    slimmer = SLIMMERS.get(ext)
    if slimmer is None:
        raise NotImplementedError
    return slimmer(content, hardcore=True)


def merger(ext, name, resources, slim=False):
    """Merges given resources.
    """
    merge_name = PREFIX + sha.new(name).hexdigest() + ext
    merge_path = os.path.join(TEMPDIR, merge_name)
    
    if os.path.exists(merge_path):
        if os.path.isdir(merge_path):
            raise NotImplementedError(
                'Merging destination %r is a directory.' % merge_path)
        os.remove(merge_path)

    depends = set()
    tempIO = StringIO()
    for filename, inclusion in resources:
        shutil.copyfileobj(open(filename, 'rb'), tempIO)
        depends.update(inclusion.depends)

    merged = open(merge_path, 'wb')
    try:
        if slim is True:
            content = tempIO.getvalue()
            slimmed = slimmer(ext, content)
            merged.write(slimmed)
        else:
            shutil.copyfileobj(tempIO, merged)
    except Exception:
        raise
    finally:
        merged.close()

    # What shall we do about bottom ?
    return ResourceInclusion(MergeLibrary, merge_name, depends=depends)
