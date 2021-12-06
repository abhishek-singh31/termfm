import os


def print_dir(dir_name):
    return("📁 " + dir_name)


def print_file(file_name):
    return("📄 " + file_name)


def get_input(buffer):
    return 


def get_folder_from_path(src):
    return src.split('/')[-1]


def get_menu_selection(data, selection):
    folder_index = 0  # which tuple we are currently at
    contents_index = 0  # to search in folders list or files list of that tuple
    final_index = 0  # position of selected file/folder in its list

    # Final position of element will always be of the form data[folder_index][contents_index][final_index] 

    for i in range(len(selection) - 1):
        for j in range(selection[i]):
            folder_index += find_skips(data, folder_index)[0]
        folder_index += 1
    folder_index -= 1

    if selection[-1] >= len(data[folder_index][1]):
        # search inside files list
        contents_index = 2
        final_index = selection[-1] - len(data[folder_index][1])
    else:
        contents_index = 1
        final_index = selection[-1]

    selection_name = data[folder_index][contents_index][final_index]
    selection_path = os.path.join(data[folder_index][0], selection_name)
    
    return_dict = {'path': selection_path, 'name': selection_name, 'type': ""}

    path=find(str(data[folder_index][contents_index][final_index]),data[0][0])
    return path


    if os.path.isfile(selection_path):
        return_dict['type'] = "file"
    else:
        return_dict['type'] = "folder"

    return return_dict

    # print(folder_index, contents_index, final_index)
    # print(data[folder_index][contents_index][final_index])
    # print(selection)



def find_skips(data, index):
    if len(data[index][1]) == 0:
        return [1, 0]

    output = [1, 0]
    sum = 0

    for i in range(len(data[index][1])):
        if index == 7:
            print(index+sum+1)
        rec = find_skips(data, index+sum+1)
        sum += rec[1] + 1
        output[0] += rec[0]
    
    output[1] = len(data[index][1])

    return output


