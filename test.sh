sudo bash -c 'echo 0 > /proc/sys/kernel/randomize_va_space'

#python main.py taget target_address target_value input_file

#python main.py ./test/commandline/commandline 0x804a02c 0x1 ./test/commandline/input_commandline.json
#python main.py ./test/secret_number/secret_number 0x0000000000601044 0xa ./test/secret_number/input_secret_number.json
#python main.py ./test/simil_stonks/simil_stonks 0x000000000060104c 0xaa ./test/simil_stonks/input_simil_stonks.json
#python main.py ./test/snprintf1/snprintf1 0xffffcebc 500 ./test/snprintf1/input_snprintf1.json
#python main.py ./test/snprintf3/snprintf3 0x000000000060104c 0x7d9a22 ./test/snprintf3/input_snprintf3.json
python main.py ./test/test1/test1 0x0000000000601050 0x602030 ./test/test1/input_test1.json
#python main.py ./test/the_answer/the_answer 0x0000000000601078 0x2A ./test/the_answer/input_the_answer.json
#python main.py ./test/vuln/vuln 0x0000000000601048 0xffffffff ./test/vuln/input_vuln.json