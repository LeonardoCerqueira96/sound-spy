# Leonardo Cesar Cerqueira (NUSP 8937483)

# Tema: Esteganografia

# Título: Sound Spy

# Descrição:
O objetivo do projeto é criar um programa que, com entrada de um arquivo 
.wav, uma chave de codificação e uma imagem .png, seja capaz de esconder o 
.wav na imagem de forma imperceptível ao olho humano, e indecifrável por 
força bruta. O mesmo programa também fará o processo contrário, porém somente
se for usada a mesma chave, para decodificar, detectar e decifrar o .wav 
dentro da imagem

# Arquivos utilizados como exemplos:
- Imagens (imagens .jpg foram convertidas para formato .png):
	* orchestra.jpg: http://www.senzaspine.com/wp-content/uploads/2016/06/20140415_PROMENADE.jpg
	* collector.jpg: https://i.ytimg.com/vi/rRVCTcLNkp0/maxresdefault.jpg
	* garrus.png: https://vignette.wikia.nocookie.net/masseffect/images/d/dc/GarrusME200.png/revision/latest?cb=20100307064656
- Soms (todos em formato WAV 16 PCM Mono):
	* fledermaus.wav, retirado e convertido de: https://www.youtube.com/watch?v=gPybrOxRoT4
	* collector.wav, retirado e convertido de: https://www.youtube.com/watch?v=cTdJ6FVYSR8
	* calibrations.wav, retirado e convertido de: https://www.youtube.com/watch?v=WQ5_fya5IdI
	
# Método - Escondendo:
- A chave fornecida ao programa é usada como seed para números aleatórios
- Primeiramente, o valor de sample rate é divido em bits e armazenado nos
bits menos significativos de posições da imagem geradas aleatoriamente
- O mesmo é feito para o número total de samples do arquivo
- O mesmo é feito para cada sample do arquivo
- A imagem modificada é salva

# Método - Recuperando:
- A chave fornecida ao programa é usada como seed para gerar os mesmos
números aleatórios da fase de esconder
- Primeiramente, o valor de sample rate do arquivo escondido é recuperado
dos bits menos significativos das posições "aleatórias" da imagem
- O mesmo é feito para o número total de samples do arquivo, N
- O mesmo é feito N vezes para recuperar as samples em significativos
- Os dados recuperados são usados para montar e salvar o arquivo .wav