import os
import requests
import sys

try:    
    def check_validity(target):
        target_type = str()
        validity_status = False
        if target.startswith('http://') or target.startswith('https://'):
            # Remove 'http://' or 'https://'
            domain_with_port = target.split('://', 1)[-1]
            domain = domain_with_port.split(':', 1)[0]
            port = domain_with_port.split(':', 1)[-1]

            if domain.count('.') == 3:
                # Check if it is a valid IP address
                target_type = 'ip'
                # check if it is a valid port
                if port.isdigit() and 0 <= int(port) <= 65535:
                    validity_status = True

                parts = domain.split('.', -1)

                for part in parts:
                    if part.isdigit() and 0 <= int(part) <= 255:
                        validity_status = True
                    else:
                        validity_status = False

            elif ('www' in domain and domain.count('.') == 2) or ('www' not in domain and domain.count('.') == 1):
                # Check if it is a valid URL
                target_type = 'url'

                if port.isdigit() and 0 <= int(port) <= 65535:
                    validity_status = True

        else:
            validity_status = False
            target_type = 'no protocol'

        return validity_status, target_type


    def probe(target):
        url = target

        try:
            response = requests.head(url, timeout=5)
            status = response.status_code
            if status < 400:
                # print('Status Code: {}'.format(status))
                return True
            else:
                # print('Status Code: {}'.format(status))
                return False

        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
            return False


    def user_option_1(target):
        alive_targets = list()
        dead_targets = list()
        invalid_targets = list()
        valid_targets = list()

        if 'http://' in target and ':80' not in target:
            if target.count(':') == 1:
                padded_target = target + ':80'
            else:
                padded_target = target
        elif 'https://' in target and ':443' not in target:
            if target.count(':') == 1:
                padded_target = target + ':443'
            else:
                padded_target = target
        elif "://" not in target:
            if ":80" in target:
                padded_target = 'http://{}'.format(target)
            elif ":443" in target:
                padded_target = 'http://{}'.format(target)
            else:
                padded_target = target
        else:
            padded_target = target

        validity_status, target_type = check_validity(padded_target)

        if target_type == 'no protocol':
            print('\n')
            print('==============================ERROR===============================')
            print('Protocol to target {} must be mentioned - http or https'.format(target))
            print('==================================================================')

        if target_type == 'url' and 'www' not in target:
            domain = padded_target.split('://', 1)[-1]
            protocol = padded_target.split('://', 1)[0]
            padded_target = '{}://www.{}'.format(protocol, domain)

        if validity_status:
            valid_targets.append(target)
            web_status = probe(padded_target)
            if web_status:
                alive_targets.append(target)
                return valid_targets, invalid_targets, alive_targets, dead_targets
            else:
                dead_targets.append(target)
                return valid_targets, invalid_targets, '', dead_targets
        else:
            invalid_targets.append(target)
            return valid_targets, invalid_targets, alive_targets, dead_targets


    def user_option_2(target_file):
        cwd = os.getcwd()
        file_path = '{}/{}'.format(cwd, target_file)
        targets = list()

        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    targets = list()
                    for line in f:
                        target = line.strip()
                        if target:
                            if target not in targets:
                                targets.append(target)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print('\n')
            print('==========================================ERROR===========================================')
            print('The file {} does not exist'.format(target_file))
            print('==========================================================================================')
            exit()

        padded_targets = list()

        for i in targets:
            if 'http://' in i and ':80' not in i:
                if i.count(':') == 1:
                    padded_target = i + ':80'
                    padded_targets.append(padded_target)
                else:
                    padded_targets.append(i)
            elif 'https://' in i and ':443' not in i:
                if i.count(':') == 1:
                    padded_target = i + ':443'
                    padded_targets.append(padded_target)
                else:
                    padded_targets.append(i)
            elif "://" not in i:
                if ":80" in i:
                    padded_target = 'http://' + i
                    padded_targets.append(padded_target)
                elif ":443" in i:
                    padded_target = 'http://' + i
                    padded_targets.append(padded_target)
                else:
                    padded_targets.append(i)
            else:
                padded_targets.append(i)

        alive_targets = list()
        dead_targets = list()
        invalid_targets = list()
        valid_targets = list()
        protocol = int()
        domain = str()
        parts = list()

        index = -1
        for i in padded_targets:
            padded_target = str()
            index = index + 1
            print('\n')
            print('------------------------------------------------------------------------------')
            print('#Target {}'.format(index+1))
            print('Target: {}'.format(targets[index]))
            print('Padded Target: {}'.format(i))

            actual_target = targets[index]
            validity_status, target_type = check_validity(i)

            print('Validity Status: {}'.format(validity_status))
            print('Target Type: {}'.format(target_type))

            if target_type == 'no protocol':
                padded_target = target_type
                print('====================================ERROR=====================================')
                print(
                    'Protocol to target {} must be mentioned - http or https'.format(targets[index]))
                print('==============================================================================')

            elif target_type == 'url' and 'www' not in i:
                parts = i.split('://')
                protocol = parts[0]
                domain = parts[1]

                if not domain.startswith('www'):
                    domain = 'www.' + domain

                padded_target = '{}://{}'.format(protocol, domain)

            elif target_type == 'ip':
                padded_target = i

            else:
                padded_target = i

            if validity_status:
                valid_targets.append(actual_target)
                web_status = probe(padded_target)
                if web_status:
                    alive_targets.append(actual_target)
                elif not web_status:
                    dead_targets.append(actual_target)
            else:
                invalid_targets.append(targets[index])

            print('------------------------------------------------------------------------------')

        return valid_targets, invalid_targets, alive_targets, dead_targets


    def inputs():

        try:
            print('Choose an option below:')
            print('1: For a single target')
            print('2: For multiple targets')
            try:
                user_option = int(input('Enter Your Option: '))
                alive_targets = list()

                if user_option == 1:
                    target = input('Target address: ')
                    valid_targets, invalid_targets, alive_targets, dead_targets = user_option_1(
                        target)
                    return valid_targets, invalid_targets, alive_targets, dead_targets
                elif user_option == 2:
                    target = input('Provide the exact file name: ')
                    valid_targets, invalid_targets, alive_targets, dead_targets = user_option_2(
                        target)
                    return valid_targets, invalid_targets, alive_targets, dead_targets
                else:
                    print('\n')
                    print('==========================================ERROR===========================================')
                    print("Invalid input. Please enter either 1 or 2.")
                    print('==========================================================================================')
                    exit()

            except ValueError:
                print('\n')
                print('==========================================ERROR===========================================')
                print("Invalid input. Please enter an integer.")
                print('==========================================================================================')
                exit()

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Exiting gracefully...")
            sys.exit(0)

    # main block

    title = r"""
    ====================================================================================================

                        \ \      / / ____| __ )|  _ \| | | | |   / ___|| ____|
                         \ \ /\ / /|  _| |  _ \| |_) | | | | |   \___ \|  _|  
                          \ V  V / | |___| |_) |  __/| |_| | |___ ___) | |___ 
                           \_/\_/  |_____|____/|_|    \___/|_____|____/|_____|

    ====================================================================================================            

    """
    print(title)

    valid_targets, invalid_targets, alive_targets, dead_targets = inputs()

    if len(alive_targets) > 0:
        print('\n')
        print('================================ALIVE TARGETS=================================')
        print('The below target(s) are alive: ')
        for i in alive_targets:
            print(i)
        print('==============================================================================')
    else:
        print('\n')
        print('================================ALIVE TARGETS=================================')
        print('There are no alive target(s)')
        print('==============================================================================')

    if len(dead_targets) > 0:
        print('\n')
        print('=================================DEAD TARGETS=================================')
        print('The below target(s) are dead: ')
        for i in dead_targets:
            print(i)
        print('==============================================================================')
    else:
        print('\n')
        print('=================================DEAD TARGETS=================================')
        print('There are no dead target(s)')
        print('==============================================================================')

    if len(invalid_targets) > 0:
        print('\n')
        print('===============================INVALID TARGETS================================')
        print('The below target(s) are invalid')
        for i in invalid_targets:
            print(i)
        print('==============================================================================')
    else:
        print('\n')
        print('===============================INVALID TARGETS================================')
        print('There are no invalid target(s)')
        print('==============================================================================')

    if len(valid_targets) > 0:
        print('\n')
        print('================================VALID TARGETS=================================')
        print('The below target(s) are alive: ')
        for i in valid_targets:
            print(i)
        print('==============================================================================')
    else:
        print('\n')
        print('================================VALID TARGETS=================================')
        print('There are no valid target(s)')
        print('==============================================================================')

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected. Exiting gracefully...")
    sys.exit(0)