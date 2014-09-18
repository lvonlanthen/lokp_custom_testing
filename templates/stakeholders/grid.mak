<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_('Grid View')} - ${_('Stakeholders')}</%def>

## Start of content

<%
    import urllib
    import datetime
    from lmkp.views.views import getQueryString
    from lmkp.views.views import (
        get_current_locale,
        get_current_profile,
        get_default_search_key,
    )

    # Get the keys and their translation
    from lmkp.views.config import getGridColumnKeys
    keys = getGridColumnKeys(request, 'stakeholders')

    default_search_translated, default_search_original = get_default_search_key(request, 'sh')

    a_uids = ','.join(invfilter) if invfilter is not None else ''
%>

## Filter
<%include file="lmkp:customization/testing/templates/parts/filter.mak" />

<!-- content -->
<div class="container">

    <div class="show-investors visible-phone">
        <i class="icon-info-sign"></i>
        <p>${_('Show deals by clicking on a specific row.')}</p>
    </div>

    <div class="content">

        ## Spatial Filter
        <%
            spatialFilterBasedOn = _('Profile')
            spatialFilterExplanation = _('You are seeing all the Investors involved in Deals within the current profile.')
            spatialFilterLink = None

            if spatialfilter == 'map':
                spatialFilterBasedOn = _('Map Extent')
                spatialFilterExplanation = _('You are currently only seeing Investors involved in Deals which are visible on the map.')
                spatialFilterLink = _('Show all the Investors involved in Deals of the profile.')
        %>

        % if spatialfilter:
        <div class="alert alert-info">
            <i class="icon-globe"></i>&nbsp;
            <strong>${_('Spatial Filter')}</strong> ${_('based on')}
                % if spatialFilterLink:
                    <strong><a href="${request.route_url('map_view')}">${spatialFilterBasedOn}</a></strong>.
                % else:
                    <strong>${spatialFilterBasedOn}</strong>.
                % endif
            ${spatialFilterExplanation}
            % if spatialFilterLink:
                <br/><a href="${getQueryString(request.url, add=[('bbox', 'profile')])}">${spatialFilterLink}</a>
            % endif
        </div>
        % endif

        ## Involvement Filter
        % if invfilter:
        <div class="alert alert-info">
            <i class="icon-filter"></i>&nbsp;
            <strong>${_('Deal Filter')}</strong>: ${_('You are currently only seeing Investors which are involved in Deal')}
            % for uid in invfilter:
                <a href="${request.route_url('activities_read_one', output='html', uid=uid)}">
                    ${uid[:6]}</a>
            % endfor
            .<br/><a href="${request.route_url('stakeholders_byactivities_all', output='html')}">${_('Remove this filter and show all Investors')}</a>.
        </div>
        % endif

        ## Status Filter
        % if statusfilter:
        <div class="alert alert-info">
            <i class="icon-filter"></i>&nbsp;
            <strong>${_('Status Filter')}</strong>: ${_('You are only seeing Investors with the following status:')} ${statusfilter}
        </div>
        % endif

        ## Tabs
        <ul class="nav nav-tabs table_tabs">
            % if request.current_route_url() in [request.route_url('activities_read_many', output='html')]:
                <li class="active">
            % else:
                <li>
            % endif
                <a href="${request.route_url('activities_read_many', output='html')}${getQueryString(request.url, ret='queryString', remove=['order_by', 'dir', 'status'])}">${_('Activities')}</a>
            </li>
            % if request.current_route_url() in [request.route_url('stakeholders_byactivities_all', output='html'), request.route_url('stakeholders_byactivities', output='html', uids=a_uids), request.route_url('stakeholders_read_many', output='html')]:
                % if is_moderator:
                    <li class="active moderator-show-pending-left">
                % else:
                    <li class="active">
                % endif
            % else:
                <li>
            % endif
                <a href="${request.route_url('stakeholders_byactivities_all', output='html')}${getQueryString(request.url, ret='queryString', remove=['order_by', 'dir', 'status'])}">${_('Stakeholders')}</a>
            </li>

            % if is_moderator:
                % if 'status=pending' in request.path_qs:
                    <li class="active moderator-show-pending-right">
                        <a href="${getQueryString(request.current_route_url(), remove=['status'])}" data-toggle="tooltip" title="${_('Show all')}">
                            <i class="icon-flag"></i>
                        </a>
                    </li>
                % else:
                    <li class="moderator-show-pending-right">
                        <a href="${getQueryString(request.current_route_url(), add=[('status', 'pending')])}" data-toggle="tooltip" title="${_('Show only pending')}">
                            <i class="icon-flag"></i>
                            </a>
                    </li>
                % endif
            % endif

            <li class="grid-tab-right">
                <a href="${request.route_url('stakeholders_read_many', output='download')}${getQueryString(request.url, ret='queryString', remove=['order_by', 'dir', 'status'])}" data-toggle="tooltip" title="${_('Download Stakeholders')}">
                    <i class="icon-download-alt"></i>
                </a>
            </li>
            <li class="grid-tab-right">
                <a href="${request.route_url('changesets_read_latest', output='rss', _query=(('_LOCALE_', get_current_locale(request)),('_PROFILE_', get_current_profile(request))))}" data-toggle="tooltip" title="${_('View and subscribe to latest changes')}">
                    <i class="icon-rss"></i>
                </a>
            </li>

            % if default_search_translated:
                <li class="grid-tab-right">
                    <a href="javascript:void(0)" id="search" data-toggle="tooltip" title="${_('Search by')} ${default_search_translated}">
                        <i class="icon-search"></i>
                    </a>
                </li>
            % endif
        </ul>

        ## Table
        <div class="table_wrapper">

            % if len(data) == 0:

                ## Empty data
                <p>&nbsp;</p>
                <h5>${_('Nothing found')}</h5>
                <p>${_('No results were found.')}</p>
                <p>&nbsp;</p>

            % else:

                ## "Tooltip" when clicking a table row
                <div class="show-investors-wrapper hidden hidden-phone">
                    <div class="show-investors">
                        <a href="#">${_('Show deals of this investor')}</a>
                    </div>
                </div>

                <table
                    class="table table-hover table-self table-bordered"
                    id="activitygrid">
                    <thead>
                        ## The table headers
                        <tr>
                            <th>${_('Investor ID')}</th>
                            <th>
                                ${_('Last Change')}
                                <a href="${getQueryString(request.url, add=[('order_by', 'timestamp'), ('dir', 'asc')])}">
                                    <div class="desc
                                         % if 'order_by=timestamp' in request.path_qs and 'dir=%s' % urllib.quote_plus('asc') in request.path_qs:
                                            active
                                         % endif
                                         ">&nbsp;</div>
                                </a>
                                <a href="${getQueryString(request.url, add=[('order_by', 'timestamp'), ('dir', 'desc')])}">
                                <div class="asc
                                     % if ('order_by=timestamp' in request.path_qs and 'dir=%s' % urllib.quote_plus('desc') in request.path_qs) or 'order_by=' not in request.path_qs:
                                        active
                                     % endif
                                     ">&nbsp;</div>
                                </a>
                            </th>
                            % for k in keys:
                                <th>${k[1]}
                                    <a href="${getQueryString(request.url, add=[('order_by', k[0]), ('dir', 'asc')])}">
                                        <div class="desc
                                             % if 'order_by=%s' % urllib.quote_plus(k[0]) in request.path_qs and 'dir=%s' % urllib.quote_plus('asc') in request.path_qs:
                                                active
                                             % endif
                                             ">&nbsp;</div>
                                    </a>
                                    <a href="${getQueryString(request.url, add=[('order_by', k[0]), ('dir', 'desc')])}">
                                    <div class="asc
                                         % if 'order_by=%s' % urllib.quote_plus(k[0]) in request.path_qs and 'dir=%s' % urllib.quote_plus('desc') in request.path_qs:
                                            active
                                         % endif
                                         ">&nbsp;</div>
                                    </a>
                                </th>
                            % endfor
                        </tr>
                    <tbody>
                        ## The table body

                        % for d in data:
                            <%
                                # Collect and prepare the necessary values to
                                # show in the grid.

                                pending = False
                                if 'status_id' in d and d['status_id'] == 1:
                                    pending = True

                                id = d['id'] if 'id' in d else _('Unknown')
                                timestamp = (datetime.datetime.strptime(d['timestamp'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M')
                                    if 'timestamp' in d else _('Unknown'))
                                values = []
                                translatedkeys = []
                                for k in keys:
                                    translatedkeys.append(k[1])
                                    values.append('Unknown')
                                for tg in d['taggroups']:
                                    for t in tg['tags']:
                                        for i, tk in enumerate(translatedkeys):
                                            if t['key'] == tk:
                                                values[i] = t['value']
                            %>

                            % if pending:
                                <tr class="pending">
                            % else:
                                <tr>
                            % endif
                                <td>
                                    <a href="${request.route_url('stakeholders_read_one', output='html', uid=id)}">
                                        ${id[:6]}
                                    </a>
                                </td>
                                <td>${timestamp}</td>
                                % for v in values:
                                    <td>${v}</td>
                                % endfor

                                <td class="identifier hide">${id}</td>
                                <td class="itemType hide">stakeholders</td>

                            </tr>
                        % endfor

                    </tbody>
                </table>

            % endif
        </div>

        ## Pagination
        % if len(data) > 0:
            <%include file="lmkp:templates/parts/pagination.mak"
                args="totalitems=total, currentpage=currentpage, pagesize=pagesize, itemsname=_('Investors')"
            />
        % endif

    </div>
</div>

## End of content

<%def name="bottom_tags()">
    <%
        from lmkp.views.views import (
            get_default_search_key,
        )

        default_search_translated, default_search_original = get_default_search_key(request, 'sh')
    %>

    <script type="text/javascript">
        $(function () {
            $("a[data-toggle='tooltip']").tooltip({
                container: 'body',
                placement: 'bottom'
            });
        });
    </script>

    % if default_search_original:
    <script type="text/javascript">
        var search_by = '${default_search_original}';
        var search_itemtype = 'sh';
        $(function () {
            $('#search').popover({
                html: true,
                trigger: 'click',
                placement: 'bottom',
                content: function () {
                    return [
                        '<form class="form-search" action="javascript:void(0);">',
                        '<div class="input-append">',
                        '<input type="text" id="search-query" class="span2 search-query">',
                        '<button type="button" id="search-button" class="btn" onclick="search();">',
                        'Search',
                        '</button></div></form>'
                    ].join('');
                }
            });
        });
        function search() {
            var term = $('#search-query').val();
            if (term && search_by) {
                addNewFilter(search_itemtype, search_by, 'ilike', ['*', term, '*'].join(''));
            }
            return false;
        }
    </script>
    % endif

    <script src="${request.static_url('lmkp:static/v2/grid.js')}" type="text/javascript"></script>
    <script src="${request.static_url('lmkp:static/v2/filters.js')}" type="text/javascript"></script>
</%def>
