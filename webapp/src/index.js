import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {OidcProvider, OidcSecure} from "@axa-fr/react-oidc";

const configuration = {
 client_id: 'interactive.public.short',
    redirect_uri: window.location.origin+'/authentication/callback',
    silent_redirect_uri: window.location.origin+'/authentication/silent-callback',
    //silent_login_uri: window.location.origin+'/authentication/silent-login',
    scope: 'openid profile email api offline_access',
    authority: 'https://demo.duendesoftware.com',
    //authority_time_cache_wellknowurl_in_second: 60* 60,
    refresh_time_before_tokens_expiration_in_second: 10,
    service_worker_relative_url:'/OidcServiceWorker.js',
    service_worker_only: false,
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <OidcProvider configuration={configuration} >
<OidcSecure>
          <App />
  </OidcSecure>
      </OidcProvider>
  </React.StrictMode>
);

