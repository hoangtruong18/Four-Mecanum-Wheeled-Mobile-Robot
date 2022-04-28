#include <SoftwareSerial.h>
SoftwareSerial AdruinoUno(52, 53);

//int LED1 = 10;
//int LED2 = 9;
#define PWMA 12    //A SPEED MOTOR 1 -  LEFT FRONT WHEEL
#define DIRA1 35 
#define DIRA2 34  //A DIRECTION MOTOR 1 - LEFT FRONT WHEEL
#define PWMB 8    //B SPEED MOTOR 2 - RIGHT FRONT WHEEL
#define DIRB1 36 
#define DIRB2 37  //B DIRECTION MOTOR 2 - RIGHT FRONT WHEEL
#define PWMC 9   //C SPEED MOTOR 3 - LEFT REAR WHEEL
#define DIRC1 42 
#define DIRC2 43  //C DIRECTION MOTOR 3 - LEFT REAR WHEEL
#define PWMD 5    //D SPEED MOTOR 4 - RIGHT REAR WHEEL
#define DIRD1 A5  //27  
#define DIRD2 A4 //26  //D DIRECTION MOTOR 4 - RIGHT REAR WHEEL

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  AdruinoUno.begin(4800);
  pinMode(PWMA, OUTPUT);
  pinMode(DIRA1, OUTPUT);
  pinMode(DIRA2, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(DIRB1, OUTPUT);
  pinMode(DIRB2, OUTPUT);
  pinMode(PWMC, OUTPUT);
  pinMode(DIRC1, OUTPUT);
  pinMode(DIRC2, OUTPUT);
  pinMode(PWMD, OUTPUT);
  pinMode(DIRD1, OUTPUT);
  pinMode(DIRD2, OUTPUT);
  //pinMode(LED1, OUTPUT);
  //pinMode(LED2, OUTPUT);
}

// Motion Control Action
#define MOTORA_FORWARD(pwm)    do{digitalWrite(DIRA1,HIGH); digitalWrite(DIRA2,LOW);analogWrite(PWMA,pwm);}while(0)
#define MOTORA_STOP(x)         do{digitalWrite(DIRA1,LOW); digitalWrite(DIRA2,LOW); analogWrite(PWMA,0);}while(0)
#define MOTORA_BACKOFF(pwm)    do{digitalWrite(DIRA1,LOW);digitalWrite(DIRA2,HIGH); analogWrite(PWMA,pwm);}while(0)

#define MOTORB_FORWARD(pwm)    do{digitalWrite(DIRB1,LOW); digitalWrite(DIRB2,HIGH);analogWrite(PWMB,pwm);}while(0)
#define MOTORB_STOP(x)         do{digitalWrite(DIRB1,LOW); digitalWrite(DIRB2,LOW); analogWrite(PWMB,0);}while(0)
#define MOTORB_BACKOFF(pwm)    do{digitalWrite(DIRB1,HIGH);digitalWrite(DIRB2,LOW); analogWrite(PWMB,pwm);}while(0)

#define MOTORC_FORWARD(pwm)    do{digitalWrite(DIRC1,HIGH); digitalWrite(DIRC2,LOW);analogWrite(PWMC,pwm);}while(0)
#define MOTORC_STOP(x)         do{digitalWrite(DIRC1,LOW); digitalWrite(DIRC2,LOW); analogWrite(PWMC,0);}while(0)
#define MOTORC_BACKOFF(pwm)    do{digitalWrite(DIRC1,LOW);digitalWrite(DIRC2,HIGH); analogWrite(PWMC,pwm);}while(0)

#define MOTORD_FORWARD(pwm)    do{digitalWrite(DIRD1,LOW); digitalWrite(DIRD2,HIGH);analogWrite(PWMD,pwm);}while(0)
#define MOTORD_STOP(x)         do{digitalWrite(DIRD1,LOW); digitalWrite(DIRD2,LOW); analogWrite(PWMD,0);}while(0)
#define MOTORD_BACKOFF(pwm)    do{digitalWrite(DIRD1,HIGH);digitalWrite(DIRD2,LOW); analogWrite(PWMD,pwm);}while(0)

int Motor_PWM = 35;

//Motor motion control    
//Macro definition

////// FORWARD
//    ↑A-----B↑   
//     |  ↑  |
//     |  |  |
//    ↑C-----D↑
void ADVANCE()
{
  MOTORA_FORWARD(Motor_PWM);MOTORB_FORWARD(Motor_PWM);    
  MOTORC_FORWARD(Motor_PWM);MOTORD_FORWARD(Motor_PWM);    
}
///// BACKWARD
//    ↓A-----B↓     //
//     |  |  |      //
//     |  ↓  |      //
//    ↓C-----D↓     //
void BACK()
{
  MOTORA_BACKOFF(Motor_PWM);MOTORB_BACKOFF(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM);MOTORD_BACKOFF(Motor_PWM);
}
///// FORWARD LEFT
//    =A-----B↑   
//     |   ↖ |
//     | ↖   |
//    ↑C-----D=
void LEFT_1()
{
  MOTORA_STOP(Motor_PWM);MOTORB_FORWARD(Motor_PWM);
  MOTORC_FORWARD(Motor_PWM);MOTORD_STOP(Motor_PWM);
}
///// LEFT
//    ↓A-----B↑   
//     |  ←  |
//     |  ←  |
//    ↑C-----D↓
void LEFT_2()
{
  MOTORA_BACKOFF(Motor_PWM);MOTORB_FORWARD(Motor_PWM);
  MOTORC_FORWARD(Motor_PWM);MOTORD_BACKOFF(Motor_PWM);
}
//    ↓A-----B=   
//     | ↙   |
//     |   ↙ |
//    =C-----D↓
void LEFT_3()
{
  MOTORA_BACKOFF(Motor_PWM);MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM);MOTORD_BACKOFF(Motor_PWM);
}
//// FORWARD RIGHT
//    ↑A-----B=   
//     | ↗   |
//     |   ↗ |
//    =C-----D↑
void RIGHT_1()
{
  MOTORA_FORWARD(Motor_PWM);MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM);MOTORD_FORWARD(Motor_PWM);
}

//// RIGHT
//    ↑A-----B↓   
//     |  →  |
//     |  →  |
//    ↓C-----D↑
void RIGHT_2()
{
  MOTORA_FORWARD(Motor_PWM);MOTORB_BACKOFF(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM);MOTORD_FORWARD(Motor_PWM);
}
///// BACKWARD RIGHT
//    =A-----B↓   
//     |   ↘ |
//     | ↘   |
//    ↓C-----D=
void RIGHT_3()
{
  MOTORA_STOP(Motor_PWM);MOTORB_BACKOFF(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM);MOTORD_STOP(Motor_PWM);
}
//////// TURNING LEFT
// ↓A-----B↑
//  |     |
//  |     |
// ↓C-----D↑
void TURN_LEFT()
{
  MOTORA_BACKOFF(Motor_PWM);MOTORB_FORWARD(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM);MOTORD_FORWARD(Motor_PWM);  
}
////// TURNING RIGHT
// ↑A-----B↓
//  |     |
//  |     |
// ↑C-----D↓
void TURN_RIGHT()
{
  MOTORA_FORWARD(Motor_PWM);MOTORB_BACKOFF(Motor_PWM);
  MOTORC_FORWARD(Motor_PWM);MOTORD_BACKOFF(Motor_PWM);  
}
///////// STOP
//    =A-----B=  
//     |  =  |
//     |  =  |
//    =C-----D=
void STOP()
{
  MOTORA_STOP(Motor_PWM);MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM);MOTORD_STOP(Motor_PWM);
}
void loop() {
  // put your main code here, to run repeatedly:
  while (AdruinoUno.available() > 0) {
    int val = AdruinoUno.parseInt();
    if (AdruinoUno.read() == '\n')
    {
      Serial.println(val);
      if (val == 0)
      {
        STOP();
        //digitalWrite(LED1, HIGH);
        //digitalWrite(LED2,LOW);
      }
      else if (val == 1)
      {
        //digitalWrite(LED1, LOW);
        //digitalWrite(LED2, LOW);
        ADVANCE();
      }
      else if (val == 2)
      {
        //digitalWrite(LED2, HIGH);
        //digitalWrite(LED1, LOW);
        BACK();
      }
      else if (val == 3)
      {
        TURN_LEFT();
      }
      else if (val == 4)
      {
        TURN_RIGHT();
      }
      else if (val == 5)
      {
        LEFT_2();
      }
      else if (val == 6)
      {
        RIGHT_2();
      }
    }
  }
  delay(30);
}
