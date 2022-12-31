# =============================================================================
# imported libraries
from paho.mqtt import client as mqtt
import time
import colorama 
from colorama import Fore
import random
import os
# =============================================================================
# Global constants

# => To referesh the cmd.
colorama.init(autoreset=True)

tcp_port = 1883
tcp_ssl_port = 8883
# =============================================================================
# Basic configurations

client_id = f'subscriber-client-id-{random.randint(0, 127)}'
broker_address = 'mqtt.eclipseprojects.io'
port = tcp_port
Qos = 2
username = f'mohamed-ashraf-wx'
password = f'mohamed-ashraf'

# Subscriber / Publisher Configurations
topic = 'mqtt_testing_python/chat_app/test1'
# =============================================================================
# Functions implementation

'''
    @brief Function to handle the files
'''
def file_dir_handle(dir_name=f'firmware_dir', file_name=f'firmware', file_extension=f'txt'):
    # Check if the file is already exsits
    if os.path.exists(f'./{dir_name}'):
        print(f'{Fore.RED}Directory {Fore.WHITE}`{dir_name}` {Fore.RED}already exisits!.')
    else:
        # Create the directory
        os.mkdir(dir_name)
        print(f'{Fore.GREEN}Created directory {Fore.WHITE}`{dir_name}` {Fore.GREEN}sucessfully.')
    # Create new file
    global file_path_name
    file_path_name = f'{dir_name}/{file_name}.{file_extension}'
    # Check if the file already exists.
    if os.path.exists(f'{file_path_name}'):
        print(f'{Fore.RED}File {Fore.WHITE}`{file_path_name}` {Fore.RED}already exisits!.')
    else:
        with open(f'{file_path_name}', 'w') as file:
            # write nothing to force the os creating the file.
            file.write(f'')

            if os.path.exists(f'{file_path_name}'):
                print(f'{Fore.GREEN}Created {Fore.WHITE}{file_name}.{file_extension} {Fore.GREEN}succesfully.')
            else:
                print(f'{Fore.RED}Could not create {Fore.WHITE}{file_name}.{file_extension}')

'''
    @brief Function to print the status on connection.
'''
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"{Fore.GREEN}Connection to the broker {Fore.WHITE}`{broker_address}` successful.")
    else:
        print(f"{Fore.RED}Connection to the broker {Fore.WHITE}`{broker_address}` failed.")

'''
    @brief Function to print the incoming message from the broker.
'''

def on_message(client, userdata, msg):
    global message
    message = msg.payload.decode('ascii')
    topic = msg.topic

    print(f'{Fore.GREEN}Received {Fore.WHITE}`{message}` {Fore.GREEN}on topic {Fore.WHITE}`{topic}`')
    
    with open(f'{file_path_name}', 'a') as firmware_file:
        firmware_file.write(f'{message}')
    firmware_file.close()

'''
    @brief Callback Function
'''
def on_publish(client, userdata, mid):
    pass

'''
    @brief Callback Function
'''
def on_subscribe(client, userdata, mid, granted_qos):
    pass

'''
    @brief Callback Function
'''
def on_unsubscribe(client, userdata, mid):
    pass

'''
    @brief Callback Function
'''
def on_disconnect(client, userdata, mid):
    pass


'''
    @brief Function to setup the basic configuration
'''
def mqtt_set_cfgs(
        client_id=None, 
        broker='mqtt.eclipseprojects.io', 
        port=1883, 
        Qos=2, 
        username=None, 
        password=None):
    # Set up the basic configurations
    client = mqtt.Client(client_id, clean_session=True)
    client.username_pw_set(username, password)
    # Callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe

    return client

'''
    @brief Function to setup the connection between the client & broker.
'''
def connect_mqtt():
    # Setting the configuration.
    client = mqtt_set_cfgs(
                client_id,
                broker_address,
                port,
                Qos,
                username,
                password)
    # Connect to the broker
    client.connect(broker_address, port, Qos)

    return client

'''
    @brief Function to subscribe to a topic to receive its messages.
'''
def subscribe(client=None):
    # Subscribe to the topic
    client.subscribe(topic)
    client.on_message = on_message

'''
    @brief Function to set and run the application.
'''
def run_app():
    try:
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
    except: 
        client.disconnect()
        client.loop_stop()
        print(f'{Fore.GREEN}Disconnected from broker {Fore.WHITE}`{broker_address}` - {Fore.GREEN}Client {Fore.WHITE}`{client_id}`')
# =============================================================================
# Program entry point

# Run the application from the entry point.
if __name__ == "__main__":

    file_dir_handle()
    # Run the MQTT application.
    run_app()
