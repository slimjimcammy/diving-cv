import sys
from typing import Type

class CmdLineParser:
    def __init__(self):
        self.file_name = None
        self.input_directory = None
        self.output_directory = None
        self.frame_granularity = None

    def parse_frame_processing(self):
        if len(sys.argv) != 2:
            print("Usage: python3 frameProcessing.py [video file name]")
            exit()
        else:
            self.file_name = sys.argv[1]

        return self.file_name

    def parse_frame_extracting(self):
        if len(sys.argv) != 7:
            print("Usage: python3 frameExtracting.py [video directory] [frame granularity]")
            exit()
        else:
            self.directory = sys.argv[1]

            if sys.argv[1] == "--in":
                self.input_directory = sys.argv[2]
            else:
                print("Usage: python3 frameExtracting.py --in [input video directory] --out [output frame directory] --granularity [frame granularity]")
                exit()
            
            if sys.argv[3] == "--out":
                self.output_directory = sys.argv[4]
            else:
                print("Usage: python3 frameExtracting.py --in [input video directory] --out [output frame directory] --granularity [frame granularity]")
                exit()

            if sys.argv[5] == "--granularity":
                try:
                    self.frame_granularity = int(sys.argv[6])
                except TypeError:
                    print("Usage: python3 frameExtracting.py --in [input video directory] --out [output frame directory] --granularity [frame granularity]")
                    exit()
            else:
                print("Usage: python3 frameExtracting.py --in [input video directory] --out [output frame directory] --granularity [frame granularity]")
                exit()
        
        return self.input_directory, self.output_directory, self.frame_granularity
