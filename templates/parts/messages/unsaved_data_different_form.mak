<strong>${_('Notice')}</strong>:
${_('Unsaved data from another form was found in the session.')} ${_('It contains:')}

% if type == 'activities':
    ${_('Deal')}
    % if name == '':
        ${_('New Deal')}
    % else:
        ${name}
    % endif
% else:
    ${_('Investor')}
    % if name == '':
        ${_('New Investor')}
    % else:
        ${name}
    % endif
% endif
. ${_('These changes will be lost if you continue to edit this form.')}
<br/>

<a href="${url}">${_('See the unsaved changes of this Deal and submit it.')}</a>