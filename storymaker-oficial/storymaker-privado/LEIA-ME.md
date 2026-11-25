# storymaker-privado

Pasta privada do cadastro de portfólios. **Suba esta pasta ao lado do `public_html`, nunca dentro dele.**

```
domains/seu-dominio/
├── public_html/
│   └── cadastro/        ← site/cadastro/
└── storymaker-privado/  ← esta pasta
    ├── lib.php
    ├── config.php       ← criar a partir de config.exemplo.php (não vai para o GitHub)
    └── dados/           ← banco SQLite (criado sozinho; não vai para o GitHub)
```

1. Copie `config.exemplo.php` para `config.php` e preencha senha (hash) e sal.
2. Deixe `'aberto' => false` até a política de privacidade ser revisada.
3. Detalhes e pendências: `docs/cadastro-portfolios.md`.
