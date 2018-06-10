# Leonardo Cesar Cerqueira (NUSP 8937483)

# Tema: Esteganografia

# T?tulo: Sound Spy

# Descri??o:
O objetivo do projeto ? criar um programa que, com entrada de um arquivo 
.wav, uma chave de codifica??o e uma imagem .png, seja capaz de esconder o 
.wav na imagem de forma impercept?vel ao olho humano, e indecifr?vel por 
for?a bruta. O mesmo programa tamb?m far? o processo contr?rio, por?m somente
se for usada a mesma chave para decodifica??o, detectar e decifrar o .wav 
dentro da imagem

# Arquivos utilizados como exemplos:
- Imagens (imagens .jpg foram convertidas para formato .png):
	* orchestra.jpg: http://www.blurbpoint.com/blog/wp-content/uploads/2013/09/Website-Traffic.jpg
	* collector.jpg: https://i.ytimg.com/vi/rRVCTcLNkp0/maxresdefault.jpg
	* garrus.png: https://vignette.wikia.nocookie.net/masseffect/images/d/dc/GarrusME200.png/revision/latest?cb=20100307064656
- Soms (todos em formato WAV 16 PCM Mono):
	* fledermaus.wav, retirado e convertido de: https://www.youtube.com/watch?v=gPybrOxRoT4
	* collector.wav, retirado e convertido de: https://www.youtube.com/watch?v=cTdJ6FVYSR8
	* calibrations.wav, retirado e convertido de: https://www.youtube.com/watch?v=WQ5_fya5IdI
	
# M?todo - Escondendo:
- A chave fornecida ao programa ? usada como seed para n?meros aleat?rios
- Primeiramente, o valor de sample rate ? divido em bits e armazenado nos
bits menos significativos de posi??es da imagem geradas aleatoriamente
- O mesmo ? feito para o n?mero total de samples do arquivo
- O mesmo ? feito para cada sample do arquivo
- A imagem modificada ? salva

# M?todo - Recuperando:
- A chave fornecida ao programa ? usada como seed para gerar os mesmos
n?meros aleat?rios da fase de esconder
- Primeiramente, o valor de sample rate do arquivo escondido ? recuperado
dos bits menos significativos das posi??es "aleat?rias" da imagem
- O mesmo ? feito para o n?mero total de samples do arquivo, N
- O mesmo ? feito N vezes para recuperar as samples em significativos
- Os dados recuperados s?o usados para montar e salvar o arquivo .wav