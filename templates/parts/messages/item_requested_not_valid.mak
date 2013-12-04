<h3 class="text-error">${_('Error')}</h3>
<p>${_('The version you requested cannot be displayed. It is not valid according to the configuration of the application, which can be the case for older versions. Please select a newer version from the history page.')}</p>
% if url:
    <p><a href="${url}"><i class="icon-time"></i>&nbsp;${_('History')}</a></p>
% endif