<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_('Grid View')} - ${_('Deals')}</%def>

## Start of content

<%
    import urllib
    import datetime
    from lmkp.views.views import (
        get_default_search_key,
    )

    # Get the keys and their translation
    from lmkp.views.config import getGridColumnKeys
    keys = getGridColumnKeys(request, 'activities')

    default_search_translated, default_search_original = get_default_search_key(request, 'a')

    sh_uids = ','.join(invfilter) if invfilter is not None else ''
%>

## Filter
<%include file="lmkp:customization/testing/templates/parts/filter.mak" />

<!-- content -->
<div class="container">

    <div class="content">

        ## Spatial Filter
        <%
            spatialFilterBasedOn = _('Profile')
            spatialFilterExplanation = _('You are seeing all the Deals within the current profile.')
            spatialFilterLink = None

            if spatialfilter == 'map':
                spatialFilterBasedOn = _('Map Extent')
                spatialFilterExplanation = _('You are currently only seeing Deals which are visible on the map.')
                spatialFilterLink = _('Show all Deals of the profile.')
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
                <br/><a href="${handle_query_string(request.url, add=[('bbox', 'profile')])}">${spatialFilterLink}</a>
            % endif
        </div>
        % endif

        ## Involvement Filter
        % if invfilter:
        <div class="alert alert-info">
            <i class="icon-filter"></i>&nbsp;
            <strong>${_('Investor Filter')}</strong>: ${_('You are currently only seeing Deals where Investor')}
            % for uid in invfilter:
                <a href="${request.route_url('stakeholders_read_one', output='html', uid=uid)}">
                    ${uid[:6]}</a>
            % endfor
            ${_('is involved.')}<br/><a href="${request.route_url('activities_read_many', output='html')}">${_('Remove this filter and show all Deals')}</a>.
        </div>
        % endif

        ## Status Filter
        % if statusfilter:
        <div class="alert alert-info">
            <i class="icon-filter"></i>&nbsp;
            <strong>${_('Status Filter')}</strong>: ${_('You are only seeing Deals with the following status:')} ${statusfilter}
        </div>
        % endif

        ## Tabs
        <ul class="nav nav-tabs table_tabs">
            % if request.current_route_url() in [request.route_url('activities_read_many', output='html'), request.route_url('activities_bystakeholders', output='html', uids=sh_uids)]:
                % if is_moderator:
                    <li class="active moderator-show-pending-left">
                % else:
                    <li class="active">
                % endif
            % else:
                <li>
            % endif
                <a href="${request.route_url('activities_read_many', output='html')}${handle_query_string(request.url, return_value='query_string', remove=['order_by', 'dir', 'status'])}">${_('Activities')}</a>
            </li>
            % if is_moderator:
                % if 'status=pending' in request.path_qs:
                    <li class="active moderator-show-pending-right">
                        <a href="${handle_query_string(request.current_route_url(), remove=['status'])}" data-toggle="tooltip" title="${_('Show all')}">
                            <i class="icon-flag"></i>
                        </a>
                    </li>
                % else:
                    <li class="moderator-show-pending-right">
                        <a href="${handle_query_string(request.current_route_url(), add=[('status', 'pending')])}" data-toggle="tooltip" title="${_('Show only pending')}">
                            <i class="icon-flag"></i>
                            </a>
                    </li>
                % endif
            % endif

            % if request.current_route_url() in [request.route_url('stakeholders_byactivities_all', output='html')]:
                <li class="active">
            % else:
                <li>
            % endif
                <a href="${request.route_url('stakeholders_byactivities_all', output='html')}${handle_query_string(request.url, return_value='query_string', remove=['order_by', 'dir', 'status'])}">${_('Stakeholders')}</a>
            </li>

            <li class="grid-tab-right">
                <a href="${request.route_url('activities_read_many', output='download')}${handle_query_string(request.url, return_value='query_string', remove=['order_by', 'dir', 'status'])}" data-toggle="tooltip" title="${_('Download Activities')}">
                    <i class="icon-download-alt"></i>
                </a>
            </li>
            <li class="grid-tab-right">
                <a href="${request.route_url('changesets_read_latest', output='rss', _query=(('_LOCALE_', locale),('_PROFILE_', profile)))}" data-toggle="tooltip" title="${_('View and subscribe to latest changes')}">
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
        <div class="table_wrapper item-grid-wrapper">

            % if len(data) == 0:

                ## Empty data
                <p>&nbsp;</p>
                <h5>${_('Nothing found')}</h5>
                <p>${_('No results were found.')}</p>
                <p>${_('Make sure there are some deals on the')} <a href="${request.route_url('map_view')}">${_('Map')}</a>.</p>
                <p>&nbsp;</p>

            % else:

                <table
                    class="table table-hover table-self table-bordered"
                    id="itemgrid">
                    <thead>
                        ## The table headers
                        <tr>
                            <th>${_('Deal ID')}</th>
                            <th>
                                ${_('Last Change')}
                                <a href="${handle_query_string(request.url, add=[('order_by', 'timestamp'), ('dir', 'asc')])}">
                                    <div class="desc
                                         % if 'order_by=timestamp' in request.path_qs and 'dir=%s' % urllib.quote_plus('asc') in request.path_qs:
                                            active
                                         % endif
                                         ">&nbsp;</div>
                                </a>
                                <a href="${handle_query_string(request.url, add=[('order_by', 'timestamp'), ('dir', 'desc')])}">
                                <div class="asc
                                     % if ('order_by=timestamp' in request.path_qs and 'dir=%s' % urllib.quote_plus('desc') in request.path_qs) or 'order_by=' not in request.path_qs:
                                        active
                                     % endif
                                     ">&nbsp;</div>
                                </a>
                            </th>
                            % for k in keys:
                                <th>${k[1]}
                                    <a href="${handle_query_string(request.url, add=[('order_by', k[0]), ('dir', 'asc')])}">
                                        <div class="desc
                                             % if 'order_by=%s' % urllib.quote_plus(k[0]) in request.path_qs and 'dir=%s' % urllib.quote_plus('asc') in request.path_qs:
                                                active
                                             % endif
                                             ">&nbsp;</div>
                                    </a>
                                    <a href="${handle_query_string(request.url, add=[('order_by', k[0]), ('dir', 'desc')])}">
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
                                    <a href="${request.route_url('activities_read_one', output='html', uid=id)}">
                                        ${id[:6]}
                                    </a>
                                </td>
                                <td>${timestamp}</td>
                                % for v in values:
                                    <td>${v}</td>
                                % endfor

                                <td class="identifier hide">${id}</td>
                                <td class="itemType hide">activities</td>

                            </tr>
                        % endfor

                    </tbody>
                </table>

            % endif
        </div>

        ## Pagination
        % if len(data) > 0:
            <%include file="lmkp:templates/parts/pagination.mak"
                args="totalitems=total, currentpage=currentpage, pagesize=pagesize, itemsname=_('Deals')"
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

        default_search_translated, default_search_original = get_default_search_key(request, 'a')
    %>

    <script type="text/javascript">
        $(function () {
            $("a[data-toggle='tooltip']").tooltip({
                container: 'body',
                placement: 'bottom'
            });
        });
        var link_involvement_text = '${_("Show [LOKP Stakeholders] for this [LOKP Activities]")}';
    </script>

    % if default_search_original:
    <script type="text/javascript">
        var search_by = '${default_search_original}';
        var search_itemtype = 'a';
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
