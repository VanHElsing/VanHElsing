import sys
import re

REGEX_LINE = re.compile('\s*([0-9]+) ([0-9]+.[0-9]+)\s*')

def main():
    result = []
    
    with open('program.out', 'r') as f_in:
        while True:
            line = f_in.readline()
            if line == "":
                break
            
            matches = REGEX_LINE.match(line)
            if matches is None:
                continue
            
            strat_i, runtime = int(matches.group(1)), float(matches.group(2))
            strat_i -= 1
            
            if runtime == 0.0:
                continue
            
            result.append((strat_i, runtime))
    
    print result

if __name__ == '__main__':
    sys.exit(main())
