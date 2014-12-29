from libelf import *
from libelf.types import *
from libelf.iterators import *
from libelf.util import *

def defined(s): return s.st_shndx != SHN_UNDEF

def defines(elf, symN):
  s = findSymbol(elf, symN)
  print elf, symN, s
  if s != None:
    print s.st_shndx, s.st_name
  return s != None and defined(s[1]) 

def derefSymbol(elf, s): 
  assert defined(s)
  if s.st_shndx == SHN_ABS: 
    raise Exception("NYI") 
  else: 
    scn = elf_getscn(elf, s.st_shndx) 
    off = 0 
    start = s.st_value 
    end = s.st_value + s.st_size 
    r = '' 
    for d in data(scn): 
      if start >= end:  break; 
      off = d.d_off 
      if start >= off and start < off + d.d_size: 
        c = cast(d.d_buf, POINTER(c_char)) 
        l = min(off + d.d_size, end) - start 
        r += c[start- off : start - off + l] 
        start += l 
 
    return r 

# Given a symbol name return the symbol and section in which it occurs
def findSymbol(elf, s):
  for scn in sections(elf, type=SHT_SYMTAB):
    strndx = section_link(elf, scn)
    for d in data(scn):
      for (ind, sym) in syms(elf, d):
        if s == elf_strptr(elf, strndx, sym.st_name):
          return (scn, sym)
  return None
