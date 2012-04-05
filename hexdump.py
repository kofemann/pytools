#!/usr/bin/env python
# hexdump.py

'''A program which dumps the content  of a file in HEX format like:

$  ./hexdump.py hexdump.py
00000   23 21 2f 75 73 72 2f 62   69 6e 2f 65 6e 76 20 70    ...usr.bin.env.p
00010   79 74 68 6f 6e 0a 0a 69   6d 70 6f 72 74 20 6d 6d    ython..import.mm
00020   61 70 0a 69 6d 70 6f 72   74 20 63 6f 6e 74 65 78    ap.import.contex
00030   74 6c 69 62 0a 69 6d 70   6f 72 74 20 73 79 73 0a    tlib.import.sys.
00040   66 72 6f 6d 20 73 74 72   69 6e 67 20 69 6d 70 6f    from.string.impo
00050   72 74 20 70 72 69 6e 74   61 62 6c 65 0a 0a 0a 43    rt.printable...C
00060   48 55 4e 4b 20 3d 20 31   36 0a 0a 0a 64 65 66 20    HUNK...16...def.
.....
'''
import mmap
import contextlib
import sys
import string

CHUNK = 16
BYTE_SPLIT = '  '

def outp(s):
  sys.stdout.write(s)

def is_printable(x):
  return x in string.printable and x not in string.whitespace


def dump_line_in_hex(chunk, offset, special='.'):

  # print offset in HEX
  outp('%.5x%s' % (offset, BYTE_SPLIT))
  length = len(chunk)

  for i in range(length):
    outp('%02x ' % ord(chunk[i]))
    # put a space between first and last 8 bytes
    if i is 7:
      outp(BYTE_SPLIT)

  # put a missing split space if we got less than 8 bytes
  if i < 8:
      outp(BYTE_SPLIT)

  # fill missing bytes with spaces
  if length < CHUNK :
    outp('   '*(CHUNK - length))

  # a space between bytes and ASCII content
  outp(BYTE_SPLIT)
  for b in chunk:
    if is_printable(b):
      outp(b)
    else:
      outp(special)

  outp('\n')


def dump_in_hex(data):
  offset = 0

  while True:
    chunk = data.read(CHUNK)
    if not chunk:
      break

    dump_line_in_hex(chunk, offset)
    offset = offset + len(chunk)

if __name__ == '__main__':

  fname = sys.argv[1]
  with open(fname, 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
      dump_in_hex(m)
