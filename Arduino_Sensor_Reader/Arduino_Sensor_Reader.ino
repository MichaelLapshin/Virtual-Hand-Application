#include <HX711.h>

// Sensor variables
#define thumb_data_pin A9
#define index_data_pin A7
#define middle_data_pin A5
#define ring_data_pin A3
#define pinky_data_pin A1

#define thumb_clock_pin A8
#define index_clock_pin A6
#define middle_clock_pin A4
#define ring_clock_pin A2
#define pinky_clock_pin A0

#define NUM_SENSORS 5
#define ROLLING_AVG 8

HX711 thumb, index, middle, ring, pinky;

// Value reporting variables
int value_index;
double values_sum[NUM_SENSORS];
double finger_values[NUM_SENSORS][ROLLING_AVG];


void setup() {
  Serial.begin(9600);
  
  // Assigns pins to each sensor
  thumb.begin(thumb_data_pin, thumb_clock_pin);
  index.begin(index_data_pin, index_clock_pin);
  middle.begin(middle_data_pin, middle_clock_pin);
  ring.begin(ring_data_pin, ring_clock_pin);
  pinky.begin(pinky_data_pin, pinky_clock_pin);

  // Zeros the values of the sensors
  delay(2000);
  
  thumb.tare();
  index.tare();
  middle.tare();
  ring.tare();
  pinky.tare();
  
  delay(500);

  value_index = 0;
}


void loop() {
  // Removes old values
  for(int i = 0; i < NUM_SENSORS; i++){
    values_sum[i] -= finger_values[i][value_index];
  }
  
  // Overrides old values with new
  finger_values[0][value_index] = (double) thumb.get_value();
  finger_values[1][value_index] = (double) index.get_value();
  finger_values[2][value_index] = (double) middle.get_value();
  finger_values[3][value_index] = (double) ring.get_value();
  finger_values[4][value_index] = (double) pinky.get_value();

  // Appends new value
  for(int i = 0; i < NUM_SENSORS; i++){
    values_sum[i] += finger_values[i][value_index];
  }

  // Increments the index and wraps if necessary
  value_index += 1;
  if(value_index >= ROLLING_AVG){
    value_index = 0;
  }

  // Send values to serial port
  Serial.println((String) " a " + (long) (values_sum[0]/ROLLING_AVG));
  Serial.println((String) " b " + (long) (values_sum[1]/ROLLING_AVG));
  Serial.println((String) " c " + (long) (values_sum[2]/ROLLING_AVG));
  Serial.println((String) " d " + (long) (values_sum[3]/ROLLING_AVG));
  Serial.println((String) " e " + (long) (values_sum[4]/ROLLING_AVG));
}
