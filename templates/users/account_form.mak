<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_('User Account')}</%def>

<%def name="head_tags()">
    <!-- REQUIREMENTS -->
    <!-- CSS -->
    % for reqt in css_links:
    <!--link rel="stylesheet" href="/formstatic/${reqt}" type="text/css" /-->
    % endfor
    % for reqt in js_links:
    <script type="text/javascript" src="/formstatic/${reqt}"></script>
    % endfor
</%def>

<%def name="inlinemenu()">
<div class="row-fluid">
    <div class="span9 text-right">
        <a href="${request.route_url('changesets_read_byuser', username=username, output='html')}">
            <i class="icon-list-ul"></i> ${_("My Changesets")}
        </a>
    </div>
</div>
</%def>

<div class="container">
    <div class="content no-border">

        ## Header menu
        ${inlinemenu()}

        <div class="row-fluid">
            <div class="span9">
                <h3 class="form-below-toolbar">${_('User Account')}</h3>
            </div>
        </div>
        <div class="row-fluid">
            <div class="span9">
                <p>${_('Update user settings')}</p>
            </div>
        </div>        <div class="row-fluid">
            <div class="span9">
                <hr class="grey" />
            </div>
        </div>
        <div class="row-fluid">
            <div class="span9">
                ${form | n}
            </div>
        </div>

        ## Footer menu
        ${inlinemenu()}

    </div>
</div>

<%def name="bottom_tags()">
    <script type="text/javascript">
        deform.load();
    </script>
</%def>
