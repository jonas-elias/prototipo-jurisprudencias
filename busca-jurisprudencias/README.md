# prototipo-jurisprudencias

Para iniciar o protótipo de busca de jurisprudências, basta realizar os pontos indicados abaixo:

- Adicionar a `openai.api_key` no arquivo `main.py` na raíz do repositório
- Adicionar a `api_key` do Qdrant no arquivo `main.py` na raíz do repositório
- Executar o comando `python3 main.py` na raíz do repositório (iniciar o servidor da API)
- Abrir o arquivo `index.html`

Quando a busca por um prompt específico ser requisitada, a aplicação realiza a inserção de um arquivo `.json` (nomeado com um hash) na pasta `database`. Quando o profissional jurídico salva a ordenação, é criado um novo arquivo `.html` (nomeado com o mesmo hash anterior) que indica a ordem das jurisprudências.

Prompts:

1: Ação de reembolso de honorários médicos em plano de saúde resulta em sentença de improcedência. Autor diagnosticado com carcinoma buscou consultas e cirurgias com médico particular, apesar de existir rede credenciada. Contrato não prevê reembolso para livre escolha de profissionais. Falha no atendimento não comprovada. Legislação e contrato não obrigam reembolso em casos de prestadores particulares.

2: O caso envolve disputa entre segurado e plano de saúde pela cobertura parcial de cirurgia ortognática. Médico solicitou procedimentos negados pela junta médica da seguradora. Alegação de cerceamento de defesa pela seguradora. Necessidade de prova pericial para esclarecimento técnico. Essencial garantir equidade na resolução.

3: Ação de obrigação de fazer visa custeio de terapias multidisciplinares para transtorno do espectro autista. Tutela provisória indeferida. Autor busca atendimento fora da rede credenciada do plano. Não há evidências de que dentro da rede não haja prestadores aptos a fornecer os atendimentos necessários.

4: Ação contra plano de saúde resulta em sentença favorável ao paciente. Seguradora contesta cobertura de procedimentos e materiais para cirurgia ortognática, negados pela junta médica. Disputa técnica levanta questões sobre a necessidade dos itens requisitados. Alegação de cerceamento de defesa pela seguradora. Prova pericial necessária para esclarecer aspectos técnicos.