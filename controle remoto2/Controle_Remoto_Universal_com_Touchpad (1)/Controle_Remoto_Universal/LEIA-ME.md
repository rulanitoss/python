# Controle Remoto Universal — Windows + telemóvel

## O que é
Uma interface estilo comando de TV servida localmente pelo computador. Funciona no navegador do próprio PC e no navegador de um telemóvel ligado à mesma rede Wi-Fi.

## Requisitos
- Windows 10 ou Windows 11
- Python 3.10 ou mais recente, instalado a partir de https://www.python.org/downloads/windows/
- PC e telemóvel na mesma rede Wi-Fi para controlo móvel

## Instalação
1. Extraia `Controle_Remoto_Universal.zip` para uma pasta normal, por exemplo `Documentos\Controle_Remoto_Universal`.
2. Instale Python 3 se ainda não existir. Durante a instalação, marque `Add python.exe to PATH`.
3. Faça duplo clique em `instalar.bat`. É necessário Internet para instalar as bibliotecas.
4. Faça duplo clique em `iniciar.bat`.
5. Deixe a janela preta aberta. Ela mostra um PIN de 6 dígitos e dois endereços.
6. No PC, abra `http://127.0.0.1:8765`.
7. No telemóvel, abra o endereço da rede local mostrado no terminal (ex.: `http://192.168.1.10:8765`). Introduza o mesmo PIN.

## Se o telemóvel não ligar
- Confirme que os dois dispositivos estão na mesma rede Wi-Fi.
- Em redes de convidados, a opção de isolamento de dispositivos pode bloquear a ligação.
- Se o Windows Defender Firewall perguntar, permita acesso apenas em redes privadas. Não ative encaminhamento de portas no router.
- Não partilhe o PIN com pessoas em quem não confia.
- Se o IP mudar, feche e volte a abrir o programa para ver o endereço atual.

## Comandos incluídos
- Touchpad para mover o cursor, clique esquerdo, duplo clique e clique direito
- Setas, OK/Enter, Esc, Tab e Espaço
- Volume, silêncio e teclas multimédia (dependem do teclado/aplicação)
- Menu Iniciar, pesquisa, alternar janelas e ambiente de trabalho
- Explorador, Calculadora, Bloco de Notas, Paint e teclado virtual
- Captura de ecrã e atalhos copiar/colar/cortar/desfazer/refazer
- Bloquear a sessão do Windows

## Segurança e limitações
- O servidor escuta na rede local para permitir o telemóvel; o PIN protege o acesso.
- A aplicação usa HTTP na rede local, não HTTPS. Use apenas numa rede de confiança e nunca exponha a porta 8765 à Internet.
- Os comandos afetam a aplicação/janela que estiver ativa no computador, não necessariamente a página do comando.
- Não há comandos de voz, acesso remoto fora de casa nem desligamento/reinício do computador nesta versão.
- A captura de ecrã guarda ficheiros em `Imagens\Capturas`.
- Para parar o servidor, pressione Ctrl+C na janela preta.
