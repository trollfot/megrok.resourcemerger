# -*- coding: utf-8 -*-

import martian
import os.path
from grokcore import view
from megrok import resource
from hurry.resource.core import EXTENSIONS
from megrok.resource.meta import ResourceLibraryGrokker
from megrok.resourcemerger.directives import merge
from megrok.resourcemerger.merger import merger

PRIORITY = martian.priority.bind().get(ResourceLibraryGrokker)


def _get_resource_path(library_path, resource):
    if not os.path.isdir(library_path):
        raise martian.error.GrokError(
            "The `%s` library is not a valid directory." % library)
    resource_path = os.path.join(library_path, resource)
    if not os.path.isfile(resource_path):
        raise martian.error.GrokError(
            "The `%s` resource of library `%s` is not a valid file." % (
                    resource, library), resource)
    return resource_path


def extract_resources(library_path, resources):
    extracted = {}
    for resource in resources:
        ext = resource.ext()
        if ext not in EXTENSIONS:
            raise martian.error.GrokError(
                "Unknow extension `%s` for resource `%r`." % (
                    ext, resource), resource)
        filepath = _get_resource_path(library_path, resource.relpath)
        extracted.setdefault(ext, []).append((filepath, resource))
    return extracted


class ResourceLibraryMerger(martian.ClassGrokker):
    martian.component(resource.ResourceLibrary)
    martian.priority(PRIORITY - 1)
    martian.directive(merge, default=False)
    martian.directive(view.path)

    def grok(self, name, factory, module_info, **kw):
        factory.module_info = module_info
        return super(ResourceLibraryMerger, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config, merge, path, **kw):
        if merge:
            library_path = factory.module_info.getResourcePath(path)
            extracted = extract_resources(library_path, factory.depends)

            factory.depends = []
            for ext, resources in extracted.items():
                if len(resources) == 1:
                    factory.depends.append(resources[0][1])
                else:
                    factory.depends.append(
                        merger(ext, library_path, resources))
        return True
