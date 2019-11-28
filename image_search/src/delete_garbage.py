import sys, os, argparse
from tqdm import tqdm
import shutil
parser = argparse.ArgumentParser()
parser.add_argument('--path', type = str)

args = parser.parse_args()

def main() :
    path = args.path
    cur_dir = os.getcwd()
    target_path = os.path.join(cur_dir, path)
    path_list = os.listdir(target_path)
    pbar = tqdm(path_list)
    i = 0
    for dir in pbar :
        pbar.set_description('Deleted files : {}'.format(i))
        final_path = os.path.join(target_path, dir)
        if not os.path.isdir(final_path) :
            continue
        file_list = os.listdir(final_path)
        for file in file_list :
            if 'TIF' not in file and 'tif' not in file :
                os.remove(os.path.join(final_path, file))
                i += 1
            else :
                shutil.move(os.path.join(final_path, file), 'patent_images/{}'.format(file))
        shutil.rmtree(final_path)
    print('Deleted.')

if __name__ == "__main__" :
    main()