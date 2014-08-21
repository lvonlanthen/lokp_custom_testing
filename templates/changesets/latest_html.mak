<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%
from lmkp.views.profile import get_current_locale
from lmkp.views.profile import get_current_profile
%>

<%def name="title()">${_('Latest approved Changesets')}</%def>

<%def name="inlinemenu()">
<div class="row-fluid">
    <div class="span9 text-right">
        <a href="${request.route_url('changesets_read_latest', output='rss', _query=(('_LOCALE_', get_current_locale(request)),('_PROFILE_', get_current_profile(request))))}">
            <i class="icon-rss"></i> ${_("Subscribe")}
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
                <h3 class="form-below-toolbar">${_('Latest approved Changesets')}</h3>
            </div>
        </div>

        ##<div class="row-fluid">
        ##    <div class="span9">
        ##        <span>${_('The latest approved changes edited on the Land Observatory')}</span>
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
                            <td>${item['pubDate']}</td>
                            <td>${item['description'] | n}</td>
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
