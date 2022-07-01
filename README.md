# Tutorial on how to build an IoT-Intercom
This IoT device makes it possible to receive a message sent from a mobile phone or other network device and then reply with button clicks. Following project is the result of an IoT course at LNU Sweden. My name is Alexander Ström (as227nn) and following is a tutorial on how to build your own!

## What is this? And how does it work?
This device receives a message sent by a Node-RED dashboard, Node-RED is a flow based programming environment which handles all the traffic from and to the device as well as the cloud solution chosen in this project. When a message is sent, it will be shown on the IoT-Intercom as well as an LED light and buzzer sound. The person who has the device will be able to choose an answer that will be sent back to Node-RED. Node-RED will only store the current question, answer and time to answer while Ubidots will be used to store all messages, also giving an average value of answer time. This tutorial will explain how to set up all this.

