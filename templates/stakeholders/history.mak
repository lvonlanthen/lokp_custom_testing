<%inherit file="lmkp:customization/testing/templates/base.mak" />

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
      ${toolbar('top')}
      <div class="row-fluid">
          <h3 class="form-below-toolbar">${_('Version History')}</h3>
      </div>
      <div class="row-fluid">
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
              % if v['version'] == active_version:
                <tr class="deal-history-active">
              % elif v['status_id'] == 1:
                <tr class="pending">
              % else:
                <tr>
              % endif
                <td class="deal-history-links">
                  <ul class="inline item-toolbar">
                    % if is_moderator and v.get('status_id') == 1:
                      <li>
                        <a href="${request.route_url('activities_read_one', output='review', uid=v['id'], _query=(('new', v['version']),))}"><i class="icon-check ttip" data-toggle="tooltip" data-original-title="${_('Review this version')}"></i></a>
                      </li>
                    % endif
                    % if active_version is not None and v.get('version') != active_version:
                      <%
                        version = v.get('version')
                        ref_version = version if version < active_version else active_version
                        new_version = version if version > active_version else active_version
                      %>
                      <li>
                        <a href="${request.route_url('activities_read_one', output='compare', uid=v['id'], _query=(('ref', ref_version),('new', new_version)))}"><i class="icon-exchange ttip" data-toggle="tooltip" data-original-title="${_('Compare this version with the active version')}"></i></a>
                      </li>
                    % endif
                    <li>
                      <a href="${request.route_url('activities_read_one', output='html', uid=v['id'], _query=(('v', v['version']),))}"><i class="icon-eye-open ttip" data-toggle="tooltip" data-original-title="${_('View this version')}"></i></a>
                    </li>
                  </ul>
                </td>
                <td>
                  ${v.get('status')}
                </td>
                <td>
                  ${v.get('timestamp')}
                </td>
                <td>
                  <a href="${request.route_url('changesets_read_byuser', username=v.get('user', dict()).get('username'), output='html')}">
                    ${v.get('user', dict()).get('username')}
                  </a>
                </td>
                <td>
                  ${v.get('version')}
                </td>
              </tr>
            % endfor
          </tbody>
        </table>
      </div>
      ${toolbar('bottom')}
    % endif
  </div>
</div>

<%def name="toolbar(position)">
<div class="row-fluid">
  <div class="span12 text-right deal-${position}-toolbar">
    <ul class="inline item-toolbar">
      <li>
        <a href="${request.route_url('activities_read_one_history', output='rss', uid=versions[0].get('id'), _query=(('_LOCALE_', locale),('_PROFILE_', profile)))}">
          <i class="icon-rss"></i><span class="link-with-icon">${_("Subscribe")}</span>
        </a>
      </li>
    </ul>
  </div>
</div>
</%def>

<%def name="bottom_tags()">
<script type="text/javascript">
    $('.ttip').tooltip({
        container: 'body'
    });
</script>
</%def>
