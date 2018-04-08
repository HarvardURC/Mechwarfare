#include <PololuMaestro.h>
 #include <SoftwareSerial.h>
 SoftwareSerial maestroSerial(10, 11);
MiniMaestro maestro(maestroSerial);

  int home1 = 6000;
  int homecrouch = 5000;

int rotate = 4000;

void setup()
{
  // Set the serial port's baud rate

  maestroSerial.begin(9600);
  Serial.begin(9600);
 /*  maestro.setTarget(0, homecrouch);
   maestro.setTarget(1, 5000);
   maestro.setTarget(2, homecrouch);
   maestro.setTarget(3, homecrouch);
   maestro.setTarget(4, 5000);
   maestro.setTarget(5, homecrouch);
   maestro.setTarget(6, homecrouch);
   maestro.setTarget(7, 5000);
   maestro.setTarget(8, homecrouch);
   maestro.setTarget(9, homecrouch);
    maestro.setTarget(10, 5000);
   maestro.setTarget(11, homecrouch);
?delay(1000);*/

   maestro.setTarget(0, home1);
   maestro.setTarget(1, homecrouch);
   maestro.setTarget(2, home1);   // all middle (standing posintion
   maestro.setTarget(3, home1);
   maestro.setTarget(4, homecrouch);
   maestro.setTarget(5, home1);
   maestro.setTarget(6, home1);
   maestro.setTarget(7, homecrouch);
   maestro.setTarget(8, home1);
   maestro.setTarget(9, home1);
    maestro.setTarget(10, homecrouch);
   maestro.setTarget(11, home1);
    delay(400);
   //move rotate_robot

   /*
    maestro.setTarget(7, 5000);
     maestro.setTarget(1, 5000);
      delay(100);
     maestro.setTarget(0, 5000);
     maestro.setTarget(6, 5000);
     delay(100);
         maestro.setTarget(7, homecrouch);
          maestro.setTarget(1, homecrouch);
       delay(100);
       maestro.setTarget(10, 5000);
     maestro.setTarget(4, 5000);
      delay(100);
     maestro.setTarget(3, 5000);
     maestro.setTarget(9, 5000);
     delay(100);
         maestro.setTarget(10, homecrouch);
          maestro.setTarget(4, homecrouch);
       delay(100);
        maestro.setTarget(3, homecrouch);
     maestro.setTarget(9, homecrouch);
       maestro.setTarget(0, homecrouch);
     maestro.setTarget(6, homecrouch);
*/


//rotate_robot();
//rotate_robot();
//rotate_robot();
//rotate_robot();

//move_robot_center_mass_stable();
//delay(100);


move_robot();
move_robot();
move_robot();
move_robot();




//move_robot_advanced(3);
//delay(100);
//move_robot_advanced(3);
//delay(100);

}
 
void loop()
{
  /*
  for (uint8_t i = 0; i < 6; i++)
  {
    uint16_t position = maestro.getPosition(i);
    Serial.print("Channel: ");
    Serial.print(i);
    Serial.print(" Position: ");
    Serial.println(position);
  }
  */
    /*int motor0 = maestro.getPosition(0);
  int motor1 = maestro.getPosition(1);
  int motor2 = maestro.getPosition(2);
  int motor3 = maestro.getPosition(3);
  int motor4 = maestro.getPosition(4);
  Serial.print(motor0);
  Serial.print(" ");
  Serial.print(motor1);
  Serial.print(" ");
  Serial.print(motor2);
  Serial.print(" ");
  Serial.print(motor3);
  Serial.print(" ");
  Serial.print(motor4);
  Serial.println(" ");
  */
  /* setTarget takes the channel number you want to control, and
     the target position in units of 1/4 microseconds. A typical
     RC hobby servo responds to pulses between 1 ms (4000) and 2
     ms (8000). */

  // Set the target of channel 0 to 1500 us and channel 1 to 1750 us.

 /*   maestro.setTarget(3, 3000);
  maestro.setTarget(4, 7000);
  maestro.setTarget(5,8000);
    maestro.setTarget(6, 3000);
  maestro.setTarget(7, 7000);
  maestro.setTarget(8,8000);
  maestro.setTarget(9, 3000);
  maestro.setTarget(10, 7000);
  maestro.setTarget(11,8000); */

  // Wait 2 seconds.
 // delay(500);

  // Set the target of channel 0 to 1250 us and channel 1 to 2000 us.
   //maestro.setTarget(0, 4000);
  //maestro.setTarget(1 , 4000);
 // maestro.setTarget(2,4000);
 /*
   maestro.setTarget(3, 5000);
  maestro.setTarget(4 , 8000);
  maestro.setTarget(5,2000);
   maestro.setTarget(6, 5000);
  maestro.setTarget(7 , 8000);
  maestro.setTarget(8,2000);
  maestro.setTarget(9, 5000);
  maestro.setTarget(10 , 8000);
  maestro.setTarget(11,2000);
 */
 /*
 for(int i =4000; i < 8000; i++)
 {

 }
 */
  // Wait 2 seconds.
  //delay(500);
}
void rotate_robot()
{

    maestro.setTarget(7, rotate);
     maestro.setTarget(1, rotate);
      delay(100);
     maestro.setTarget(0, rotate);
     maestro.setTarget(6, rotate);
     delay(100);
         maestro.setTarget(7, homecrouch);
          maestro.setTarget(1, homecrouch);
       delay(100);
       maestro.setTarget(10, rotate);
     maestro.setTarget(4, rotate);
      delay(100);
     maestro.setTarget(3, rotate);
     maestro.setTarget(9, rotate);
     delay(100);
         maestro.setTarget(10, homecrouch);
          maestro.setTarget(4, homecrouch);
       delay(100);
        maestro.setTarget(3, home1);
     maestro.setTarget(9, home1);
       maestro.setTarget(0, home1);
     maestro.setTarget(6, home1);
}

void move_robot()
{
    //lift adjacent legs (not opposite ones like in rotation)
    maestro.setTarget(7, rotate);
     maestro.setTarget(1, rotate);
      delay(100);

    // rotate those legs forward
     maestro.setTarget(6, rotate);
     maestro.setTarget(0, 2*home1 - rotate);
     delay(100);

     // lower legs back
         maestro.setTarget(7, homecrouch);
          maestro.setTarget(1, homecrouch);
       delay(100);


    // lift two other legs

//      maestro.setTarget(10, rotate);
//     maestro.setTarget(4, rotate);

       maestro.setTarget(10, homecrouch - (homecrouch - rotate)/2.0);
     maestro.setTarget(4, homecrouch - (homecrouch - rotate)/2.0);
       maestro.setTarget(0, home1);
     maestro.setTarget(6, home1);

       delay(100);

     // lower legs back
         maestro.setTarget(10, homecrouch);
          maestro.setTarget(4, homecrouch);



       delay(100);



           // lower legs back
     maestro.setTarget(10, rotate);
     maestro.setTarget(4, rotate);
       delay(100);
    // rotate two legs other direction
     maestro.setTarget(9, rotate);
     maestro.setTarget(3, 2*home1 - rotate);
     delay(100);

     // lower legs back
     maestro.setTarget(10, homecrouch);
     maestro.setTarget(4, homecrouch);
     delay(100);


         // lift two other legs
       maestro.setTarget(7, homecrouch - (homecrouch - rotate)/2.0);
     maestro.setTarget(1, homecrouch - (homecrouch - rotate)/2.0);
        maestro.setTarget(3, home1);
     maestro.setTarget(9, home1);

       delay(100);

     // lower legs back
         maestro.setTarget(7, homecrouch);
          maestro.setTarget(1, homecrouch);



}

//void move_robot_advanced(int direction) //  0 forward, 1 right, 2 backwards, 3 left
//{
//
////lift adjacent legs (not opposite ones like in rotation)
//    maestro.setTarget((7+ 3*direction)%12, rotate);
//     maestro.setTarget((1+ 3*direction)%12, rotate);
//      delay(100);
//
//    // rotate those legs forward
//     maestro.setTarget((6+ 3*direction)%12, rotate);
//     maestro.setTarget((3*direction)%12, 2*home1 - rotate);
//     delay(100);
//
//     // lower legs back
//         maestro.setTarget((7+ 3*direction)%12, homecrouch);
//          maestro.setTarget((1+ 3*direction)%12, homecrouch);
//       delay(100);
//
//
//    // lift two other legs
//
////      maestro.setTarget(10, rotate);
////     maestro.setTarget(4, rotate);
//
//       maestro.setTarget((10+ 3*direction)%12, homecrouch - (homecrouch - rotate)/2.0);
//     maestro.setTarget((4+ 3*direction)%12, homecrouch - (homecrouch - rotate)/2.0);
//       maestro.setTarget((3*direction)%12, home1);
//     maestro.setTarget((6+ 3*direction)%12, home1);
//
//       delay(100);
//
//     // lower legs back
//         maestro.setTarget((10+ 3*direction)%12, homecrouch);
//          maestro.setTarget((4+ 3*direction)%12, homecrouch);
//
//
//
//       delay(100);
//
//
//
//           // lower legs back
//     maestro.setTarget((10+ 3*direction)%12, rotate);
//     maestro.setTarget((4+ 3*direction)%12, rotate);
//       delay(100);
//    // rotate two legs other direction
//     maestro.setTarget((9+ 3*direction)%12, rotate);
//     maestro.setTarget((3+ 3*direction)%12, 2*home1 - rotate);
//     delay(100);
//
//     // lower legs back
//     maestro.setTarget((10+ 3*direction)%12, homecrouch);
//     maestro.setTarget((4+ 3*direction)%12, homecrouch);
//     delay(100);
//
//
//         // lift two other legs
//       maestro.setTarget((7+ 3*direction)%12, homecrouch - (homecrouch - rotate)/2.0);
//     maestro.setTarget((1+ 3*direction)%12, homecrouch - (homecrouch - rotate)/2.0);
//        maestro.setTarget((3+ 3*direction)%12, home1);
//     maestro.setTarget((9+ 3*direction)%12, home1);
//
//       delay(100);
//
//     // lower legs back
//         maestro.setTarget(7, homecrouch);
//          maestro.setTarget(1, homecrouch);
//
//}

void move_robot_center_mass_stable()
{
     //lift leg in creep motion
     maestro.setTarget(7, rotate);
     maestro.setTarget(8, 2*homecrouch - rotate);
     delay(400);

    // rotate leg in z axis
     maestro.setTarget(6, rotate);
     delay(400);

     // lower legs back
     maestro.setTarget(7, homecrouch);
     maestro.setTarget(8, home1);
     delay(400);

     maestro.setTarget(6, home1);


//
//     maestro.setTarget(7, 2*homecrouch - rotate);
//     maestro.setTarget(8, rotate);
//     delay(100);
//
//    // rotate leg in z axis
//     maestro.setTarget(6, rotate);
//     delay(100);
//
//     // lower legs back
//     maestro.setTarget(7, homecrouch);
//     maestro.setTarget(8, homecrouch);
//     delay(100);


}
