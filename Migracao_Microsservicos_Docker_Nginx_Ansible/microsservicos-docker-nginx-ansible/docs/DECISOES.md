# Decisões técnicas

- **Docker Compose:** reduz o custo e a dificuldade para um estudo júnior/pleno. Não é um orquestrador de cluster.
- **Nginx:** centraliza a entrada e faz o roteamento das APIs sem publicar portas individuais.
- **Python padrão:** evita bibliotecas externas; a parte principal do exercício é infraestrutura, não framework.
- **Ansible local:** automatiza o provisionamento da aplicação no host com Docker, sem inventário de servidores remotos.
- **Dados em memória:** permitem comparar arquitetura legada e arquitetura distribuída; não prometem persistência ou migração real de dados.
- **GitHub Actions:** testa código, valida Compose e faz smoke test em Linux.

## Checklist de demonstração

1. Mostrar monólito respondendo a três rotas na porta 8081.
2. Mostrar três containers separados e Nginx na porta 8080.
3. Inspecionar o arquivo `nginx/default.conf`.
4. Desligar um serviço e observar impacto na rota específica.
5. Executar playbook Ansible e verificar resultado.
6. Mostrar testes e workflow de CI no GitHub.
