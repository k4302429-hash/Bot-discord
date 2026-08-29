Deploy — deixar o bot online 24/7 (instruções rápidas)

1) Crie uma instância na Oracle Cloud (Always Free) com imagem Ubuntu 22.04 e adicione sua chave SSH pública.

2) Conecte via SSH:
ssh opc@<IP_DA_VM>
ou
ssh ubuntu@<IP_DA_VM>

3) No VM, rode o script de setup (como root):
sudo bash setup.sh

4) Edite .env e adicione seu token do Discord:
vi .env
# DISCORD_TOKEN=SEU_TOKEN_AQUI

5) Se o setup.sh não criou o serviço systemd automaticamente (ou você prefere configurar manualmente):
- Edite /etc/systemd/system/bot-discord.service com o conteúdo de SYSTEMD_UNIT.txt substituindo usuário e caminho.
- Rode:
  sudo systemctl daemon-reload
  sudo systemctl enable bot-discord
  sudo systemctl start bot-discord
  sudo journalctl -u bot-discord -f

6) Segurança e boas práticas:
- Nunca comite o arquivo .env com o token real no GitHub.
- Use chaves SSH em vez de senhas.
- Mantenha o sistema atualizado (apt upgrade).

Se quiser, eu posso também criar o arquivo systemd (.service) no repositório ou abrir um Pull Request com estes arquivos em uma branch separada. Quer que eu também crie uma branch e PR ao invés de commitar direto na default branch?