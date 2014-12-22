import sys
import os
import libelf
from libelf import *
from libelf.constants import *

def _class(elf):  elf_getident(elf, None)[EI_CLASS]

def _is32(elf):   _class(elf) == ELFCLASS32 
def _is64(elf):   _class(elf) == ELFCLASS64 

def select(elf, fname):
  if _is32(elf):
    return libelf.__getattribute__('elf32_' + fname)
  else:
    return libelf.__getattribute__('elf64_' + fname)

def sections(elf):
  i = None
  while 1:
    i = elf_nextscn(elf, i)
    if (not bool(i)):
      break

    yield i.contents

def shdrs(elf):
  i = None
  while 1:
    i = elf_nextscn(elf, i)
    if (not bool(i)):
      break

    yield select(elf, 'getshdr')(i.contents).contents
