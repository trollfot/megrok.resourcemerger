import os
import sha
import shutil
import tempfile
from megrok import resource
from hurry.resource import ResourceInclusion


TEMPDIR = tempfile.gettempdir()
PREFIX = "merged-library-"


class MergeLibrary(resource.Library):
    resource.use_hash(False)
    resource.path(TEMPDIR)


def merger(ext, name, resources, slimmer=False):
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
    destination = open(merge_path, 'wb')
    for filename, inclusion in resources:
        shutil.copyfileobj(open(filename, 'rb'), destination)
        depends.update(inclusion.depends)
    destination.close()

    # What shall we do about bottom ?
    return ResourceInclusion(MergeLibrary, merge_name, depends=depends)
