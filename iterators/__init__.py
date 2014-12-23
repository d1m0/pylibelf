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

def arr_iter(data, itemT):
  size = data.d_size

  if size % sizeof(itemT) != 0:
    raise Exception("Data size not a multiple of symbol size!")

  buf = cast(data.d_buf, POINTER(itemT))
  nelems = size / sizeof(itemT)

  for i in xrange(0, nelems):
    yield buf[i]

def syms(elf, data):
  symT = Elf32_Sym if (_is32(elf)) else Elf64_Sym
  return arr_iter(data, symT)

def rels(elf, data):
  relT = Elf32_Rel if (_is32(elf)) else Elf64_Rel
  return arr_iter(data, relT)

def relas(elf, data):
  relaT = Elf32_Rela if (_is32(elf)) else Elf64_Rela
  return arr_iter(data, relaT)
