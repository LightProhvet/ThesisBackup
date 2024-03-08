



input_closed = False
input_open = False
input_start = False
input_stop = False
output = ['none', 'open', 'close']
do = 'none'
max_count = 10
count = 0

def check_inputs():
    pass

def reset_inputs():
    input_closed = False
    input_open = False
    input_start = False
    input_stop = False
while True:
    if input_start:
        play = True
    while play:
        check_inputs()
        if input_stop or count >= max_count:
            reset_inputs()
            do = output[0]
            play = False
        if input_open and not input_closed:
            do = output[1]
        elif input_closed:
            do = output[2]