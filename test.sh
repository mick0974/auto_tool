sudo bash -c 'echo 0 > /proc/sys/kernel/randomize_va_space'

#python main.py ./test/the_answer/the_answer 0x0000000000601078 0x2A ./test/the_answer/input_the_answer.json
#python main.py ./test/snprintf1/snprintf1 0xffffd5f8 500 ./test/snprintf1/input_snprintf1.json
python main.py ./test/commandline/commandline 0x804a030 0x1 ./test/commandline/input_commandline.json
#python main.py ./test/secret_number/secret_number 0x000000000060104c 0xa ./test/secret_number/input_secret_number.json
#python main.py ./test/simil_stonks/simil_stonks 0x0000000000601054 0xaa ./test/simil_stonks/input_simil_stonks.json
#python main.py ./test/snprintf2/snprintf2 0x000000000060105c 0xcc0 ./test/snprintf2/input_snprintf2.json
#python main.py ./test/vuln/vuln 0x0000000000601060 0xffffffff ./test/vuln/input_vuln.json