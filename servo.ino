#include <Servo.h>

int posicao = 0;
Servo servo;

#define bt1 2

bool bt1State = LOW;
bool lastBt1State = LOW;
unsigned long buttonPressTime = 0;
unsigned long currentTime = 0;
const int pressDuration = 3000; // Duração do pressionamento em milissegundos (3 segundos)

void setup()
{
  Serial.begin(9600);
  servo.attach(7);
  servo.write(0); // INICIA O MOTOR NA POSIÇÃO 0º
  pinMode(bt1, INPUT);
}

void loop()
{
  currentTime = millis();
  bt1State = digitalRead(bt1);

  // Detectar a borda de subida (quando o botão é pressionado)
  if (bt1State == HIGH && lastBt1State == LOW) {
    posicao += 50; // Incrementa a posição em 10 graus
    if (posicao > 180) { // Limita a posição máxima a 180 graus
      posicao = 180;
    }
    servo.write(posicao);
    buttonPressTime = currentTime; // Registra o tempo de pressionamento
    delay(200); // Pequeno atraso para evitar múltiplas leituras
  }

  // Verifica se o botão está sendo pressionado continuamente por 3 segundos
  if (bt1State == HIGH && (currentTime - buttonPressTime >= pressDuration)) {
    posicao = 0;
    servo.write(posicao);
    delay(200); // Pequeno atraso para evitar múltiplas leituras
  }

  // Atualiza o estado anterior do botão
  lastBt1State = bt1State;

  // Verifica comandos recebidos via Serial
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "MOVE") {
      posicao += 50; // Incrementa a posição em 10 graus
      if (posicao > 180) {
        posicao = 180;
      }
      servo.write(posicao);
    }
  }
}