<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_('Not found')}</%def>

<div class="container">
    <div class="content no-border text-center">
        <h3>404 ${_('Not found')}</h3>
        <p>${_('The requested page was not found.')}</p>
    </div>
</div>
