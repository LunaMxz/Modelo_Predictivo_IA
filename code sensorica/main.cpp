#include <Arduino.h>
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define DHTPIN 4
#define DHTTYPE DHT22

#define SENSOR_SUELO 35
#define SENSOR_LLUVIA 34

const char* ssid = "IUSH";
const char* password = "IUSH@@2023*";
const char* servidor = "http://10.0.9.164/agroindustrial/guardar_datos.php";

// DHT22
DHT dht(DHTPIN, DHTTYPE);

// Calibración lluvia
const int LLUVIA_SECO = 4095;
const int LLUVIA_MOJADO = 1200;

// Calibración suelo (AJUSTAR CON TUS VALORES)
const int SUELO_SECO = 4095;
const int SUELO_HUMEDO = 1500;

void setup() {
    Serial.begin(115200);
    dht.begin();

    WiFi.begin(ssid, password);

    Serial.print("Conectando al WiFi");

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println();
    Serial.println("WiFi conectado");
    Serial.print("IP del ESP32: ");
    Serial.println(WiFi.localIP());

    Serial.println("Sistema de monitoreo iniciado");
}

void loop() {

    // ===== DHT22 =====
    float humedadAmbiente = dht.readHumidity();
    float temperatura = dht.readTemperature();

    // ===== HUMEDAD DEL SUELO =====
    int lecturaSuelo = analogRead(SENSOR_SUELO);

    int humedadSuelo = map(
        lecturaSuelo,
        SUELO_SECO,
        SUELO_HUMEDO,
        0,
        100
    );

    humedadSuelo = constrain(humedadSuelo, 0, 100);

    // ===== LLUVIA =====
    int lecturaLluvia = analogRead(SENSOR_LLUVIA);

    int porcentajeLluvia = map(
        lecturaLluvia,
        LLUVIA_SECO,
        LLUVIA_MOJADO,
        0,
        100
    );

    porcentajeLluvia = constrain(porcentajeLluvia, 0, 100);

    // ===== MOSTRAR DATOS =====

    Serial.println("================================");

    if (isnan(temperatura) || isnan(humedadAmbiente)) {
        Serial.println("Error al leer DHT22");
    } else {
        Serial.print("Temperatura: ");
        Serial.print(temperatura);
        Serial.println(" °C");

        Serial.print("Humedad ambiente: ");
        Serial.print(humedadAmbiente);
        Serial.println(" %");
    }

    Serial.print("Humedad del suelo: ");
    Serial.print(humedadSuelo);
    Serial.println(" %");

    Serial.print("Lluvia: ");
    Serial.print(porcentajeLluvia);
    Serial.println(" %");

    Serial.println("================================");
    Serial.println();

if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

    String url = String(servidor) +
                 "?temperatura=" + String(temperatura) +
                 "&humedad_ambiente=" + String(humedadAmbiente) +
                 "&humedad_suelo=" + String(humedadSuelo) +
                 "&lluvia=" + String(porcentajeLluvia);

    Serial.println("Enviando datos...");
    Serial.println(url);

    http.begin(url);

    int httpCode = http.GET();

    Serial.print("Codigo HTTP: ");
    Serial.println(httpCode);

    if (httpCode > 0) {
        String respuesta = http.getString();
        Serial.println(respuesta);
    } else {
        Serial.println("Error al enviar los datos");
    }

    http.end();
}

    delay(5000); // 1 segundo
}