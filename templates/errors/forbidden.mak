<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_('Forbidden')}</%def>

<div class="container">
    <div class="content no-border text-center">
        <h3>403 ${_('Forbidden')}</h3>
        <p>${_("Access denied. You don't have permission to see this page.")}</p>
    </div>
</div>
