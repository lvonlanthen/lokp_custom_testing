<h3 class="text-error">${_('Error')}</h3>
<p>${_('The selected versions cannot be compared. At least one of them is not valid according to the configuration of the application, which can be the case for older versions. Please select other versions from the history to compare.')}</p>
% if url:
    <p><a href="${url}"><i class="icon-time"></i>&nbsp;${_('History')}</a></p>
% endif