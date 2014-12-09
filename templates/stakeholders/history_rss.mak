<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
  <channel>
    <title>${_('Version history of stakeholder #%s' % versions[0]['id'].split('-')[0].upper())}</title>
    <link></link>
    <language>en-US</language>
    <pubDate>Sat, 5 Apr 2014 22:11:29</pubDate>
    <image>
      <url>/custom/img/logo.png</url>
      <title>${_('[LOKP]')}</title>
      <link>${request.route_url('index')}</link>
    </image>
    % for v in versions:
      <item>
        <title>${_("Version %s: %s" % (v['version'], v['status']))}</title>
        <description>
          <![CDATA[
            <span>${_("Last change on %s by user %s" % (v['timestamp'], v.get('user', dict()).get('username')))}</span><br/>
            % if is_moderator and v.get('status_id') == 1:
              <span>
                <a href="${request.route_url('stakeholders_read_one', output='review', uid=v['id'], _query=(('new', v['version']),))}">
                  ${_('Review this version')}
                </a>
              </span><br/>
            % endif
            % if v.get('status_id') != 2:
              <span>
                <a href="${request.route_url('stakeholders_read_one', output='compare', uid=v['id'], _query=(('ref', v['version']),('new', active_version)))}">
                  ${_('Compare this version with the active version')}
                </a>
              </span><br/>
            % endif
            <span>
              <a href="${request.route_url('stakeholders_read_one', output='html', uid=v['id'], _query=(('v', v['version']),))}">
                ${_('View this version')}
              </a>
            </span>
          ]]>
        </description>
        <link>${request.route_url('stakeholders_read_one', output='html', uid=v['id'], _query=(('v', v['version']),))}</link>
        <author>${v.get('user', dict()).get('username')}</author>
        <guid>${"%s?v=%s" % (v['id'], v['version'])}</guid>
        <pubDate>${v.get('timestamp')}</pubDate>
      </item>
    % endfor
  </channel>
</rss>
