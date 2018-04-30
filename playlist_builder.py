import os
import sys

from systems_list import systems_list, emu_dict


def clear_screen():
    """clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def set_system():
    # print all available systems
    for x in range(len(systems_list)):
        print(x, systems_list[x])

    # ask user to chose system
    system_id = input("Choose the system you want to create a playlist for: ")
    selected_system = systems_list[int(system_id)]
    return selected_system


def set_roms_dir():
    # ask user for directory containing ROMS
    print("\n")
    print("I need to know the exact path of the directory that your ROMs are stored in. This should look similar to the example below:")
    print("\n")
    print("-"*54)
    print("C:\\Users\\USERNAME\\Documents\\ROMs\\NES\\Licensed Releases")
    print("-"*54)
    print("\n")
    while True:
        roms_dir = input("Paste ROMs directory path here: ")
        if os.path.exists(roms_dir) is False:
            print("That directory doesn't appear to exist...")
        else:
            break
    return roms_dir
    

def set_core(selected_system):
    # ask user if they want to write cores into the playlist
    while True:
        print("\n")
        core_or_no = input("Would you like to write CORES to this playlist? Y/n: ").lower()
        if core_or_no == "y":
            # find installed cores
            print("\n")
            print("I need to know the exact path of the directory your CORES are stored in.  This should look similar to the example below: ")
            print("\n")
            print("-"*49)
            print("C:\\Users\\USERNAME\\AppData\\Roaming\\RetroArch\\cores")
            print("-"*49)
            print("\n")
            while True:
                cores_dir = input("Paste CORES directory path here: ")
                if os.path.exists(cores_dir) is False:
                    print("That directory doesn't appear to exist...")
                else:
                    break
            installed_cores = sorted(os.listdir(cores_dir))

            # print all installed cores
            print("\n")
            for x in range(len(installed_cores)):
                print(x, installed_cores[x])

            # ask user for core they would like to use
            print("\n")
            core_id = input("Select CORE for {}: ".format(selected_system))
            selected_core = (cores_dir + '\\' + installed_cores[int(core_id)])
            break
        if core_or_no == "n":
            selected_core = 'DETECT'
            break
        else:
            print("That is not a valid input.")
            continue
    return selected_core


def setup_check(selected_system, roms_dir, selected_core):
    while True:
        print("\n")
        print("The system you selected is: {}".format(selected_system))
        print("Your ROMs directory located at: {}".format(roms_dir))
        print("Your CORES directory is located at: {}".format(selected_core))
        print("\n")
        setup_check = input("Are these settings correct? Y/n: ").lower()
        if setup_check == "y":
            break
        if setup_check == "n":
            playlist_builder_loop()
        else:
            print("That is not a valid input.")
            continue


def find_core_name(selected_core):
    for core, name in emu_dict.items():
        if core in selected_core:
            core_name = name
            break
        else:
            core_name = 'DETECT'
    return core_name


def generate_playlist_file(selected_system, roms_dir, selected_core, core_name):
    zip_files = sorted(os.listdir(roms_dir))
    new_playlist_file = open((selected_system + ".lpl"), "w")

    first = True
    i = 0

    for zip_file in zip_files:
        if not os.path.isdir(os.path.join(roms_dir, zip_file)):
            if not first:
                new_playlist_file.write("\n")
            else:
                first = False

            # full path
            new_playlist_file.write(os.path.join(roms_dir, zip_file) + "\n")
            # name
            game_name = os.path.splitext(os.path.basename(zip_file))[0]
            game_name = game_name.split(' (')
            new_playlist_file.write(game_name[0] + "\n")
            # core's path
            new_playlist_file.write(selected_core + "\n")
            # core's name
            new_playlist_file.write(core_name + "\n")
            # crc placeholder
            new_playlist_file.write("DETECT" + "\n")
            # playlist's name
            new_playlist_file.write(selected_system + ".lpl")

            i += 1

    new_playlist_file.close()
    print("\n")
    print("Found: {} ROMS for {}".format(i, selected_system))
    print("Playlist complete!")
    print("\n")


def playlist_builder_loop():
    clear_screen()
    selected_system = set_system()
    clear_screen()
    roms_dir = set_roms_dir()
    clear_screen()
    selected_core = set_core(selected_system)
    clear_screen()
    setup_check(selected_system, roms_dir, selected_core)
    clear_screen()
    core_name = find_core_name(selected_core)
    generate_playlist_file(selected_system, roms_dir, selected_core, core_name)


def main(argv):
    if len(argv) > 0:
        for opt in argv:
            if opt == "--start":
                playlist_builder_loop()
            else:
                print('to initialize use cmd: playlist_builder.py [arg]')
                print('\'--start\' - starts the program')
                sys.exit()
    else:
        print("\n")
        print("-"*len("RetroArch Playlist Generator"))
        print("RetroArch Playlist Generator")
        print("-"*len("RetroArch Playlist Generator"))
        print("\n")
        input("Press any key to start program")
        playlist_builder_loop()


if __name__ == "__main__":
    main(sys.argv[1:])


