// Proyecto: Monitor en Tiempo Real - ESP32 + WiFi + Sensores
// Fecha: 2025-05-12 01:56:16
// Todos los sensores funcionan, se inician pruebas con lora

#include <WiFi.h>
#include <WebServer.h>
#include <TinyGPSPlus.h>
#include <HardwareSerial.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <driver/i2s.h>

// === WiFi ===
const char* ssid = "FTTH0-C732EE";
const char* password = "4BD13LYN";
WebServer server(80);

// === GPS ===
TinyGPSPlus gps;
HardwareSerial gpsSerial(1);
#define GPS_RX 21
#define GPS_TX 20

// === MPU6050 ===
Adafruit_MPU6050 mpu;
#define I2C_SDA 18
#define I2C_SCL 19
sensors_event_t accelEvent, gyroEvent, tempEvent;

// === DHT11 ===
#define DHTPIN 40
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// === INMP441 ===
#define I2S_PORT   I2S_NUM_0
#define I2S_SD     14
#define I2S_WS     41
#define I2S_SCK    42
#define SAMPLE_RATE 16000
#define BUFFER_SIZE 512
#define MAX_PEAKS 20
#define RMS_HISTORY 25

float rmsHistory[RMS_HISTORY] = {0};
int rmsIndex = 0;
bool aboveThreshold = false;
unsigned long peakTimestamps[MAX_PEAKS] = {0};
int peakIndex = 0;
unsigned long lastPeakTime = 0;
int bpm = 0;

String latestPayload = "-";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado. IP: " + WiFi.localIP().toString());
  server.on("/", handleRoot);
  server.begin();

  gpsSerial.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);
  Wire.begin(I2C_SDA, I2C_SCL);
  mpu.begin();
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  dht.begin();

  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 4,
    .dma_buf_len = BUFFER_SIZE,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };
  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };
  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
  i2s_zero_dma_buffer(I2S_PORT);
}

void loop() {
  server.handleClient();

  while (gpsSerial.available()) gps.encode(gpsSerial.read());
  double lat = gps.location.isValid() ? gps.location.lat() : 19.819222;
  double lng = gps.location.isValid() ? gps.location.lng() : -97.369810;

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  if (isnan(temp)) temp = -99;
  if (isnan(hum)) hum = -99;

  mpu.getEvent(&accelEvent, &gyroEvent, &tempEvent);

  int32_t buffer[BUFFER_SIZE];
  size_t bytes_read;
  i2s_read(I2S_PORT, &buffer, sizeof(buffer), &bytes_read, portMAX_DELAY);
  int samples = bytes_read / sizeof(int32_t);
  int64_t square_sum = 0;
  for (int i = 0; i < samples; i++) {
    int32_t sample = buffer[i] >> 16;
    square_sum += (int64_t)sample * sample;
  }
  float rms = sqrt((float)square_sum / samples);
  rmsHistory[rmsIndex % RMS_HISTORY] = rms;
  rmsIndex++;

  float avgRMS = 0;
  for (int i = 0; i < RMS_HISTORY; i++) avgRMS += rmsHistory[i];
  avgRMS /= RMS_HISTORY;
  float delta = rmsHistory[(rmsIndex - 1) % RMS_HISTORY] - rmsHistory[(rmsIndex - 2 + RMS_HISTORY) % RMS_HISTORY];
  unsigned long now = millis();
  float dynamicThreshold = avgRMS * 0.6;

  if (avgRMS > dynamicThreshold && delta > -50 && !aboveThreshold && (now - lastPeakTime > 200)) {
    lastPeakTime = now;
    peakTimestamps[peakIndex % MAX_PEAKS] = now;
    peakIndex++;
    aboveThreshold = true;
  }
  if (aboveThreshold && (now - lastPeakTime > 600)) {
    aboveThreshold = false;
  }

  static unsigned long lastPrint = 0;
  if (now - lastPrint >= 5000) {
    lastPrint = now;
    int validCount = 0;
    float totalInterval = 0;
    for (int i = 1; i < MAX_PEAKS; i++) {
      int prev = (peakIndex - i - 1 + MAX_PEAKS) % MAX_PEAKS;
      int curr = (peakIndex - i + MAX_PEAKS) % MAX_PEAKS;
      unsigned long t1 = peakTimestamps[prev];
      unsigned long t2 = peakTimestamps[curr];
      if (t1 == 0 || t2 == 0) break;
      unsigned long interval = t2 - t1;
      if ((now - t2) <= 15000 && interval > 200 && interval < 2500) {
        totalInterval += interval;
        validCount++;
      }
    }
    bpm = (validCount > 0) ? 60000.0 / (totalInterval / validCount) : 0;
  }
}

void handleRoot() {
  String html = "<!DOCTYPE html><html><head><meta charset='UTF-8'>";
  html += "<meta http-equiv='refresh' content='5'>";
  html += "<style>body{font-family:sans-serif;padding:10px;}table{border-collapse:collapse;width:100%;}td,th{border:1px solid #ddd;padding:8px;text-align:left;}th{background:#4CAF50;color:white;}</style>";
  html += "<h2>📡 Monitoreo en Tiempo Real - ESP32</h2><table>";
  html += "<tr><th>Parámetro</th><th>Valor</th></tr>";
  html += "<tr><td>Latitud</td><td>" + String(gps.location.isValid() ? gps.location.lat() : 19.819222, 6) + "</td></tr>";
  html += "<tr><td>Longitud</td><td>" + String(gps.location.isValid() ? gps.location.lng() : -97.369810, 6) + "</td></tr>";
  html += "<tr><td>Temperatura (°C)</td><td>" + String(dht.readTemperature(), 1) + "</td></tr>";
  html += "<tr><td>Humedad (%)</td><td>" + String(dht.readHumidity(), 1) + "</td></tr>";
  html += "<tr><td>BPM</td><td>" + String(bpm) + "</td></tr>";
  html += "<tr><td>Aceleración</td><td>" + String(accelEvent.acceleration.x, 2) + ", " + String(accelEvent.acceleration.y, 2) + ", " + String(accelEvent.acceleration.z, 2) + "</td></tr>";
  html += "<tr><td>Giroscopio</td><td>" + String(gyroEvent.gyro.x, 2) + ", " + String(gyroEvent.gyro.y, 2) + ", " + String(gyroEvent.gyro.z, 2) + "</td></tr>";
  html += "</table><br><h3>🛰️ Datos crudos del GPS</h3><ul>";
  html += "<li><b>Satélites:</b> " + String(gps.satellites.isValid() ? gps.satellites.value() : 0) + "</li>";
  html += "<li><b>HDOP:</b> " + String(gps.hdop.isValid() ? gps.hdop.hdop() : 0.0) + "</li>";
  html += "<li><b>Altitud:</b> " + String(gps.altitude.isValid() ? gps.altitude.meters() : 0.0) + " m</li>";
  html += "<li><b>Fecha:</b> " + (gps.date.isValid() ? String(gps.date.day()) + "/" + String(gps.date.month()) + "/" + String(gps.date.year()) : "N/D") + "</li>";
  html += "<li><b>Hora:</b> " + (gps.time.isValid() ? String(gps.time.hour()) + ":" + String(gps.time.minute()) + ":" + String(gps.time.second()) : "N/D") + "</li></ul>";
  html += "<p style='font-size:smaller;color:#999'>IP: " + WiFi.localIP().toString() + "</p></body></html>";
  server.send(200, "text/html", html);
}
