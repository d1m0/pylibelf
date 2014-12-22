from ctypes import *

# TODO: Hack! Should be getting this from types/
EI_NIDENT = 16

# Obtained from /usr/lib/elf.h

# Type for a 16-bit quantity.  
Elf32_Half = c_uint16 
Elf64_Half = c_uint16 

# Types for signed and unsigned 32-bit quantities.  
Elf32_Word = c_uint32 
Elf32_Sword = c_int32 
Elf64_Word = c_uint32 
Elf64_Sword = c_int32 

# Types for signed and unsigned 64-bit quantities.  
Elf32_Xword = c_uint64 
Elf32_Sxword = c_int64 
Elf64_Xword = c_uint64 
Elf64_Sxword = c_int64 

# Type of addresses.  
Elf32_Addr = c_uint32 
Elf64_Addr = c_uint64 

# Type of file offsets.  
Elf32_Off = c_uint32 
Elf64_Off = c_uint64 

# Type for section indices, which are 16-bit quantities.  
Elf32_Section = c_uint16 
Elf64_Section = c_uint16 

# Type for version symbol information.  
Elf32_Versym = Elf32_Half 
Elf64_Versym = Elf64_Half 

# The ELF file header.  This appears at the start of every ELF file.  

Elf_IdentT = c_char * EI_NIDENT

Elf_Cmd = c_int

# Libelf opaque handles
class Elf(Structure): pass; 
class Elf_Scn(Structure): pass; 

class Elf_Data(Structure):
  _fields_ = [
    ('d_buf', c_void_p),
    ('d_type', c_int),
    ('d_size', c_size_t),
    ('d_off', c_size_t),
    ('d_align', c_size_t),
    ('d_version', c_uint)
  ]

ElfP = POINTER(Elf)
Elf_ScnP = POINTER(Elf_Scn)
Elf_DataP = POINTER(Elf_Data)

class Elf32_Ehdr(Structure):
  _fields_ = [
    ('e_ident',   Elf_IdentT ), # Magic number and other info 
    ('e_type',   Elf32_Half ),     # Object file type 
    ('e_machine',   Elf32_Half ),    # Architecture 
    ('e_version',   Elf32_Word ),    # Object file version 
    ('e_entry',   Elf32_Addr ),    # Entry point virtual address 
    ('e_phoff',   Elf32_Off),    # Program header table file offset 
    ('e_shoff',   Elf32_Off),    # Section header table file offset 
    ('e_flags',   Elf32_Word ),    # Processor-specific flags 
    ('e_ehsize',   Elf32_Half ),   # ELF header size in bytes 
    ('e_phentsize',   Elf32_Half ),    # Program header table entry size 
    ('e_phnum',   Elf32_Half ),    # Program header table entry count 
    ('e_shentsize',   Elf32_Half ),    # Section header table entry size 
    ('e_shnum',   Elf32_Half ),    # Section header table entry count 
    ('e_shstrndx',   Elf32_Half ),   # Section header string table index 
  ]

class Elf64_Ehdr(Structure):
  _fields_ = [
    ('e_ident',   Elf_IdentT ), # Magic number and other info 
    ('e_type',   Elf64_Half ),     # Object file type 
    ('e_machine',   Elf64_Half ),    # Architecture 
    ('e_version',   Elf64_Word ),    # Object file version 
    ('e_entry',   Elf64_Addr ),    # Entry point virtual address 
    ('e_phoff',   Elf64_Off),    # Program header table file offset 
    ('e_shoff',   Elf64_Off),    # Section header table file offset 
    ('e_flags',   Elf64_Word ),    # Processor-specific flags 
    ('e_ehsize',   Elf64_Half ),   # ELF header size in bytes 
    ('e_phentsize',   Elf64_Half ),    # Program header table entry size 
    ('e_phnum',   Elf64_Half ),    # Program header table entry count 
    ('e_shentsize',   Elf64_Half ),    # Section header table entry size 
    ('e_shnum',   Elf64_Half ),    # Section header table entry count 
    ('e_shstrndx',   Elf64_Half ),   # Section header string table index 
 ] 

class Elf32_Shdr(Structure):
  _fields_ = [
		('sh_name', Elf32_Word), # Section name (string tbl index) 
		('sh_type', Elf32_Word), # Section type 
		('sh_flags', Elf32_Word), # Section flags 
		('sh_addr', Elf32_Addr), # Section virtual addr at execution 
		('sh_offset', Elf32_Off), # Section file offset 
		('sh_size', Elf32_Word), # Section size in bytes 
		('sh_link', Elf32_Word), # Link to another section 
		('sh_info', Elf32_Word), # Additional section information 
		('sh_addralign', Elf32_Word), # Section alignment 
		('sh_entsize', Elf32_Word), # Entry size if section holds table 
 ] 

class Elf64_Shdr(Structure):
  _fields_ = [
		('sh_name', Elf64_Word), # Section name (string tbl index) 
		('sh_type', Elf64_Word), # Section type 
		('sh_flags', Elf64_Xword), # Section flags 
		('sh_addr', Elf64_Addr), # Section virtual addr at execution 
		('sh_offset', Elf64_Off), # Section file offset 
		('sh_size', Elf64_Xword), # Section size in bytes 
		('sh_link', Elf64_Word), # Link to another section 
		('sh_info', Elf64_Word), # Additional section information 
		('sh_addralign', Elf64_Xword), # Section alignment 
		('sh_entsize', Elf64_Xword), # Entry size if section holds table 
 ] 

class Elf32_Phdr(Structure):
  _fields_ = [
		('p_type', Elf32_Word), # Segment type 
		('p_offset', Elf32_Off), # Segment file offset 
		('p_vaddr', Elf32_Addr), # Segment virtual address 
		('p_paddr', Elf32_Addr), # Segment physical address 
		('p_filesz', Elf32_Word), # Segment size in file 
		('p_memsz', Elf32_Word), # Segment size in memory 
		('p_flags', Elf32_Word), # Segment flags 
		('p_align', Elf32_Word), # Segment alignment 
  ]

class Elf64_Phdr(Structure):
  _fields_ = [
		('p_type', Elf64_Word), # Segment type 
		('p_flags', Elf64_Word), # Segment flags 
		('p_offset', Elf64_Off), # Segment file offset 
		('p_vaddr', Elf64_Addr), # Segment virtual address 
		('p_paddr', Elf64_Addr), # Segment physical address 
		('p_filesz', Elf64_Xword), # Segment size in file 
		('p_memsz', Elf64_Xword), # Segment size in memory 
		('p_align', Elf64_Xword), # Segment alignment 
  ]
