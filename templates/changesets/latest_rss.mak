<?xml version="1.0" encoding="utf-8"?>

<rss version="2.0">

  <channel>
    <title>${_('Latest approved Changesets')} - ${_('Land Observatory')}</title>
    <link>${link}</link>
    <description>${_('The latest approved changes on the Land Observatory')}</description>
    <language>en-US</language>
    <copyright>Autor des Feeds</copyright>
    <pubDate>Thu, 3 Apr 2014 16:54:19</pubDate>
    <image>
      <url>${image['url']}</url>
      <title>${image['title']}</title>
      <link>${image['link']}</link>
    </image>

    % for item in items:
    <item>
      <title>${item['title']}</title>
      <description>${item['description']}</description>
      <link>${item['link']}</link>
      <author>${item['author']}</author>
      <guid>${item['guid']}</guid>
      <pubDate>${item['pubDate']}</pubDate>
    </item>
    % endfor

  </channel>

</rss>
