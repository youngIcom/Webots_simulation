#include <webots/distance_sensor.h> 
#include <webots/motor.h> 
#include <webots/robot.h> 
#include <stdio.h> 
 
#define TIME_STEP 64 
#define RANGE (1024.0 / 2.0) 
 
int main(void) { 
  wb_robot_init(); 
 
  // --- sensors: ds0 (depan-kiri), ds1 (depan-kanan) 
  WbDeviceTag ds0 = wb_robot_get_device("ds0"); 
  WbDeviceTag ds1 = wb_robot_get_device("ds1"); 
  wb_distance_sensor_enable(ds0, TIME_STEP); 
  wb_distance_sensor_enable(ds1, TIME_STEP); 
 
  // --- motors (pastikan NAMA persis seperti di Scene Tree!) 
  WbDeviceTag left_motor  = wb_robot_get_device("left_wheel_motor"); 
  WbDeviceTag right_motor = wb_robot_get_device("right_wheel_motor"); 
  wb_motor_set_position(left_motor,  INFINITY); 
  wb_motor_set_position(right_motor, INFINITY); 
 
  // opsional: ketahui batas kecepatan 
  double vmax_l = wb_motor_get_max_velocity(left_motor); 
  double vmax_r = wb_motor_get_max_velocity(right_motor); 
 
  const double BASE_FWD = 0.6 * vmax_l;   // kecepatan maju dasar 
  const double TURN_GAIN = 0.4 * vmax_l;  // penguat belok 
 
  while (wb_robot_step(TIME_STEP) != -1) { 
    double sL = wb_distance_sensor_get_value(ds0); 
    double sR = wb_distance_sensor_get_value(ds1); 
 
    // Normalisasi 0..1 (semakin dekat → makin besar). 
    double nL = sL / RANGE; 
    double nR = sR / RANGE; 
 
    // Komponen belok dari perbedaan sensor. 
    double turn = TURN_GAIN * (nR - nL); 
 
    double vL = BASE_FWD - turn; 
    double vR = BASE_FWD + turn; 
 
    // jaga dalam batas kecepatan 
    if (vL > vmax_l) vL = vmax_l; 
    if (vL < -vmax_l) vL = -vmax_l; 
    if (vR > vmax_r) vR = vmax_r;
    if (vR < -vmax_r) vR = -vmax_r; 
 
    wb_motor_set_velocity(left_motor,  vL); 
    wb_motor_set_velocity(right_motor, vR); 
  } 
 
  wb_robot_cleanup(); 
  return 0; 
} 
