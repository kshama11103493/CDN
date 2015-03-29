import os

class cachesize:
 def get_size(self):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk('home/varsha/Desktop/CD/minor/cache4/'):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

