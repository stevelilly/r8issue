#!/usr/bin/env python3

import re
import sys


def grep(pattern, stream):
    for line in stream:
        match = re.match(pattern, line)
        if match is not None:
            yield match


def class_mappings(stream):
    return ((match.group(1), match.group(2)) for match in grep("^(.*) -> (.*):$", stream))


def common_package(packageA, packageB):
    prefix = common_iter_prefix(packageA.split("."), packageB.split("."))
    return ".".join(prefix)


def common_iter_prefix(iterA, iterB):
    iterA = iterA.__iter__()
    iterB = iterB.__iter__()
    result = []
    try:
        while True:
            a = iterA.__next__()
            b = iterB.__next__()
            if a != b:
                return result
            result.append(a)
    except StopIteration:
        return result


cleartextPackages = set()
for fromClass, toClass in class_mappings(sys.stdin):
    common = common_package(fromClass, toClass)
    if len(common) > 0:
        cleartextPackages.add(common)

cleartextPackages = list(cleartextPackages)
cleartextPackages.sort()
for pkg in cleartextPackages:
    print(pkg)
