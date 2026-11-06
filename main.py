import os, shutil, json, csv, sys
from pathlib import Path

class Initialize:

    def operation_history(self, operation, status):
        data= {
            'Operation': operation,
            'Status': status
        }
        file_path = Path.joinpath(Path.cwd() / 'SmartFileManager' / 'reports' / 'operation_log.csv')
        str_file_path = file_path.as_posix()
        is_empty = not Path.exists(file_path) or os.path.getsize(file_path) == 0
        fieldnames = ['Operation', 'Status']
        with open(str_file_path, 'a+', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if is_empty:
                writer.writeheader()

            writer.writerow(data)

    def make_dirs(self):
        dir_paths = [
            os.path.join(os.getcwd(), 'SmartFileManager'),
            os.path.join(os.getcwd(), 'SmartFileManager', 'workspace'),
            os.path.join(os.getcwd(), 'SmartFileManager', 'workspace', 'documents'),
            os.path.join(os.getcwd(), 'SmartFileManager', 'workspace', 'images'),
            os.path.join(os.getcwd(), 'SmartFileManager', 'workspace', 'videos'),
            os.path.join(os.getcwd(), 'SmartFileManager', 'workspace', 'others'),
            os.path.join(os.getcwd(), 'SmartFileManager', 'backups'),
            os.path.join(os.getcwd(), 'SmartFileManager', 'metadata'),
            os.path.join(os.getcwd(), 'SmartFileManager', 'reports'),
            os.path.join(os.getcwd(), 'SmartFileManager', 'quarantine'),
        ]

        for i in dir_paths:
            try:
                os.mkdir(i)
                
            except:
                pass

        self.operation_history('Make Folders', 'Success')

    def json_writer(self):
        new_list = {'Files':[]}
        files = os.walk(os.path.join(os.getcwd(), 'SmartFileManager', 'workspace'))
        for root, dir, file in files:
            for i in file:
                data = os.stat(os.path.join(root, i))
                set = {
                    'Name' : i,
                    'Path' : os.path.join(root, i),
                    'Size' : data.st_size,
                    'Extension' : os.path.splitext(i)[1],
                    'Modified' : data.st_mtime
                }
                new_list["Files"].append(set)
        return new_list

    def json_loader(self):
        json_file = os.path.join(os.getcwd(), 'SmartFileManager', 'metadata', 'file_index.json')
        with open(json_file, 'r') as f:
            file = json.load(f)

        return file

    def organize(self):
        dir_path = os.path.join(os.getcwd(), 'SmartFileManager')
        with os.scandir(dir_path) as f:
            for i in f:
                if i.is_file():
                    counter = 1
                    new_name = i.name
                    loop = True                
                    while loop:
                        available = True
                        files = os.walk(os.path.join(os.getcwd(), 'SmartFileManager', 'workspace'))
                        for root, dir, file in files:
                            if new_name in file:
                                new_name = os.path.splitext(new_name)[0] + str(counter) + os.path.splitext(new_name)[1]
                                counter += 1
                                available = False

                        if available:
                            loop = False

                    if os.path.splitext(new_name)[1] == '.pdf':
                        src = os.path.join(dir_path, i.name)
                        dst = os.path.join(os.getcwd(),'SmartFileManager', 'workspace', 'documents', new_name)
                        shutil.move(src, dst)
                    elif os.path.splitext(new_name)[1] == '.png':
                        src = os.path.join(dir_path, i.name)
                        dst = os.path.join(os.getcwd(),'SmartFileManager', 'workspace', 'images', new_name)
                        shutil.move(src, dst)
                    elif os.path.splitext(new_name)[1] == '.mp4':
                        src = os.path.join(dir_path, i.name)
                        dst = os.path.join(os.getcwd(),'SmartFileManager', 'workspace', 'videos', new_name)
                        shutil.move(src, dst)
                    else:
                        src = os.path.join(dir_path, i.name)
                        dst = os.path.join(os.getcwd(),'SmartFileManager', 'workspace', 'others', new_name)
                        shutil.move(src, dst)
        new_list = self.json_writer()
        with open(os.path.join(os.getcwd(), 'SmartFileManager', 'metadata', 'file_index.json'), 'w') as g:
            json.dump(new_list, g, indent=4, ensure_ascii=False)
        self.operation_history('File Organize', 'Success')

    def scaner(self):
        new_list = self.json_writer()

        new_dict = {"Files":[]}


        file_index_path = os.path.join(os.getcwd(), 'SmartFileManager', 'metadata', 'file_index.json')
        with open(file_index_path, 'r') as h:
            old_list = json.load(h)
            for i, j in old_list.items():
                for k in j:
                    avai = False
                    for x, y in new_list.items():
                        for z in y:
                            if k["Name"] == z["Name"]:
                                avai = True
                                break
                    if avai:
                        if z["Size"] == k["Size"] and z["Modified"] == k["Modified"]:
                            new_dict["Files"].append(k)
                        else:
                            new_dict['Files'].append(z)
                    else:
                        report_path = os.path.join(os.getcwd(), 'SmartFileManager', 'reports', 'inventory.csv')
                        is_empty = not os.path.exists(report_path) or os.path.getsize(report_path) == 0
                        fieldnames = ["Name", "Path", "Size", "Extension", "Modified", "Status"]
                        k["Status"] = "Missing"

                        with open(report_path, 'a', newline="", encoding="utf-8") as p:
                            writer = csv.DictWriter(p, fieldnames=fieldnames)
                            if is_empty:
                                writer.writeheader()
                                writer.writerow(k)
                            else:
                                writer.writerow(k)

        with open(file_index_path, 'w') as l:
            json.dump(new_dict, l, indent=4, ensure_ascii=False)
        self.operation_history('Scanned Files', 'Success')

    def search(self, file_name):
        json_file = self.json_loader()

        detail = []

        for i, j in json_file.items():
            for k in j:
                if k["Name"] == file_name:
                    detail.append(k)
        return detail[0]

    def create_backup(self):
        src = os.path.join(os.getcwd(), 'SmartFileManager')
        dst_temp = os.path.join(src, 'backups')
        dir_list = os.listdir(dst_temp)
        count = 1
        name = 'backup_000'
        loop = True

        while loop:
            if name in dir_list:
                name = name[:7] + str(f'{count:03d}')
                count += 1
            else:
                loop = False
        
        dst = os.path.join(dst_temp, name)

        shutil.copytree(src, dst,ignore=shutil.ignore_patterns('backups', 'reports'))
        self.operation_history('Create Backup', 'Success')

    def list_backup(self):
        return os.listdir(os.path.join(os.getcwd(), 'SmartFileManager', 'backups'))
    
    def restore_backup(self, backup_001):
        src = Path.joinpath(Path.cwd()) / 'SmartFileManager' / 'backups' / backup_001
        with os.scandir(Path.joinpath(Path.cwd()/'SmartFileManager')) as f:
            dirs = [i for i in f if i.is_dir() and i.name != 'backups' and i.name != 'reports']        
        for j in dirs:
            shutil.rmtree(j, ignore_errors=True)
        dst = Path.joinpath(Path.cwd()/'SmartFileManager')
        shutil.copytree(src, dst, dirs_exist_ok=True)
        self.operation_history('Restore Backup', 'Success')

    def duplicet_finder(self):
        with open(Path.joinpath(Path.cwd()/'SmartFileManager'/'metadata'/'file_index.json')) as f:
            data = json.load(f)
            file_list = []
            duplicates = []
            for i, j in data.items():
                for k in j:
                    file_list.append(k)
            for x in range(len(file_list)):
                for y in range(x+1, len(file_list)):
                    if file_list[x]["Name"] == file_list[y]["Name"] and file_list[x]["Size"] == file_list[y]["Size"]:
                        duplicates.append(file_list[y])
                        break
            report_path = Path.joinpath(Path.cwd()/'SmartFileManager'/'reports'/'inventory.csv')
            is_empty = not Path.exists(report_path) or os.path.getsize(report_path) == 0
            fieldnames = ["Name", "Path", "Size", "Extension", "Modified", "Status"]
            
            with open(report_path, 'a') as g:
                writer = csv.DictWriter(g, fieldnames=fieldnames)
                if is_empty:
                    writer.writeheader()
                    if duplicates:
                        for p in duplicates:
                            p["Status"] = 'Duplicate'
                            writer.writerow(p)
                else:
                    for p in duplicates:
                        p["Status"] = 'Duplicate'
                        writer.writerow(p)
                self.operation_history('Duplicated Fined', 'Success')

    def quarantine(self, file_path):
        p = Path(file_path)
        json_data = {'Files': []}
        dst_path = str(Path.joinpath(Path.cwd() / 'SmartFileManager' / 'quarantine' / p.name))
        data_path = str(Path.joinpath(Path.cwd() / 'SmartFileManager' / 'quarantine' / 'data.json'))

        with open(data_path, 'a+') as f:
            try:
                data = json.load(f)
                for i, j in data.items():
                    for k in j:
                        json_data['Files'].append(k)
            except:
                pass

        set = {
            'Name' : p.name,
            'Src_Path' : file_path,
            'Dst_Path' : dst_path
        }

        json_data['Files'].append(set)

        with open(data_path, 'w') as g:
            json.dump(
                json_data,
                g,
                indent=4,
                ensure_ascii=False
            )

        shutil.move(file_path, dst_path)
        self.operation_history('Quarantined', 'Success')

    def restore_quarantine(self, file_name):
        all_files = {'Files': []}
        json_file = Path.joinpath(Path.cwd() / 'SmartFileManager' / 'quarantine' / 'data.json')
        json_str_path = json_file.as_posix()
        with open(json_str_path, 'r') as f:
            try:
                data = json.load(f)
                for i, j in data.items():
                    for k in j:
                        all_files['Files'].append(k)
            except:
                print('No quarantine file exist')
                sys.exit()
        for x in all_files['Files']:
            if x['Name'] == file_name:
                shutil.move(x['Dst_Path'], x['Src_Path'])
                all_files['Files'].remove(x)
        with open(json_str_path, 'w') as g:
            json.dump(
                all_files,
                g,
                indent=4,
                ensure_ascii=False
            )
        self.operation_history('Rstore from Quarantine', 'Success')

    def view_op_history(self):
        log_path = Path.joinpath(
            Path.cwd() /
            'SmartFileManager' /
            'reports' /
            'operation_log.csv'
        )
        str_log_path = log_path.as_posix()

        with open(str_log_path, 'r') as f:
            reader = csv.DictReader(f)
            for i in reader:
                print(i['Operation'], ' = ', i['Status'] )
                               
    def gen_report(self):
        total_file = 0
        root_dir = os.path.join(os.getcwd(), 'SmartFileManager')
        files = os.walk(root_dir)
        for root, dir, file in files:
            total_file += len(file)
        total_size = os.path.getsize(root_dir)
        total_dirs = len(os.listdir(os.path.join(root_dir, 'backups')))
        total_qua = 0
        with os.scandir(os.path.join(root_dir, 'quarantine')) as f:
            for i in f:
                if i.is_file():
                    total_qua += 1

        
        print('=========== Report ==========\n\n')
        print(
            f'{'Total file':<30} : {total_file}\n'
            f'{'Total size':<30} : {total_size}\n'
            f'{'Total backup':<30} : {total_dirs}\n'
            f'{'Total quarantine':<30} : {total_qua}'
        )


if __name__ == '__main__':

    initial = Initialize()

    print(f"""
========================================
    SMART FILE MANAGEMENT SYSTEM
========================================

1. Initialize Workspace
2. Organize Files
3. Scan Files
4. Search Files
5. View File Metadata
6. Create Backup
7. List Available Backups
8. Restore Backup
9. Find Duplicate Candidates
10. Move File to Quarantine
11. Restore from Quarantine
12. View Operation History
13. Generate Report
14. Exit

Select an option:
    """)

    choice = input('= ')

    if choice == '1':
        initial.make_dirs()
    elif choice == '2':
        initial.organize()
    elif choice == '3':
        initial.scaner()
    elif choice == '4' or choice == '5':
        file_name = input('Enter File name : ')
        detail = initial.search(file_name)
        if detail:
            print('Found')
            for i, j in detail.items():
                print(i, '=', j)
        else:
            print('File not found')
    elif  choice == '6':
        initial.create_backup()
    elif choice == '7':
        backup = initial.list_backup()
        for i in backup:
            print(i)
    elif choice == '8':
        backup = initial.list_backup()
        for i in backup:
            print(i)
        item = input('Enter backup name: ')
        if item  in backup:
            initial.restore_backup(item)
        else:
            print('Invalid Backup Name')
    elif choice == '9':
        initial.duplicet_finder()
    elif choice == '10':
        files = os.walk(Path.joinpath(Path.cwd()/'SmartFileManager'))
        for root, dir, file in files:
            for i in file:
                print(root+'/'+i)
        file_path = input('Copy a file path and paste here : \n = ')
        initial.quarantine(file_path)
    elif choice == '11':
        json_file = Path.joinpath(Path.cwd() / 'SmartFileManager' / 'quarantine' / 'data.json')
        json_str_path = json_file.as_posix()        
        try:
            with open(json_str_path, 'r') as f:
                data = json.load(f)
                for i, j in data.items():
                    if len(j) > 0:
                        for k in j:
                            print(k['Name'])
                        qu_file = input('Enter Name from upper: ')
                        initial.restore_quarantine(qu_file)
                    else:
                        raise Exception
                    
        except:
            print('No quarantine file exist')
            sys.exit()
    elif choice == '12':
        initial.view_op_history()
    elif choice == '13':
        initial.gen_report()
    else:
        sys.exit()       






