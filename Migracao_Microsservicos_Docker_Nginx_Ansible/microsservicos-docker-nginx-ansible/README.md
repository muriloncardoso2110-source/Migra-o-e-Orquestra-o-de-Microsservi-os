# Loja Demo | Migração para microsserviços

Laboratório técnico de modernização de uma API monolítica simples para três serviços independentes. O foco é mostrar a diferença entre os dois modelos, colocar um proxy reverso na frente das APIs e automatizar o deploy local com Ansible.

**Stack:** Docker Compose, Nginx, Python 3.12, Ansible e GitHub Actions.

## Desenho da solução

```text
Navegador --> Nginx :8080 --> /api/products  --> catalog :8000
                         --> /api/customers --> customers :8000
                         --> /api/orders    --> orders :8000
                         --> /            --> página estática

Monólito antigo (opcional): localhost:8081 --> as três APIs no mesmo processo
```

Os serviços têm rede interna Docker; apenas o Nginx fica exposto por padrão. O monólito só é executado quando você solicita o perfil `legacy`.

## Pré-requisitos

- Docker Desktop com Compose v2 (Windows) ou Docker Engine + Compose v2 (Linux).
- PowerShell no Windows ou bash no Linux.
- Para o deploy via Ansible: Ubuntu/WSL2 ou Linux com Python 3 e Ansible instalado. O Ansible não roda nativamente como nó de controle no Windows; use WSL2.

Não é necessário instalar Python localmente para rodar a aplicação, apenas para testes fora dos containers.

## Inicialização rápida

No Windows, abra o Docker Desktop, extraia a pasta, abra o terminal PowerShell dentro dela e execute:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\iniciar.ps1
.\scripts\testar.ps1
```

No Linux/WSL:

```bash
bash scripts/start.sh
bash scripts/smoke.sh
```

Acesse **http://localhost:8080**. Para parar: `docker compose down` ou `scripts/parar.ps1` no Windows.

### Testes isolados

```bash
python -m unittest discover -s tests -v
```

## Demonstrando a migração

1. Suba o sistema antigo: `docker compose --profile legacy up -d --build monolith`.
2. Confira `http://localhost:8081/api/products`, `/api/customers` e `/api/orders`: tudo é atendido por um único processo.
3. Execute `docker compose up -d --build` para iniciar os três serviços e o Nginx.
4. Acesse `http://localhost:8080`; cada rota será atendida pelo serviço responsável.
5. Confira `docker compose ps` e os logs: `docker compose logs -f nginx catalog customers orders`.
6. Desligue o monólito: `docker compose --profile legacy stop monolith`.

**Escopo:** demonstração de decomposição e roteamento. A base é propositalmente em memória e somente leitura. Não há migração de banco, filas ou autenticação. Assim, a migração é ilustrativa, não uma migração real de dados de produção.

## Automação com Ansible (Ubuntu / WSL2)

O Ansible faz validação do Docker e do Compose, constrói os containers, inicia os serviços e verifica a saúde do Nginx.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install 'ansible-core>=2.17,<2.20'
ansible-galaxy collection install -r ansible/requirements.yml
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
```

Se usar WSL2, a integração WSL do Docker Desktop deve estar ligada, e `docker info` deve funcionar dentro do Ubuntu. Pare via `ansible-playbook -i ansible/inventory.ini ansible/stop.yml`.

Módulo utilizado: `community.docker.docker_compose_v2`. Consulte a [documentação oficial](https://docs.ansible.com/projects/ansible/latest/collections/community/docker/docker_compose_v2_module.html).

## Rotas

| Método | URL | Resposta |
| --- | --- | --- |
| GET | `/health` | Saúde do Nginx |
| GET | `/api/products` | Catálogo |
| GET | `/api/customers` | Clientes |
| GET | `/api/orders` | Pedidos |

## Organização

- `services/`: código reutilizado nas quatro imagens (três serviços + monólito didático).
- `nginx/`: proxy e página demonstrativa.
- `ansible/`: inventário e playbooks de implantação/parada.
- `scripts/`: comandos de inicialização, testes e parada.
- `tests/`: testes unitários.
- `.github/workflows/`: CI automatizada no GitHub.
- `docs/`: decisões e troubleshooting.

## Solução de problemas

- **Porta 8080 ocupada:** copie `.env.example` para `.env` e altere `APP_PORT=8090`; acesse `localhost:8090`.
- **Docker não encontrado:** abra Docker Desktop e confirme `docker compose version` e `docker info`.
- **Nginx 502:** veja `docker compose ps` e `docker compose logs catalog customers orders nginx`.
- **Ansible não conecta ao Docker no WSL:** habilite a integração da distro no Docker Desktop > Settings > Resources > WSL Integration.
- **Falha de download de imagens:** verifique conexão com a internet e proxy corporativo.

## Próximas melhorias

Persistência PostgreSQL, mensageria, autenticação, métricas e deploy em uma VM Linux são extensões futuras — não implementadas neste laboratório.

Projeto educacional, para execução local. Não exponha diretamente à internet sem autenticação, TLS, proteção de rede e endurecimento adicional.
