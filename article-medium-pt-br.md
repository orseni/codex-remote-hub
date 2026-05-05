# Eu Queria Usar o Codex CLI Pelo Celular, Então Criei uma Ferramenta Pra Isso

*Uma ferramenta open-source para acessar o Codex CLI remotamente. Só tmux + ttyd + Tailscale fazendo o trabalho pesado.*

---

## O Problema

Eu uso assistentes de código com IA diariamente. Tanto o Claude Code quanto o Codex CLI. E uma coisa que sempre me incomodou era não conseguir verificar uma sessão do Codex em execução pelo celular.

Com o Claude Code, já existem algumas formas de fazer isso:

1. **Remote Control** é a solução oficial da Anthropic. Você executa `/rc`, escaneia um QR code e continua pelo app do Claude. Limpo, simples, funciona muito bem para verificações rápidas.

2. **[Claude Remote Hub](https://github.com/orseni/claude-remote-hub)** é um projeto paralelo que montei há um tempo. É um servidor Python que expõe sessões de terminal do Claude Code no navegador via Tailscale. Mais manual, mas te dá a experiência completa do terminal.

Com o Codex CLI, porém, não encontrei nada parecido. Talvez eu tenha deixado passar, talvez ninguém tenha sentido a necessidade ainda. De qualquer forma, eu queria, então construí algo.

## O Que Eu Realmente Precisava

Coisas bem simples:

- Verificar tarefas de longa duração sem ter que voltar até a mesa
- Iniciar uma sessão rápida pelo celular quando uma ideia surge
- Manter sessões ativas mesmo depois de fechar o terminal
- Retomar de onde parei a partir de outro dispositivo

Nada revolucionário. Apenas qualidade de vida que economiza algumas idas ao computador.

## Como Funciona

**[Codex Remote Hub](https://github.com/orseni/codex-remote-hub)** é basicamente a mesma abordagem que usei para o Claude Remote Hub, adaptada para o Codex CLI. É uma camada fina sobre ferramentas que já existem:

```
Celular/Navegador  ←── Tailscale (VPN) ──→  Seu Computador
                                             ├── :7690  Dashboard (web)
                                             └── :77xx  ttyd → tmux → codex
```

### O Que Ele Faz

- **Inicie sessões pelo celular.** Um dashboard simples onde você escolhe um diretório de projeto e pronto.
- **Sessões persistentes.** O tmux mantém tudo vivo. Feche o navegador, volte depois, tudo ainda está lá.
- **Capture sessões em execução.** Já tem o Codex rodando localmente? Você pode trazê-lo para o hub com `codex fork`.
- **Terminal completo.** É o seu CLI real, não uma interface simplificada.
- **Seguro por padrão.** Tudo passa pelo Tailscale, então nada é exposto à internet.
- **Sem dependências.** Apenas Python stdlib, um arquivo, ~1000 linhas.

### Começando

```bash
# 1. Certifique-se de que o Codex CLI está instalado
npm install -g @openai/codex

# 2. Clone e instale
git clone https://github.com/orseni/codex-remote-hub.git
cd codex-remote-hub
bash install.sh

# 3. Abra no celular
# https://sua-maquina.tailnet.ts.net:7690
```

O instalador cuida da configuração: tmux, ttyd, autostart (LaunchAgent no macOS, systemd no Linux) e certificados HTTPS do Tailscale.

## Se Você Vem do Claude Remote Hub

O mapeamento é bem direto:

| Claude Code | Codex CLI |
|---|---|
| binário `claude` | binário `codex` |
| `npm install -g @anthropic-ai/claude-code` | `npm install -g @openai/codex` |
| `--dangerously-skip-permissions` | `--dangerously-bypass-approvals-and-sandbox` |
| `--resume ID --fork-session` | `codex fork <session_id>` |
| `--continue` | `codex resume --last` |
| variável `CLAUDECODE` | variável `CODEX_HOME` |
| Destaque laranja (#E8734A) | Verde OpenAI (#10a37f) |
| CLAUDE.md | CODEX.md |

Mesma arquitetura, mesmo modelo de segurança, mesmo fluxo. Se você usou um, o outro vai parecer familiar.

## "Mas a OpenAI Pode Lançar Algo Oficial..."

Totalmente possível. E se lançarem, provavelmente será mais polido que isso. A Anthropic fez com o Remote Control e é uma ótima experiência.

Isso é apenas uma solução para quem quer acesso remoto *hoje*. Se algo melhor aparecer, oficial ou feito pela comunidade, é uma vitória para todos. Enquanto isso, resolve o problema.

## O Que Tem Por Baixo

Nada exótico:

- **Python 3** (apenas stdlib), o servidor, ~1000 linhas
- **tmux** para persistência de sessão
- **ttyd** como ponte terminal-para-web
- **Tailscale** para VPN criptografada + certificados HTTPS

Sem frameworks, sem serviços em nuvem, sem etapa de build.

## Experimente

O Codex Remote Hub é open source sob a licença MIT.

**GitHub**: [github.com/orseni/codex-remote-hub](https://github.com/orseni/codex-remote-hub)

Se você usa o Codex CLI e alguma vez desejou poder verificá-lo pelo celular, isso pode ajudar. Feedback, issues e PRs são bem-vindos.

Se você usa o Claude Code, também existe o [Claude Remote Hub](https://github.com/orseni/claude-remote-hub) para o mesmo workflow.

---

*Isso começou porque eu queria verificar minhas sessões do Codex do sofá. O kit de ferramentas Unix (tmux, ttyd, Tailscale) tornou surpreendentemente fácil montar tudo. Espero que seja útil para mais alguém.*

---

**Tags**: `#OpenAI` `#Codex` `#CodexCLI` `#ClaudeCode` `#IA` `#Ferramentas-de-Desenvolvedor` `#Open-Source` `#CLI` `#Desenvolvimento-Mobile` `#Tailscale` `#Python` `#Desenvolvimento-Remoto`
