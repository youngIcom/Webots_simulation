#include <webots/robot.h>
#include <webots/distance_sensor.h>
#include <webots/motor.h>
#include <math.h>

// time in [ms] of a simulation step
#define TIME_STEP 64
#define MAX_SPEED 6.28
#define PI 3.14159265358979

// Function to turn 90 degrees counter-clockwise
void turn180ccw(WbDeviceTag left_motor, WbDeviceTag right_motor);

// entry point of the controller
int main(int argc, char **argv) {
  // initialize the Webots API
  wb_robot_init();

  // internal variables
  int i;
  WbDeviceTag ps[8];
  char ps_names[8][4] = {
    "ps0", "ps1", "ps2", "ps3",
    "ps4", "ps5", "ps6", "ps7"
  };

  // initialize devices
  for (i = 0; i < 8; i++) {
    ps[i] = wb_robot_get_device(ps_names[i]);
    wb_distance_sensor_enable(ps[i], TIME_STEP);
  }

  WbDeviceTag left_motor = wb_robot_get_device("left wheel motor");
  WbDeviceTag right_motor = wb_robot_get_device("right wheel motor");
  wb_motor_set_position(left_motor, INFINITY);
  wb_motor_set_position(right_motor, INFINITY);
  wb_motor_set_velocity(left_motor, 0.0);
  wb_motor_set_velocity(right_motor, 0.0);

  // feedback loop: step simulation until an exit event is received
  while (wb_robot_step(TIME_STEP) != -1) {
    // read sensors outputs
    double ps_values[8];
    for (i = 0; i < 8; i++) {
      ps_values[i] = wb_distance_sensor_get_value(ps[i]);
    }

    // detect obstacles
    bool right_obstacle =
      ps_values[0] > 80.0 ||
      ps_values[1] > 80.0 ||
      ps_values[2] > 80.0;
    bool left_obstacle =
      ps_values[5] > 80.0 ||
      ps_values[6] > 80.0 ||
      ps_values[7] > 80.0;

    // initialize motor speeds at 50% of MAX_SPEED.
    double left_speed  = 0.5 * MAX_SPEED;
    double right_speed = 0.5 * MAX_SPEED;

    // modify speeds according to obstacles
    if (left_obstacle) {
      // turn right 90° counter-clockwise
      turn180ccw(left_motor, right_motor);
    }
    else if (right_obstacle) {
      // turn left
      turn180ccw(left_motor, right_motor);
    }

    // write actuators inputs
    wb_motor_set_velocity(left_motor, left_speed);
    wb_motor_set_velocity(right_motor, right_speed);
  }

  // cleanup the Webots API
  wb_robot_cleanup();
  return 0; //EXIT_SUCCESS
}

// Function to turn robot 90 degrees counter-clockwise
void turn180ccw(WbDeviceTag left_motor, WbDeviceTag right_motor) {

  // Set the motors to turn the robot
  wb_motor_set_velocity(left_motor, -0.5 * MAX_SPEED);  // Move left motor backward
  wb_motor_set_velocity(right_motor, 0.5 * MAX_SPEED); // Move right motor forward

  // Let the robot turn for a specific time to complete the 90° turn
  wb_robot_step(1450);  // Adjust time depending on your robot's speed and turn radius

  // Stop the motors after turning
  wb_motor_set_velocity(left_motor, 0.0);
  wb_motor_set_velocity(right_motor, 0.0);
}
