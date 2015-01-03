import sys
import os
import libelf
from libelf import *
from libelf.constants import *
from libelf.types import *
from libelf.util import *
from ctypes import *

def sections(elf, **kwargs):
  i = None
  if 'info' in kwargs:
    if (isinstance(kwargs['info'], Elf_Scn)):
      info = elf_ndxscn(kwargs['info'])
    else:
      print type(kwargs['info'])
      info = kwargs['info']
  else:
    info = None
  while 1:
    i = elf_nextscn(elf, i)
    if (not bool(i)):
      break

    try:
      if ('name' in kwargs and section_name(elf, i) != kwargs['name']):
        continue

      if ('type' in kwargs and section_type(elf, i) != kwargs['type']):
        continue

      if ('link' in kwargs and section_link(elf, i) != kwargs['link']):
        continue

      if (info != None and section_hdr(elf, i).sh_info != info):
        continue
    except ValueError:
      print "Error iterating over section ", i
      continue

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

def strings(v):
  if (isinstance(v, Elf_Data)):
    strtab_data = v
    size = strtab_data.d_size
    buf = cast(strtab_data.d_buf, POINTER(c_char))
    start = 0;
    while start < size:
      end = start;
      while buf[end] != '\x00': end += 1
      yield (strtab_data.d_off + start, buf[start:end])

      start = end+1
  elif (isinstance(v, Elf_Scn)):
    for d in data(v):
      strtab_data = d
      size = strtab_data.d_size
      buf = cast(strtab_data.d_buf, POINTER(c_char))
      start = 0;
      while start < size:
        end = start;
        while buf[end] != '\x00': end += 1
        yield (strtab_data.d_off + start, buf[start:end])

        start = end+1
      

def arr_iter(data, itemT, ind = False):
  size = data.d_size

  if size % sizeof(itemT) != 0:
    raise Exception("Data size not a multiple of symbol size!")

  buf = cast(data.d_buf, POINTER(itemT))
  nelems = size / sizeof(itemT)

  for i in xrange(0, nelems):
    if ind:
      yield (i, buf[i])
    else:
      yield buf[i]

def syms(elf, v = None):
  symT = Elf32_Sym if (is32(elf)) else Elf64_Sym
  if v == None:
    for s in sections(elf, type=SHT_SYMTAB):
      for d in data(s):
        for (ind, sym) in arr_iter(d, symT, True):
          yield (ind, sym)
  elif isinstance(v, Elf_Scn):
    for d in data(v):
      for (ind, sym) in arr_iter(d, symT, True):
        yield (ind, sym)
  else:
    assert isinstance(v, Elf_Data)
    for (ind, sym) in arr_iter(v, symT, True):
      yield (ind, sym)

def rels(elf, **kwargs):
  relT = Elf32_Rel if (is32(elf)) else Elf64_Rel
  if 'section' in kwargs:
    secl = sections(elf, type = SHT_REL, info = kwargs['section'])
  else:
    secl = sections(elf, type = SHT_REL)


  if 'range' in kwargs:
    for scn in secl:
      for d in data(scn):
        for rel in arr_iter(d, relT):
          if (rel.r_offset >= kwargs['range'][0] and
             rel.r_offset < kwargs['range'][1]):
            yield (rel, section_hdr(elf, scn).sh_link)
  else:
    for scn in secl:
      for d in data(scn):
        for rel in arr_iter(d, relT):
          yield (rel, section_hdr(elf, scn).sh_link)

def relas(elf, **kwargs):
  relT = Elf32_Rela if (is32(elf)) else Elf64_Rela
  if 'section' in kwargs:
    scn = kwargs['section']
    if (type(scn) == str):  scn = list(sections(elf, name=scn))[0]
    if (isinstance(scn, Elf_Scn)):  scn = elf_ndxscn(byref(scn))
    secl = list(sections(elf, type = SHT_RELA, info = scn))
  else:
    secl = list(sections(elf, type = SHT_RELA))

  if 'range' in kwargs:
    for scn in secl:
      for d in data(scn):
        for rel in arr_iter(d, relT):
          if (rel.r_offset  + rel.r_addend >= kwargs['range'][0] and
             rel.r_offset + rel.r_addend < kwargs['range'][1]):
            yield (rel, section_hdr(elf, scn).sh_link)
  else:
    for s in secl:
      for d in data(scn):
        for rel in arr_iter(d, relT):
          yield (rel, section_hdr(elf, scn).sh_link)

def elfs(fname):
  fd = os.open(fname, os.O_RDONLY)
  ar = elf_begin(fd, ELF_C_READ, None)
  
  i = None
  while 1:
    i = elf_begin(fd, ELF_C_READ, ar)
    if (not bool(i)):
      break

    yield i

  elf_end(ar)
  os.close(fd)
