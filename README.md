# Cumbuco de Buggy — Site oficial

Site de passeios de buggy em **Cumbuco (Caucaia – CE)** com o bugueiro credenciado **Igor Vasconcelos**.
Site estático, rápido e **trilíngue** (Português, Inglês e Espanhol), com reservas feitas pelo **WhatsApp**.

---

## Sumário

1. [Visão geral](#visão-geral)
2. [Estrutura de pastas](#estrutura-de-pastas)
3. [Como o site é gerado](#como-o-site-é-gerado)
4. [Rodar no computador](#rodar-no-computador)
5. [Como editar o conteúdo](#como-editar-o-conteúdo)
6. [Fotos e vídeos](#fotos-e-vídeos)
7. [Seções da página](#seções-da-página)
8. [Responsividade](#responsividade)
9. [SEO](#seo)
10. [Publicar (deploy)](#publicar-deploy)

---

## Visão geral

| Item | Detalhe |
|---|---|
| Tipo | Site estático (HTML + CSS + JavaScript puro, sem framework) |
| Idiomas | `pt-br/`, `en/`, `es/` — com troca de idioma no topo |
| Contato | Todos os botões abrem o WhatsApp com mensagem pronta |
| Gerador | `build.py` (Python 3, sem dependências externas) |

---

## Estrutura de pastas

```
Cumbuco-de-Buggy/
├── build.py            # TODOS os textos (PT/EN/ES), preços, avaliações e configurações
├── template.html       # Estrutura HTML única usada pelos 3 idiomas
├── index.html          # Página raiz (redireciona para o idioma)
├── pt-br/index.html    # GERADO — não editar à mão
├── en/index.html       # GERADO — não editar à mão
├── es/index.html       # GERADO — não editar à mão
├── sitemap.xml         # GERADO
├── robots.txt          # GERADO
└── assets/
    ├── css/style.css   # Todo o visual (cores, layout, responsivo)
    ├── js/main.js      # Menu, galeria, carrossel, formulário de busca, animações
    ├── js/i18n.js      # GERADO — textos para trocar de idioma sem recarregar
    ├── img/            # Fotos otimizadas usadas no site
    │   └── brincadeiras/  # Fotos das atividades opcionais
    └── video/          # Vídeos da seção "Cumbuco em movimento"
```

> ⚠️ **Regra de ouro:** nunca edite `pt-br/`, `en/`, `es/`, `i18n.js`, `sitemap.xml` ou `robots.txt` diretamente.
> Edite `build.py` (textos) ou `template.html` (estrutura) e rode o build.

---

## Como o site é gerado

```
build.py (textos PT/EN/ES)  ─┐
                             ├──►  python build.py  ──►  pt-br/ · en/ · es/ · i18n.js · sitemap · robots
template.html (estrutura)  ──┘
```

- No `template.html`, cada texto aparece como `{{chave}}` — ex.: `{{t1.title}}`.
- No `build.py`, o dicionário de textos define cada chave nos 3 idiomas:

```python
"t1.title": {"pt": "Passeio Completo", "en": "Complete Buggy Tour", "es": "Paseo Completo"},
```

- Variações especiais no template:
  - `{{attr:chave}}` → texto seguro para atributos (`alt`, `placeholder`).
  - `{{wa:chave}}` → link do WhatsApp com mensagem pronta.
  - `data-i18n="chave"` → permite trocar o idioma na hora, sem recarregar.

---

## Rodar no computador

Requisito: **Python 3**.

```bash
# 1. Gerar o site
python build.py

# 2. Servidor local
python -m http.server 8080

# 3. Abrir no navegador
http://localhost:8080/pt-br/
```

Depois de cada alteração: rode `python build.py` de novo e recarregue com **Ctrl + F5**.

---

## Como editar o conteúdo

Tudo fica no `build.py`. Busque pela chave e altere os textos nos 3 idiomas.

| O que mudar | Onde (`build.py`) |
|---|---|
| Número do WhatsApp | `WHATSAPP = "55..."` |
| Domínio do site | `SITE = "https://..."` |
| Avaliações do Google | lista `REVIEWS`, `GOOGLE_RATING`, `GOOGLE_COUNT` (usar só depoimentos reais) |
| Topo (hero) | chaves `hero.*` |
| Cards "Por que passear com Igor" | chaves `cred.*` |
| Passeio Completo | chaves `t1.*` |
| Passeio Tradicional | chaves `t2.*` |
| Paradas do roteiro | chaves `st.*` e `tour.intro`, `tour.note` |
| Preços das atividades opcionais | chaves `op.*.p` (ex.: `op.skibunda.p`) |
| Formulário "Buscamos você" | chaves `pick.*` |
| Buggy Credenciado | chaves `cr.*` |
| Avisos importantes | chaves `notice.*` |
| Rodapé | chaves `foot.*` |

**Exemplo — mudar um preço:**

```python
"op.skibunda.p": {"pt": "R$ 30 por pessoa", "en": "R$ 30 per person", "es": "R$ 30 por persona"},
```

**Adicionar uma parada no roteiro:** crie as chaves `st.nova.t` / `st.nova.d` no `build.py` e acrescente
um `<li>` na lista `<ol class="stops">` do passeio correspondente no `template.html`.

---

## Fotos e vídeos

- Use **JPG** otimizado (~960×1280 px, qualidade ~82) em `assets/img/`.
- Fotos do iPhone (`.HEIC`) precisam ser convertidas antes. Exemplo com Python:

```python
from PIL import Image, ImageOps
import pillow_heif; pillow_heif.register_heif_opener()
im = ImageOps.exif_transpose(Image.open("IMG_0000.HEIC")).convert("RGB")
im.thumbnail((960, 1280))
im.save("assets/img/nome-da-foto.jpg", quality=82, optimize=True, progressive=True)
```

- Para trocar uma foto, altere o `src` correspondente no `template.html`.
- Os arquivos originais (`.HEIC`, `.MOV`, `.MP4` na raiz) **não vão para o GitHub** (ver `.gitignore`).

---

## Seções da página

1. **Topo (hero)** — chamada principal, selos e botão de reserva
2. **Por que passear com Igor** — experiência, credenciamento, seguro passageiro, buggy com som
3. **Sobre** — apresentação do Igor
4. **Passeios** — Completo (~2h30, 28,5 km) e Tradicional (~1h30), com roteiro expansível
5. **Brincadeiras opcionais** — atividades e preços
6. **Buscamos você onde estiver!** — formulário que monta a mensagem do WhatsApp
7. **Galeria de Fotos** — com filtros por categoria e visualização ampliada
8. **Vídeo** — Cumbuco em movimento
9. **Buggy Credenciado** — como identificar um buggy autorizado
10. **Avisos importantes**
11. **Avaliações** — depoimentos reais do Google
12. **Rodapé**

---

## Responsividade

O layout se adapta a celular, tablet e computador (`assets/css/style.css`, pontos de quebra em
380, 560, 600, 720, 860, 960, 1060 e 1200 px). A rolagem horizontal é bloqueada para evitar
"arrastar para o lado" no celular.

Para testar: Chrome → **F12** → **Ctrl + Shift + M** → escolha iPhone SE, Galaxy, iPad etc.

---

## SEO

- `<title>`, descrição e palavras-chave por idioma (chaves `meta.*`)
- Tags `hreflang` ligando PT/EN/ES
- Dados estruturados (Schema.org `TouristTrip`)
- `sitemap.xml` e `robots.txt` gerados automaticamente

---

## Publicar (deploy)

Por ser estático, basta enviar a pasta inteira (exceto os originais ignorados) para qualquer
hospedagem: Hostinger, GitHub Pages, Netlify, Vercel etc.

1. Ajuste `SITE` no `build.py` para o domínio final.
2. Rode `python build.py`.
3. Envie os arquivos para a hospedagem.

---

© Cumbuco de Buggy — Igor Vasconcelos · Bugueiro credenciado em Cumbuco, Ceará.
