/*
  Web client
 
 This sketch connects to a website (http://www.google.com)
 using an Arduino Wiznet Ethernet shield. 
 
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 
 created 18 Dec 2009
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe, based on work by Adrian McEwen

 check and change ip address
 check and change localtunnel
 check and change noise level
 check and change switch shit
 

  
 
*/

#include <SPI.h>
#include <Ethernet.h>

const int threshold = 570;
const int micPin = A0;
const int motorPin = 5;
const int switchPin = A1;
int switchVal = 0;
int micVal = 0;
int motorVal = 0;
int resendCounter = 0;
boolean running = false;
String site = "3i4t.localtunnel.com";

// Enter a MAC address for your controller below.
// Newer Ethernet shields have a MAC address printed on a sticker on the shield
byte mac[] = {  
   0x58, 0xB0, 0x35, 0x71, 0x51, 0x60};
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
//IPAddress server(74,125,232,128);  // numeric IP for Google (no DNS)
char server[] = "3i4t.localtunnel.com";    
// name address for Google (using DNS)

// Set the static IP address to use if the DHCP fails to assign
IPAddress ip(128,122,81,246);

// Initialize the Ethernet client library
// with the IP address and port of the server 
// that you want to connect to (port 80 is default for HTTP):
EthernetClient client;

void setup() {
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
  pinMode(motorPin,OUTPUT);
  pinMode(micPin,INPUT);
  pinMode(switchPin,INPUT);
   while (!Serial) {
      ; // wait for serial port to connect. Needed for Leonardo only
    }

  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    //Serial.println("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(mac, ip);
  }
  // give the Ethernet shield a second to initialize:
  delay(100);
  Serial.println("connecting...");

  // if you get a connection, report back via serial:
  if (client.connect(server, 80)) {
    Serial.println("connected");
    // Make a HTTP request:
    /*
    client.println("GET /resend HTTP/1.1");
    client.println("Host: 3pnk.localtunnel.com ");
    client.println("Connection: close");
    client.println(); 
    */
  } 
  else {
    // kf you didn't get a connection to the server:
    Serial.println("connection failed");
  }
}

void loop()
{
  
  boolean activated = false;
  micVal = analogRead(micPin);
  switchVal = digitalRead(switchPin);
  Serial.println(micVal);
  if(!activated && (micVal > threshold)) {
    Serial.println("activated");
    activated = true;
    client.connect(server, 80);
    client.println("GET /next HTTP/1.1");
    client.println("Host: "+site);
    client.println("Connection: close");
    client.println();
    client.stop();
  }
  if (activated) {
    resendCounter++;
    if (resendCounter >= 1000) {
      client.connect(server, 80);
      client.println("GET /resend HTTP/1.1");
      client.println("Host: "+site);
      client.println("Connection: close");
      client.println();
      client.stop();
    }
    motorVal = 150;
    analogWrite(motorPin,150);
  }
  if (switchVal == HIGH) {
    motorVal = 0;
    analogWrite(motorPin,0);
    Serial.println("SWITCH PRESSED");
    activated = false;
    delay(300L*1000L);
    Serial.println("end of delay");
  }
  
  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    //Serial.println();
    Serial.println("disconnecting.");
    client.stop();
    client.connect(server,80);
    

    // do nothing forevermore:

  }
}

