import sys

class CmdLineParser:
    def __init__(self):
        self.file_name = None

    def parse_frame_processing(self):
        if len(sys.argv) != 2:
            print("Usage: python3 frameProcessing.py [video file name]")
            exit()
        else:
            self.file_name = sys.argv[1]

        return self.file_name