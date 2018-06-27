## Leonardo Cesar Cerqueira (NUSP 8937483)

# Tema: Esteganografia

# Título: Sound Spy

# Descrição:
O objetivo do projeto é criar um programa que, com entrada de um arquivo 
.wav, uma chave de codificação e uma imagem .png, seja capaz de esconder o 
.wav na imagem de forma imperceptível ao olho humano, e indecifrável por 
força bruta. O mesmo programa também fará o processo contrário, porém somente
se for usada a mesma chave, para decodificar, detectar e decifrar o .wav 
dentro da imagem

## Como usar:
- Esconder: "$ py sound_spy.py" -e <key> <wav to hide> <png where it will be hidden> <number of bits to use> <png output file>
- Recuperar: "$ py sound_spy.py" -d <key> <png with hidden wav> <number of bits used> <wav output file>
  