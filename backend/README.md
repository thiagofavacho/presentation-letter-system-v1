## Importação de planilhas

Antes de iniciar o backend atualizado, instale a dependência de leitura de
planilhas junto das dependências existentes:

```bash
pip install -r requirements.txt -r requirements-import.txt
```

As rotas administrativas são `POST /promoters/import` e `POST /stores/import`.
Elas aceitam apenas arquivos `.xlsx` de até 10 MB, atualizam registros já
existentes pela matrícula ou código e cancelam toda a importação se alguma
linha obrigatória estiver inválida.
