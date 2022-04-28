/*********
  Rui Santos
  Complete project details at https://randomnerdtutorials.com  
*********/

// Load Wi-Fi library
#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>


// Replace with your network credentials
const char* ssid     = "SSID";
const char* password = "Password";

// Set web server port number to 80
WiFiServer server(80);

// Variable to store the HTTP request
String header;

// Auxiliar variables to store the current output state
String output1State = "off";
String output0State = "off";
String output2State = "off";
String output3State = "off";
String output4State = "off";
String output5State = "off";
String output6State = "off";

// Assign output variables to GPIO pins

int a;
SoftwareSerial NodeMCU(D2, D3);


// Current time
unsigned long currentTime = millis();
// Previous time
unsigned long previousTime = 0; 
// Define timeout time in milliseconds (example: 2000ms = 2s)
const long timeoutTime = 500;

void setup() {
  Serial.begin(9600);
  NodeMCU.begin(4800);
  pinMode(D2, INPUT);
  pinMode(D3, OUTPUT);
  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();                                                
}

void loop(){
  WiFiClient client = server.available();   // Listen for incoming clients

  if (client) {                             // If a new client connects,
    Serial.println("New Client.");          // print a message out in the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    currentTime = millis();
    previousTime = currentTime;
    while (client.connected() && currentTime - previousTime <= timeoutTime) { // loop while the client's connected
      currentTime = millis();         
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        header += c;
        if (c == '\n') {                    // if the byte is a newline character
          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();
            
            // turns the GPIOs on and off
            if (header.indexOf("GET /0/off") >= 0) {
              Serial.println("ALL off");
              output0State = "on";
              output1State = "off";
              output2State = "off";
              output3State = "off";
              output4State = "off";
              output5State = "off";
              output6State = "off";
              a = 0;
              NodeMCU.print(a);
              NodeMCU.println("\n");
            } else if (header.indexOf("GET /1/on") >= 0) {
              Serial.println("GPIO 1 on");
              output0State = "off";
              output1State = "on";
              output2State = "off";
              output3State = "off";
              output4State = "off";
              output5State = "off";
              output6State = "off";
              a = 1;
              NodeMCU.print(a);
              NodeMCU.println("\n");
            } else if (header.indexOf("GET /2/on") >= 0) {
              Serial.println("GPIO 2 on");
              output0State = "off";
              output1State = "off";
              output2State = "on";
              output3State = "off";
              output4State = "off";
              output5State = "off";
              output6State = "off";
              a = 2;
              NodeMCU.print(a);
              NodeMCU.println("\n");
            } else if (header.indexOf("GET /3/on") >= 0) {
              Serial.println("GPIO 3 on");
              output0State = "off";
              output1State = "off";
              output2State = "off";
              output3State = "on";
              output4State = "off";
              output5State = "off";
              output6State = "off";
              a = 3;
              NodeMCU.print(a);
              NodeMCU.println("\n");
            } else if (header.indexOf("GET /4/on") >= 0) {
              Serial.println("GPIO 4 on");
              output0State = "off";
              output1State = "off";
              output2State = "off";
              output3State = "off";
              output4State = "on";
              output5State = "off";
              output6State = "off";
              a = 4;
              NodeMCU.print(a);
              NodeMCU.println("\n");
            } else if (header.indexOf("GET /5/on") >= 0) {
              Serial.println("GPIO 5 on");
              output0State = "off";
              output1State = "off";
              output2State = "off";
              output3State = "off";
              output4State = "off";
              output5State = "on";
              output6State = "off";
              a = 5;
              NodeMCU.print(a);
              NodeMCU.println("\n");
            } else if (header.indexOf("GET /6/on") >= 0) {
              Serial.println("GPIO 6 on");
              output0State = "off";
              output1State = "off";
              output2State = "off";
              output3State = "off";
              output4State = "off";
              output5State = "off";
              output6State = "on";
              a = 6;
              NodeMCU.print(a);
              NodeMCU.println("\n");
            }
            
            
            // Display the HTML web page
            client.println("<!DOCTYPE html><html>");
            client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
            client.println("<link rel=\"icon\" href=\"data:,\">");
            // CSS to style the on/off buttons 
            // Feel free to change the background-color and font-size attributes to fit your preferences
            client.println("<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}");
            client.println(".button { background-color: #195B6A; border: none; color: white; padding: 16px 40px;");
            client.println("text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}");
            client.println(".button2 {background-color: #77878A;}</style></head>");
            
            // Web Page Heading
            client.println("<body><h1>ESP8266 Web Server</h1>");

            // Display current state, and ON/OFF buttons for GPIO 0  
            client.println("<p>STOP " + output0State + "</p>");
            // If the output0State is off, it displays the ON button       
            if (output0State=="off") {
              client.println("<p><a href=\"/0/off\"><button class=\"button\">STOP</button></a></p>");
            } else {
              client.println("<p><a href=\"/0/off\"><button class=\"button button2\">STOP</button></a></p>");
            } 
            
            // Display current state, and ON/OFF buttons for GPIO 1  
            client.println("<p>FOWARD " + output1State + "</p>");
            // If the output1State is off, it displays the ON button       
            if (output1State=="off") {
              client.println("<p><a href=\"/1/on\"><button class=\"button\">FOWARD</button></a></p>");
            } else {
              client.println("<p><a href=\"/1/on\"><button class=\"button button2\">FOWARD</button></a></p>");
            } 
            
            // Display current state, and ON/OFF buttons for GPIO 2 
            client.println("<p>BACKWARD " + output2State + "</p>");
            // If the output2State is off, it displays the ON button       
            if (output2State=="off") {
              client.println("<p><a href=\"/2/on\"><button class=\"button\">BACKWARD</button></a></p>");
            } else {
              client.println("<p><a href=\"/2/on\"><button class=\"button button2\">BACKWARD</button></a></p>");
            } 
            
            // Display current state, and ON/OFF buttons for GPIO 3  
            client.println("<p>TURN LEFT " + output3State + "</p>");
            // If the output3State is off, it displays the ON button       
            if (output3State=="off") {
              client.println("<p><a href=\"/3/on\"><button class=\"button\">TURN LEFT</button></a></p>");
            } else {
              client.println("<p><a href=\"/3/on\"><button class=\"button button2\">TURN LEFT</button></a></p>");
            }

            // Display current state, and ON/OFF buttons for GPIO 4  
            client.println("<p>TURN RIGHT " + output4State + "</p>");
            // If the output4State is off, it displays the ON button       
            if (output4State=="off") {
              client.println("<p><a href=\"/4/on\"><button class=\"button\">TURN RIGHT</button></a></p>");
            } else {
              client.println("<p><a href=\"/4/on\"><button class=\"button button2\">TURN RIGHT</button></a></p>");
            } 
            client.println("</body></html>");

            // Display current state, and ON/OFF buttons for GPIO 5  
            client.println("<p>GO LEFT " + output5State + "</p>");
            // If the output5State is off, it displays the ON button       
            if (output5State=="off") {
              client.println("<p><a href=\"/5/on\"><button class=\"button\">GO LEFT</button></a></p>");
            } else {
              client.println("<p><a href=\"/5/on\"><button class=\"button button2\">GO LEFT</button></a></p>");
            } 
            client.println("</body></html>");

            // Display current state, and ON/OFF buttons for GPIO 6  
            client.println("<p>GO RIGHT " + output6State + "</p>");
            // If the output6State is off, it displays the ON button       
            if (output6State=="off") {
              client.println("<p><a href=\"/6/on\"><button class=\"button\">GO RIGHT</button></a></p>");
            } else {
              client.println("<p><a href=\"/6/on\"><button class=\"button button2\">GO RIGHT</button></a></p>");
            } 
            client.println("</body></html>");
               
            // The HTTP response ends with another blank line
            client.println();
            // Break out of the while loop
            break;
          } else { // if you got a newline, then clear currentLine
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
      }
    }
    // Clear the header variable
    header = "";
    // Close the connection
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}
