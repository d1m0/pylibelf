def ELF32_R_SYM(i):
  return i >> 8

def ELF32_R_TYPE(i):
  return i % 256 # Lowest 8 bits

def ELF32_R_INFO(sym, typ):
  return (((sym) << 8) + typ % 256)

def ELF64_R_SYM(i):
  return i >> 32

def ELF64_R_TYPE(i):
  return i & 0xffffffffL

def ELF64_R_INFO(sym, typ):
  return ((sym << 32) + (typ & 0xffffffffL))
