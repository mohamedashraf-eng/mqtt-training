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
client_id = f'publisher-client-id-{random.randint(0, 127)}'
broker_address = 'mqtt.eclipseprojects.io'
port = tcp_port
Qos = 2
username = f'mohamed-ashraf-wx'
password = f'mohamed-ashraf'

# Subscriber / Publisher Configurations
topic = 'mqtt_testing_python/chat_app/test1'
# =============================================================================
# Functions implementation

firmware = []
def load_firmware(dir_name=None, file_name=None, file_extension=None):

    file_path_name = f'{dir_name}/{file_name}.{file_extension}'
    with open(f'CAN_PROTOCOL_TEST.hex', 'r') as file:
        for line in file.readlines():
            firmware.append(line)

    print(f'{Fore.GREEN}Loading the firmware done.')

'''
    @brief Callback Function to print the status on connection.
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
        client_id='0', 
        broker='mqtt.eclipseprojects.io', 
        port=1883, 
        Qos=2, 
        username=None, 
        password=None):

    # Constructing setter


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
    @brief Function to publish (send) a message to the broker
           with the specified topic. 
'''
def publish(client=None, topic=None, message=None):
    # Publish the message
    result = client.publish(topic, message)
    # Get the status
    status = result[0]
    if status == 0:
        print(f"{Fore.GREEN} Published {Fore.WHITE}`{message}` {Fore.GREEN}on Topic {Fore.WHITE}`{topic}`")
    else:
        print(f"{Fore.RED} Failed to Publish {Fore.WHITE}`{message}` {Fore.RED}on Topic {Fore.WHITE}`{topic}`")

'''        
    @brief Function to subscribe to a topic to receive its messages.
'''
def subscribe(client=None, topic=None):
    # Subscribe to the topic
    client.subscribe(topic)
    client.on_message = on_message

'''
    @brief Function to set and run the application.
'''
def run_app():

    pub_topic = f'{topic}/client1-pub'
    sub_topic = f'{topic}/client2-pub'

    try:
        client = connect_mqtt()

        subscribe(client, sub_topic)
        client.loop_start()

        time.sleep(1)

        while True:
            #msg = str(input("Enter: "))
            msg = "Hello!"

            publish(client, pub_topic, msg)

            time.sleep(1)

    except: 
        client.disconnect()
        client.loop_stop()
        print(f'{Fore.GREEN}Disconnected from broker {Fore.WHITE}`{broker_address}` - {Fore.GREEN}Client {Fore.WHITE}`{client_id}`')
        
# =============================================================================
# Program entry point

# Run the application from the entry point.
if __name__ == "__main__":
    
    load_firmware(file_name=f'CAN_PROTOCOL_TEST', file_extension=f'hex')
    # Run the MQTT application.
    run_app()

