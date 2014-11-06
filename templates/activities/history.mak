<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%
from lmkp.views.views import (
    get_current_locale,
    get_current_profile,
)
%>

<%def name="title()">${_('Version History')}</%def>

<div class="container">
    <div class="content no-border">

        ## Session messages
        <%include file="lmkp:templates/parts/sessionmessage.mak"/>

        % if len(versions) == 0:
            <div class="row-fluid">
                <p>${_('No version to display.')}</p>
            </div>
        % else:
            <div class="row-fluid">
                <div class="span9 text-right">
                    <a href="${request.route_url('activities_read_one_history', output='rss', uid=versions[0]['identifier'], _query=(('_LOCALE_', get_current_locale(request)),('_PROFILE_', get_current_profile(request))))}">
                        <i class="icon-rss"></i> ${_("Subscribe")}
                    </a>
                </div>
            </div>

            <div class="row-fluid">
                <div class="span9">
                    <h3 class="form-below-toolbar">${_('Version History')}</h3>
                </div>
            </div>
            <div class="row-fluid">
                <div class="span9">
                    <table class="table">
                        <thead>
                            <tr>
                                <th></th>
                                <th>${_('Status')}</th>
                                <th>${_('Last Change')}</th>
                                <th>${_('Username')}</th>
                                <th>${_('Version')}</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for v in versions:
                                % if v['version'] == activeVersion:
                                <tr class="deal-history-active">
                                % elif v['statusId'] == 1:
                                <tr class="pending">
                                % else:
                                <tr>
                                % endif
                                    <td class="deal-history-links">
                                        % if isModerator and v['statusId'] == 1:
                                            <a href="${request.route_url('activities_read_one', output='review', uid=v['identifier'], _query=(('new', v['version']),))}">
                                                <i class="icon-check ttip" data-toggle="tooltip" data-original-title="${_('Review this version')}"></i>
                                            </a>
                                            |
                                        % endif
                                        % if activeVersion is not None and v['version'] != activeVersion:
                                            <%
                                                refV = v['version'] if v['version'] < activeVersion else activeVersion
                                                newV = v['version'] if v['version'] > activeVersion else activeVersion
                                            %>
                                            <a href="${request.route_url('activities_read_one', output='compare', uid=v['identifier'], _query=(('ref', refV),('new', newV)))}">
                                                <i class="icon-exchange ttip" data-toggle="tooltip" data-original-title="${_('Compare this version with the active version')}"></i>
                                            </a>
                                            |
                                        % endif
                                        <a href="${request.route_url('activities_read_one', output='html', uid=v['identifier'], _query=(('v', v['version']),))}">
                                            <i class="icon-eye-open ttip" data-toggle="tooltip" data-original-title="${_('View this version')}"></i>
                                        </a>
                                    </td>
                                    <td>
                                        ${v['statusName']}
                                    </td>
                                    <td>
                                        ${v['timestamp']}
                                    </td>
                                    <td>
                                        ${v['username']}
                                    </td>
                                    <td>
                                        ${v['version']}
                                    </td>
                                </tr>
                            % endfor
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="row-fluid">
                <div class="span9 text-right">
                    <a href="${request.route_url('activities_read_one_history', output='rss', uid=versions[0]['identifier'], _query=(('_LOCALE_', get_current_locale(request)),('_PROFILE_', get_current_profile(request))))}">
                        <i class="icon-rss"></i> ${_("Subscribe")}
                    </a>
                </div>
            </div>
        % endif
    </div>
</div>

<%def name="bottom_tags()">
<script type="text/javascript">
    $('.ttip').tooltip({
        container: 'body'
    });
</script>
</%def>
