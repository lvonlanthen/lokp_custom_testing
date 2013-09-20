<%inherit file="lmkp:customization/lo/templates/base.mak" />

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

<div class="container">
    <div class="content no-border">
        <h3>${_('User Account')}</h3>
        <p>${_('Update user settings')}</p>
        <hr class="grey" />
        ${form | n}
    </div>
</div>

<%def name="bottom_tags()">
    <script type="text/javascript">
        deform.load();
    </script>
</%def>