<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_('Stakeholder Editor')}</%def>

<%def name="head_tags()">

    <link rel="stylesheet" href="/static/form.css" type="text/css" />

    <script type="text/javascript" src="${request.static_url('lmkp:static/v2/form.js')}"></script>

    % for reqt in js_links:
        <script type="text/javascript" src="/formstatic/${reqt}"></script>
    % endfor
</%def>

<div class="container deal-edit-content">
    <div class="content no-border">
        
        ## Session messages
        <%include file="lmkp:templates/parts/sessionmessage.mak"/>
        
        ${form | n}
    </div>
</div>

<%def name="bottom_tags()">
    <script type="text/javascript">
        if (window.deform) {
            deform.load();
        }
    </script>
</%def>
