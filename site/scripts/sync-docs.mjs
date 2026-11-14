// Copies the long docs from the repository into the site, so each text has one source.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const out = resolve(root, 'site', 'src', 'content', 'docs');
const gh = 'https://github.com/butyavk/job-search-kit/blob/main/';

const pages = [
  { from: 'docs/how-it-works.md', to: 'how-it-works.md', title: 'The method and its numbers', description: 'How the search worked: the gate, applications, follow-ups, interview prep, and what did not work.' },
  { from: 'docs/how-it-works.ru.md', to: 'ru/how-it-works.md', title: 'Метод и цифры', description: 'Как был устроен поиск: гейт, подачи, фоллоу-апы, подготовка к интервью и что не сработало.' },
  { from: 'docs/sources.ru.md', to: 'ru/sources.md', title: 'Откуда берутся вакансии', description: 'Все источники вакансий — LinkedIn, борды компаний в ATS, площадки, борды стран — и как читается каждый.' },
  { from: 'skills/job-search/sources.md', to: 'sources.md', title: 'Where vacancies come from', description: 'Every source of vacancies — LinkedIn, company ATS boards, job sites, country boards — and how each one reads.' },
];

for (const p of pages) {
  let text = readFileSync(resolve(root, p.from), 'utf8');
  text = text
    .replace(/^# .*\n+/, '')                                        // the page title comes from frontmatter
    .replace(/^\[(Русская версия|English version)\]\([^)]*\)\n+/m, '') // the site has a language switcher
    .replace(/^Перевод `skills\/job-search\/sources\.md`[^\n]*\n+/m, '')
    .replace(/^A Russian translation for people: [^\n]*\n+/m, '')
    .replace(/<a id="[^"]*"><\/a>\n/g, '')
    .replace(/\]\((?!https?:|#)([^)]+)\)/g, (_, link) => `](${gh}${link.replace(/^\.\.\//, '')})`);
  const front = `---\ntitle: ${JSON.stringify(p.title)}\ndescription: ${JSON.stringify(p.description)}\n---\n\n`;
  mkdirSync(dirname(resolve(out, p.to)), { recursive: true });
  writeFileSync(resolve(out, p.to), front + text);
}
console.log(`synced ${pages.length} pages`);
