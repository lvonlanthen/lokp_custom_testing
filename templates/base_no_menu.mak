<%
from lmkp.utils import handle_query_string
from lmkp.views.translation import get_languages
languages = get_languages()
selectedlanguage = languages[0]
for l in languages:
    if locale == l[0]:
        selectedlanguage = l
mode = None
if 'lmkp.mode' in request.registry.settings:
    if str(request.registry.settings['lmkp.mode']).lower() == 'demo':
        mode = 'demo'

use_piwik_analytics = False
if 'lmkp.use_piwik_analytics' in request.registry.settings:
    if str(request.registry.settings['lmkp.use_piwik_analytics']).lower() == "true":
        use_piwik_analytics = True
%>

<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta name="content-language" content="${selectedlanguage[0]}" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>
            <%
                try:
                    context.write("%s - %s" % (self.title(), _("LOKP")))
                except AttributeError:
                    context.write(_("LOKP"))
            %>
        </title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">

        <link rel="stylesheet" href="/custom/css/bootstrap-combined.no-icons.min.css">
        <link rel="stylesheet" href="/custom/css/font-awesome/css/font-awesome.min.css">

        <link rel="stylesheet" href="/custom/css/bootstrap-responsive.min.css">
        <link rel="stylesheet" href="/custom/css/main.css">

        <link rel="stylesheet" href="/custom/css/custom.css">

        <!--[if IE 7]>

            <link rel="stylesheet" href="/custom/css/ie7.css">
            <link rel="stylesheet" href="/custom/css/font-awesome/css/font-awesome-ie7.css">

        <![endif]-->

        <!--[if IE 8]>

            <link rel="stylesheet" href="/custom/css/ie8.css')}">

        <![endif]-->

        <script src="/custom/js/vendor/modernizr-2.6.2-respond-1.1.0.min.js"></script>
        <script src="/custom/js/vendor/jquery-1.9.1.min.js"></script>

        <style type="text/css">
            .user {
                margin-top: -8px;
                padding-right: 0;
            }
            #main {
                padding-bottom: 50px;
            }
            .wrap {
                margin: 0 auto -50px;
            }
            .header_self {
                height: inherit;
                max-height: none;
            }
            .lo_logo {
                margin: 0 0 5px 5px;
            }
            .btn-country-selector, .btn-start {
                text-transform: uppercase;
            }
        </style>

        ## Include the head tags of the child template if available.
        <%
            try:
                self.head_tags()
            except AttributeError:
                pass
        %>

    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
        <![endif]-->

        <div class="wrap">

        <!-- Header  -->

                <div id="main" class="clearfix">

                    <div class="navbar header_self">
                        <div class="container">
                            <div class="row-fluid hidden-phone">
                              <div class="span3 text-right">
                                <a href="${request.route_url('index')}">
                                  % if mode == 'demo':
                                      <img src="/custom/img/logo_demo.png" class="lo_logo" alt="${_('LOKP')}" />
                                  % else:
                                      <img src="/custom/img/logo.png" class="lo_logo" alt="${_('LOKP')}" />
                                  % endif
                                </a>
                              </div>

                              <div class="span6 landing-introduction">
                                  <p>
                                      LOKP Introduction
                                  </p>
                              </div>
                              <div class="user">
                                  <ul class="nav nav-pills">
                                      <li>
                                          <div class="dropdown">
                                              <a class="dropdown-toggle blacktemp" data-toggle="dropdown" href="#">
                                                  ${selectedlanguage[1]}
                                                  <b class="caret"></b>
                                              </a>
                                              <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                                  % for l in languages:
                                                  <li class="cursor">
                                                      <a href="${handle_query_string(request.url, add=[('_LOCALE_', l[0])])}">${l[1]}</a>
                                                  </li>
                                                  % endfor
                                              </ul>
                                          </div>
                                      </li>
                                  </ul>
                              </div>
                            </div>
                            <div class="row-fluid visible-phone">
                              <div class="span3">
                                  <a href="${request.route_url('index')}">
                                      <img src="custom/img/logo.png" class="lo_logo" />
                                  </a>
                              </div>
                              <div class="span6 landing-introduction">
                                  <p>
                                      LOKP Introduction
                                  </p>
                              </div>
                              <div class="span3">
                                  <div class="user">
                                      <ul class="nav nav-pills">
                                          <li>
                                              <div class="dropdown">
                                                  <a class="dropdown-toggle blacktemp" data-toggle="dropdown" href="#">
                                                      ${selectedlanguage[1]}
                                                      <b class="caret"></b>
                                                  </a>
                                                  <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                                      % for l in languages:
                                                      <li class="cursor">
                                                          <a href="${handle_query_string(request.url, add=[('_LOCALE_', l[0])])}">${l[1]}</a>
                                                      </li>
                                                      % endfor
                                                  </ul>
                                              </div>
                                          </li>
                                      </ul>
                                  </div>
                              </div>
                            </div>

                        </div>
                    </div>

                    <!-- content -->

                    <div class="container">
                        <div class="content no-border">

                            ## Use the body content of the child template
                            ${self.body()}

                        </div>
                    </div>
                </div>

                <div class="landing-page-push">
                </div>

            </div>

            <div class="navbar footer landing-page-footer">
                <ul class="nav pull-right">
                    <%
                        # The entries of the footer as arrays with
                        # - url
                        # - name
                        footer = [
                            [request.route_url('faq_view'), _('FAQ')],
                            [request.route_url('about_view'), _('About')],
                            [request.route_url('partners_view'), _('Partners & Donors')]
                        ]
                    %>

                    % for f in footer:
                    <li
                        % if request.current_route_url() == f[0]:
                            class="active"
                        % endif
                        >
                        <a href="${f[0]}">${f[1]}</a>
                    </li>
                    % endfor
                </ul>
            </div>

        <script type="text/javascript">
         /* <![CDATA[ */
         document.write(unescape("%3Cscript src='" + (("https:" == document.location.protocol) ? "https://" : "http://") + "www.google.com/jsapi' type='text/javascript'%3E%3C/script%3E"));
         /* ]]> */
        </script>

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="/custom/js/vendor/jquery-1.9.1.min.js"><\/script>')</script>

        <script src="/custom/js/vendor/bootstrap.min.js"></script>

        <script src="/custom/js/main.js"></script>

        % if use_piwik_analytics==True:
        <!-- Piwik -->
        <script type="text/javascript">
          var _paq = _paq || [];
          _paq.push(["trackPageView"]);
          _paq.push(["enableLinkTracking"]);

          (function() {
            var u=(("https:" == document.location.protocol) ? "https" : "http") + "://webstats.landobservatory.org/";
            _paq.push(["setTrackerUrl", u+"piwik.php"]);
            _paq.push(["setSiteId", "1"]);
            var d=document, g=d.createElement("script"), s=d.getElementsByTagName("script")[0]; g.type="text/javascript";
            g.defer=true; g.async=true; g.src=u+"piwik.js"; s.parentNode.insertBefore(g,s);
          })();
        </script>
        <!-- End Piwik Code -->
        % endif

        ## Include the bottom tags of the child template if available.
        <%
            try:
                self.bottom_tags()
            except AttributeError:
                pass
        %>
    </body>
</html>
