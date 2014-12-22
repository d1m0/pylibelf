pylibelf
========

A thin (but mostly complete) python binding for libelf. Here is a brief example of using it (assuming the repo is checked out in a directory libelf under the current directory):


```
from libelf import *
from libelf.iterators import *
from libelf.types import *
from libelf.constants import *

import os

# Some executable...
fd = os.open('/home/sd/scripts/foo', os.O_RDONLY)

e = elf_begin(fd, ELF_C_READ, None)

res = c_size_t(0)
elf_getshstrndx(e, byref(res))
shstrtab = res.value

def sectionName(sec):
  shdr = elf64_getshdr(s).contents
  return elf_strptr(e, shstrtab, shdr.sh_name)

def sectionType(sec):
  return elf64_getshdr(s).contents.sh_type

# Example on using iterators to iterate through parts of a file
print "Sections"
for s in sections(e):
  print s

print "Section Headers"
for s in shdrs(e):
  print s

print "All data for all sections"
for s in sections(e):
  print sectionName(s)
  for d in data(s):
    print d

print "All strings in all sections"
for s in sections(e):
  if (sectionType(s) != SHT_STRTAB):
    continue

  print sectionName(s)
  for d in data(s):
    for s in strings(d):
      print s

print "All symbols in all symtab sections"
for s in sections(e):
  if (sectionType(s) != SHT_SYMTAB):
    continue

  print sectionName(s)
  shdr = elf64_getshdr(s).contents
  strtab = shdr.sh_link
  for d in data(s):
    for s in syms(e, d):
      print elf_strptr(e, strtab, s.st_name), s
```
