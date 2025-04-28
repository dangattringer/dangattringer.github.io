import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';


// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'd://log',
  // tagline: 'Dinosaurs are cool',
  favicon: 'img/favicon/favicon.ico',

  // Set the production url of your site here
  url: 'https://dangattringer.github.io',
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'dangattringer', // Usually your GitHub org/user name.
  projectName: 'dangattringer.github.io', // Usually your repo name.
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  customFields: {
    name: 'Daniel Gattringer',
    descriptionLines: [
      "AI • MLOps • DevOps",
      "Covering Computer Vision, NLP, and more.",
      "My personal tech log and discoveries."
    ]
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  plugins: [
    [
      "posthog-docusaurus",
      {
        apiKey: process.env.POSTHOG_API_KEY || "",
        appUrl: "https://eu.i.posthog.com",
        enableInDevelopment: false,
      },
    ],
  ],


  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          exclude: ['**/*.draft.md'],
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          //   editUrl:
          //     'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: false,
        // blog: {
        //   showReadingTime: true,
        //   feedOptions: {
        //     type: ['rss', 'atom'],
        //     xslt: true,
        //   },
        //   // Please change this to your repo.
        //   // Remove this to remove the "edit this page" links.
        //   // editUrl:
        //   //   'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        //   // Useful options to enforce blogging best practices
        //   onInlineTags: 'warn',
        //   onInlineAuthors: 'warn',
        //   onUntruncatedBlogPosts: 'warn',
        // },
        theme: {
          customCss: './src/css/custom.css',
        },
        // gtag: {},
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'd://log',
      // logo: {
      //   alt: 'My Site Logo',
      //   src: 'img/fox.png',
      // },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'notes',
          position: 'left',
          label: 'Notes',
        },
        // {
        //   type: 'docSidebar',
        //   sidebarId: 'tutorialSidebar',
        //   position: 'left',
        //   label: 'Tutorial',
        // },
        // { to: '/blog', label: 'Blog', position: 'left' },
        {
          href: 'https://github.com/dangattringer/',
          "link": "external",
          position: 'right',
          className: 'header-github-link',
          'aria-label': 'GitHub repository',
        },
      ],
    },
    footer: {
      // style: 'dark',
      links: [
        {
          items: [
            {
              html: `<a class='footer__link-item' target='_blank' rel='noopener noreferrer' href='https://x.com/_dangat'><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="X logo" class="svg-inline--fa fa-twitter fa-w-16">  <path fill='currentColor' d="M 6.9199219 6 L 21.136719 26.726562 L 6.2285156 44 L 9.40625 44 L 22.544922 28.777344 L 32.986328 44 L 43 44 L 28.123047 22.3125 L 42.203125 6 L 39.027344 6 L 26.716797 20.261719 L 16.933594 6 L 6.9199219 6 z" transform="translate(-1, -1) scale(1.3)"/> </svg></a>`
            },
            {
              html: `<a class='footer__link-item' target='_blank' rel='noopener noreferrer' href='https://linkedin.com/in/daniel-gattringer06'><svg role='img' aria-hidden='true' focusable='false' data-prefix='fab' data-icon='linkedin' class='svg-inline--fa fa-linkedin fa-w-14' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 448 512'><path fill='currentColor' d='M416 32H31.9C14.3 32 0 46.5 0 64.3v383.4C0 465.5 14.3 480 31.9 480H416c17.6 0 32-14.5 32-32.3V64.3c0-17.8-14.4-32.3-32-32.3zM135.4 416H69V202.2h66.5V416zm-33.2-243c-21.3 0-38.5-17.3-38.5-38.5S80.9 96 102.2 96c21.2 0 38.5 17.3 38.5 38.5 0 21.3-17.2 38.5-38.5 38.5zm282.1 243h-66.4V312c0-24.8-.5-56.7-34.5-56.7-34.6 0-39.9 27-39.9 54.9V416h-66.4V202.2h63.7v29.2h.9c8.9-16.8 30.6-34.5 62.9-34.5 67.2 0 79.7 44.3 79.7 101.9V416z'></path></svg></a>`
            },
            {
              html: `<a class='footer__link-item' target='_blank' rel='noopener noreferrer' href='https://medium.com/@dangattringer'><svg xmlns="http://www.w3.org/2000/svg" aria-hidden='true' focusable='false'  viewBox="0 0 64 64" role="img" aria-label="m logo" class="svg-inline--fa fa-medium fa-w-16"> <path fill='currentColor' d="M52,8H12c-2.209,0-4,1.791-4,4v40c0,2.209,1.791,4,4,4h40c2.209,0,4-1.791,4-4V12C56,9.791,54.209,8,52,8z M47,19.5	l-1.821,2.197C45.064,21.811,45,21.965,45,22.125V41.75c0,0.16,0.064,0.314,0.179,0.428L47,44.546V45H37v-0.454l2.821-2.368	C39.936,42.064,40,41.91,40,41.75V23.879L31.848,45h-0.001h-1.543L22,24.375v16.108c0,0.22,0.076,0.433,0.215,0.605L25,44.546V45h-8	v-0.454l2.783-3.438C19.923,40.936,20,40.721,20,40.5V22.388c0-0.142-0.05-0.279-0.142-0.388L18,19.5V19h7.097l7.624,19.183	L40.002,19H47V19.5z" transform="translate(-4.5, -4.5) scale(1.15)"/> </svg></a>`
            },
            {
              html: `<a class='footer__link-item' target='_blank' rel='noopener noreferrer' href='https://dev.to/dangattringer'><svg xmlns="http://www.w3.org/2000/svg" aria-hidden='true' focusable='false'  viewBox="0 0 64 64" class='svg-inline--fa fa-dev fa-w-16' role="img" aria-label="dev logo"> <path fill='currentColor' d="M 2 7 L 2 25 L 30 25 L 30 7 L 2 7 z M 4 9 L 28 9 L 28 23 L 4 23 L 4 9 z M 6 11 L 6 21 L 9 21 C 10.654 21 12 19.654 12 18 L 12 14 C 12 12.346 10.654 11 9 11 L 6 11 z M 16 11 C 14.897 11 14 11.897 14 13 L 14 19 C 14 20.103 14.897 21 16 21 L 18 21 L 18 19 L 16 19 L 16 17 L 18 17 L 18 15 L 16 15 L 16 13 L 18 13 L 18 11 L 16 11 z M 19.691406 11 L 21.775391 20.025391 C 21.907391 20.595391 22.415 21 23 21 C 23.585 21 24.092609 20.595391 24.224609 20.025391 L 26.308594 11 L 24.255859 11 L 23 16.439453 L 21.744141 11 L 19.691406 11 z M 8 13 L 9 13 C 9.552 13 10 13.448 10 14 L 10 18 C 10 18.552 9.552 19 9 19 L 8 19 L 8 13 z" transform="translate(0, 0) scale(2)"/> </svg></a>`
            },
          ]
        }
      ],
      copyright: `<span style='font-size: 10px; '>Copyright © ${new Date().getFullYear()} Daniel Gattringer. Built with Docusaurus.</span>`
    },
    prism: {
      theme: prismThemes.jettwaveLight,
      darkTheme: prismThemes.jettwaveDark,
      additionalLanguages: ['bash', 'python', 'java', 'go', 'cpp', 'json', 'yaml', 'rust', 'css'],
    },
    sitemap: {
      cacheTime: 600 * 1000,
      changefreq: 'weekly',
      priority: 0.5
    }
  } satisfies Preset.ThemeConfig,
};

export default config;
