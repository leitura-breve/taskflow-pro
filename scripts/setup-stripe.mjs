#!/usr/bin/env node
/**
 * LEITURA BREVE — Stripe setup
 *
 * Uso (no SEU computador, NUNCA neste container):
 *   1. Rotacione a chave em https://dashboard.stripe.com/apikeys (a antiga vazou no chat).
 *   2. Use uma chave Restricted com permissões: Products write, Prices write, Payment Links write.
 *   3. Rode:
 *        STRIPE_KEY=rk_live_xxx node scripts/setup-stripe.mjs
 *      ou em modo teste:
 *        STRIPE_KEY=rk_test_xxx node scripts/setup-stripe.mjs
 *   4. O script imprime o bloco `window.LB_LINKS = {...}` pronto para colar no index.html.
 *
 * O script é idempotente: usa metadata.lb_sku para reconhecer produtos já criados
 * e reaproveita preços/links existentes. Rode quantas vezes precisar.
 */

const STRIPE_KEY = process.env.STRIPE_KEY;
if (!STRIPE_KEY) {
  console.error('ERRO: defina STRIPE_KEY=rk_live_... (ou rk_test_...) antes de rodar.');
  process.exit(1);
}
if (!/^(rk|sk)_(live|test)_/.test(STRIPE_KEY)) {
  console.error('ERRO: chave invalida. Esperado rk_live_, rk_test_, sk_live_ ou sk_test_.');
  process.exit(1);
}

const BASE = 'https://api.stripe.com/v1';
const auth = 'Basic ' + Buffer.from(STRIPE_KEY + ':').toString('base64');

/** Catalogo: SKU, titulo, autor, paginas, tier, preco em centavos. */
const CATALOG = [
  { sku:'LB.01', title:'Habitos Atomicos',                author:'James Clear',                  pages:39, tier:'c', cents:1699 },
  { sku:'LB.02', title:'O Alquimista',                    author:'Paulo Coelho',                 pages:30, tier:'b', cents:1499 },
  { sku:'LB.03', title:'A Sutil Arte de Ligar o F*da-Se', author:'Mark Manson',                  pages:22, tier:'a', cents:1199 },
  { sku:'LB.04', title:'O Poder do Habito',               author:'Charles Duhigg',               pages:26, tier:'b', cents:1499 },
  { sku:'LB.05', title:'Mindset',                         author:'Carol S. Dweck',               pages:25, tier:'a', cents:1199 },
  { sku:'LB.06', title:'O Milagre da Manha',              author:'Hal Elrod',                    pages:25, tier:'a', cents:1199 },
  { sku:'LB.07', title:'Pai Rico, Pai Pobre',             author:'Robert T. Kiyosaki',           pages:25, tier:'a', cents:1199 },
  { sku:'LB.08', title:'Os 7 Habitos das Pessoas Altamente Eficazes', author:'Stephen R. Covey', pages:25, tier:'a', cents:1199 },
  { sku:'LB.09', title:'Como Fazer Amigos e Influenciar Pessoas',     author:'Dale Carnegie',    pages:25, tier:'a', cents:1199 },
  { sku:'LB.10', title:'O Homem Mais Rico da Babilonia',  author:'George S. Clason',             pages:25, tier:'a', cents:1199 },
  { sku:'LB.11', title:'O Monge e o Executivo',           author:'James C. Hunter',              pages:25, tier:'a', cents:1199 },
  { sku:'LB.12', title:'Inteligencia Emocional',          author:'Daniel Goleman',               pages:25, tier:'a', cents:1199 },
  { sku:'LB.13', title:'Rapido e Devagar',                author:'Daniel Kahneman',              pages:25, tier:'a', cents:1199 },
  { sku:'LB.14', title:'Trabalhe 4 Horas por Semana',     author:'Timothy Ferriss',              pages:25, tier:'a', cents:1199 },
  { sku:'LB.15', title:'Os Segredos da Mente Milionaria', author:'T. Harv Eker',                 pages:26, tier:'b', cents:1499 },
  { sku:'LB.16', title:'Dom Casmurro',                    author:'Machado de Assis',             pages:26, tier:'b', cents:1499 },
  { sku:'LB.17', title:'Capitaes da Areia',               author:'Jorge Amado',                  pages:26, tier:'b', cents:1499 },
  { sku:'LB.18', title:'O Pequeno Principe',              author:'Antoine de Saint-Exupery',     pages:26, tier:'b', cents:1499 },
  { sku:'LB.19', title:'Comece pelo Porque',              author:'Simon Sinek',                  pages:25, tier:'a', cents:1199 },
  { sku:'LB.20', title:'A Coragem de Ser Imperfeito',     author:'Brene Brown',                  pages:25, tier:'a', cents:1199 },
  { sku:'LB.21', title:'Essencialismo',                   author:'Greg McKeown',                 pages:25, tier:'a', cents:1199 },
  { sku:'LB.22', title:'Antifragil',                      author:'Nassim Nicholas Taleb',        pages:25, tier:'a', cents:1199 },
  { sku:'LB.23', title:'A Arte da Guerra',                author:'Sun Tzu',                      pages:27, tier:'b', cents:1499 },
  { sku:'LB.24', title:'Meditacoes',                      author:'Marco Aurelio',                pages:26, tier:'b', cents:1499 },
  { sku:'LB.25', title:'As 48 Leis do Poder',             author:'Robert Greene',                pages:27, tier:'b', cents:1499 },
  { sku:'LB.26', title:'Estrategia Oceano Azul',          author:'W. Chan Kim & Renee Mauborgne',pages:25, tier:'a', cents:1199 },
  { sku:'LB.27', title:'De Zero a Um',                    author:'Peter Thiel',                  pages:25, tier:'a', cents:1199 },
  { sku:'LB.28', title:'Tudo e F*da',                     author:'Mark Manson',                  pages:25, tier:'a', cents:1199 },
  { sku:'LB.29', title:'Em Busca de Sentido',             author:'Viktor Frankl',                pages:25, tier:'a', cents:1199 },
  { sku:'LB.30', title:'Vidas Secas',                     author:'Graciliano Ramos',             pages:26, tier:'b', cents:1499 },
  { sku:'LB.31', title:'Memorias Postumas de Bras Cubas', author:'Machado de Assis',             pages:26, tier:'b', cents:1499 },
  { sku:'LB.32', title:'A Hora da Estrela',               author:'Clarice Lispector',            pages:26, tier:'b', cents:1499 },
  { sku:'LB.33', title:'Quarto de Despejo',               author:'Carolina Maria de Jesus',      pages:26, tier:'b', cents:1499 },
  { sku:'LB.34', title:'Cem Anos de Solidao',             author:'Gabriel Garcia Marquez',       pages:26, tier:'b', cents:1499 },
  { sku:'LB.35', title:'1984',                            author:'George Orwell',                pages:26, tier:'b', cents:1499 },
  { sku:'LB.36', title:'O Diario de Anne Frank',          author:'Anne Frank',                   pages:26, tier:'b', cents:1499 },
  { sku:'LB.37', title:'A Revolucao dos Bichos',          author:'George Orwell',                pages:26, tier:'b', cents:1499 },
  { sku:'LB.38', title:'Sapiens',                         author:'Yuval Noah Harari',            pages:26, tier:'b', cents:1499 },
];

const SUBSCRIPTION = {
  sku: 'BIBLIOTECA.ANUAL',
  name: 'LEITURA BREVE — Biblioteca Anual',
  description: 'Acesso completo a toda a colecao por 12 meses. Novos volumes incluidos automaticamente.',
  cents: 4999,
};

async function stripe(method, path, params) {
  const opts = { method, headers: { Authorization: auth } };
  if (params) {
    const body = new URLSearchParams();
    const flatten = (obj, prefix='') => {
      for (const [k, v] of Object.entries(obj)) {
        if (v === undefined || v === null) continue;
        const key = prefix ? `${prefix}[${k}]` : k;
        if (Array.isArray(v)) {
          v.forEach((item, i) => {
            if (typeof item === 'object') flatten(item, `${key}[${i}]`);
            else body.append(`${key}[${i}]`, String(item));
          });
        } else if (typeof v === 'object') {
          flatten(v, key);
        } else {
          body.append(key, String(v));
        }
      }
    };
    flatten(params);
    opts.body = body.toString();
    opts.headers['Content-Type'] = 'application/x-www-form-urlencoded';
  }
  const res = await fetch(`${BASE}${path}`, opts);
  const data = await res.json();
  if (!res.ok) {
    throw new Error(`Stripe ${method} ${path}: ${data.error?.message || res.statusText}`);
  }
  return data;
}

/** Busca produto existente pelo metadata.lb_sku. */
async function findProductBySku(sku) {
  const q = encodeURIComponent(`metadata['lb_sku']:'${sku}' AND active:'true'`);
  const data = await stripe('GET', `/products/search?query=${q}`);
  return data.data?.[0] || null;
}

/** Busca primeiro price ativo de um produto. */
async function findPrice(productId, recurring=false) {
  const q = `product=${productId}&active=true&limit=10`;
  const data = await stripe('GET', `/prices?${q}`);
  return data.data?.find(p => (recurring ? !!p.recurring : !p.recurring)) || null;
}

/** Busca payment link ativo pelo metadata. */
async function findPaymentLink(sku) {
  const data = await stripe('GET', `/payment_links?active=true&limit=100`);
  return data.data?.find(l => l.metadata?.lb_sku === sku) || null;
}

async function ensureBook(item) {
  process.stdout.write(`  ${item.sku.padEnd(7)} ${item.title.slice(0,42).padEnd(42)} `);

  let product = await findProductBySku(item.sku);
  if (!product) {
    product = await stripe('POST', '/products', {
      name: `${item.sku} · ${item.title}`,
      description: `Resumo PDF do livro "${item.title}", de ${item.author}. Aproximadamente ${item.pages} paginas, leitura em ~22 min. Colecao LEITURA BREVE.`,
      metadata: { lb_sku: item.sku, lb_author: item.author, lb_pages: item.pages, lb_tier: item.tier },
      tax_code: 'txcd_10000000', // Digital goods
    });
  }

  let price = await findPrice(product.id, false);
  if (!price || price.unit_amount !== item.cents) {
    price = await stripe('POST', '/prices', {
      product: product.id,
      currency: 'brl',
      unit_amount: item.cents,
      metadata: { lb_sku: item.sku },
    });
  }

  let link = await findPaymentLink(item.sku);
  if (!link) {
    link = await stripe('POST', '/payment_links', {
      line_items: [{ price: price.id, quantity: 1 }],
      metadata: { lb_sku: item.sku },
      after_completion: { type: 'hosted_confirmation', hosted_confirmation: { custom_message: `Obrigado por adquirir ${item.title}. O PDF chegara no seu email em ate 5 minutos.` } },
      allow_promotion_codes: true,
      billing_address_collection: 'auto',
    });
  }

  console.log('OK');
  return link.url;
}

async function ensureSubscription() {
  const item = SUBSCRIPTION;
  process.stdout.write(`  ${item.sku.padEnd(18)} ${item.name.slice(0,42).padEnd(42)} `);

  let product = await findProductBySku(item.sku);
  if (!product) {
    product = await stripe('POST', '/products', {
      name: item.name,
      description: item.description,
      metadata: { lb_sku: item.sku, lb_type: 'subscription' },
      tax_code: 'txcd_10000000',
    });
  }

  let price = await findPrice(product.id, true);
  if (!price || price.unit_amount !== item.cents) {
    price = await stripe('POST', '/prices', {
      product: product.id,
      currency: 'brl',
      unit_amount: item.cents,
      recurring: { interval: 'year' },
      metadata: { lb_sku: item.sku },
    });
  }

  let link = await findPaymentLink(item.sku);
  if (!link) {
    link = await stripe('POST', '/payment_links', {
      line_items: [{ price: price.id, quantity: 1 }],
      metadata: { lb_sku: item.sku },
      after_completion: { type: 'hosted_confirmation', hosted_confirmation: { custom_message: 'Bem-vindo a Biblioteca LEITURA BREVE. Voce recebera o acesso em seu email em ate 10 minutos.' } },
      allow_promotion_codes: true,
      billing_address_collection: 'required',
    });
  }

  console.log('OK');
  return link.url;
}

(async () => {
  const mode = STRIPE_KEY.includes('_test_') ? 'TEST' : 'LIVE';
  console.log(`\nLEITURA BREVE — Stripe setup [${mode}]\n`);

  console.log('Validando chave...');
  const acct = await stripe('GET', '/account');
  console.log(`  Conta: ${acct.id} (${acct.business_profile?.name || acct.email || acct.country})\n`);

  console.log('Criando assinatura...');
  const subUrl = await ensureSubscription();

  console.log('\nCriando 38 produtos avulsos...');
  const links = {};
  for (const item of CATALOG) {
    links[item.sku] = await ensureBook(item);
  }

  console.log('\n' + '='.repeat(72));
  console.log('PRONTO. Cole o bloco abaixo no index.html, logo antes do </body>:');
  console.log('='.repeat(72) + '\n');

  console.log('<script>');
  console.log('window.LB_LINKS = {');
  for (const [sku, url] of Object.entries(links)) {
    console.log(`  '${sku}': '${url}',`);
  }
  console.log(`  '${SUBSCRIPTION.sku}': '${subUrl}'`);
  console.log('};');
  console.log('</script>');
  console.log('\n' + '='.repeat(72) + '\n');
})().catch(err => {
  console.error('\nFALHA:', err.message);
  process.exit(1);
});
