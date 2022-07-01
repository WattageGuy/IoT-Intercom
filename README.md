# Tutorial on how to build an IoT-Intercom
## Short Overview
This IoT device makes it possible to receive a message sent from a mobile phone or other network device and then reply with button clicks. Following project is the result of an IoT course at LNU Sweden. My name is Alexander Ström (as227nn) and following is a tutorial on how to build your own!

## What is this? And how does it work? (Detailed Overview)
This device receives a message sent by a Node-RED dashboard, Node-RED is a flow based programming environment which handles all the traffic from and to the device as well as the cloud solution chosen in this project. When a message is sent, it will be shown on the IoT-Intercom as well as an LED light and buzzer sound. The person who has the device will be able to choose an answer that will be sent back to Node-RED. Node-RED will only store the current question, answer and time to answer while Ubidots will be used to store all messages, also giving an average value of answer time. This tutorial will explain how to set up all this.


**How much time it might take to do (approximation):**

Considering everything working as expected without any unmentioned problems with solutions this project might take 2 days, or approximation 15-20 hours to complete.

## Origin
### Project idea and purpose:
This project idea started from an earlier software solution called "Matroparen" (Enligsh: Food announcements), that acted as a way to tell everybody at home that the food was to be served. This was pretty simple and built upon webhooks messaging devices. But now it wanted something more complex and connected to the IoT spectrum with some hardware and circuitry involved. The way this device is built also makes it possible to collect data such of how long it takes for the person to answer the question. 

### Insights
Completing this project will give a brief understanding of the IoT world as well as some basic circuitry, cloud solutions and programming (mainly python). You will also get a brief understanding on some communication protocols and solutions used in it for example: MQTT and HTTP Requests

# Materials
To bee able to follow this tutorial please gather microcontroller, sensors etc with same specifications as descibred bellow. I've already gathered all those components from different kits at different times, but you can buy them from the links below:

| Component            | Purpose                                                                                                                                                                                                                                     | Can be bought at (Sweden):                                                                                                                                                                                                                                                                                                               | Price (approximately) |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| Heltec LoRa v2/ESP32 | Heltec LoRa v2 has been used in this<br>project, but no LoRa is used so almost <br>any ESP32 based device will work as well.  The choosen Heltec development board is based on ESP32 which is a low-cost and low-powered system on a chip with intergrated WiFi and Bluetooth possiblities, and the Heltec one also comes with LoRa. Development board makes it easy to connect to components with their pins located on the sides.                                                                                                                     | [amazon.se](https://www.amazon.se/gp/product/B078M74NNN/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)                                                                                                                                                                                                                                             | 300kr                 |
| 2 PCB Buttons        | These buttons will be used to make the user<br>choose answer by opeing a voltage circuit and trigger input pin                                                                                                                                                                                    | [electrokit.com](https://www.electrokit.com/produkt/knappar-pcb-sortiment-12st/)                                                                                                                                                                                                                                                                           | 80kr (12pcs)          |
| Bread board          | This is used to connect all components solderless, but <br>you can design and print your own PCB if enough knowledge                                                                                                                                        | [sizable.se](https://sizable.se/P.TVY7M/Kopplingsdack-med-830-punkter)                                                                                                                                                                                                                                                                                 | 53kr                  |
| Jumper Wires         | Only if bread board: Theese wires is used<br>to connect all components. Three difrent<br>contacts used as in link: female-to-female, male-to-female male-to-male!                                                                                                                              | [amazon.se](https://www.amazon.se/Elegoo-Flerf%C3%A4rgad-Breadboard-Bandkablar-Arduino/dp/B01EV70C78/ref=asc_df_B01EV70C78/?tag=shpngadsglede-21&linkCode=df0&hvadid=476462430370&hvpos=&hvnetw=g&hvrand=7042316417688917121&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1012345&hvtargid=pla-362913641420&psc=1)                                                                                                                                                                                                                                                                                                     | 80kr                  |
| Resistors (2: 10k, 1:220)            | The resistor acts as a electrical resistance and reduce current, correct signal levels etc. In this project only two 10K Ohm is used as <br>pull-down resistor and one 220 Ohm for the LED.<br>But a pack of resistors is always good to have.                                                                                              | [sizable.se](https://sizable.se/P.3MSQ6/30-Varden-Motstand-600-st)                                                                                                                                                                                                                                                                                     | 72kr                    |
| Red LED              | This is used to warn user that a message has arrived.<br>The projects uses a red LED that emits red light (red defuse) but any color and diameter<br>can be used (consider that you need different resistors for<br>different LEDs, this project uses 5mm RED 2v forward voltage) | [electrokit.com](https://www.electrokit.com/produkt/led-5mm-rod-diffus-1500mcd/)                                                                                                                                                                                                                                                                           | 5kr                      |
| LCD 16x2             | This is the main component that displays the message. You<br>can use any size you want but in this project 16x2 is used.<br> An LCD consists of liquid-crystal that can turn on and off to display text or other pictures. Consider one with I2C (syncron serial communication), that makes it easier and requires less<br>wireing.                                           | [amazon.se](https://www.amazon.se/AZDelivery-LCD-Modulvisningsbunt-I2C-Gr%C3%A4nssnitt-kompatibel-Raspberry/dp/B07CQG6CMT/ref=asc_df_B07CQG6CMT/?tag=shpngadsglede-21&linkCode=df0&hvadid=476555136704&hvpos=&hvnetw=g&hvrand=582242616344342109&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1012345&hvtargid=pla-653596068129&psc=1) | 89kr                      |
| Buzzer               | This buzzer makes a sound (with frequency) when receiving a message and also when<br>sent successfully. This outputs a lower db sound than a speaker, <br>so if correct knowledge speaker is recommended.                                                        | [conrad.com](https://www.conrad.se/p/conrad-components-93038c212a-miniatyr-summer-ljudniva-85-db-spaenning-5-v-1-st-1511467?utm_campaign=shopping-feed&utm_content=free-google-shopping-clicks&utm_medium=surfaces&utm_source=google&utm_term=1511467&vat=true)                                                                                        | 8kr                      |

**Total: 700kr**
