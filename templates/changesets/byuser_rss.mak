<?xml version="1.0" encoding="utf-8"?>

<rss version="2.0">

  <channel>
    <title>${_('Approved changesets by %s' % username)} - ${_('Land Observatory')}</title>
    <link>${request.route_url("changesets_read_latest", output="rss")}</link>
    <description>${_('Approved changesets by %s' % username)}</description>
    <language>en-US</language>
    <copyright>${username}</copyright>
    <pubDate>Thu, 3 Apr 2014 16:54:19</pubDate>
    <image>
      <url>/custom/img/logo.png</url>
      <title>www.landobservatory.org</title>
      <link>${request.route_url('index')}</link>
    </image>

    % for item in items:
    <item>
      <%
      short_uuid = item['identifier'].split('-')[0].upper()
      timestamp = item['timestamp'].strftime('%a, %d %b %Y %H:%M:%S')
      if item['type'] == 'activity':
          title = _(u'Activity #%s updated to version %s' % (short_uuid, item['version']))
          activity_link = request.route_url('activities_read_one', output='html', uid=item['identifier'], _query={'v': item['version']})
          desc = 'Update of activity <a href=\"%s\">#%s</a> on %s to version&nbsp;%s' % (activity_link, short_uuid, timestamp, item['version'])
      else:
          title = _(u'Stakeholder #%s updated to version %s' % (short_uuid, item['version']))
          stakeholder_link = request.route_url('stakeholders_read_one', output='html', uid=item['identifier'], _query={'v': item['version']})
          desc = 'Update of stakeholder <a href=\"%s\">#%s</a> on %s to version&nbsp;%s' % (stakeholder_link, short_uuid, timestamp, item['version'])
      %>
      <title>${title | n}</title>
      <description><![CDATA[${desc | n}]]></description>
      <link>${activity_link}</link>
      ##<author>${username}</author>
      ##<guid>${'%s?v=%s' % (item['identifier'], item['version'])}</guid>
      ##<pubDate>${timestamp}</pubDate>
    </item>
    % endfor

  </channel>

</rss>
