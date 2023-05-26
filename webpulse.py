import os
import requests
import sys

try:    
    # Function to check the validity of a target URL or IP address
    def check_validity(target):
        target_type = str() # Variable to store the type of target
        validity_status = False # Variable to store the validity status
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
            # Invalid target without protocol
            validity_status = False
            target_type = 'no protocol'

        return validity_status, target_type


    def probe(target):
        # Function to probe a target URL or IP address
        url = target

        try:
            response = requests.head(url, timeout=5)
            status = response.status_code
            if status < 400 and status>= 200:
                # Successful response
                return True
            else:
                # Unsuccessful response
                return False

        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
             # Exception occurred during the request
            return False


    def user_option_1(target):
        # Initialize lists to store different types of targets
        alive_targets = list()
        dead_targets = list()
        invalid_targets = list()
        valid_targets = list()

        # Determine the appropriate protocol and port based on the target URL
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
        
        # Check the validity of the target and get the target type
        validity_status, target_type = check_validity(padded_target)

        # Handle cases where target type is not valid
        if target_type == 'no protocol':
            print('\n')
            print('==============================ERROR===============================')
            print('Protocol to target {} must be mentioned - http or https'.format(target))
            print('==================================================================')

        # Handle cases where target type is URL and doesn't contain 'www'
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
            # Determine the appropriate protocol and port for each target URL
            
            if 'http://' in i and ':80' not in i:
                # If 'http://' is present and port 80 is not specified, add ':80' to the target URL
                if i.count(':') == 1:
                    padded_target = i + ':80'
                    padded_targets.append(padded_target)
                else:
                    padded_targets.append(i)
            elif 'https://' in i and ':443' not in i:
                 # If 'https://' is present and port 443 is not specified, add ':443' to the target URL
                if i.count(':') == 1:
                    padded_target = i + ':443'
                    padded_targets.append(padded_target)
                else:
                    padded_targets.append(i)
            elif "://" not in i:
                # If no protocol is specified in the target URL
                if ":80" in i:
                    padded_target = 'http://' + i
                    padded_targets.append(padded_target)
                elif ":443" in i:
                    padded_target = 'http://' + i
                    padded_targets.append(padded_target)
                else:
                    padded_targets.append(i)
            else:
                 # If the target URL already contains the protocol, add it as it is
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

            actual_target = targets[index]
            validity_status, target_type = check_validity(i)
            
            print('Target Type: {}'.format(target_type))

            if target_type == 'no protocol':
                # If the target URL is missing the protocol (http:// or https://)
                padded_target = target_type
                print('====================================ERROR=====================================')
                print(
                    'Protocol to target {} must be mentioned - http or https'.format(targets[index]))
                print('==============================================================================')

            elif target_type == 'url' and 'www' not in i:
                # If the target type is a URL and 'www' is not present in the target URL
                parts = i.split('://')
                protocol = parts[0]
                domain = parts[1]

                if not domain.startswith('www'):
                    domain = 'www.' + domain

                padded_target = '{}://{}'.format(protocol, domain)

            elif target_type == 'ip':
                # If the target type is an IP address
                padded_target = i

            else:
                # For other target types, add the target URL as it is
                padded_target = i

            if validity_status:
                # If the target URL is valid
                valid_targets.append(actual_target)
                web_status = probe(padded_target)
                
                if web_status:
                    # If the target is reachable
                    alive_targets.append(actual_target)
                    
                elif not web_status:
                    # If the target is not reachable
                    dead_targets.append(actual_target)
            else:
                # If the target URL is invalid
                invalid_targets.append(targets[index])

            print('------------------------------------------------------------------------------')

        return valid_targets, invalid_targets, alive_targets, dead_targets


    def inputs():
        print('Choose an option below:')
        print('1: For a single target')
        print('2: For multiple targets')
        
        try:
            user_option = int(input('Enter Your Option: '))
            alive_targets = list()
            
            if user_option == 1:
                target = input('Target address: ')
                # User selected option 1: Single target
                # Call the user_option_1 function to process the target
                valid_targets, invalid_targets, alive_targets, dead_targets = user_option_1(
                    target)
                return valid_targets, invalid_targets, alive_targets, dead_targets
            
            elif user_option == 2:
                target = input('Provide the exact file name: ')
                # User selected option 2: Multiple targets
                # Call the user_option_2 function to process the file containing targets
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


    # main block

    # Displaying a title banner
    title = r"""
    ====================================================================================================

                        \ \      / / ____| __ )|  _ \| | | | |   / ___|| ____|
                         \ \ /\ / /|  _| |  _ \| |_) | | | | |   \___ \|  _|  
                          \ V  V / | |___| |_) |  __/| |_| | |___ ___) | |___ 
                           \_/\_/  |_____|____/|_|    \___/|_____|____/|_____|

    ====================================================================================================            

    """
    print(title)

    # Getting inputs for targets
    valid_targets, invalid_targets, alive_targets, dead_targets = inputs()

    # Printing alive targets if any
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

    # Printing dead targets if any
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

    # Printing invalid targets if any
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

    # Printing valid targets if any
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
    # Handling KeyboardInterrupt gracefully
    print("\nKeyboardInterrupt detected. Exiting gracefully...")
    sys.exit(0)