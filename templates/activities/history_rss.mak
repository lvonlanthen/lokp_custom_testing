<?xml version="1.0" encoding="utf-8"?>
<%
from datetime import datetime
%>
<rss version="2.0">
    <channel>
        <title>${_('Version history of activity #%s' % versions[0]['identifier'].split('-')[0].upper())}</title>
        <link></link>
        ## <description>description</description>
        <language>en-US</language>
        ## <copyright>Autor des Feeds</copyright>
        <pubDate>Sat, 5 Apr 2014 22:11:29</pubDate>
        <image>
            <url>/custom/img/logo.png</url>
            <title>${_('Land Observatory')}</title>
            <link>${request.route_url('index')}</link>
        </image>

        % for v in versions:
        <item>
            <title>${_("Version %s: %s" % (v['version'], v['statusName']))}</title>
            <description>
                <![CDATA[
                <span>${_("Last change on %s by user %s" % (v['timestamp'], v['username']))}</span><br/>
                % if isModerator and v['statusId'] == 1:
                <span>
                    <a href="${request.route_url('activities_read_one', output='review', uid=v['identifier'], _query=(('new', v['version']),))}">
                        ${_('Review this version')}
                    </a>
                </span><br/>
                % endif
                % if v['statusId'] != 2:
                <span>
                    <a href="${request.route_url('activities_read_one', output='compare', uid=v['identifier'], _query=(('ref', v['version']),('new', activeVersion)))}">
                        ${_('Compare this version with the active version')}
                    </a>
                </span>
                <br/>
                % endif
                <span>
                    <a href="${request.route_url('activities_read_one', output='html', uid=v['identifier'], _query=(('v', v['version']),))}">
                        ${_('View this version')}
                    </a>
                </span>
                ]]>
            </description>
            <link>${request.route_url('activities_read_one', output='html', uid=v['identifier'], _query=(('v', v['version']),))}</link>
            <author>${v['username']}</author>
            <guid>${"%s?v=%s" % (v['identifier'], v['version'])}</guid>
            <pubDate>${datetime.strptime(v['timestamp'], '%Y-%m-%d %H:%M:%S').strftime("%a, %d %b %Y %H:%M:%S %Z")}</pubDate>
        </item>
        % endfor
    </channel>
</rss>
