#codgin: utf8
import sys
import lib
o = lib.get_api()
o.update_status(sys.argv[1])
