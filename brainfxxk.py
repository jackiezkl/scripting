#!/usr/bin/python
# code is from jochasinga. did a very minor change.

tape = []
tape_pos = 0
code_pos = 0
code = ""
result = ""

def _scan(skip=False):
    global tape_pos
    global code_pos
    global result
    global code
    skipping = skip
    while tape_pos >= 0 and code_pos < len(code):
        if tape_pos >= len(tape):
            tape.append(0)
        if code[code_pos] == '[':
            code_pos += 1
            old_pos = code_pos
            skipping = tape[tape_pos] == 0
            while _scan(skipping):
                code_pos = old_pos
        elif code[code_pos] == ']':
            return tape[tape_pos] != 0
        else:
            if code[code_pos] == '+':
                tape[tape_pos] += 1
            elif code[code_pos] == '-':
                tape[tape_pos] -= 1
            elif code[code_pos] == '>':
                tape_pos += 1
            elif code[code_pos] == '<':
                tape_pos -= 1
            elif code[code_pos] == '.':
                result += chr(tape[tape_pos])
            elif code[code_pos] == ',':
                tape[tape_pos] = sys.stdin.read(1)
            else:
                pass

        # read further
        code_pos += 1

def interpret(code_str):
    _scan(code_str)

if __name__ == "__main__":
    import sys
    print ("Welcome to brainfxxk!")
    if len(sys.argv) > 1:
        print "Scanning..."
        with open(sys.argv[1], "r") as f:
            code += f.read()
    else:
        code += sys.stdin.readline()

    interpret(code)
    # print "Received:"
    # print code
    print ("Result: " + result)
