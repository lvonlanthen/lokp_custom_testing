<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%
from lmkp.views.profile import get_current_locale
from lmkp.views.profile import get_current_profile
%>

<%def name="title()">${_('Approved changesets by %s' % username)}</%def>

<%def name="inlinemenu()">
<div class="row-fluid">
    <div class="span9 text-right">
        <a href="${request.route_url('changesets_read_byuser', username=username, output='rss', _query=(('_LOCALE_', get_current_locale(request)),))}">
            <i class="icon-rss"></i> ${_(u'Subscribe')}
        </a>
        &nbsp;|&nbsp
        % if pagesize != 10:
        <a href="${request.route_url('changesets_read_latest', output='html', _query=(('pagesize', pagesize),))}">
        % else:
        <a href="${request.route_url('changesets_read_latest', output='html')}">
        % endif
            <i class="icon-list-ul"></i> ${_(u'All Changesets')}
        </a>
    </div>
</div>
</%def>

<div class="container">
    <div class="content no-border">

        ## Header menu bar
        ${inlinemenu()}

        <div class="alert alert-info">
            ${_('Please note that only approved changes are visible in the changesets.')}
        </div>

        <div class="row-fluid">
            <div class="span9">
                <h3 class="form-below-toolbar">${_('Approved changesets by %s' % username)}</h3>
            </div>
        </div>

        ##<div class="row-fluid">
            ##    <div class="span9">
                ##        <span>${_('The latest changes edited on the Land Observatory by %s' % username)}</span>
                ##    </div>
            ##</div>

        <div class="row-fluid">
            <div class="span9">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>${_('Timestamp')}</th>
                            <th>${_('Changeset description')}</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for item in items:
                        <tr>
                            <td>${item['timestamp'].strftime("%a, %d %b %Y %H:%M:%S %Z")}</td>
                            <%
                            date = item['timestamp'].strftime("%a, %d %b %Y %H:%M:%S %Z")
                            %>
                            % if item['type'] == "activity":
                            <td>Update of activity
                                <a href="${request.route_url('activities_read_one', output='html', uid=item['identifier'], _query=(('v', item['version']),))}">
                                    #${item['identifier'].split("-")[0].upper()}
                                </a> on ${date} to version&nbsp;${item['version']}
                            </td>
                            % elif item['type'] == "stakeholder":
                            <td>Update of stakeholder
                                <a href="${request.route_url('stakeholders_read_one', output='html', uid=item['identifier'], _query=(('v', item['version']),))}">
                                    #${item['identifier'].split("-")[0].upper()}
                                </a>
                                on ${date} to version&nbsp;${item['version']}</td>
                            % endif
                        </tr>
                        % endfor
                    </tbody>
                </table>
            </div>
        </div>

        ## Pagination
        % if len(items) > 0:
        <div class="row-fluid">
            <div class="span9">
                <%include file="lmkp:templates/parts/pagination.mak"
                args="totalitems=totalitems, currentpage=currentpage, pagesize=pagesize, itemsname=_('Changesets')"
                />
            </div>
        </div>
        % endif

        ## Footer menu bar
        ${inlinemenu()}

    </div>
</div>
