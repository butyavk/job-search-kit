// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://butyavk.github.io',
  base: '/job-search-kit',
  trailingSlash: 'always',
  integrations: [
    starlight({
      title: { en: 'Job search kit', ru: 'Job search kit' },
      description: 'The whole job search with Claude: search, rank, apply, track, follow up, prepare, mock and debrief. Claude prepares; you send.',
      favicon: '/favicon.png',
      defaultLocale: 'root',
      locales: {
        root: { label: 'English', lang: 'en' },
        ru: { label: 'Русский', lang: 'ru' },
      },
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/butyavk/job-search-kit' }],
      editLink: { baseUrl: 'https://github.com/butyavk/job-search-kit/edit/main/' },
      sidebar: [
        { label: 'Start', translations: { ru: 'Начало' }, items: [
          { slug: 'install', label: 'Install and connect', translations: { ru: 'Установка и подключения' } },
          { slug: 'path', label: 'The path: 9 commands', translations: { ru: 'Путь: 9 команд' } },
        ] },
        { label: 'How it works', translations: { ru: 'Как устроено' }, items: [
          { slug: 'answer-blocks', label: 'Answer blocks', translations: { ru: 'Кубики ответов' } },
          { slug: 'sources', label: 'Where vacancies come from', translations: { ru: 'Откуда вакансии' } },
          { slug: 'autonomy', label: 'Autonomy and privacy', translations: { ru: 'Самостоятельность и приватность' } },
          { slug: 'how-it-works', label: 'The method and its numbers', translations: { ru: 'Метод и цифры' } },
        ] },
      ],
    }),
  ],
});
