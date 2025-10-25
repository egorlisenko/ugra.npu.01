import { defineConfig } from '@rsbuild/core';
import { pluginReact } from '@rsbuild/plugin-react';
import { pluginSass } from '@rsbuild/plugin-sass';
import { pluginSvgr } from '@rsbuild/plugin-svgr';

export default defineConfig({
  plugins: [pluginReact(), pluginSass(), pluginSvgr()],
  html: {
    title: 'Збройні Сили України | UG-01',
    favicon: './src/assets/images/AFoU.png',
    meta: {
      charset: 'UTF-8',
      viewport: 'width=device-width, initial-scale=1.0',
      description: 'Офіційний портал Збройних Сил України UKRAINE GTA 01 — Центральна Україна. Дізнайся про службу, керівництво, підрозділи та можливість доєднатися до армії.',
      keywords: 'ЗСУ гта, ЗСУ01, Ukraine GTA, ЗСУ 01 сервер, Юкрейн гта, Збройні Сили України 01, ЗСУ 1, ЗСУ сайт 01 сервер',
      author: 'beloglazikov',

      // Security 
      'http-equiv': 'X-UA-Compatible', content: 'IE=edge',
      'format-detection': 'telephone=no',

      // Apple 
      'mobile-web-app-capable': 'yes',
      'apple-mobile-web-app-status-bar-style': 'black-translucent',

      'og:title': 'Збройні Сили України — Офіційний портал',
      'og:description': 'Служба, підрозділи, керівництво та все про ЗСУ — у тебе під рукою.',

      'twitter:card': 'summary_large_image',
      'twitter:title': 'Збройні Сили України — Офіційний портал',
      'twitter:description': 'Всі важливі відповіді щодо служби, підрозділів та вступу до армії'
    }
  },
  output: {
    assetPrefix: '/ugra.army.01/',
  }
});
