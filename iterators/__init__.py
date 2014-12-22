import sys
import os
import libelf
from libelf import *
from libelf.constants import *
from libelf.types import *
from ctypes import *

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


def data(elf_scn):
  i = None
  while 1:
    i = elf_getdata(elf_scn, i)

    if (not bool(i)):
      break

    yield i.contents

def strings(strtab_data):
  size = strtab_data.d_size
  buf = cast(strtab_data.d_buf, POINTER(c_char))
  start = 0;
  while start < size:
    end = start;
    while buf[end] != '\x00': end += 1
    yield (strtab_data.d_off + start, buf[start:end])

    start = end+1

def syms(elf, strtab_data):
  size = strtab_data.d_size

  symT = Elf32_Sym if (_is32(elf)) else Elf64_Sym
  buf = cast(strtab_data.d_buf, POINTER(symT))

  if size % sizeof(symT) != 0:
    raise Exception("Data size not a multiple of symbol size!")

  nelems = size / sizeof(symT)

  for i in xrange(0, nelems):
    yield buf[i]
