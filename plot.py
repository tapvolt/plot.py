import argparse
import serial
import sys

# Credit to Dhananjay Balan https://blog.dbalan.in/blog/2019/02/23/resurracting-an-hp-7440a-plotter/index.html

def read_file(file):
    f = open(file, "r")
    return f.read()


def stitch(hpgl_string, buffer_length=1024):
    count = 0
    buffer = []
    instructions = hpgl_string.split(";")
    for ins in instructions:
        ins += ";"
        if count + len(ins) >= buffer_length:
            yield "".join(buffer)
            buffer = []
            count = len(ins)
        else:
            count += len(ins)
        buffer.append(ins)

    # send rest of the code
    yield "".join(buffer)


def exec_hpgl(hpgl_string, port):
    # remove the last IN; that vpype always adds and breaks my plotter
    body = stitch(hpgl_string.rpartition("IN;")[0])
    with serial.Serial(port, 9600, timeout=5) as plt:
        for ins in body:
            # For block sent, end with OA, which reports back current position on the pen
            plt.write((ins + "OA;").encode())
            c = bytearray()
            data = bytearray()
            while c.decode() != '\r':
                c = plt.read()
                data += c
            print("OA returns x, y, pen: {}".format(data.decode()))
            # We got data, mean OA got executed, so the instruction buffer is all consumed, ready to sent more.


def parse():
    parser = argparse.ArgumentParser(description="Plot a file via a serial port.")
    parser.add_argument("--file", type=str, metavar="image.hpgl", help="A path to or the HPGL file you would like to plot.")
    parser.add_argument("--port", type=str, metavar="/dev/tty.usbserial-1220", help="The serial port to use.")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    return args


def main():
    args = parse()
    hpgl_string = read_file(args.file)
    exec_hpgl(hpgl_string, args.port)


if __name__ == "__main__":
    main()
