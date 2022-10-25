import argparse
import  os
def delect(dir1,dir2):
  list2=os.listdir(dir2)
  list3=[]
  for i in list2:
      list3.append(i)

  list1=os.listdir(dir1)
  for i in list1:
      if i in list3:
        os.remove(dir1+ '\\'+i)
      else:
          continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delet same file in two folder')
    parse.add_argument('--deleted', '-d', help='input folder which files will be delet', required=True)
    parse.add_argument('--source', '-s', help='input folder which is source', required=True)
    args = parser.parse_args()
    dir1 = os.path.abspath(args.deleted)
    if not os.path.isdir(args.deleted):
        print('--input ({}) must be a folder.'.format(args.deleted))
        sys.exit(1)
    dir2 = os.path.abspath(args.source)
    if not os.path.isdir(args.source):
        print('--input ({}) must be a folder.'.format(args.source))
        sys.exit(1) 
    
    delect(dir1,dir2)
